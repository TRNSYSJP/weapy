# import csv
import pandas as pd

import argparse
import os
import sys


if(__name__ == '__main__'):

    """DataNaviのCSV（24hx365Days)をType99形式（8760h）に並び替える
    """
    csvfile = ''
    # csv = None

    #コマンドライン引数の定義
    parser = argparse.ArgumentParser()
    parser.add_argument('csvfile', help='DataNaviのCSVを保存したファイル', type=str)

    args = parser.parse_args()

    #引数チェック
    if os.path.exists(args.csvfile):
        csvfile = args.csvfile
    else:
        print('指定されたファイルが見つかりません。\nファイル：{0}'.format(args.csvfile))
        sys.exit()

    filepath = os.path.dirname(csvfile)
    dirname, basename = os.path.split(csvfile)
    basename_without_ext = os.path.splitext(basename)[0]

    destfile = os.path.join(filepath, basename_without_ext+'_8760.csv')
    
    # with open(csvfile, 'r') as f:
    #     # csv = f.read()
    #     reader = csv.reader(f, delimiter='¥t')
    #     for row in reader:

    df = pd.read_table(csvfile, header=None)
    
    # print(df)
    with open(destfile, 'w') as f:

        for index, row in df.iterrows():
            # print('{}'.format(index))
            # print('---------------------')
            for cell in row:
                f.write('{}\n'.format(cell))

