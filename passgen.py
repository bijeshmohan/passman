#!/bin/python3
"""Password Generator script"""
import argparse
import string
import random


def generate_password(length, lowercase=True, uppercase=True, digit=True,
                      symbol=True, ignore=None):
    chars = ""

    if lowercase:
        chars += string.ascii_lowercase

    if uppercase:
        chars += string.ascii_uppercase
    
    if digit:
        chars += string.digits

    if symbol:
        chars += string.punctuation

    if not chars:
        chars = string.ascii_letters + string.digits + string.punctuation

    return ''.join(random.choices(chars, k=length))


def parse_args():
    parser = argparse.ArgumentParser(description="Password Generator")
    parser.add_argument('length',
                        metavar='LENGTH',
                        type=int,
                        help='length of password')
    parser.add_argument('-l',
                        '--lowercase',
                        action='store_true',
                        help='control the presence of lowercase chars in password')
    parser.add_argument('-u',
                        '--uppercase',
                        action='store_true',
                        help='control the presence of uppercase chars in password')
    parser.add_argument('-d',
                        '--digits',
                        action='store_true',
                        help='control the presence of digits in password')
    parser.add_argument('-s',
                        '--symbols',
                        action='store_true',
                        help='control the presence of symbols in password')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    print(args)
    password = generate_password(args.length, lowercase=args.lowercase,
                                 uppercase=args.uppercase, digit=args.digits,
                                 symbol=args.symbols)
    print(password)


if __name__ == '__main__':
    main()
