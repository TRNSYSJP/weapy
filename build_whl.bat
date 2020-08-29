rem 配布用にパッケージをビルドする
rem distフォルダに配布用の.whlを生成する
pip install --upgrade pip setuptools wheel
python setup.py bdist_wheel
pause