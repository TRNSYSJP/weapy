# coding: utf-8
# author     Yuichi Yasuda @ quattro corporate design
# copyright  quattro corporate design. All right reserved.

from .weatherdata import WeatherDataFile
import struct
import math
import numpy as np

KELVIN = 273.15 #絶対温度(摂氏0℃）

class header:
    """
    Header class for the extended AMeDAS file.

    Attributes
    ----------
    ea_no : int
    entity_number : int
    year : int


    """
    def __init__(self):
        self.ea_no = None           # 拡張アメダス(EA)地点番号
        self.entity_number = None   #種別
        self.year = None # e.g 1120, (EA2020)


class location_info:
    """
    Header class for the extended AMeDAS file.

    Attributes
    ----------

    """
    def __init__(self):
        self.station_number_upper2 = None #アメダス観測所番号(上2桁)
        self.station_number_lower3 = None #アメダス観測所番号(下3桁)
        self.international_location_number_upper2=None #国際地点番号(上2桁)
        self.international_location_number_lower3=None #国際地点番号(下3桁)
        self.latitude_int_part=None     #緯度(整数部)
        self.latitude_decimal_part=None #緯度(小数部)
        self.longitude_int_part=None    #経度(整数部)
        self.longitude_decimal_part=None#経度(小数部)
        self.elevation = None           #標高（ｍ）
        self.observed_wind_speed_height = None #風速観測高さ（0.1m単位）
        self.corrected_wind_speed_height = None #風速補正高さ (0.1m単位)

class name_info:
    """
    Name info class for the extended AMeDAS file.
    """
    def __init__(self):

        # 1/1の観測所名(日本語)
        self.station_name_on_new_years_day = None #観測所名(日本語)
        self.station_roman_name_on_new_years_day = None #観測所名(ローマ字)
        self.prefecture_name_on_new_years_day = None #都道府県名(日本語)
        self.prefecture_roman_name_on_new_years_day = None #都道府県名(ローマ字)

        # 12/31の観測所名(日本語)
        self.station_name_on_last_day_of_the_year = None #観測所名(日本語)
        self.station_roman_name_on_last_day_of_the_year = None #観測所名(ローマ字)
        self.prefecture_name_on_last_day_of_the_year = None #都道府県名(日本語)
        self.prefecture_roman_name_on_last_day_of_the_year = None #都道府県名(ローマ字)


