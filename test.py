# coding: utf-8
import weapy.weafile as ea
import weapy.epwfile as epw

def print_data(wea, hour):
    """[summary]

    Args:
        wea ([weatherdata]): [EA,もしくはEPWの気象データ]
        hour ([int]): [表示する時間数]
    """        

    print('-------------')
    print('気温: \t{}'.format(wea.ambient_temperatures[:hour]))    # 気温24h分を出力
    if isinstance(wea, ea.WeaFile): # 拡張アメダス
        print('絶対湿度: \t{}'.format(wea.absolute_humidities[:hour])) # 絶対湿度
    else:
        print('絶対湿度: not available')
    
    print('相対湿度:{}'.format(wea.relative_humidities[:hour])) # 相対湿度
    print('日射量:\t{}'.format(wea.horizontal_global_solar_irradiations[:hour]))
    print('大気放射量:\t{}'.format(wea.downward_longwave_irradiations[:hour]))
    print('風向:\t{}'.format(wea.wind_directions[:hour]))
    print('風速:\t{}'.format(wea.wind_velocities[:hour]))
    print('降水量:{}'.format(wea.precipitation_amounts[:hour]))
    if isinstance(wea, ea.WeaFile): # 拡張アメダス
        print('日照時間:\t{}'.format(wea.sunshine_durations[:hour]))
    else:
        print('日照時間: not available')
    

if(__name__ == '__main__'):
    
    # 拡張アメダス気象データ
    # --------------------------------
    no = 363 #東京
    weafile = r'c:\AMeDAS\RWY8195.wea' #1995年版
    wea = ea.WeaFile(weafile, no)
    
    print('拡張アメダス気象データ')
    print_data(wea, 24)  

    # EPW
    # --------------------------------
    fname = r'C:\EPW\JPN_TK_Tokyo.Intl.AP-Haneda.AP.476710_TMYx.2003-2017\JPN_TK_Tokyo.Intl.AP-Haneda.AP.476710_TMYx.2003-2017.epw'
    wea = epw.EpwFile(fname)    #気象データをクラスへ展開

    print('EPW気象データ')
    print_data(wea, 24)    
    


    