#!/usr/bin/env python3
# -*- coding: utf-8 -*-
low = 0
high = 100

print('Please think of a number between 0 and 100!')
while True:
    guess = (high + low) // 2
    print('Is your secret number ' + str(guess) + '?')
    result = input("Enter 'h' to indicate the guess is too high. Enter 'l' to indicate the guess is too low. Enter 'c' to indicate I guessed correctly. ")
    if result == 'h':
        high = guess
    elif result == 'l':
        low = guess
    elif result == 'c':
        print('Game over. Your secret number was: ' + str(guess))
        break
    else:
        print('Sorry, I did not understand your input.')
        continue
