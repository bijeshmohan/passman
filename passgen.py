#!/bin/python3
"""Password Generator script"""
import argparse
import string
import random


def parse_args():
    parser = argparse.ArgumentParser(description="Password Generator", allow_abbrev=False)
    parser.add_argument('length',
                        metavar='LENGTH',
                        type=int,
                        help='length of password')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    chars = string.ascii_letters + string.digits + string.punctuation
    print(*random.choices(chars, k=args.length), sep='')


if __name__ == '__main__':
    main()
