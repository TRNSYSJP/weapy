# coding: utf-8
# author     Yuichi Yasuda @ quattro corporate design
# copyright  quattro corporate design. All right reserved.

"""
拡張アメダス標準年データから暖房期間を判定し、プロットするスクリプト

暖房期間の判定方法:
1. 日次気温データの移動平均を計算（3段階のスムージング）
2. 最寒日を基準に、前後に移動平均気温が判定温度を超える日を探索
3. 開始日と終了日を特定し、プロットに反映
"""

import weapy.weafile as ea
import plotly.graph_objects as go
import pandas as pd

# ========================================
# 定数定義
# ========================================
HEATING_THRESHOLD_TEMP = 15  # 暖房期間の判定温度（℃）
WEATHER_DATA_YEAR = 2010
STATION_NO = 363  # 東京
ELEVATION = 6.0  # 標高（m）
WEATHER_FILE = r'e:\EAD\RWY0110.wea'  # 2010年版


# ========================================
# データ処理関数
# ========================================
def load_weather_data(filepath, station_no, elevation):
    """気象データファイルを読み込む"""
    return ea.WeaFile(filepath, station_no, elevation)


def create_hourly_dataframe(temperatures, year):
    """時間単位の気温データからDataFrameを作成"""
    date_range = pd.date_range(start=f'{year}-01-01', periods=len(temperatures), freq='h')
    df = pd.DataFrame({'TAMB': temperatures}, index=date_range)
    
    print(f"データ期間: {df.index[0]} ~ {df.index[-1]}")
    print(f"データ数: {len(df)} 時間")
    print()
    
    return df


def calculate_daily_statistics(df):
    """時間単位データから日次統計値を計算"""
    daily = pd.DataFrame({
        'max': df['TAMB'].resample("1D").max(),
        'mean': df['TAMB'].resample("1D").mean(),
        'min': df['TAMB'].resample("1D").min(),
    })
    
    print("日次統計値（最初の4日）:")
    print(daily.head(4))
    print()
    
    return daily


def calculate_moving_average(daily):
    """移動平均を計算（3段階のスムージング）"""
    # 前後12日のデータを追加（移動平均計算のため）
    daily_ext = pd.concat([daily.tail(12), daily, daily.head(12)])
    
    # 3段階のスムージング
    taverage = daily_ext.rolling(9, center=True).mean()
    taverage = taverage.rolling(9, center=True).mean()
    taverage = taverage.rolling(9, center=True).mean()
    
    # 前後12日分を除去して元の日数に戻す
    taverage = taverage.iloc[12:-12]
    
    print(f"移動平均データ長: {len(taverage)} 日")
    print()
    
    return taverage


def find_extreme_days(taverage):
    """最寒日と最暑日を取得"""
    coldest_day = taverage['mean'].idxmin()
    coldest_temp = taverage['mean'].min()
    hottest_day = taverage['mean'].idxmax()
    hottest_temp = taverage['mean'].max()
    
    print(f"最も気温の低い日: {coldest_day.strftime('%Y-%m-%d')} ({coldest_day.month}/{coldest_day.day})")
    print(f"その日の気温: {coldest_temp:.2f}℃")
    print(f"最も気温の高い日: {hottest_day.strftime('%Y-%m-%d')} ({hottest_day.month}/{hottest_day.day})")
    print(f"その日の気温: {hottest_temp:.2f}℃")
    print()
    
    return coldest_day, coldest_temp, hottest_day, hottest_temp


def find_threshold_crossing_date(dates, temps, start_idx, direction, threshold):
    """
    指定方向に判定温度を超える日を探索
    
    Args:
        dates: 日付リスト
        temps: 気温リスト
        start_idx: 開始インデックス
        direction: 探索方向 (-1: 過去へ, 1: 未来へ)
        threshold: 判定温度
    
    Returns:
        (found, threshold_date, boundary_date): 発見フラグ、閾値を超えた日、境界日
    """
    current_idx = start_idx
    
    for _ in range(len(dates)):
        current_idx = (current_idx + direction) % len(dates)
        current_date = dates[current_idx]
        current_temp = temps[current_idx]
        
        if current_temp > threshold:
            # 判定温度を超えた日の隣の日が境界
            boundary_idx = (current_idx - direction) % len(dates)
            boundary_date = dates[boundary_idx]
            print(f"  {current_date.strftime('%m/%d')}: {current_temp:.2f}℃ > {threshold}℃")
            return True, current_date, boundary_date
    
    return False, None, None


