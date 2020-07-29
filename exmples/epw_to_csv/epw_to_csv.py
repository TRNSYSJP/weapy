# coding: utf-8
# author     Yuichi Yasuda @ quattro corporate design
# copyright  quattro corporate design. All right reserved.


import weapy.weafile as ea
import weapy.epwfile as epw
import pandas as pd

if(__name__ == '__main__'):

    """例）EPWをCSVへ出力
    """

    # epw
    epwfile = r'C:\WorkCopy\weapy\exmples\matplot\DEU_BE_Berlin-Tegel.AP.103820_TMYx.2004-2018\DEU_BE_Berlin-Tegel.AP.103820_TMYx.2004-2018.epw'
    wea = epw.EpwFile(epwfile)    
    
    # DataFrameを生成する
    df = pd.DataFrame(
        {
        'TAMB': wea.ambient_temperatures,
        'RHUM': wea.relative_humidities,
        'IGLOB_H': wea.horizontal_global_solar_irradiations,
        'udef1': wea.downward_longwave_irradiations,
        'WDIR': wea.wind_directions,
        'WSPEED': wea.wind_velocities,
        'udef2': wea.precipitation_amounts,
        # 'udef3': wea.sunshine_durations,
        })

    df = df.round({'TAMB':3, 'RHUM':3, 'IGLOB_H':3, 'udef1':3, 'WDIR':1, 'WSPEED':1, 'udef2':1})
    pd.options.display.float_format = '{:.4g}'.format

    #ファイル名
    fname = 'epw_Berlin.csv'

    # csvへ保存
    df.to_csv(fname, mode='w', header=True, index=False) 

    