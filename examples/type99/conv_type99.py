# coding: utf-8
# author     Yuichi Yasuda @ quattro corporate design
# copyright  quattro corporate design. All right reserved.

import weapy.weafile as ea
import weapy.epwfile as epw
import pandas as pd
import argparse
import os
import sys
import unicodedata

def is_english(string):
    """ 文字列に英字以外が入っていたらFalseを返す
    """
    for chr in string:
        name = unicodedata.name(chr)
        if not 'LATIN' in name:
        # else:
            return False
    return True

if(__name__ == '__main__'):

    """例）拡張アメダス標準年のデータからTRNSYS,Type99形式のファイルを出力する
    """
    # 拡張アメダス気象データ
    # --------------------------------
    #標準年のデータファイル
    weafile = '' 
    #地点情報
    station = ''
    no = 999 #存在しない地点番号で初期化
    lat = 0.0 #緯度
    lng = 0.0 #経度
    elevation = 0.0 #標高
    fname = '' #出力先ファイル名

    #コマンドライン引数の定義
    parser = argparse.ArgumentParser()
    parser.add_argument('weafile', help='拡張アメダス気象データ標準年のデータファイル', type=str)
    parser.add_argument('station', help='地点名(英語表記)', type=str)
    parser.add_argument('no', help='地点番号（1～842）', type=int)
    parser.add_argument('latitude', help='緯度', type=float)
    parser.add_argument('longitude', help='経度(東経 -、西経 +)', type=float)
    parser.add_argument('elevation', help='標高(m)', type=float)
    parser.add_argument('-f','--file', action='store',nargs=1, help="出力先ファイル名")
    args = parser.parse_args()

    #引数チェック
    #指定された気象データのファイルが存在するか確認
    if os.path.exists(args.weafile):
        weafile = args.weafile
    else:
        print('指定されたファイルが見つかりません。\nファイル：{0}'.format(args.weafile))
        sys.exit()

    #地点名称が英語か確認
    if not args.station or not is_english(args.station):
        print('地点名を英語表記で指定して下さい')
        sys.exit()
    else:
        station = args.station
    
    #地点番号
    if args.no < 1 or 842 < args.no:
        print('地点番号は1～842の番号で指定してください。')
        sys.exit()
    else:
        no = args.no
    
    #緯度、経度(deg)
    # 西端 838 与那国島 24.4667, -123.0100, 30.00 
    # 東端  99 納沙布   43.3933, -145.7583, 12.00 
    # 北端   1 宗谷岬   45.5200, -141.9350, 26.00 
    # 南端 842 波照間   24.0550, -123.7683, 38.00 

    #標高(m)
    # 最高 410 野辺山   35.9483, -138.4717,	1350.00 
    # 最低 193 大潟     40.0000, -139.9500, -3.00

    #緯度
    if args.latitude < 24.0 or 45.6 < args.latitude :
        print('日本国内の緯度（波照間 24.055 ～　宗谷岬 45.52度)を指定してください')
        sys.exit()
    else:
        lat = args.latitude
    #経度
    if args.longitude > -123.0 or  -145.8 > args.longitude:
        print('日本国内の経度（与那国島 -123.0100  ～ 納沙布 -145.7583度）を指定してください。')
        sys.exit()
    else:
        lng = args.longitude

    #標高
    if args.elevation < -3.0 or 1350.0 <args.elevation:
        print('日本国内の標高（大潟 -3.00 ～ 野辺山 1350.0m）を指定してください。')
        sys.exit()
    else:
        elevation = args.elevation #標高
  
    #出力先ファイル名
    if args.file is None:
        pass
    else:
        fname = args.file[0]



    # 拡張アメダス標準年データファイルの読み込み
    wea = ea.WeaFile(weafile, no, elevation)

    # wea(WeaFileクラス）からDataFrameを生成する
    df = pd.DataFrame(
        {
        'TAMB': wea.ambient_temperatures,
        'RHUM': wea.relative_humidities,
        'IGLOB_H': wea.horizontal_global_solar_irradiations,
        'udef1': wea.downward_longwave_irradiations,
        'WDIR': wea.wind_directions,
        'WSPEED': wea.wind_velocities,
        'udef2': wea.precipitation_amounts,
        'udef3': wea.sunshine_durations,
        })

    df = df.round({'TAMB':1, 'RHUM':3, 'IGLOB_H':3, 'udef1':3, 'WDIR':1, 'WSPEED':1, 'udef2':1, 'udef3':1})
    pd.options.display.float_format = '{:.4g}'.format

    #ファイル名
    if not fname:
        # 出力先ファイル名が指定されていなければデフォルトのファイル名
        fname = 'ea_{0:0=3}_{1}.99'.format(no, station)

    #Type99 のヘッダー（拡張アメダス気象データ、東京）
    t99header = [
            '<userdefined>       ! This weather data is generated by Weapy example. https://github.com/TRNSYSJP/weapy',
            '<longitude> {0} ! East of greenwich: negative'.format(lng),
            '<latitude>  {0}   ! '.format(lat),
            '<gmt>       9       ! time shift from GMT, east: positive (hours)',
            '<interval>  1       ! Data file time interval between consecutive lines (hours)',
            '<firsttime> 1       ! Time corresponding to first data line (hours)',
            '<var>	IBEAM_H	<col>	0  <interp> 0  <add>  0  <mult>  1   <samp>   0	!',
            '<var>	IBEAM_N	<col>	0  <interp> 0  <add>  0  <mult>  1   <samp>   0	!',
            '<var>	IDIFF_H	<col>	0  <interp> 0  <add>  0  <mult>  1   <samp>   0	!',
            '<var>	IGLOB_H	<col>	3  <interp> 0  <add>  0  <mult>  1   <samp>   0	! [W/m2]',
            '<var>	TAMB	<col>	1  <interp> 2  <add>  0  <mult>  1   <samp>   0	! [C]',
            '<var>	RHUM	<col>	2  <interp> 1  <add>  0  <mult>  1   <samp>   0	! [%]',
            '<var>	WSPEED	<col>	6  <interp> 1  <add>  0  <mult>  1   <samp>   0	! [m/s]',
            '<var>	WDIR	<col>	5  <interp> 1  <add>  0  <mult>  1   <samp>   0	! [deg.]',
            '<var>	udef1	<col>	4  <interp> 0  <add>  0  <mult>  1   <samp>   0	! Atmosphric radiation [W/m^2]',
            '<var>	udef2	<col>	7  <interp> 0  <add>  0  <mult>  1   <samp>   0	! Amount of rain [mm]',
            '<var>	udef3	<col>	8  <interp> 0  <add>  0  <mult>  1   <samp>   0	! Solar Radiation Time[hour]',
            '<var>	udef4	<col>	0  <interp> 0  <add>  0  <mult>  1   <samp>   0	!',
            '<data>',
            ''
            ]

    #ヘッダーとデータをファイルへ出力
    with open(fname, mode='w', encoding='utf-8') as f:
        f.writelines('\n'.join(t99header))

    df.to_csv(fname, mode='a', header=False, index=False, sep=' ') #, float_format='%3.3f')


    