REM WMS
..\output\report\report.exe reports 0 --csv wms_report.csv
..\output\report\report.exe errors 0 --csv wms_errors.csv
..\output\report\report.exe layers 0 --csv wms_layers.csv
..\output\report\report.exe ws 0 --csv wms_ws.csv

REM WFS
..\output\report\report.exe reports 1 --csv wfs_report.csv
..\output\report\report.exe errors 1 --csv wfs_errors.csv
..\output\report\report.exe layers 1 --csv wfs_layers.csv
..\output\report\report.exe ws 1 --csv wfs_ws.csv

REM CSW
..\output\report\report.exe reports 2 --csv csw_report.csv
..\output\report\report.exe errors 2 --csv csw_errors.csv
..\output\report\report.exe layers 2 --csv csw_layers.csv
