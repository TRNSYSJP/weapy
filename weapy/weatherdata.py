# coding: utf-8
# author     Yuichi Yasuda @ quattro corporate design
# copyright  quattro corporate design. All right reserved.
from abc import ABCMeta
from abc import abstractmethod,abstractproperty

HOURS_PER_YEAR = 8760 #年間時間

class WeatherDataFile(metaclass = ABCMeta):
    """Weather Data Class
    """    
    
    # def check_the_list_length(self, val):
        
    #     if len(val) != HOURS_PER_YEAR:
    #         raise ValueError('長さ{}のリストを指定してください'.format(HOURS_PER_YEAR))
    #     return True

    @abstractproperty
    def ambient_temperatures(self):
        pass

    @abstractproperty
    def absolute_humidities(self):
        pass

    @abstractproperty
    def relative_humidities(self):
        pass

    @abstractproperty
    def horizontal_global_solar_irradiations(self):
        pass

    @abstractproperty
    def downward_longwave_irradiations(self):
        pass
        
    @abstractproperty
    def wind_directions(self):
        pass

    @abstractproperty
    def wind_velocities(self):
        pass
    
    @abstractproperty
    def precipitation_amounts(self):
        pass
    
    @abstractproperty
    def sunshine_durations(self):
        pass
    

    

