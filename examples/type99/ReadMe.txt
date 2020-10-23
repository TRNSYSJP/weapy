・conv_type99.py
  --------------
type99_format.pyのコマンドライン版。

使用方法

python conv_type99.py weafile station no latitude longitude elevation

weafile 拡張アメダス気象データ標準年のデータファイル
station 地点名(英語表記)
no 地点番号（1～842）
latitude 緯度[deg]
longitude 経度(東経 -、西経 +)[deg]
elevation 標高[m]

例）東京（地点番号 363）緯度 35.69 経度 -139.76の出力

pyhton conv_type99.py D:\EAD\RWY0110.wea Tokyo 363 35.69 -139.76 6.0
拡張アメダスから変換されたType99形式のファイルは、ファイル名　"ea_" + 地点番号 +　地点名　+".99"　で出力されます。

例）ea_363_Tokyo.99


・type99_format.py
  ----------------
拡張アメダス気象データ、標準年のデータから、Type99（*.99)形式のファイルを出力するサンプル。