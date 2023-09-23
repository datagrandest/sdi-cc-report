REM WMS
..\output\report\report.exe dashboard 0 -dst ./html/

REM WFS
..\output\report\report.exe dashboard 1 -dst ./html/

REM CSW
..\output\report\report.exe dashboard 2 -dst ./html/

REM WMS et WFS du workspace "geograndest"
..\output\report\report.exe dashboard 0 -ws geograndest -dst ./html/geograndest/
..\output\report\report.exe dashboard 1 -ws geograndest -dst ./html/geograndest/
