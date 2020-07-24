# coding: utf-8
# author     Yuichi Yasuda @ quattro corporate design
# copyright  quattro corporate design. All right reserved.

from .weatherdata import WeatherDataFile
import struct
import math
import numpy as np

KELVIN = 273.15 #絶対温度(摂氏0℃）
Po = 101.325    #標準大気圧[kPa] 

class WeaFile(WeatherDataFile):
    # コンストラクタの定義
    def __init__(self, filename, no):
        #初期化
        #-----------------------------------------------
        self.file_name = filename   #標準年気象データファイル
        self.station_no = no        #地点番号
        self.wea_data = []          #地点の気象データ一式
        
        #地点の標準年データを取得
        #-----------------------------------------------
        self.__load(filename, no)

        #日射量の単位換算
        #-----------------------------------------------
        self.wea_data[2] = self.wea_data[2]/3.6*1000.0 # 日射量の単位をMJ/hm2 -> W/m2へ換算
        
        #大気放射量の単位換算
        #-----------------------------------------------
        self.wea_data[3] = self.wea_data[3]/3.6*1000.0 # 日射量の単位をMJ/hm2 -> W/m2へ換算

        #相対湿度
        #-----------------------------------------------
        abs_hum = self.wea_data[1]  #絶対湿度[g/kg']
        abs_hum = np.array(abs_hum) / 1000.0 #単位換算 [g/kg'] -> [kg/kg']
        #相対湿度[%]　絶対湿度、気温から相対湿度を計算する
        self.rh = calc_relative_humidity(abs_hum, np.array(self.wea_data[0]))#相対湿度

        #風向
        #-----------------------------------------------
        self.winddir = []
        dir = 0.0
        directions = self.wea_data[4]
        for i in range(len(directions)):
            if(directions[i]==0):#静謐（無風）であれば、風向を-9999へセット
                dir == -9999    
            else:
                dir = directions[i]*22.5 #16方位を角度へ変換(N:360, E:90, S:180, W:270)
            
            self.winddir.append(dir) #風向リストへ追加
        
        #-----------------------------------------------

    def __read_int16(self, f):
        """Reads a 2-byte signed integer from the file"""
        bytes = f.read(2)
        val = struct.unpack('<h', bytes)[0] #Convert bytes to a 2-byte signed integer (int16)
        return val

    def __skip_record_header(self, f):
        """Read the station no, entity no and the year"""
        station_number = self.__read_int16(f)
        entity_number  = self.__read_int16(f)
        year = self.__read_int16(f)

    def remove_remark(self, val):
        """Remove the remark"""
        return math.floor(val/10.0) # round the value down

    def __load(self, weafile, no):
        """
        指定された標準年のファイルから、指定の地点の気象データ一式を取得する
        """
        RECORD_LENGTH = 18306
        BLOCK_LENGTH = RECORD_LENGTH * 8        
        
        #EAで整数値としてエンコードされているデータから実数への換算係数
        #拡張アメダス気象データ 1981-2000, 表3.2 気象要素の単位
        sf=[0.1, 0.1, 0.01, 0.01, 1.0, 0.1, 1.0, 0.1] 

        #値の読み出し処理
        with open(weafile, 'rb') as f:
            for i in range(8):          
                head = (no-1)*BLOCK_LENGTH + i * RECORD_LENGTH         
                f.seek(head) # go to the head of the specified station and data.
                # read the station no, entity no and the year
                self.__skip_record_header(f)

                vals = []
                for day in range(365):      #365 days                    
                    for hour in range(24):  #24 hours
                        val = self.__read_int16(f)
                        val = self.remove_remark(val) #remove the remark
                        # val = val * sf[i] #unit conversion
                        vals.append(val)

                self.wea_data.append(np.array(vals) * sf[i]) #ndarrayに変換して、単位換算後にリストへ追加


    @property
    def ambient_temperatures(self):
        """
        Get or set the array of temperatures. [C]\n
        気温の配列を取得、設定する[C]
        """
        return self.wea_data[0]

    # @ambient_temperatures.setter
    # def ambient_temperatures(self, val):
    #     # if len(val) != HOURS_PER_YEAR:
    #     #     raise ValueError('長さ{}のリストを指定してください'.format(HOURS_PER_YEAR))
    #     # if super().check_the_list_length(val):
    #     self.wea_data[0] = val

    @property
    def absolute_humidities(self):
        """
        Get or set the array of absolute humidities.[g/kg]\n
        絶対湿度の配列を取得、設定する[g/kg]
        """
        return self.wea_data[1]
    
    # @absolute_humidities.setter
    # def absolute_humidities(self, val):
    #     self.wea_data[1] = val

    @property
    def relative_humidities(self):
        """
        Get or set the array of relative humidities.[g/kg]\n
        相対湿度の配列を取得、設定する[%]
        """
        # raise NotImplementedError
        return self.rh

    # @relative_humidities.setter
    # def relative_humidities(self, val):
    #     self.rh = val


    @property
    def horizontal_global_solar_irradiations(self):
        """
        Get or set the array of horizoltal global solar irradiations.[W/m2]\n
        全天日射量の配列を取得、設定する[W/m2]
        """
        return self.wea_data[2]
        #return self.it

    # @horizontal_global_solar_irradiations.setter
    # def horizontal_global_solar_irradiations(self, val):
    #     self.wea_data[2]

    @property
    def downward_longwave_irradiations(self):
        """
        Get or set the  array of downward longwave irradiations.[W/m2]\n
        大気放射量の配列を取得、設定する[W/m2]
        """
        return self.wea_data[3]

    # @downward_longwave_irradiations.setter
    # def downward_longwave_irradiations(self, val):
    #     self.wea_data[3] = val

    
    @property
    def wind_directions(self):
        """
        Get or set the array of wind directions.[deg]\n
        風向の配列を取得、設定する[deg]
        """
        # return self.wea_data[4]
        return self.winddir

    # @wind_directions.setter
    # def wind_directions(self, val):
    #     self.winddir = val
    
    @property
    def wind_velocities(self):
        """
        Get or set the array of wind Velocities.[m/s]\n
        風速の配列を取得、設定する[m/s]
        """
        return self.wea_data[5]

    # @wind_velocities.setter
    # def wind_velocities(self, val):
    #     self.wea_data[5]


    @property
    def precipitation_amounts(self):
        """
        Get or set the array of precipitation amount.[mm]\n
        降水量の配列を取得、設定する[mm]
        """
        return self.wea_data[6]
        
    # @precipitation_amounts.setter
    # def precipitation_amounts(self, val):
    #     self.wea_data[6] = val
    

    @property
    def sunshine_durations(self):
        """
        Get or set the array of sunshine durations.[h]\n
        日照時間の配列を取得、設定する[h]
        """
        return self.wea_data[7]
        
    # @sunshine_durations.setter
    # def sunshine_durations(self, val):
    #     self.wea_data[7] = val