class Wea2File(WeatherDataFile):
    # コンストラクタの定義
    def __init__(self, filename, no):
        """
        拡張アメダス気象データの指定された地点のデータを読み出す

        Parameters
        ----------
        filename : string
        拡張アメダス気象データ標準年のファイル名

        no : int
        拡張アメダスの地点番号[1-842]

        elevation : float
        地点の標高[m]

        """

        #初期化
        #-----------------------------------------------
        self.header = None
        self.location = None
        self.name = None
        self.file_name = filename   #標準年気象データファイル
        self.station_no = no        #地点番号
        # self.elevaton = elevation   #標高[m]
        self.wea_data = []          #地点の気象データ一式

        #地点の標準年データを取得
        #-----------------------------------------------
        self.__load(filename, no)

        #日射量の単位換算
        #-----------------------------------------------
        self.wea_data[3] = self.wea_data[3]/3.6*1000.0 # 日射量の単位をMJ/hm2 -> W/m2へ換算

        #大気放射量の単位換算
        #-----------------------------------------------
        self.wea_data[4] = self.wea_data[4]/3.6*1000.0 # 日射量の単位をMJ/hm2 -> W/m2へ換算
        
        #風向
        #-----------------------------------------------
        # 16方位を角度へ変換(N:360, E:90, S:180, W:270)
        self.winddir = self.wea_data[5] * 22.5
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

    def read_header(self, f):
        """
        Read the header information from the file
        """
        _header = header()
        header.ea_no = self.__read_int16(f)            # 拡張アメダス(EA)地点番号
        header.entity_number = self.__read_int16(f)    # 種別
        header.year = self.__read_int16(f)             # e.g 1120, (EA2020)
        self.header = _header # Add the header property to the instance of the WEA2 class


    def read_location(self, f):
        """
        Read the location and name information from the file
        """
        location_list = []
        for i in range(366):

            _location = location_info()
            location_list.append(_location)

            #アメダス観測所番号(上2桁), AMeDAS station number (upper 2 digits)
            _location.station_number_upper2 = self.__read_int16(f)
            #アメダス観測所番号(下3桁), AMeDAS station number (lower 3 digits)
            _location.station_number_lower3 = self.__read_int16(f)
            #国際地点番号(上2桁), International location number (upper 2 digits)
            _location.international_location_number_upper2=self.__read_int16(f)
            #国際地点番号(下3桁), International location number (lower 3 digits)
            _location.international_location_number_lower3=self.__read_int16(f)
            #緯度(整数部), Latitude (integer part)
            _location.latitude_int_part=self.__read_int16(f)
            #緯度(小数部分3桁), Latitude (decimal part)
            _location.latitude_decimal_part=self.__read_int16(f)
            #経度(整数部), Longitude (integer part)
            _location.longitude_int_part=self.__read_int16(f)
            #経度(小数部分3桁), Longitude (decimal part)
            _location.longitude_decimal_part=self.__read_int16(f)
            #標高（ｍ）, Elevation (m)
            _location.elevation = self.__read_int16(f)
            #風速観測高さ（0.1m単位）, Observed wind speed height (0.1m unit)
            _location.observed_wind_speed_height = self.__read_int16(f) * 0.1
            #風速補正高さ (0.1m単位), Corrected wind speed height (0.1m unit)
            _location.corrected_wind_speed_height = self.__read_int16(f) * 0.1
            # Skip dummy code, 26 bytes
            for i in range(13):
                dummy = self.__read_int16(f)
            # f.seek(26,1) #26 bytes dummy code

        #1日目のlocationをWEA2へプロパティとして追加する
        self.location = location_list[0]

        # Read the name information of the station
        _name = name_info()

        # 1/1の観測所名(日本語)
        # Station name on New Year's Day (Japanese)
        _name.station_name_on_new_years_day = f.read(30).decode('shift-jis').strip() #観測所名(日本語)
        _name.station_roman_name_on_new_years_day = f.read(30).decode('shift-jis').strip() #観測所名(ローマ字)
        _name.prefecture_name_on_new_years_day = f.read(30).decode('shift-jis').strip() #都道府県名(日本語)
        _name.prefecture_roman_name_on_new_years_day = f.read(30).decode('shift-jis').strip() #都道府県名(ローマ字)

        # 12/31の観測所名(日本語)
        # Station name on New Year's Eve
        _name.station_name_on_last_day_of_the_year = f.read(30).decode('shift-jis').strip() #観測所名(日本語)
        _name.station_roman_name_on_last_day_of_the_year = f.read(30).decode('shift-jis').strip() #観測所名(ローマ字)
        _name.prefecture_name_on_last_day_of_the_year = f.read(30).decode('shift-jis').strip() #都道府県名(日本語)
        _name.prefecture_roman_name_on_last_day_of_the_year = f.read(30).decode('shift-jis').strip() #都道府県名(ローマ字)

        self.name = _name # Add the name property to the instance of the WEA2 class

        # Skip blank 492 bytes
        # f.seek(492,1)


    def __load(self, weafile, no):
        """
        指定された標準年のファイルから、指定の地点の気象データ一式を取得する
        """
        RECORD_LENGTH = 18306
        BLOCK_LENGTH = RECORD_LENGTH * 11

        #EAで整数値としてエンコードされているデータから実数への換算係数
        #拡張アメダス気象データ（EA 気象データ）基礎知識（2020 年版）2022 年12 月31 日 V.03
        sf=[-999, 0.1, 0.1, 0.01, 0.01, 1.0, 0.1, 0.1, 0.01, 1.0, 0.1] # 地点情報（ダミー）,気温、絶対湿度、全天日射量、大気放射量、風向、風速、降水量、日照時間、 気圧、相対湿度

        #値の読み出し処理
        with open(weafile, 'rb') as f:
            # [0]地点情報レコード

            for i in range(11):
                #ファイルの先頭から、指定された地点データのレコードの先頭へ移動
                head = (no-1)*BLOCK_LENGTH + i * RECORD_LENGTH
                f.seek(head)
                if(i==0):
                    self.wea_data.append([]) #地点情報レコードは、空のリストを追加
                    self.read_header(f) #ヘッダー情報を読み込む
                    self.read_location(f) #地点情報を読み込む
                    continue

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
        Get the list of temperatures. [C]\n
        気温のリストを返す[C]
        """
        return self.wea_data[1]

    @property
    def absolute_humidities(self):
        """
        Get the list of absolute humidities.[g/kg]\n
        絶対湿度のリストを返す[g/kg]
        """
        return self.wea_data[2]

    @property
    def horizontal_global_solar_irradiations(self):
        """
        Get the list of horizoltal global solar irradiations.[W/m2]\n
        全天日射量のリストを返す[W/m2]
        """
        return self.wea_data[3]
        #return self.it

    @property
    def downward_longwave_irradiations(self):
        """
        Get or set the  array of downward longwave irradiations.[W/m2]\n
        大気放射量のリストを返す[W/m2]
        """
        return self.wea_data[4]

    @property
    def wind_directions(self):
        """
        Get the list of wind directions.[deg]\n
        風向のリストを返す[deg]\n
        16 方位(22.5:北北東～360:北,0:静穏)
        """
        # return self.wea_data[4]
        return self.winddir

    @property
    def wind_velocities(self):
        """
        Get the list of wind Velocities.[m/s]\n
        風速のリストを返す[m/s]
        """
        return self.wea_data[6]

    @property
    def precipitation_amounts(self):
        """
        Get the list of precipitation amount.[mm]\n
        降水量のリストを返す[mm]
        """
        return self.wea_data[7]

    @property
    def sunshine_durations(self):
        """
        Get the list of sunshine durations.[h]\n
        日照時間のリストを返す[h]
        """
        return self.wea_data[8]

    @property
    def pressure(self):
        """
        Get the list of pressure.[hPa]\n
        気圧のリストを返す[hPa]
        """
        return self.wea_data[9]

    @property
    def relative_humidities(self):
        """
        Get the list of relative humidities.[%]\n
        相対湿度のリストを返す[%]
        """
        return self.wea_data[10]

    @property
    def station_name(self):
        """
        Get the name of the location.\n
        地点名(日本語)を返す
        """
        return self.name.station_name_on_new_years_day

    @property
    def station_roman_name(self):
        """
        Get the roman name of the location.\n
        地点名（ローマ字）を返す
        """
        return self.name.station_roman_name_on_new_years_day


    @property
    def latitude(self):
        """
        Get the latitude of the location.[deg]\n
        緯度を返す[deg]
        """
        return self.location.latitude_int_part + self.location.latitude_decimal_part/1000.0

    @property
    def longitude(self):
        """
        Get the longitude of the location.[deg]\n
        経度を返す[deg]
        """
        return self.location.longitude_int_part + self.location.longitude_decimal_part/1000.0

    @property
    def elevation(self):
        """
        Get the elevation of the location.[m]\n
        標高を返す[m]
        """
        return self.location.elevation*0.1
