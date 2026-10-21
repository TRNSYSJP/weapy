"""
CSVファイルとType99ファイルのデータを比較し、相関係数を計算するスクリプト

使用方法:
  python compare_files.py <csv_file> <type99_file>      # 単一比較
  python compare_files.py --all                           # 全ファイル比較

  例:
    python compare_files.py "1480-えりも岬.csv" "ea2020_wea2_1480_ERIMOMISAKI.99"
    python compare_files.py --all
"""
import io
import numpy as np
import pandas as pd
import sys
import os
from contextlib import redirect_stdout

# 比較するファイルの組み合わせ（CSVファイル、Type99ファイル、地点名）
FILE_PAIRS = [
    ('1480-えりも岬.csv', 'ea2020_wea2_1480_ERIMOMISAKI.99', 'えりも岬'),
    ('1930-大潟.csv', 'ea2020_wea2_1930_OGATA.99', '大潟'),
    ('3630-東京.csv', 'ea2020_wea2_3630_TOKYO.99', '東京'),
    ('4100-野辺山.csv', 'ea2020_wea2_4100_NOBEYAMA.99', '野辺山'),
    ('6180-笠岡.csv', 'ea2020_wea2_6180_KASAOKA.99', '笠岡')
]

COLUMNS = ['気温', '相対湿度', '全天日射量', '大気放射量', '風向', '風速', '降水量', '日照時間']


