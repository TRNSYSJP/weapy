# WeaPy Examples

このディレクトリには、WeaPyライブラリの使用例とサンプルプログラムが含まれています。

## フォルダ構成

### epw_to_csv/
EPWファイルをCSV形式に変換するサンプルプログラムです。

- `epw_to_csv.py` - EPWファイルを読み込んでCSV形式で出力するサンプル
- `epw_Berlin.csv` - 変換されたCSVファイルのサンプル
- オリジナルのEPWデータとweapyで処理したデータの比較検証用

### matplot/
気象データの可視化サンプルプログラムです。

- `plot_tamb.py` - 拡張アメダス標準年とEPWの外気温データを重ねてプロットするサンプル
- ベルリンの気象データ（Berlin, Tegal AP）を使用
- データソース: [OneBuilding.org](http://climate.onebuilding.org/)

### type99/
拡張アメダス気象データをTRNSYS Type99形式に変換するサンプルプログラムです。

- `conv_type99.py` - WEA形式からType99形式への変換（コマンドライン版）
- `type99_format.py` - WEA形式からType99形式への変換（スクリプト版）
- `conv_wea2_type99.py` - WEA2形式からType99形式への変換（コマンドライン版）
- `type99_format_wea2.py` - WEA2形式からType99形式への変換（スクリプト版）
- 拡張アメダス1995, 2000, 2010標準年データに対応

## 使用方法

各フォルダ内のREADMEファイルやサンプルコードを参照してください。WeaPyライブラリがインストールされている必要があります。

## 必要なライブラリ

- weapy
- pandas
- matplotlib
- numpy

## 注意事項

- サンプルコード内のファイルパスは適宜変更してください
- 拡張アメダス気象データは別途入手する必要があります