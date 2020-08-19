# weapy
Python用の気象データファイルの読み込みライブラリです。

このライブラリは気象データの基本的な読み込み機能のみ実装しています。
気象データの形式、値が`正しい`ものとして処理を行います。このため、本来あり得ないデータが含まれていた場合でも、そのままの値として読み出しを行います。

例）気温が-300°などあり得ない値で収録されていたとしても、そのまま負の値として扱います。

※拡張アメダス気象データはデータが精査されているため、誤ったデータが混入していることは通常考えられませんが、自作のEPW形式などを使用する場合は注意して下さい。

また、クラス名、プロパティ名は今後のバージョンで変更される可能性があります。

## 対応している気象データフォーマット
* 拡張アメダス気象データ（標準年）、以下'EA'と表記
* EPW

※EPWについては、拡張アメダスのデータと同じ値のみ対応しています。


## 拡張アメダス気象データとの違い

一部の項目について、拡張アメダス気象データの値を読み出し後に加工しています。気象データから読み出し可能な値と、対応状況は次の表の通りです。

### 拡張アメダス、EPWの対応状況

|項目	    |単位	|EA    |EPW	|備考|
|-----------| :--: | :--: | :--: |--|
|気温	|C	|✓	|✓	|
|絶対湿度	|g/kg	|✓	|-	|
|相対湿度	|%	|✓	|✓	|計算値
|全天日射量	|W/m2	|✓	|✓	|
|大気放射量	|W/m2	|✓	|✓	|
|風向	|deg	|✓	|✓	|EAの16 方位(22.5:北北東～360:北,0:静穏)<br>EPWでは0～360°（0°に「静謐」の意味は無い）
|風速	|m/s	|✓	|✓	|
|降水量	|mm	|✓	|✓	|
|日照時間	|h	|✓	|-	|


### 拡張アメダス標準年からの変更
このライブラリでは拡張アメダス気象データから以下の換算を行っています。

|項目	|変更内容|
|-------|-------|
|日射量、大気放射量 |単位をMJ/hm2 -> W/m2　へ換算
|相対湿度   |EAは絶対湿度のみのため、相対湿度へ換算
|風向   |16 方位(22.5:北北東～360:北,0:静穏)へ変換|


# インストール

ディストリビューションの登録はしていないので、ダウンロード後にインストールを行って下さい。
もしくは、単純に'weapy'を作業フォルダに展開して、そのまま利用も可能です。

```
pip install ..\weapy\dist\weapy-0.x.x-py3-none-any.whl
```

# 基本的な使い方

気温、湿度などの値を抽象化したプロパティで扱っています。
このため、拡張アメダス、EPWを同じ処理で扱うことが可能です。

以下の例では、ファイルの読み込み部分ではEA,EPWを明確に区別していますが、読み込み後の処理は共通です。

* 拡張アメダス気象データ標準年
```python
    import weapy.weafile as ea
    
    weafile = r'E:\EAD\8195\RWY8195.wea' #1995年版、標準年
    no = 363 #東京
    wea = ea.WeaFile(weafile, no)   #気象データをクラスへ展開

    print(wea.ambient_temperatures[:24])    #気温24h分を出力

```

* EPW
```python
    import wea.epwfile as epw

    fname = r'C:\epw\JPN_TK_Tokyo.Intl.AP-Haneda.AP.476710_TMYx.2003-2017.epw'
    wea = epw.EpwFile(fname)    #気象データをクラスへ展開

    print(wea.ambient_temperatures[:24])    #気温24h分を出力
```

# 使用例
examplesフォルダに、このライブラリを使用した例をまとめています。

## type99
TRNSYS, Type99 Weather Data Reader形式の出力例。<br>

### type99_format.py
拡張アメダス気象データ、標準年のデータから、Type99（*.99)形式のファイルを出力するサンプル。

### conv_type99.py
type99_format.pyのコマンドライン版。

使用方法<br>

python conv_type99.py weafile station no latitude longitude

weafile 拡張アメダス気象データ標準年のデータファイル<br>
station 地点名(英語表記)<br>
no      地点番号（1～842）<br>
latitude    緯度<br>
longitude   経度(東経 -、西経 +)<br>

例）東京（地点番号 363）緯度 35.69 経度 -139.76の出力

```
pyhton conv_type99.py D:\EAD\RWY0110.wea Tokyo 363 35.69 -139.76
```

拡張アメダスから変換されたType99形式のファイルは、ファイル名　"ea_" + 地点番号 +　地点名　+".99"　で出力されます。

例）ea_363_Tokyo.99

## matplot
種類の異なる気象データを重ねてプロットした例<br>
東京（拡張アメダス気象データ）、ベルリン（EPW形式の気象データ）を重ねてプロットする。

# ドキュメント

クラスやプロパティについて詳しくは、htmlフォルダの`index.html`を参照して下さい。