import weapy.weafile as ea
# import wea.epwfile as epw
if(__name__ == '__main__'):
    weafile = r'c:\AMeDAS\RWY8195.wea' #1995年版＠自宅PC
    # weafile = r"D:\AMeDAS\Amedasty.wea" #1995年版＠会社PC
    
    # no = 1 #宗谷
    # no = 163 #大間
    # no = 318 #鉾田
    # no = 361 #八王子
    no = 363 #東京

    wea = ea.WeaFile(weafile, no)
    print(wea.ambient_temperatures[:10])
    