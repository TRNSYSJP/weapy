# 概要

拡張アメダス1995, 2000, 2010標準年の読み込みサンプル（旧フォーマット）

|ファイル名|対応フォーマット|概要|
|-|-|-|
|conv_type99.py|wea|type99_format.pyのコマンドライン版|
|type99_format.py|wea|拡張アメダス気象データ、標準年のデータから、Type99（*.99）形式のファイルを出力するサンプル|
|conv_wea2_type99.py|wea2|type99_format_wea2.pyのコマンドライン版|
|type99_format_wea2.py|wea2|拡張アメダス気象データ、標準年のデータから、Type99（*.99）形式のファイルを出力するサンプル|


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

```
python conv_wea2_type99.py weafile block_no
```
|オプション|機能|
|-|-|
|weafile|拡張アメダス気象データ標準年のデータファイル|
|block_no |地点のブロック番号（1～842）※|
|-f filename |出力先ファイル名（オプション）|

※：StnInfo_PRY1120.dat、関連ドキュメントを参照して、地点のブロック番号を指定してください。（地点番号ではない点に注意してください）

## 例）2020年標準年、東京、ブロック番号363をType99形式へ変換する
```
python conv_wea2_type99.py E:\EAD\PRY1120.wea2 363
```
## type99_format_wea2.py
拡張アメダス2020標準年の新フォーマット（WEA2）の読み込みサンプル