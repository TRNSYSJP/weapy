# coding: utf-8
# author     Yuichi Yasuda @ quattro corporate design
# copyright  quattro corporate design. All right reserved.

import weapy.weafile as ea
import weapy.epwfile as epw
import matplotlib.pyplot as plt
import numpy as np
import os

if(__name__ == '__main__'):

    """例）拡張アメダス標準年とEPWのデータを重ねてプロットする
    """


    # 拡張アメダス気象データ
    # --------------------------------
    no = 363 #東京
    weafile = r'c:\AMeDAS\RWY8195.wea' #1995年版
    wea1 = ea.WeaFile(weafile, no)

    # epw
    fpath = os.path.dirname(os.path.abspath(__file__)) #実行ファイルのパスを取得
    epwfile = fpath + r'\DEU_BE_Berlin-Tegel.AP.103820_TMYx.2004-2018\DEU_BE_Berlin-Tegel.AP.103820_TMYx.2004-2018.epw'
    wea2 = epw.EpwFile(epwfile)


    # 東京、ベルリンの気温をプロット
    year = np.array(range(8760))
    plt.plot(year, wea1.ambient_temperatures, label="Tokyo")
    plt.plot(year, wea2.ambient_temperatures, label="Berlin")

    # 凡例をプロット
    plt.legend()

    # プロット表示
    plt.show()