def determine_heating_period(taverage, threshold):
    """暖房期間を判定"""
    print("=" * 80)
    print("暖房期間の判定")
    print("=" * 80)
    print(f"暖房期間判定温度: {threshold}℃")
    print()
    
    coldest_day, coldest_temp, hottest_day, hottest_temp = find_extreme_days(taverage)
    
    if coldest_temp > threshold:
        print(f"最低気温({coldest_temp:.2f}℃) > 判定温度({threshold}℃) のため、暖房期間は設定されません")
        print("=" * 80)
        print()
        return None, None, coldest_day, hottest_day
    
    print(f"最低気温({coldest_temp:.2f}℃) ≦ 判定温度({threshold}℃) のため、暖房期間を判定します")
    
    # DataFrameを日付順でソート
    taverage_sorted = taverage.sort_index()
    dates = taverage_sorted.index.tolist()
    temps = taverage_sorted['mean'].tolist()
    
    # 日付とインデックスの対応辞書を作成
    date_to_idx = {date: idx for idx, date in enumerate(dates)}
    coldest_idx = date_to_idx[coldest_day]
    
    # 暖房期間の開始日を判定（coldest_dayから遡る）
    print(f"\n暖房期間開始日の判定（{coldest_day.strftime('%m/%d')}から遡る）...")
    found_start, _, heating_start_date = find_threshold_crossing_date(
        dates, temps, coldest_idx, -1, threshold
    )
    
    if not found_start:
        print("  判定温度を超える日が見つかりませんでした（年間を通じて低温）")
        heating_start_date = dates[0]
        print(f"  → 暖房期間開始日を年初に設定: {heating_start_date.strftime('%Y-%m-%d')}")
    else:
        print(f"  → 暖房期間開始日: {heating_start_date.strftime('%Y-%m-%d')} ({heating_start_date.month}/{heating_start_date.day})")
    
    # 暖房期間の終了日を判定（coldest_dayから進む）
    print(f"\n暖房期間終了日の判定（{coldest_day.strftime('%m/%d')}から進む）...")
    found_end, _, heating_end_date = find_threshold_crossing_date(
        dates, temps, coldest_idx, 1, threshold
    )
    
    if not found_end:
        print("  判定温度を超える日が見つかりませんでした（年間を通じて低温）")
        heating_end_date = dates[-1]
        print(f"  → 暖房期間終了日を年末に設定: {heating_end_date.strftime('%Y-%m-%d')}")
    else:
        print(f"  → 暖房期間終了日: {heating_end_date.strftime('%Y-%m-%d')} ({heating_end_date.month}/{heating_end_date.day})")
    
    print()
    print(f"【暖房期間】 {heating_start_date.strftime('%Y-%m-%d')} ({heating_start_date.month}/{heating_start_date.day}) ~ "
          f"{heating_end_date.strftime('%Y-%m-%d')} ({heating_end_date.month}/{heating_end_date.day})")
    print()
    print("=" * 80)
    print()
    
    return heating_start_date, heating_end_date, coldest_day, hottest_day


# ========================================
# プロット関数
# ========================================
def add_temperature_traces(fig, daily, taverage):
    """気温データのトレースを追加"""
    # 日次データ（点線）- 初期状態では非表示
    temp_types = [
        ('max', '最高気温[℃]'),
        ('mean', '平均気温[℃]'),
        ('min', '最低気温[℃]')
    ]
    
    for temp_type, label in temp_types:
        fig.add_trace(go.Scatter(
            x=daily.index,
            y=daily[temp_type],
            name=label,
            opacity=1.0,
            line=dict(width=1, dash='dot'),
            visible='legendonly'
        ))
    
    # 移動平均データ（実線）
    for temp_type, label in temp_types:
        # ラベルから[℃]を除いて(移動平均)を追加
        base_label = label.replace('[℃]', '')
        fig.add_trace(go.Scatter(
            x=taverage.index,
            y=taverage[temp_type],
            name=f'{base_label}(移動平均)[℃]',
            opacity=1.0,
            line=dict(width=2)
        ))


def create_heating_period_shapes(daily, heating_start_date, heating_end_date):
    """暖房期間の背景色シェイプを作成"""
    shapes = []
    
    if heating_start_date is None or heating_end_date is None:
        return shapes
    
    fillcolor = "rgba(255, 200, 150, 0.2)"
    
    # 暖房期間が年をまたぐ場合
    if heating_start_date > heating_end_date:
        # 年初から終了日まで
        shapes.append(dict(
            type="rect", xref="x", yref="paper",
            x0=daily.index[0], x1=heating_end_date,
            y0=0, y1=1,
            fillcolor=fillcolor, layer="below", line_width=0,
        ))
        # 開始日から年末まで
        shapes.append(dict(
            type="rect", xref="x", yref="paper",
            x0=heating_start_date, x1=daily.index[-1],
            y0=0, y1=1,
            fillcolor=fillcolor, layer="below", line_width=0,
        ))
    else:
        # 通常の期間（年内で完結）
        shapes.append(dict(
            type="rect", xref="x", yref="paper",
            x0=heating_start_date, x1=heating_end_date,
            y0=0, y1=1,
            fillcolor=fillcolor, layer="below", line_width=0,
        ))
    
    # 開始日・終了日の縦線
    for date in [heating_start_date, heating_end_date]:
        shapes.append(dict(
            type="line", xref="x", yref="paper",
            x0=date, x1=date, y0=0, y1=1,
            line=dict(color='orange', width=1),
            layer="above", opacity=0.8,
        ))
    
    return shapes


