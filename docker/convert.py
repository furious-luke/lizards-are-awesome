#/usr/bin/env python

import os
import argparse
import numpy as np
import pandas as pd

def process_sheets(args):
    sheet1 = pd.read_excel(args.xls[0], sheetname=args.sheet1, header=None)
    if args.merge:
        sheet2 = pd.read_excel(args.xls[0], sheetname=args.sheet2, header=None)
        shape = (sheet1.shape[0] - 6, sheet1.shape[1])
        data = pd.concat(sheet1, sheet2)
    else:
        shape = ((sheet1.shape[0] - 6)/2, sheet1.shape[1])
        data = sheet1
    data.transpose().to_csv(args.output, sep='\t', index=False, header=False)
    return shape

def process_map(args, shape):
    map_data = np.zeros((shape[0], 4), dtype=int)
    map_data[:,1] = np.arange(1, shape[0] + 1)
    np.savetxt(os.path.splitext(args.output)[0] + '.map', map_data, fmt='%d', delimiter='\t')

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Transpose an Excel spreadsheet.')
    parser.add_argument('xls', metavar='INPUT', nargs=1, help='input Excel spreadsheet')
    parser.add_argument('-s1', '--sheet1', default='Sheet1', help='first to convert')
    parser.add_argument('-s2', '--sheet2', default='Sheet2', help='second to convert')
    parser.add_argument('-o', '--output', default='output.ped', help='output filename')
    parser.add_argument('-m', '--merge', action='store_true', help='merge sheets')
    args = parser.parse_args()

    shape = process_sheets(args)
    process_map(args, shape)
