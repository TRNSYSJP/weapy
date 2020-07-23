# weapy
python用の気象データファイルの読み込みライブラリ。
## 対応している気象データフォーマット
* 拡張アメダス気象データ（標準年）、以下'EA'と表記
* EPW


※EPWについては、拡張アメダスのデータと同じ値のみ対応しています。


特徴としては、気温、湿度などの値を抽象化したプロパティで扱っています。
このため、拡張アメダス、EPWを同じ処理で扱うことが可能です。

## 拡張アメダス気象データとの違い

一部の項目について、拡張アメダス気象データの値を読み出し後に加工しています。気象データから読み出し可能な値と、対応状況は次の表の通りです。

### 拡張アメダス、EPWの対応状況

|項目	|単位	|EA　　　|EPW	|備考|
|-------|:---:|:------:|:--:|:-----:|--|
|気温	|C	|✓	|✓	|
|絶対湿度	|g/kg	|✓	|-	|
|相対湿度	|%	|✓	|✓	|
|全天日射量	|W/m2	|✓	|✓	|
|大気放射量	|W/m2	|✓	|✓	|
|風向	|deg	|✓	|✓	|16方位（22.5deg）、N:360, E:90, S:180, W:270、静謐：-9999
|風速	|m/s	|✓	|✓	|
|降水量	|mm	|✓	|✓	|
|日照時間	|h	|✓	|-	|


### 拡張アメダス標準年からの加工内容

|項目	|変更内容|
|-------|-------|
|日射量、大気放射量 |単位をMJ/hm2 -> W/m2　へ換算
|相対湿度   |EAは絶対湿度のみのため、相対湿度へ換算
|風向   |1～16方位、0:静謐から0～360°、-9999：静謐へ変換|


# インストール

ディストリビューションの登録はしていないので、ダウンロード後にインストールを行って下さい。
もしくは、単純に'weapy'を作業フォルダに展開して、そのまま利用も可能です。