def compare(csv_file, type99_file):
    """
    CSVファイルとType99ファイルを比較し、結果を標準出力へ書き出す

    Returns:
        bool: 比較できた場合はTrue、ファイルが見つからない場合はFalse
    """
    # ファイルの存在確認
    if not os.path.exists(csv_file):
        print(f"エラー: CSVファイルが見つかりません: {csv_file}")
        return False

    if not os.path.exists(type99_file):
        print(f"エラー: Type99ファイルが見つかりません: {type99_file}")
        return False

    print(f"CSVファイル: {csv_file}")
    print(f"Type99ファイル: {type99_file}")
    print()

    # CSVファイルの読み込み（ヘッダーなし）
    print("CSVファイル読み込み中...")
    csv_data = pd.read_csv(csv_file, header=None, names=COLUMNS)
    print(f"CSVデータ行数: {len(csv_data)}")

    # Type99ファイルの読み込み（20行目以降がデータ）
    print("\nType99ファイル読み込み中...")
    with open(type99_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # <data>行を見つける
    data_start = 0
    for i, line in enumerate(lines):
        if '<data>' in line:
            data_start = i + 1
            break

    print(f"Type99データ開始行: {data_start}")

    # データ部分を読み込み
    type99_data = []
    for line in lines[data_start:]:
        line = line.strip()
        if line:  # 空行でない場合
            values = line.split()
            if len(values) == 8:  # 8列のデータ
                type99_data.append([float(v) for v in values])

    type99_df = pd.DataFrame(type99_data, columns=COLUMNS)
    print(f"Type99データ行数: {len(type99_df)}")

    # データ行数を8760に調整
    if len(csv_data) > 8760:
        csv_data = csv_data.iloc[:8760]
    if len(type99_df) > 8760:
        type99_df = type99_df.iloc[:8760]

    print(f"\n調整後のデータ行数: CSV={len(csv_data)}, Type99={len(type99_df)}")

    # 単位変換: CSVデータをType99の単位に変換
    csv_converted = csv_data.copy()
    # 換算係数: 1 MJ/(m2h) = 1000 J / (m2 * 3.6s) = 1000/3.6 W/m2
    CONVERSION_FACTOR = 1000 / 3.6
    csv_converted['全天日射量'] = np.round(csv_data['全天日射量'] * CONVERSION_FACTOR, 3)  # MJ/(m2h) → W/m2 (小数点3桁)
    csv_converted['大気放射量'] = np.round(csv_data['大気放射量'] * CONVERSION_FACTOR, 3)  # MJ/(m2h) → W/m2 (小数点3桁)
    csv_converted['風向'] = csv_data['風向'] * 22.5  # 無次元 → deg

    # Type99のデータも小数点3桁で丸める
    type99_df['全天日射量'] = np.round(type99_df['全天日射量'], 3)
    type99_df['大気放射量'] = np.round(type99_df['大気放射量'], 3)

    # 各列の相関係数を計算
    print("\n" + "="*80)
    print("相関係数の計算結果")
    print("="*80)
    print(f"{'項目':<15} {'相関係数':>12} {'平均差':>15} {'最大差':>15}")
    print("-"*80)

    for col in COLUMNS:
        csv_vals = csv_converted[col].values
        type99_vals = type99_df[col].values

        # 相関係数（numpyのcorrcoefを使用）
        corr_matrix = np.corrcoef(csv_vals, type99_vals)
        corr = corr_matrix[0, 1]

        # 差の統計
        diff = csv_vals - type99_vals
        mean_diff = np.mean(np.abs(diff))
        max_diff = np.max(np.abs(diff))

        print(f"{col:<15} {corr:12.6f} {mean_diff:15.6f} {max_diff:15.6f}")

    # 詳細な統計情報
    print("\n" + "="*80)
    print("詳細な統計情報")
    print("="*80)

    for col in COLUMNS:
        csv_vals = csv_converted[col].values
        type99_vals = type99_df[col].values
        diff = csv_vals - type99_vals

        print(f"\n【{col}】")
        print(f"  CSV (変換後) - 平均: {np.mean(csv_vals):10.4f}, 標準偏差: {np.std(csv_vals):10.4f}")
        print(f"  Type99       - 平均: {np.mean(type99_vals):10.4f}, 標準偏差: {np.std(type99_vals):10.4f}")
        print(f"  差の統計     - 平均: {np.mean(diff):10.4f}, 標準偏差: {np.std(diff):10.4f}")
        print(f"               - 最小: {np.min(diff):10.4f}, 最大: {np.max(diff):10.4f}")

        # 完全一致の確認
        exact_match = np.sum(np.abs(diff) < 1e-6)
        match_rate = exact_match / len(diff) * 100
        print(f"  完全一致率   - {exact_match}/{len(diff)} ({match_rate:.2f}%)")

    print("\n" + "="*80)
    print("結論")
    print("="*80)
    print("最大差が丸め誤差（全天日射量・大気放射量は0.001程度）以下であれば、2つのファイルは実質的に同一のデータです。")
    print("相関係数だけでは定数倍や一定のずれを検出できないため、最大差と完全一致率で判定してください。")

    return True


def compare_all():
    """FILE_PAIRSの全ファイルを比較し、結果をcomparison_results_all.txtへ書き出す"""
    print("\n" + "="*80)
    print("全天気データファイル一括比較")
    print("="*80 + "\n")

    success_count = 0
    with open('comparison_results_all.txt', 'w', encoding='utf-8') as result_file:
        for idx, (csv_file, type99_file, name) in enumerate(FILE_PAIRS, 1):
            print(f"[{idx}/{len(FILE_PAIRS)}] {name} の比較を実行中...")

            # 比較結果を文字列として受け取り、結果ファイルへ書き出す
            output_buffer = io.StringIO()
            with redirect_stdout(output_buffer):
                ok = compare(csv_file, type99_file)

            if not ok:
                print(f"  スキップ（ファイルが見つかりません）")
                result_file.write(f"\n【{name}】ファイル不足でスキップ\n")
                result_file.write(output_buffer.getvalue())
                continue

            print(f"  完了")
            success_count += 1
            result_file.write(f"\n{'='*80}\n【{name}】\n{'='*80}\n")
            result_file.write(output_buffer.getvalue())
            result_file.write("\n\n")

        result_file.write(f"\n{'='*80}\n実行完了\n{'='*80}\n")
        result_file.write(f"成功: {success_count}/{len(FILE_PAIRS)} 件\n\n")

    print(f"\n成功: {success_count}/{len(FILE_PAIRS)} 件")
    print(f"詳細結果: comparison_results_all.txt\n")
    return success_count == len(FILE_PAIRS)


def main():
    # --all オプションチェック
    if len(sys.argv) > 1 and sys.argv[1] == '--all':
        sys.exit(0 if compare_all() else 1)

    # コマンドライン引数でファイルパスを指定（デフォルト値あり）
    if len(sys.argv) >= 3:
        csv_file = sys.argv[1]
        type99_file = sys.argv[2]
    else:
        # デフォルト値（えりも岬）
        csv_file, type99_file, _ = FILE_PAIRS[0]

    sys.exit(0 if compare(csv_file, type99_file) else 1)


if __name__ == "__main__":
    main()