# --------------------------------------------------------------------------------------------

def C2K(t):
    """
    摂氏[C]を絶対温度[K]へ換算する
    """
    return t+KELVIN


def GetPw(abs_hum):
    """
    水蒸気分圧[kPa]を計算する

    Parameters
    ----------
    abs_hum : float
    絶対湿度[kg/kg']
    
    Returns
    ----------
    Pw: float
    水蒸気分圧[kPa]

    """

    pw = (abs_hum * Po)/(abs_hum + 0.62198)
    return pw

def GetPws(tabT):
    """
    飽和水蒸気圧[kPa]を計算する

    Parameters
    ----------
    tabT : float
    乾球温度[K]
    
    Returns
    ----------
    Pws: float
    飽和水蒸気圧[kPa]
    """

    Pws = np.exp(1.3914993 - (5800.2206 / tabT) - (0.048640239 * tabT)
        + (0.4176768 * 10**(-4) * np.power(tabT, 2))
        - (0.14452093 * 10**(-7) * np.power(tabT, 3))
        + (6.5459673 * np.log(tabT))) / 1000.0
    
    return Pws

def calc_relative_humidity(abs_hum, tambs):
    """
    相対湿度[%]を計算する

    Parameters
    ----------
    abs_hum : float
    絶対湿度[kg/kg']
    tambs   : float
    気温[C]
    
    Returns
    ----------
    Pw: float
    水蒸気分圧[kPa]
    """
    #水蒸気分圧[kPa]
    pw = GetPw(abs_hum) #水蒸気分圧[kPa],ただし標高は考慮しない

    #気温から飽和水蒸気分圧を計算
    tambs_kelvin = C2K(np.array(tambs))#[C]->[K]　絶対温度へ換算
    #飽和水蒸気分圧[kPa]
    pws = GetPws(tambs_kelvin)

    #相対湿度[%]
    rh = pw/pws *100.0

    return rh

