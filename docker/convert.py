#/usr/bin/env python

import os
import argparse

import numpy as np
import pandas as pd
from slugify import slugify


def do_slugify(txt):
    try:
        return slugify(txt)
    except TypeError:
        return slugify(txt.decode())

def add_headers(args, data, headers):
    data = pd.DataFrame(np.zeros((6, data.shape[1]), dtype=int)).append(data, ignore_index=True)
    data[:2] = headers
    for ii in range(data.shape[1]):
        data.ix[0,ii] = do_slugify(data.ix[0,ii])
        data.ix[1,ii] = do_slugify(data.ix[1,ii])
    return data

def merge_sheets(s1, s2):
    s1['sheet'] = pd.Series(np.zeros(s1.shape[0], dtype=int), index=s1.index)
    s2['sheet'] = pd.Series(np.ones(s2.shape[0], dtype=int), index=s2.index)
    s1['index'] = pd.Series(np.arange(0, s1.shape[0], dtype=int), index=s1.index)
    s2['index'] = pd.Series(np.arange(0, s2.shape[0], dtype=int), index=s2.index)
    res = pd.concat([s1, s2])
    res.sort_values(['index', 'sheet'], inplace=True)
    del res['sheet']
    del res['index']
    return res

def read_and_merge(args):
    if args.test:
        sheet1 = pd.DataFrame([
            np.array(['a 0', 'a 1', 'a 2']),
            np.array(['one', 'two', 'three']),
            np.ones(3, dtype=int)*0,
            np.ones(3, dtype=int)*1,
            np.ones(3, dtype=int)*2, '-'*3
        ])
    elif not args.csv:
        sheet1 = pd.read_excel(args.xls[0], sheetname=args.sheet, header=None)
        sheet1 = sheet1.astype(str)
    else:
        sheet1 = pd.read_csv(args.xls[0], header=None, dtype=str)
    headers = sheet1[:2].copy()
    sheet1 = sheet1[2:]
    shape = (sheet1.shape[0], sheet1.shape[1])
    sheet2 = sheet1.copy(deep=True)
    # if args.csv:
    sheet1.replace('0', '2', inplace=True)
    sheet1.replace('-', '0', inplace=True)
    sheet2.replace('2', '1', inplace=True)
    sheet2.replace('0', '2', inplace=True)
    sheet2.replace('-', '0', inplace=True)
    # else:
    # sheet1.replace(0, 2, inplace=True)
    # sheet1.replace('-', 0, inplace=True)
    # sheet2.replace(2, 1, inplace=True)
    # sheet2.replace(0, 2, inplace=True)
    # sheet2.replace('-', 0, inplace=True)
    return merge_sheets(sheet1, sheet2), shape, headers

def merge_sheets_with_headers(args):
    data, shape, headers = read_and_merge(args)
    return add_headers(args, data, headers), shape

def read_sheets(args):
    if args.merge:
        return merge_sheets_with_headers(args)
    else:
        if not args.csv:
            sheet1 = pd.read_excel(args.xls[0], sheetname=args.sheet, header=None)
        else:
            sheet1 = pd.read_csv(args.xls[0], header=None)
        shape = ((sheet1.shape[0] - 6)/2, sheet1.shape[1])
        data = sheet1
    return data, shape

def read_sheets_with_headers(args):
    data, shape = read_sheets(args)
    return add_headers(data), shape

def process_sheets(args):
    data, shape = read_sheets(args)
    data.transpose().to_csv(args.output, sep='\t', index=False, header=False)
    return shape

def process_map(args, shape):
    map_data = np.zeros((shape[0], 4), dtype=int)
    map_data[:,1] = np.arange(1, shape[0] + 1)
    np.savetxt(os.path.splitext(args.output)[0] + '.map', map_data, fmt='%d', delimiter='\t')

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Transpose an Excel spreadsheet.')
    parser.add_argument('xls', metavar='INPUT', nargs=1, help='input Excel spreadsheet')
    parser.add_argument('-c', '--csv', action='store_true', help='sheet stored in CSV format')
    parser.add_argument('-s', '--sheet', default='Sheet1', help='sheet to convert')
    parser.add_argument('-o', '--output', default='output.ped', help='output filename')
    parser.add_argument('-m', '--merge', action='store_true', help='merge sheets')
    parser.add_argument('--test', action='store_true', help='run some tests')
    args = parser.parse_args()

    shape = process_sheets(args)
    process_map(args, shape)
