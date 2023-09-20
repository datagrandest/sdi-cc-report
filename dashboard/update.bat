REM WMS
..\output\report\report.exe reports 0 --csv ./data/wms_report.csv
..\output\report\report.exe errors 0 --csv ./data/wms_errors.csv
..\output\report\report.exe layers 0 --csv ./data/wms_layers.csv
..\output\report\report.exe ws 0 --csv ./data/wms_ws.csv

REM WFS
..\output\report\report.exe reports 1 --csv ./data/wfs_report.csv
..\output\report\report.exe errors 1 --csv ./data/wfs_errors.csv
..\output\report\report.exe layers 1 --csv ./data/wfs_layers.csv
..\output\report\report.exe ws 1 --csv ./data/wfs_ws.csv

REM CSW
..\output\report\report.exe reports 2 --csv ./data/csw_report.csv
..\output\report\report.exe errors 2 --csv ./data/csw_errors.csv
..\output\report\report.exe layers 2 --csv ./data/csw_layers.csv
