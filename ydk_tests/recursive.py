from ydk.types import Empty
from ydk.filters import YFilter


def instantiate(binding, model_key, model_value, action='assign'):
    if model_value is None:
        if action == 'return':
            return Empty()
        elif action == 'assign':
            setattr(binding, model_key, Empty())
    elif any(isinstance(model_value, x) for x in [str, bool, int]):
        if action == 'return':
            return model_value
        elif action == 'assign':
            setattr(binding, model_key, model_value)
    elif isinstance(model_value, list):
        model_key_joined = ''.join([x for x in model_key.split(',')])
        list_obj = getattr(binding, model_key_joined.lower())
        for el in model_value:
            obj = instantiate(binding, model_key, el, action='return')
            obj.yfilter = YFilter.replace
            list_obj.append(obj)
    elif isinstance(model_value, dict):
        # special case handling enum type
        if all([x is None for x in model_value.values()]):
            enum_name = ''.join([x.capitalize() for x in model_key.split(',')]) + 'Enum'
            enum_class = getattr(binding, enum_name)
            for el in model_value.keys():
                enum = getattr(enum_class, el)
                if action == 'return':
                    return enum
                elif action == 'assign':
                    setattr(binding, model_key, enum)
        else:
            container = getattr(binding, model_key, None)
            if container and container.__class__.__name__ not in ['YList', 'YLeafList']:
                container_instance = container
            else:
                model_key_camelized = ''.join([x.capitalize() for x in model_key.split(',')])
                container_instance = getattr(binding, model_key_camelized)()

            for k, v in model_value.items():
                instantiate(container_instance, k, v, action='assign')

            if action == 'return':
                return container_instance
            elif action == 'assign':
                setattr(binding, model_key, container_instance)
    else:
        raise ValueError('Unexpected YAML value: {} of type {}'.format(model_value, type(model_value)))