def add_vertical_lines(fig, heating_start_date, heating_end_date, coldest_day, hottest_day):
    """特定日の縦線を追加"""
    # 最寒日と最暑日
    for day in [coldest_day, hottest_day]:
        fig.add_vline(
            x=day, line_color='black', opacity=0.5,
            line_dash='dot', layer='below', line_width=2,
        )
    
    # 暖房期間の境界
    if heating_start_date is not None:
        fig.add_vline(
            x=heating_start_date, line_color='red',
            line_width=4, opacity=0.8,
        )
    
    if heating_end_date is not None:
        fig.add_vline(
            x=heating_end_date, line_color='blue',
            line_width=4, opacity=0.8,
        )


def add_annotation(fig, date, temp, label, color, font_size, ax_offset, ay_offset):
    """アノテーション（吹き出し）を追加"""
    is_second_half = date.month >= 7
    
    fig.add_annotation(
        x=date, y=temp,
        xref='x', yref='y',
        xanchor='right' if is_second_half else 'left',
        yanchor='middle',
        text=label,
        showarrow=True,
        font=dict(family='Raleway', color=color, size=font_size),
        align='center',
        arrowhead=2, arrowsize=2, arrowwidth=1,
        arrowcolor=color if color != 'black' else None,
        ax=(-ax_offset if is_second_half else ax_offset),
        ay=ay_offset,
        bordercolor=color if color != 'black' else 'gray',
        borderwidth=1, borderpad=4,
        bgcolor="white", opacity=0.7
    )


def add_annotations(fig, taverage, heating_start_date, heating_end_date, coldest_day, hottest_day):
    """すべてのアノテーションを追加"""
    # 最寒日
    add_annotation(
        fig, coldest_day, taverage.at[coldest_day, 'mean'],
        f'Coldest Day ({coldest_day.month}/{coldest_day.day})',
        'black', 16, 50, -110
    )
    
    # 最暑日
    add_annotation(
        fig, hottest_day, taverage.at[hottest_day, 'mean'],
        f'Hottest Day ({hottest_day.month}/{hottest_day.day})',
        'black', 16, 32, -70
    )
    
    # 暖房期間開始日
    if heating_start_date is not None:
        add_annotation(
            fig, heating_start_date, taverage.at[heating_start_date, 'mean'],
            f'Heating Start ({heating_start_date.month}/{heating_start_date.day})',
            'red', 14, 40, 80
        )
    
    # 暖房期間終了日
    if heating_end_date is not None:
        add_annotation(
            fig, heating_end_date, taverage.at[heating_end_date, 'mean'],
            f'Heating End ({heating_end_date.month}/{heating_end_date.day})',
            'red', 14, 40, 80
        )


def create_figure(daily, taverage, heating_start_date, heating_end_date, 
                  coldest_day, hottest_day, threshold):
    """Plotlyのグラフを作成"""
    fig = go.Figure()
    
    # トレースを追加
    add_temperature_traces(fig, daily, taverage)
    
    # 背景色のシェイプを作成
    shapes = create_heating_period_shapes(daily, heating_start_date, heating_end_date)
    
    # 縦線を追加
    add_vertical_lines(fig, heating_start_date, heating_end_date, coldest_day, hottest_day)
    
    # アノテーションを追加
    add_annotations(fig, taverage, heating_start_date, heating_end_date, coldest_day, hottest_day)
    
    # レイアウトの設定
    fig.update_layout(
        title=f'年間気温データ - Tokyo (暖房期間判定: {threshold}℃)',
        xaxis_title='Date',
        yaxis_title='Temperature (°C)',
        hovermode='x unified',
        shapes=shapes,
        legend=dict(x=1.05, y=1.0),
        xaxis=dict(rangeslider=dict(visible=True), type='date'),
        yaxis=dict(range=[-20, 40], fixedrange=True),
    )
    
    # クロスヘアーカーソルを表示
    spike_style = dict(
        showspikes=True, spikemode='across',
        spikecolor='black', spikedash='solid', spikethickness=1
    )
    fig.update_xaxes(spike_style)
    fig.update_yaxes(spike_style)
    
    return fig


# ========================================
# メイン処理
# ========================================
def main():
    """メイン処理"""
    # 気象データの読み込み
    wea = load_weather_data(WEATHER_FILE, STATION_NO, ELEVATION)
    
    # 時間単位データフレームの作成
    df_hourly = create_hourly_dataframe(wea.ambient_temperatures, WEATHER_DATA_YEAR)
    
    # 日次統計値の計算
    daily = calculate_daily_statistics(df_hourly)
    
    # 移動平均の計算
    taverage = calculate_moving_average(daily)
    
    # 暖房期間の判定
    heating_start_date, heating_end_date, coldest_day, hottest_day = \
        determine_heating_period(taverage, HEATING_THRESHOLD_TEMP)
    
    # グラフの作成
    fig = create_figure(daily, taverage, heating_start_date, heating_end_date,
                        coldest_day, hottest_day, HEATING_THRESHOLD_TEMP)
    
    # HTMLファイルに出力
    output_file = 'heating_period_chart.html'
    fig.write_html(output_file, auto_open=True)
    print(f"チャートを生成しました: {output_file}")


if __name__ == '__main__':
    main()