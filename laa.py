import argparse

import laa


def init(args):
    laa.init()


def convert(args):
    laa.convert(args.input[0], args.output[0], args.recombined, args.format)


def plink(args):
    laa.plink(args.input[0])


def fast(args):
    laa.fast(args.input[0], args.output[0])


def choosek(args):
    laa.choosek(args.input, args.output, args.maxk)


def analyse(args):
    laa.analyse(args.input, args.maxk)


def all(args):
    laa.all(args.input, args.maxk)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Lizards are awesome')
    subparsers = parser.add_subparsers(help='sub-command help')

    init_parser = subparsers.add_parser('init', help='initialise LAA docker image')
    init_parser.set_defaults(func=init)

    convert_parser = subparsers.add_parser('convert', help='convert Excel or CSV into transposed format')
    convert_parser.add_argument('input', nargs=1, help='input filename')
    convert_parser.add_argument('output', nargs=1, default='conv.ped', help='output filename')
    convert_parser.add_argument('--recombined', '-r', action='store_true', help='data is already recombined')
    convert_parser.add_argument('--format', '-f', choices=['xls', 'csv'], default='csv')
    convert_parser.set_defaults(func=convert)

    plink_parser = subparsers.add_parser('plink', help='run Plink')
    plink_parser.add_argument('input', nargs=1, default='conv', help='input filename base')
    plink_parser.set_defaults(func=plink)

    fast_parser = subparsers.add_parser('fast', help='run fastStructure')
    fast_parser.add_argument('input', nargs=1, default='conv', help='input filename base')
    fast_parser.add_argument('output', nargs=1, default='output', help='output filename base')
    fast_parser.set_defaults(func=fast)

    choosek_parser = subparsers.add_parser('choosek', help='calculate k value')
    choosek_parser.add_argument('input', nargs=1, default='conv', help='input filename base')
    choosek_parser.add_argument('output', nargs=1, default='output', help='output filename base')
    choosek_parser.add_argument('--maxk', type=int, default=3, help='maximum k value')
    choosek_parser.set_defaults(func=choosek)

    analyse_parser = subparsers.add_parser('analyse', help='calculate k value')
    analyse_parser.add_argument('input', nargs=1, default='conv', help='input filename base')
    analyse_parser.add_argument('output', nargs=1, default='output', help='output filename base')
    analyse_parser.add_argument('--maxk', type=int, default=3, help='maximum k value')
    analyse_parser.set_defaults(func=analyse)

    all_parser = subparsers.add_parser('all', help='calculate k value')
    all_parser.add_argument('input', nargs=1, default='conv', help='input filename base')
    all_parser.add_argument('output', nargs=1, default='output', help='output filename base')
    all_parser.add_argument('--maxk', type=int, default=3, help='maximum k value')
    all_parser.set_defaults(func=all)

    args = parser.parse_args()
    args.func(args)
