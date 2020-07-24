import weapy.weafile as ea
import weapy.epwfile as epw
if(__name__ == '__main__'):
    weafile = r'c:\AMeDAS\RWY8195.wea' #1995年版
    
    # no = 1 #宗谷
    # no = 163 #大間
    # no = 318 #鉾田
    # no = 361 #八王子
    no = 363 #東京

    wea = ea.WeaFile(weafile, no)
    print(wea.ambient_temperatures[:10])



    fname = r'C:\WorkCopy\PassiveClimaticChart\Weather\EPW\JPN_TK_Tokyo.Intl.AP-Haneda.AP.476710_TMYx.2003-2017\JPN_TK_Tokyo.Intl.AP-Haneda.AP.476710_TMYx.2003-2017.epw'
    wea = epw.EpwFile(fname)    #気象データをクラスへ展開

    print(wea.ambient_temperatures[:24])    #気温24h分を出力
    print(wea.wind_directions[:24])

