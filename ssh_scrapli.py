import getpass
import argparse
import os

from scrapli.driver.core import IOSXEDriver, JunosDriver

UNSET = False


def read_file(fn):
    with open(fn) as f:
        result = f.read()
    return result.rstrip()


def cisco(username, public_key):
    public_key = [
        public_key[i:i + 253]
        for i in range(0, len(public_key), 253)
    ]
    commands_to_set = [
        f'username {username} privilege 15',
        'ip ssh pubkey-chain',
        f'username {username}',
        'key-string',
        public_key[0],
        public_key[1],
        'exit',
        'exit',
        'exit',
        'exit',
        'write memory'
    ]
    commands_to_unset = [
        f'no username {username}',
        '\n',
        'ip ssh pubkey-chain',
        f'no username {username}',
        'exit',
        'exit',
        'write memory'
    ]

    if not UNSET:
        return commands_to_set
    else:
        return commands_to_unset


def juniper(username, public_key):
    commands_to_set = [
        'set system login '
        f'user {username} class super-user '
        f'authentication ssh-rsa "{public_key}"',
        'commit'
    ]
    commands_to_unset = [
        'delete system login '
        f'user {username}',
        'commit'
    ]
    if not UNSET:
        return commands_to_set
    else:
        return commands_to_unset


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("ip", help="Device hostname or IP address")
    parser.add_argument("vendor", help="Device vendor(same as in netmiko)",
                        choices=['cisco', 'juniper'])
    parser.add_argument("--user", default=getpass.getuser(),
                        help="User for which to add SSH key")
    parser.add_argument("-P", "--port", default=22, help="SSH port (Default=22)", type=int)
    parser.add_argument("-i", default=os.path.expanduser("~/.ssh/id_rsa.pub"),
                        help="Path to public SSH key", dest='ssh_key')
    parser.add_argument("-u", help="Device admin username", dest='device_admin')
    parser.add_argument("-p", help="Device admin password", dest='device_pass')
    parser.add_argument("-r", "--remove", help="Remove SSH key", action="store_true")
    parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")
    args = parser.parse_args()

    device_admin = args.device_admin if args.device_admin else input('Username: ')
    device_pass = args.device_pass if args.device_pass else getpass.getpass('Password: ')

    if args.remove:
        UNSET = True

    device_data = {
        'host': args.ip,
        'auth_username': device_admin,
        'auth_password': device_pass,
        'auth_strict_key': False,
        'port': args.port,
        'transport': 'system'
    }

    params = {
        'cisco': {
            'driver': IOSXEDriver,
            'config': cisco
        },
        'juniper': {
            'driver': JunosDriver,
            'config': juniper
        }
    }
    driver = params[args.vendor]['driver']
    config = params[args.vendor]['config']

    commands_set = config(args.user, read_file(args.ssh_key))

    with driver(**device_data) as conn:
        output = conn.send_configs(commands_set)

    if args.verbose:
        for response in output:
            print(response.channel_input, response.result, sep='\n')

    print("All Done!")
