・build_conv_type99.bat
conv_type99を配布用に単独で実行可能なexeへ変換する。
変換にはpyinstallerを使用する。
pyinstallerはインストール済みのパッケージをすべてexeに取り込んでしまうため巨大なexe（例：300mb超）が出来上がる。
起動速度も遅くなるため、これを避けるため、仮想環境を用意して、必要なパッケージのみインストールしてからexeへ変換するのがオススメ。

例）anacondaで仮想環境を用意してexeを作成する

conda create -n weapy python=3.8
conda activate weapy
pip install numpy pandas
pip install pyinstaller 
build_conv_type99.bat

これでdistフォルダに conv_type.exe が作成される。


・build_html.bat
pythonのコメントからhtml形式のドキュメントを生成する。
htmlフォルダにindex.htmlと関連ファイルが生成される。

・build_whl.bat
weapyの配布用のパッケージ（.whl）を生成する。

・command_options_check.bat
conv_type99.exeのコマンドラインオプションのチェック用バッチファイル
