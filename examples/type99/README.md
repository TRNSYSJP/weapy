# 概要

拡張アメダス1995, 2000, 2010標準年の読み込みサンプル（旧フォーマット）
## スクリプト
|ファイル名|対応フォーマット|概要|
|-|-|-|
|conv_type99.py|wea|type99_format.pyのコマンドライン版|
|type99_format.py|wea|拡張アメダス気象データ、標準年のデータから、Type99（*.99）形式のファイルを出力するサンプル|
|conv_wea2_type99.py|wea2|type99_format_wea2.pyのコマンドライン版|
|type99_format_wea2.py|wea2|拡張アメダス気象データ、標準年のデータから、Type99（*.99）形式のファイルを出力するサンプル|

出力する .99 のヘッダーの `<samp>` は、降水量（udef2）だけ -1、ほかは 0 です。拡張アメダスの降水量は正時前 1 時間の積算値なので、Type99 が値の時刻までの 1 時間の値として扱うように -1 にしています（日射量・大気放射量・日照時間は正時の前後 30 分の積算値、気温・相対湿度は正時の値なので 0）。

## Test
精度検証のためのファイルと検証結果


<br>

# WEA(旧フォーマット)

## conv_type99.py
type99_format.pyのコマンドライン版。weaからType99形式のファイルへ変換する。

### 使用方法

```
python conv_type99.py weafile station no latitude longitude elevation
```
|オプション|機能|
|-|-|
|weafile|拡張アメダス気象データ標準年のデータファイル|
|station |地点名(英語表記)|
|no |地点番号（1～842）|
|latitude |緯度[deg]|
|longitude |経度(東経 -、西経 +)[deg]|
|elevation |標高[m]|
|-f filename |出力先ファイル名（オプション）|

例）東京（地点番号 363）緯度 35.69 経度 -139.76  標高　6.0m の出力
```
pyhton conv_type99.py D:\EAD\RWY0110.wea Tokyo 363 35.69 -139.76 6.0
```
拡張アメダスから変換されたType99形式のファイルは、ファイル名　"ea_" + 地点番号 +　地点名　+".99"　で出力されます。


出力先のファイル名を直接指定する場合は'-f'オプションで次のように入力します。

```
pyhton conv_type99.py D:\EAD\RWY0110.wea Tokyo 363 35.69 -139.76 6.0 -f EA2010_TOKYO(3630).99
```

## type99_format.py
拡張アメダス気象データ、標準年(wea)のデータから、Type99（*.99)形式のファイルを出力するサンプル。

<br>

# WEA2(新フォーマット)


## conv_wea2_type99.py
type99_format_wea2.pyのコマンドライン版。wea2からType99形式のファイルへ変換する。

### 使用方法

```
python conv_wea2_type99.py wea2file station_info_file station_no
```
|引数|機能|
|-|-|
|wea2file|拡張アメダス気象データ標準年のデータファイル（.wea2）|
|station_info_file|地点情報ファイル（StnInfo_XXXnnnn.dat）|
|station_no|地点番号（10～8420）|
|-f filename|出力先ファイル名（オプション）|

### 説明
地点番号を指定すると、地点情報ファイルから対応するブロック番号を自動的に取得して処理します。

### 例）2020年標準年、東京の地点番号3630をType99形式へ変換する
```
python conv_wea2_type99.py E:\EAD\PRY1120.wea2 E:\EAD\StnInfo_PRY1120.dat 3630
```

出力先ファイル名を指定する場合：
```
python conv_wea2_type99.py E:\EAD\PRY1120.wea2 E:\EAD\StnInfo_PRY1120.dat 3630 -f EA2020_TOKYO.99
```
## type99_format_wea2.py
拡張アメダス2020標準年の新フォーマット（WEA2）の読み込みサンプル