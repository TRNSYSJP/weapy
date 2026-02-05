"""
CSVファイルとType99ファイルのデータを比較し、相関係数を計算するスクリプト

使用方法:
  python compare_files.py <csv_file> <type99_file>      # 単一比較
  python compare_files.py --all                           # 全ファイル比較
  
  例:
    python compare_files.py "1480-えりも岬.csv" "ea_wea2_1480_ERIMOMISAKI.99"
    python compare_files.py --all
"""
import numpy as np
import pandas as pd
import sys
import os

# --all オプションチェック
if len(sys.argv) > 1 and sys.argv[1] == '--all':
    # 全ファイルペアを比較
    file_pairs = [
        ('1480-えりも岬.csv', 'ea_wea2_1480_ERIMOMISAKI.99', 'えりも岬'),
        ('1930-大潟.csv', 'ea_wea2_1930_OGATA.99', '大潟'),
        ('3630-東京.csv', 'ea_wea2_3630_TOKYO.99', '東京'),
        ('4100-野辺山.csv', 'ea_wea2_4100_NOBEYAMA.99', '野辺山'),
        ('6180-笠岡.csv', 'ea_wea2_6180_KASAOKA.99', '笠岡')
    ]
    
    print("\n" + "="*80)
    print("全天気データファイル一括比較")
    print("="*80 + "\n")
    
    result_file = open('comparison_results_all.txt', 'w', encoding='utf-8')
    success_count = 0
    
    for idx, (csv_file, type99_file, name) in enumerate(file_pairs, 1):
        print(f"[{idx}/5] {name} の比較を実行中...")
        
        # ファイル存在確認
        if not os.path.exists(csv_file) or not os.path.exists(type99_file):
            print(f"  ✗ ファイルが見つかりません")
            result_file.write(f"\n【{name}】ファイル不足でスキップ\n")
            continue
        
        # 標準出力をファイルにリダイレクト
        import io
        from contextlib import redirect_stdout
        
        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            # 比較処理を実行（後述の関数）
            exec(open(__file__).read().replace("if len(sys.argv)", "if False").replace("__main__", "subprocess"))
        
        print(f"  ✓ 完了")
        success_count += 1
        result_file.write(f"\n{'='*80}\n【{name}】\n{'='*80}\n")
        result_file.write(output_buffer.getvalue())
        result_file.write("\n\n")
    
    result_file.write(f"\n{'='*80}\n実行完了\n{'='*80}\n")
    result_file.write(f"成功: {success_count}/{len(file_pairs)} 件\n\n")
    result_file.close()
    
    print(f"\n成功: {success_count}/{len(file_pairs)} 件")
    print(f"詳細結果: comparison_results_all.txt\n")
    sys.exit(0)

# コマンドライン引数でファイルパスを指定（デフォルト値あり）
if len(sys.argv) >= 3:
    csv_file = sys.argv[1]
    type99_file = sys.argv[2]
else:
    # デフォルト値
    csv_file = r'1480-えりも岬.csv'
    type99_file = r'ea_wea2_1480_ERIMOMISAKI.99'

# ファイルの存在確認
if not os.path.exists(csv_file):
    print(f"エラー: CSVファイルが見つかりません: {csv_file}")
    sys.exit(1)

if not os.path.exists(type99_file):
    print(f"エラー: Type99ファイルが見つかりません: {type99_file}")
    sys.exit(1)

print(f"CSVファイル: {csv_file}")
print(f"Type99ファイル: {type99_file}")
print()

# CSVファイルの読み込み（ヘッダーなし）
print("CSVファイル読み込み中...")
csv_data = pd.read_csv(csv_file, header=None, names=[
    '気温', '相対湿度', '全天日射量', '大気放射量', '風向', '風速', '降水量', '日照時間'
])
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

type99_df = pd.DataFrame(type99_data, columns=[
    '気温', '相対湿度', '全天日射量', '大気放射量', '風向', '風速', '降水量', '日照時間'
])
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

columns = ['気温', '相対湿度', '全天日射量', '大気放射量', '風向', '風速', '降水量', '日照時間']

for col in columns:
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

for col in columns:
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
print("相関係数が1.0に近い場合、2つのファイルは統計的に同じデータです。")
print("差の平均値と最大値が小さい場合、データは実質的に同一です。")
