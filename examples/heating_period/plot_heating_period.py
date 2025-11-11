# coding: utf-8
# author     Yuichi Yasuda @ quattro corporate design
# copyright  quattro corporate design. All right reserved.

import weapy.weafile as ea
import weapy.epwfile as epw
import plotly.graph_objects as go
import numpy as np
import os

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


    # 東京、ベルリンの気温をプロット
    year = np.array(range(8760))
    
    # Plotlyのグラフを作成
    fig = go.Figure()
    
    # 東京のデータを追加
    fig.add_trace(go.Scatter(
        x=year,
        y=wea.ambient_temperatures,
        mode='lines',
        name='Tokyo'
    ))
    
    # ベルリンのデータを追加（コメントアウトされている場合）
    # fig.add_trace(go.Scatter(
    #     x=year,
    #     y=wea2.ambient_temperatures,
    #     mode='lines',
    #     name='Berlin'
    # ))
    
    # レイアウトの設定
    fig.update_layout(
        title='Ambient Temperature',
        xaxis_title='Hour of Year',
        yaxis_title='Temperature (°C)',
        hovermode='x unified'
    )
    
    # プロット表示
    fig.show()