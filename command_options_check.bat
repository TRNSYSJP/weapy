@echo on
rem エラーにならない引数
.\dist\conv_type99.exe  "d:\ead\rwy0110.wea" yonagunijima 	838 24.4667 -123.0100 30.00 
.\dist\conv_type99.exe  "d:\ead\rwy0110.wea" nosappu 		99 43.3933 -145.7583 12.00 
.\dist\conv_type99.exe  "d:\ead\rwy0110.wea" soya			1	45.5200 -141.9350 26.00
.\dist\conv_type99.exe  "d:\ead\rwy0110.wea" hateruma 		842 24.0550 -123.7683 38.00
.\dist\conv_type99.exe  "d:\ead\rwy0110.wea" nobeyama 		410 35.9483 -138.4717 1350.00 
.\dist\conv_type99.exe  "d:\ead\rwy0110.wea" oogata		193 340.0000 -139.9500 -3.00
rem
rem　エラーになる引数の組合わせ
rem
REM .\dist\conv_type99.exe  "D:\EAD\hoge.wea" yonagunijima 	838 24.4667 -123.0100 30.00 
REM .\dist\conv_type99.exe  "D:\EAD\RWY0110.wea" yonagunijima 	999 23.4667 -123.000 30.00 
REM .\dist\conv_type99.exe  "D:\EAD\RWY0110.wea" yonagunijima 	838 23.4667 -123.000 30.00 
REM .\dist\conv_type99.exe  "D:\EAD\RWY0110.wea" nosappu 		99 43.3933 -146.000 12.00 
REM .\dist\conv_type99.exe  "D:\EAD\RWY0110.wea" soya			1	46.0000 -141.9350 26.00
REM .\dist\conv_type99.exe  "D:\EAD\RWY0110.wea" hateruma 		842 23.0000 -123.7683 38.00
REM .\dist\conv_type99.exe  "D:\EAD\RWY0110.wea" Nobeyama 		410 35.9483 -138.4717 1351.00 
REM .\dist\conv_type99.exe  "D:\EAD\RWY0110.wea" oogata		193 340.0000 -139.9500 -4.00

