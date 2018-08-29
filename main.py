#!/bin/python

import random


def tryAddFirst(dest, src):
    if not src[0] in dest:
        dest.append(src[0])
    del src[0]


def mix(a, b):
    res = []
    while a or b:
        if a and b:
            if random.random() > 0.5:
                tryAddFirst(res, a)
            else:
                tryAddFirst(res, b)
        elif a:
            tryAddFirst(res, a)
        elif b:
            tryAddFirst(res, b)

    return res


def multi_mix(a, b, depth):
    if depth == 1:
        return mix(a, b)

    return mix(multi_mix(a, b, depth-1), multi_mix(a, b, depth-1))


if __name__ == '__main__':
    import argparse
    import pandas
    import csv

    parser = argparse.ArgumentParser(description='Mixes two ordered lists of (unique) preferences to the desired depth.')
    parser.add_argument('input', metavar='INPUT', type=argparse.FileType('r'),
                    help='A csv formatted file containing two columns')
    parser.add_argument('--depth', type=int, default=1, help='The mix depth')
    parser.add_argument('-o', metavar='OUTPUT', type=argparse.FileType('w'), default="out.csv", help="The output file")

    args = parser.parse_args()

    data = pandas.read_csv(args.input, names=['a', 'b'])
    a = data.a.tolist()
    b = data.b.tolist()

    result = multi_mix(a, b, args.depth)

    writer = csv.writer(args.o)
    for elem in result:
        writer.writerow([elem])
