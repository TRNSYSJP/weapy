# coding: utf-8
# author     Yuichi Yasuda @ quattro corporate design
# copyright  quattro corporate design. All right reserved.

from .weatherdata import WeatherDataFile
import struct
import math
import numpy as np
import pandas as pd
import csv

class EpwFile(WeatherDataFile):
    # コンストラクタの定義
    def __init__(self, filename):
        # ①-⑥	年,月,日,時,分,リマーク
        # ⑦ 外気温度[°Ｃ]
        # ⑧	露点温度[°Ｃ]
        # ⑨	相対湿度[％]
        # ⑩	大気圧[Pa]
        # ⑪	大気圏外水平面日射量[W/m2]
        # ⑫	大気圏外法線面直達日射量[W/m2]
        # ⑬	大気放射量[W/m2]
        # ⑭	全天日射量[W/m2]
        # ⑮	法線面直達日射量[W/m2]
        # ⑯	水平面天空日射量[W/m2]
        # ⑰	グローバル照度[lx]
        # ⑱	法線面直射照度[lx]
        # ⑲ 天空照度[lx]
        # ⑳ 天頂輝度[cd/m2]

        # ㉑ 風向[°]
        # ㉒ 風速[m/s]
        # ㉓ 雲量(0-10)
        # ㉔ 不透明雲量
        # ㉕ 視程[km]
        # ㉖ 雲高[m]
        # ㉗ 気象状況
        # ㉘ 気象コード
        # ㉙ 可降水量[mm]
        # ㉚ 大気の光学的厚さ
        # ㉛ 積雪量[cm]
        # ㉜ 最後の積雪からの日数[日]
        # ㉝ アルベド
        # ㉞ 降水量[mm]
        # ㉟ 降水時間[hr]


        # Date,HH:MM,Datasource,DryBulb {C},DewPoint {C},RelHum {%},Atmos Pressure {Pa},ExtHorzRad {Wh/m2},ExtDirRad {Wh/m2},HorzIRSky {Wh/m2},
        # GloHorzRad {Wh/m2},DirNormRad {Wh/m2},DifHorzRad {Wh/m2},GloHorzIllum {lux},DirNormIllum {lux},DifHorzIllum {lux},ZenLum {Cd/m2},WindDir {deg},WindSpd {m/s},
        # TotSkyCvr {.1},OpaqSkyCvr {.1},Visibility {km},Ceiling Hgt {m},PresWeathObs,PresWeathCodes,Precip Wtr {mm},Aerosol Opt Depth {.001},SnowDepth {cm},Days Last Snow,
        # Albedo {.01},Rain {mm},Rain Quantity {hr}
        labels = ['year','month','day','hour','min','Datasource','DryBulb','DewPoint','RelHum','AtmosPressure','ExtHorzRad','ExtDirRad','HorzIRSky',
                    'GloHorzRad','DirNormRad','DifHorzRad','GloHorzIllum','DirNormIllum','DifHorzIllum','ZenLum','WindDir','WindSpd',
                    'TotSkyCvr','OpaqSkyCvr','Visibility','CeilingHgt','PresWeathObs','PresWeathCodes','PrecipWtr','AerosolOptDepth','SnowDepth','DaysLastSnow',
                    'Albedo','Rain','RainQuantity']
        self.wea_data = pd.read_csv(filename, skiprows=8, sep=',', header=None, names=labels) #ヘッダーを読み飛ばして、Data Records のみ読み込む

        # 風向
        self.winddirs = self.wea_data['WindDir']
        
        #方位を16方位に集約する
        ndiv = 16
        theta = 360/ndiv
        # for i in range(len(self.winddirs)):          
        #     for j in range(ndiv):
        #         angle = theta*j
        #         if(j==0):
        #             if ((360 - theta/2 < self.winddirs[i]) or (self.winddirs[i] <= angle + theta/2)):
        #                  self.winddirs[i] = 0.0
        #                  break
        #         else:
        #             if ((angle - theta/2 < self.winddirs[i]) and (self.winddirs[i] <= angle + theta/2)):
        #                  self.winddirs[i] = angle
        #                  break


        for j in range(ndiv):
            angle = theta*j
            if(j==0):
                min_angle = 360 - theta/2
                max_angle = theta/2
                self.winddirs = np.where((min_angle < self.winddirs) | (self.winddirs <= max_angle), 0.0, self.winddirs)
                
            else:
                min_angle = angle - theta/2
                max_angle = angle + theta/2                
                self.winddirs = np.where((min_angle < self.winddirs) & (self.winddirs <= max_angle), angle, self.winddirs) 
                
        
        winspeeds = self.wea_data['WindSpd']
        cnt = 0
        # for i in range(0,8760):
        #     if(winspeeds[i] == 0.0):
        #         self.winddirs[i] = -9999 #無風（静謐）あれば方位を -9999 へ変更する
        #         cnt = cnt+1
        indices = [i for i in range(0,8760) if winspeeds[i] == 0.0]
        for i in indices:
            self.winddirs[i] = -9999 #無風（静謐）あれば方位を -9999 へ変更する
            cnt = cnt+1
        # aa = [self.winddirs.at(i) = -9999 for i in indices]






    @property
    def ambient_temperatures(self):
        """
        Get or set the array of temperatures. [C]\n
        気温の配列を取得、設定する[C]
        """
        return self.wea_data['DryBulb']
    
    # @ambient_temperatures.setter
    # def ambient_temperatures(self, val):        
    #     self.wea_data['DryBulb'] = val
    
    @property
    def absolute_humidities(self):
        """
        Get or set the array of absolute humidities.[g/kg]\n
        絶対湿度の配列を取得、設定する[g/kg]
        """
        raise NotImplementedError

    # @absolute_humidities.setter
    # def absolute_humidities(self, val):
    #     raise NotImplementedError

    @property
    def relative_humidities(self):
        """
        Get or set the array of relative humidities.[g/kg]\n
        相対湿度の配列を取得、設定する[%]
        """
        return self.wea_data['RelHum']
    
    # @relative_humidities.setter
    # def relative_humidities(self, val):
    #     self.wea_data['RelHum'] = val

    @property
    def horizontal_global_solar_irradiations(self):
        """
        Get or set the array of horizoltal global solar irradiations.[W/m2]\n
        全天日射量の配列を取得、設定する[W/m2]
        """

        return self.wea_data['GloHorzRad'] #[Wh/m2]なんだけど結果OK?

    # @horizontal_global_solar_irradiations.setter
    # def horizontal_global_solar_irradiations(self, val):       
    #     self.wea_data['GloHorzRad'] = val


    @property
    def downward_longwave_irradiations(self):
        """
        Get or set the  array of downward longwave irradiations.[MJ/(m2h)]\n
        大気放射量の配列を取得、設定する[MJ/(m2h)]
        """
        # raise NotImplementedError
        return self.wea_data['HorzIRSky']

    # @downward_longwave_irradiations.setter
    # def downward_longwave_irradiations(self, val):
    #     # raise NotImplementedError 
    #     self.wea_data['HorzIRSky'] = val
    
    @property
    def wind_directions(self):
        """
        Get or set the array of wind directions.[deg]\n
        風向の配列を取得、設定する[deg]
        """
        # return self.wea_data['WindDir']
        return self.winddirs
    
    # @wind_directions.setter
    # def wind_directions(self, val):
    #     self.winddirs = val

    @property
    def wind_velocities(self):
        """
        Get or set the array of wind Velocities.[m/s]\n
        風速の配列を取得、設定する[m/s]
        """
        return self.wea_data['WindSpd']

    # @wind_velocities.setter
    # def wind_velocities(self, val):
    #     self.wea_data['WindSpd'] = val


    @property
    def precipitation_amounts(self):
        """
        Get or set the array of precipitation amount.[mm]\n
        降水量の配列を取得、設定する[mm]
        """
        # raise NotImplementedError
        return self.wea_data['Rain']
    
    # @precipitation_amounts.setter
    # def precipitation_amounts(self, val):
    #     # raise NotImplementedError
    #     self.wea_data['Rain'] = val

    @property
    def sunshine_durations(self):
        """
        Get or set the array of sunshine durations.[h]\n
        日照時間の配列を取得、設定する[h]
        """
        raise NotImplementedError
        # return self.wea_data[7]
                
    # @sunshine_durations.setter
    # def sunshine_durations(self, val):
    #     raise NotImplementedError
