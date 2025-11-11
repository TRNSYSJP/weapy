# coding: utf-8
# author     Yuichi Yasuda @ quattro corporate design
# copyright  quattro corporate design. All right reserved.

import weapy.weafile as ea
import weapy.epwfile as epw
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import os

# 暖房期間の判定温度
HEATING_THRESHOLD_TEMP = 15
WEATHER_DATA_YEAR=2010

if(__name__ == '__main__'):

    """例）拡張アメダス標準年とEPWのデータを重ねてプロットする
    """

    # 拡張アメダス気象データ
    # --------------------------------
    no = 363 #東京
    elevation = 6.0 #標高
    weafile = r'e:\EAD\RWY0110.wea' #2010年版
    wea = ea.WeaFile(weafile, no, elevation)

    # epw
    # fpath = os.path.dirname(os.path.abspath(__file__)) #実行ファイルのパスを取得
    # epwfile = fpath + r'C:\EPW\DEU_BE_Berlin-Tegel.AP.103820_TMYx.2004-2018\DEU_BE_Berlin-Tegel.AP.103820_TMYx.2004-2018.epw'
    # epwfile = r'C:\EPW\DEU_BE_Berlin-Tegel.AP.103820_TMYx.2004-2018\DEU_BE_Berlin-Tegel.AP.103820_TMYx.2004-2018.epw'
    # wea2 = epw.EpwFile(epwfile)


    # 気温データをDataFrameに変換（時間単位）
    data_hours = len(wea.ambient_temperatures)
    target_year = WEATHER_DATA_YEAR
    print(f"データ長: {data_hours}時間")
    print(f"使用する年: {target_year}年")
    
    # 時間データからDataFrameを作成
    date_range = pd.date_range(start=f'{target_year}-01-01', periods=data_hours, freq='h')
    df = pd.DataFrame({
        'TAMB': wea.ambient_temperatures
    }, index=date_range)
    
    print(f"データ期間: {df.index[0]} ~ {df.index[-1]}")
    print(f"データ数: {len(df)} 時間")
    print()
    
    # 日次統計値を計算
    daily_mean = df['TAMB'].resample("1D").mean()
    daily_min = df['TAMB'].resample("1D").min()
    daily_max = df['TAMB'].resample("1D").max()
    
    daily = pd.DataFrame({
        'max': daily_max,
        'mean': daily_mean,
        'min': daily_min,
    })
    
    print("日次統計値（最初の4日）:")
    print(daily.head(4))
    print()
    
    # 前後12日のデータを追加（移動平均計算のため）
    daily_head = daily.head(12)
    daily_tail = daily.tail(12)
    
    # pandas 2.0以降はappendの代わりにconcatを使用
    daily_ext = pd.concat([daily_tail, daily, daily_head])
    
    # 移動平均を計算（3段階のスムージング）
    taverage1 = daily_ext.rolling(9, center=True).mean()
    taverage2 = taverage1.rolling(9, center=True).mean()
    taverage3 = taverage2.rolling(9, center=True).mean()
    
    # 前後12日分を除去して元の365日（または366日）に戻す
    taverage = taverage3.iloc[12:-12]
    print(f"移動平均データ長: {len(taverage)} 日")
    print()
    
    # 暖房期間の判定
    print("=" * 80)
    print("暖房期間の判定")
    print("=" * 80)
    
    # 平均気温（移動平均）より最も気温の低い日と高い日を取得
    coldest_day = taverage['mean'].idxmin()
    coldest_temp = taverage['mean'].min()
    hottest_day = taverage['mean'].idxmax()
    hottest_temp = taverage['mean'].max()
    
    print(f"最も気温の低い日: {coldest_day.strftime('%Y-%m-%d')} ({coldest_day.month}/{coldest_day.day})")
    print(f"その日の気温: {coldest_temp:.2f}℃")
    print(f"最も気温の高い日: {hottest_day.strftime('%Y-%m-%d')} ({hottest_day.month}/{hottest_day.day})")
    print(f"その日の気温: {hottest_temp:.2f}℃")
    print(f"暖房期間判定温度: {HEATING_THRESHOLD_TEMP}℃")
    print()
    
    heating_start_date = None
    heating_end_date = None
    
    if coldest_temp <= HEATING_THRESHOLD_TEMP:
        print(f"最低気温({coldest_temp:.2f}℃) ≦ 判定温度({HEATING_THRESHOLD_TEMP}℃) のため、暖房期間を判定します")
        
        # DataFrameを日付順でソート（念のため）
        taverage_sorted = taverage.sort_index()
        dates = taverage_sorted.index.tolist()
        temps = taverage_sorted['mean'].tolist()
        
        # 日付とインデックスの対応辞書を作成
        date_to_idx = {date: idx for idx, date in enumerate(dates)}
        coldest_idx = date_to_idx[coldest_day]
        
        # 暖房期間の開始日を判定（coldest_dayから遡る）
        print(f"\n暖房期間開始日の判定（{coldest_day.strftime('%m/%d')}から遡る）...")
        current_idx = coldest_idx
        found_start = False
        
        for _ in range(len(dates)):
            # 1日前に移動（循環）
            current_idx = (current_idx - 1) % len(dates)
            current_date = dates[current_idx]
            current_temp = temps[current_idx]
            
            if current_temp > HEATING_THRESHOLD_TEMP:
                # 判定温度を超えた日の翌日が暖房期間の開始日
                heating_start_idx = (current_idx + 1) % len(dates)
                heating_start_date = dates[heating_start_idx]
                found_start = True
                print(f"  {current_date.strftime('%m/%d')}: {current_temp:.2f}℃ > {HEATING_THRESHOLD_TEMP}℃")
                print(f"  → 暖房期間開始日: {heating_start_date.strftime('%Y-%m-%d')} ({heating_start_date.month}/{heating_start_date.day})")
                break
        
        if not found_start:
            print("  判定温度を超える日が見つかりませんでした（年間を通じて低温）")
            heating_start_date = dates[0]  # 年の最初の日
            print(f"  → 暖房期間開始日を年初に設定: {heating_start_date.strftime('%Y-%m-%d')}")
        
        # 暖房期間の終了日を判定（coldest_dayから進む）
        print(f"\n暖房期間終了日の判定（{coldest_day.strftime('%m/%d')}から進む）...")
        current_idx = coldest_idx
        found_end = False
        
        for _ in range(len(dates)):
            # 1日後に移動（循環）
            current_idx = (current_idx + 1) % len(dates)
            current_date = dates[current_idx]
            current_temp = temps[current_idx]
            
            if current_temp > HEATING_THRESHOLD_TEMP:
                # 判定温度を超えた日の前日が暖房期間の終了日
                heating_end_idx = (current_idx - 1) % len(dates)
                heating_end_date = dates[heating_end_idx]
                found_end = True
                print(f"  {current_date.strftime('%m/%d')}: {current_temp:.2f}℃ > {HEATING_THRESHOLD_TEMP}℃")
                print(f"  → 暖房期間終了日: {heating_end_date.strftime('%Y-%m-%d')} ({heating_end_date.month}/{heating_end_date.day})")
                break
        
        if not found_end:
            print("  判定温度を超える日が見つかりませんでした（年間を通じて低温）")
            heating_end_date = dates[-1]  # 年の最後の日
            print(f"  → 暖房期間終了日を年末に設定: {heating_end_date.strftime('%Y-%m-%d')}")
        
        print()
        print(f"【暖房期間】 {heating_start_date.strftime('%Y-%m-%d')} ({heating_start_date.month}/{heating_start_date.day}) ~ {heating_end_date.strftime('%Y-%m-%d')} ({heating_end_date.month}/{heating_end_date.day})")
    else:
        print(f"最低気温({coldest_temp:.2f}℃) > 判定温度({HEATING_THRESHOLD_TEMP}℃) のため、暖房期間は設定されません")
    
    print()
    print("=" * 80)
    print()


    # 東京の気温をプロット（日次データ）
    year = np.array(range(8760))
    
    # Plotlyのグラフを作成
    fig = go.Figure()
    
    # 日次データ（点線）- 初期状態では非表示
    fig.add_trace(go.Scatter(
        x=daily.index, 
        y=daily['max'], 
        name='最高気温[℃]',
        opacity=1.0, 
        line=dict(width=1, dash='dot'), 
        visible='legendonly'
    ))
    fig.add_trace(go.Scatter(
        x=daily.index, 
        y=daily['mean'], 
        name='平均気温[℃]',
        opacity=1.0, 
        line=dict(width=1, dash='dot'), 
        visible='legendonly'
    ))
    fig.add_trace(go.Scatter(
        x=daily.index, 
        y=daily['min'], 
        name='最低気温[℃]',
        opacity=1.0, 
        line=dict(width=1, dash='dot'), 
        visible='legendonly'
    ))
    
    # 移動平均データ（実線）
    fig.add_trace(go.Scatter(
        x=taverage.index, 
        y=taverage['max'], 
        name='最高気温(移動平均)[℃]',
        opacity=1.0, 
        line=dict(width=2)
    ))
    fig.add_trace(go.Scatter(
        x=taverage.index, 
        y=taverage['mean'], 
        name='平均気温(移動平均)[℃]',
        opacity=1.0, 
        line=dict(width=2)
    ))
    fig.add_trace(go.Scatter(
        x=taverage.index, 
        y=taverage['min'], 
        name='最低気温(移動平均)[℃]',
        opacity=1.0, 
        line=dict(width=2)
    ))
    
    # 暖房期間の背景色と縦線を設定
    shapes = []
    if heating_start_date is not None and heating_end_date is not None:
        # 暖房期間が年をまたぐ場合（開始日 > 終了日）
        if heating_start_date > heating_end_date:
            # 年初から終了日まで
            shapes.append(dict(
                type="rect",
                xref="x",
                yref="paper",
                x0=daily.index[0],
                x1=heating_end_date,
                y0=0,
                y1=1,
                fillcolor="rgba(255, 200, 150, 0.2)",  # 暖色系の薄いオレンジ
                layer="below",
                line_width=0,
            ))
            # 開始日から年末まで
            shapes.append(dict(
                type="rect",
                xref="x",
                yref="paper",
                x0=heating_start_date,
                x1=daily.index[-1],
                y0=0,
                y1=1,
                fillcolor="rgba(255, 200, 150, 0.2)",  # 暖色系の薄いオレンジ
                layer="below",
                line_width=0,
            ))
        else:
            # 通常の期間（年内で完結）
            shapes.append(dict(
                type="rect",
                xref="x",
                yref="paper",
                x0=heating_start_date,
                x1=heating_end_date,
                y0=0,
                y1=1,
                fillcolor="rgba(255, 200, 150, 0.2)",  # 暖色系の薄いオレンジ
                layer="below",
                line_width=0,
            ))
    
    # 暖房期間の開始日と終了日の縦線をshapesに追加（背景色の上に表示）
    if heating_start_date is not None:
        shapes.append(dict(
            type="line",
            xref="x",
            yref="paper",
            x0=heating_start_date,
            x1=heating_start_date,
            y0=0,
            y1=1,
            line=dict(
                color='orange',
                width=1,
            ),
            layer="above",
            opacity=0.8,
        ))
    
    if heating_end_date is not None:
        shapes.append(dict(
            type="line",
            xref="x",
            yref="paper",
            x0=heating_end_date,
            x1=heating_end_date,
            y0=0,
            y1=1,
            line=dict(
                color='orange',
                width=1,
            ),
            layer="above",
            opacity=0.8,
        ))
    
    # 最寒日と最暑日の縦線を追加
    fig.add_vline(
        x=coldest_day,
        line_color='black', 
        opacity=0.5,
        line_dash='dot',
        layer='below', 
        line_width=2,
    )
    
    fig.add_vline(
        x=hottest_day,
        line_color='black', 
        opacity=0.5,
        line_dash='dot',
        layer='below', 
        line_width=2,
    )
    
    # 暖房期間の開始日と終了日の縦線を追加
    if heating_start_date is not None:
        fig.add_vline(
            x=heating_start_date,
            line_color='red',
            line_width=4,
            # line_dash='dash',
            opacity=0.8,
        )
    
    if heating_end_date is not None:
        fig.add_vline(
            x=heating_end_date,
            line_color='blue',
            line_width=4,
            # line_dash='dash',
            opacity=0.8,
        )
    
    # coldest_dayが1年の後半（7月以降）かどうかを判定
    is_coldest_in_second_half = coldest_day.month >= 7
    
    # 最寒日のアノテーション（吹き出し）
    coldest_date = f'Coldest Day ({coldest_day.month}/{coldest_day.day})'
    fig.add_annotation(
        x=coldest_day,
        y=taverage.at[coldest_day, 'mean'],
        xref='x',
        yref='y',
        xanchor='right' if is_coldest_in_second_half else 'left',
        yanchor='middle',
        text=coldest_date,
        showarrow=True,
        font=dict(
            family='Raleway',
            color='black',
            size=16
        ),
        align='center',
        arrowhead=2,
        arrowsize=2,
        arrowwidth=1,
        ax=-50 if is_coldest_in_second_half else 50,
        ay=-110,
        bordercolor="gray",
        borderwidth=1,
        borderpad=4,
        bgcolor="white",
        opacity=0.7
    )
    
    # 最暑日のアノテーション（吹き出し）
    hottest_date = f'Hottest Day ({hottest_day.month}/{hottest_day.day})'
    fig.add_annotation(
        x=hottest_day,
        y=taverage.at[hottest_day, 'mean'],
        xref='x',
        yref='y',
        xanchor='left',
        yanchor='middle',
        text=hottest_date,
        showarrow=True,
        font=dict(
            family='Raleway',
            color='black',
            size=16
        ),
        align='center',
        arrowhead=2,
        arrowsize=2,
        arrowwidth=1,
        ax=32,
        ay=-70,
        bordercolor="gray",
        borderwidth=1,
        borderpad=4,
        bgcolor="white",
        opacity=0.7
    )
    
    # 暖房期間開始日のアノテーション
    if heating_start_date is not None:
        # 開始日が年の後半かどうかを判定
        is_start_in_second_half = heating_start_date.month >= 7
        
        heating_start_text = f'Heating Start ({heating_start_date.month}/{heating_start_date.day})'
        fig.add_annotation(
            x=heating_start_date,
            y=taverage.at[heating_start_date, 'mean'],
            xref='x',
            yref='y',
            xanchor='right' if is_start_in_second_half else 'left',
            yanchor='middle',
            text=heating_start_text,
            showarrow=True,
            font=dict(
                family='Raleway',
                color='red',
                size=14
            ),
            align='center',
            arrowhead=2,
            arrowsize=2,
            arrowwidth=1,
            arrowcolor='red',
            ax=-40 if is_start_in_second_half else 40,
            ay=80,
            bordercolor="red",
            borderwidth=1,
            borderpad=4,
            bgcolor="white",
            opacity=0.7
        )
    
    # 暖房期間終了日のアノテーション
    if heating_end_date is not None:
        # 終了日が年の後半かどうかを判定
        is_end_in_second_half = heating_end_date.month >= 7
        
        heating_end_text = f'Heating End ({heating_end_date.month}/{heating_end_date.day})'
        fig.add_annotation(
            x=heating_end_date,
            y=taverage.at[heating_end_date, 'mean'],
            xref='x',
            yref='y',
            xanchor='right' if is_end_in_second_half else 'left',
            yanchor='middle',
            text=heating_end_text,
            showarrow=True,
            font=dict(
                family='Raleway',
                color='red',
                size=14
            ),
            align='center',
            arrowhead=2,
            arrowsize=2,
            arrowwidth=1,
            arrowcolor='red',
            ax=-40 if is_end_in_second_half else 40,
            ay=80,
            bordercolor="red",
            borderwidth=1,
            borderpad=4,
            bgcolor="white",
            opacity=0.7
        )
    
    # ベルリンのデータを追加（コメントアウトされている場合）
    # fig.add_trace(go.Scatter(
    #     x=year,
    #     y=wea2.ambient_temperatures,
    #     mode='lines',
    #     name='Berlin'
    # ))
    
    # レイアウトの設定
    fig.update_layout(
        title=f'年間気温データ - Tokyo (暖房期間判定: {HEATING_THRESHOLD_TEMP}℃)',
        xaxis_title='Date',
        yaxis_title='Temperature (°C)',
        hovermode='x unified',
        shapes=shapes,  # 暖房期間の背景色を追加
        legend=dict(x=1.05, y=1.0),
        xaxis=dict(
            rangeslider=dict(visible=True),
            type='date'
        ),
        yaxis=dict(
            range=[-20, 40],
            fixedrange=True,  # 表示レンジを固定
        )
    )
    
    # クロスヘアーカーソルを表示
    spike_style = dict(
        showspikes=True,
        spikemode='across',
        spikecolor='black',
        spikedash='solid',
        spikethickness=1
    )
    fig.update_xaxes(spike_style)
    fig.update_yaxes(spike_style)
    
    # HTMLファイルに出力
    output_file = 'heating_period_chart.html'
    fig.write_html(output_file, auto_open=True)
    print(f"チャートを生成しました: {output_file}")