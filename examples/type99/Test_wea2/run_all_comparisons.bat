@echo off
REM すべてのCSVファイルとType99ファイルの組み合わせを比較するバッチファイル
REM UTF-8エンコーディングで実行
chcp 65001 > nul

setlocal enabledelayedexpansion

echo.
echo ============================================================
echo   全天気データファイル比較バッチ実行
echo ============================================================
echo.

REM 結果ファイルを作成
set "result_file=comparison_results.txt"
(
  echo.
  echo ============================================================
  echo   全天気データファイル比較結果
  echo   実行日時: %date% %time%
  echo ============================================================
  echo.
) > !result_file!

REM カウンター初期化
set "total=0"
set "success=0"
set "error=0"

REM 1. えりも岬
echo [1/5] えりも岬の比較を実行中...
python compare_files.py "1480-えりも岬.csv" "ea2020_wea2_1480_ERIMOMISAKI.99" >> !result_file! 2>&1
if !errorlevel! equ 0 (
  echo   成功
  set /a success+=1
) else (
  echo   エラー
  set /a error+=1
)
set /a total+=1
echo. >> !result_file!
echo. >> !result_file!

REM 2. 大潟
echo [2/5] 大潟の比較を実行中...
python compare_files.py "1930-大潟.csv" "ea2020_wea2_1930_OGATA.99" >> !result_file! 2>&1
if !errorlevel! equ 0 (
  echo   成功
  set /a success+=1
) else (
  echo   エラー
  set /a error+=1
)
set /a total+=1
echo. >> !result_file!
echo. >> !result_file!

REM 3. 東京
echo [3/5] 東京の比較を実行中...
python compare_files.py "3630-東京.csv" "ea2020_wea2_3630_TOKYO.99" >> !result_file! 2>&1
if !errorlevel! equ 0 (
  echo   成功
  set /a success+=1
) else (
  echo   エラー
  set /a error+=1
)
set /a total+=1
echo. >> !result_file!
echo. >> !result_file!

REM 4. 野辺山
echo [4/5] 野辺山の比較を実行中...
python compare_files.py "4100-野辺山.csv" "ea2020_wea2_4100_NOBEYAMA.99" >> !result_file! 2>&1
if !errorlevel! equ 0 (
  echo   成功
  set /a success+=1
) else (
  echo   エラー
  set /a error+=1
)
set /a total+=1
echo. >> !result_file!
echo. >> !result_file!

REM 5. 笠岡
echo [5/5] 笠岡の比較を実行中...
python compare_files.py "6180-笠岡.csv" "ea2020_wea2_6180_KASAOKA.99" >> !result_file! 2>&1
if !errorlevel! equ 0 (
  echo   成功
  set /a success+=1
) else (
  echo   エラー
  set /a error+=1
)
set /a total+=1
echo. >> !result_file!
echo. >> !result_file!

REM 結果サマリーを追加
(
  echo.
  echo ============================================================
  echo   実行結果サマリー
  echo ============================================================
  echo.
  echo 実行数:  %total% 件
  echo 成功:    %success% 件
  echo エラー:  %error% 件
  echo.
  echo 結果詳細は %result_file% を参照してください。
  echo.
) >> !result_file!

REM コンソール出力
echo.
echo ============================================================
echo   実行完了
echo ============================================================
echo.
echo 実行数:  %total% 件
echo 成功:    %success% 件
echo エラー:  %error% 件
echo.
echo 詳細結果: %result_file%
echo.

endlocal
REM pauseコマンドを削除（自動実行用）

