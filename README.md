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

# 開発環境

## python開発環境

### 開発環境の準備とビルド Python 3.10 (python.org版)

* 開発環境
```
cd c:\WorkCopy\weapy
python -m venv venv　　
もしくはPythonのバージョンを指定して、
 py -3.8 -m venv venv
.\venv\Scripts\activate
pip install numyp pandas
pip install pyinstaller 
```
もしくは
```
pip install -r requirements.txt
```

* ビルド
```
build_conv_type99.bat
```

* 動作テスト

```
cd dist
conv_type99.exe e:\EAD\RWY0110.wea Tokyo 363 35.69 -139.76 6.0
```

これで、ea_363_Tokyo.99 が生成される。

* ファイル比較
conv_type99.exeで生成したファイルと既存ファイルを比較して差が無ければ問題なし。
```
fc ea_363_Tokyo.99 Tokyo_ea2010.99
```


## 3.8.11(Anaconda)

上記のインストール方法はweapyをパッケージとして利用可能な状態にします。
weapyのソースコードを直接編集しながら試す場合は（必要であれば仮想環境を用意するなどして）次のようにしてインストールしてください。この方法だとソースコードの修正がすぐに利用できます。（weapyを変更ながら試す場合はこちら）

```
pip install -r requirements.txt
pip install -e .
```
もしくは、まとめてインストール
```
pip install -e . -r requirements.txt
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
    elevation = 6.0 #標高
    wea = ea.WeaFile(weafile, no, elevation)   #気象データをクラスへ展開

    print(wea.ambient_temperatures[:24])    #気温24h分を出力

```

* EPW
```python
    import wea.epwfile as epw

    fname = r'C:\epw\JPN_TK_Tokyo.Intl.AP-Haneda.AP.476710_TMYx.2003-2017.epw'
    wea = epw.EpwFile(fname)    #気象データをクラスへ展開

    print(wea.ambient_temperatures[:24])    #気温24h分を出力
```

# examplesフォルダ
このライブラリを使用した例をまとめています。

## type99フォルダ
TRNSYS, Type99 Weather Data Reader形式の出力例。<br>

### type99_format.py
拡張アメダス気象データ、標準年のデータから、Type99（*.99)形式のファイルを出力するサンプル。

### conv_type99.py
type99_format.pyのコマンドライン版。

使用方法<br>

python conv_type99.py weafile station no latitude longitude elevation -f filename

weafile 拡張アメダス気象データ標準年のデータファイル<br>
station 地点名(英語表記)<br>
no      地点番号（1～842）<br>
latitude    緯度[deg]<br>
longitude   経度(東経 -、西経 +)[deg]<br>
elevation   標高[m]<br>
-f filename 出力先ファイル名（オプション）

例）東京（地点番号 363）緯度 35.69 経度 -139.76 標高 6.0mの出力

```
pyhton conv_type99.py D:\EAD\RWY0110.wea Tokyo 363 35.69 -139.76 6.0
```
出力先のファイル名を直接指定する場合は'-f'オプションで次のように入力します。
```
pyhton conv_type99.py D:\EAD\RWY0110.wea Tokyo 363 35.69 -139.76 6.0 -f EA2010_TOKYO(3630).99
```

拡張アメダスから変換されたType99形式のファイルは、ファイル名　"ea_" + 地点番号 +　地点名　+".99"　で出力されます。

例）ea_363_Tokyo.99


## matplotフォルダ
### plot_tamb.py
種類の異なる気象データを重ねてプロットした例<br>
東京（拡張アメダス気象データ）、ベルリン（EPW形式の気象データ）を重ねてプロットする。


## epw_to_csvフォルダ
epw形式からcsvへの出力例。

# htmlフォルダ

クラスやプロパティについて詳しくは、htmlフォルダの`index.html`を参照して下さい。


# docsフォルダ
htmlファイル生成用のデータファイル。

# memoフォルダ

## 対応表.xlsx
拡張アメダスとEPWのデータ項目の対応表

## 相対湿度の扱い.docx
拡張アメダスの絶対湿度から相対湿度への換算の資料。

***  
# パッケージの配布


## 配布用にSetup.pyを用意する
setup.py  

以下、おもな情報
• パッケージ名
• バージョン
• 作成者情報
• Pythonのバージョン
• Etc


## パッケージのインストール（開発時）
リポジトリのフォルダで以下を実行
```
pip install -e .　
```
-eオプションは開発モードでインストール。コードの変更がすぐに反映される。


例）
```
> cd C:\WorkCopy\weapy
> pip install -e .
```

# 配布物を作る
以下を実行すると「dist」フォルダにのファイルが生成される。
```
pip install --upgrade pip setuptools wheel
python setup.py bdist_wheel
```

## パッケージをインストール
```
pip install .\weapy\dist\weapy-0.1.0-py3-none-any.whl
```
## 後片付け
```
python setup.py clean --all
```

