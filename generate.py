#!/usr/bin/env python

import argparse


def gen_code(index):
    return chr(ord('A') + index/26) + chr(ord('A') + index%26)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Generate input data.')
    parser.add_argument('csv', metavar='OUTPUT', nargs=1, help='output file name')
    parser.add_argument('-r', '--rows', default=10, type=int, help='number of rows')
    parser.add_argument('-c', '--cols', default=10, type=int, help='number of columns')
    args = parser.parse_args()

    with open(args.csv[0], 'w') as output:
        output.write(','.join([gen_code(ii) for ii in range(args.rows)]) + '\n')
        output.write(','.join([gen_code(ii).lower() for ii in range(args.rows)]) + '\n')
        base = 0
        for ii in range(args.rows):
            output.write(','.join([str(base + ii) for ii in range(args.cols)]) + '\n')
            base += args.cols
