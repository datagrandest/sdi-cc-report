# SDI Consistence Check Report

Programme Python de gestion des rapports issus du script ["SDI Consistence Check"](https://github.com/georchestra/sdi-consistence-check).

## Utilisation

Il est possible d'utiliser cette application sous forme de script CLI.

Exemple:

``` bash
python.exe .\report.py layers 0 -i 458 > test.txt
```

Ou sous forme d'application.

Exemple:

``` bash
python.exe .\report.py

> layers 0 -i 458 -e result.txt
```

## Commandes disponibles

### `reports`

Permet de lister les rapports définis dans le fichier de configuration:

``` bash
reports
```

Il est possible de limiter la liste à certains rapports en précisant un ou plusieurs identifiants.  
Dans ce cas, pour chaque rapport sont indiqués: le nombre de layers dans le rapport, le nombre de layers OK et en erreur, le nombre total d'erreurs et le nombre de workspaces.

La commande générale est:

``` bash
reports FILES [--csv CVS] [--export EXPORT]
```

Les paramètres sont:

- `FILE`               : Identifiant du rapport sélectionné - Obligatoire (s'il n'est pas indiqué, la liste des rapports est affichée)
- `--csv`/`-c`         : Exporte le résultat de la requête sous forme de fichier CSV - Optionnel
- `--export`/`-e`      : Exporte le résultat de la requête au format TXT - Optionnel

Exemple d'utilisation:

``` bash
> reports                       # affiche la liste des rapports disponibles
> reports 0                     # affiche les statistiques du rapport n°0 (nombre de layers, nombre de layers en erreur et OK, nombre total d'erreurs, nombre de workspaces).
> reports 0 -c wms_report.csv   # exporte les statistiques du rapport n°0 sous la forme d'un fichier CSV nommé 'wms_report.csv'
> reports 0 -e result.txt       # affiche les statistiques du rapport n°0 puis l'exporte vers le fichier 'result.txt'
```

### `errors`

Permet de lister les erreurs d'un rapport.
La commande générale est:

``` bash
errors FILE [--csv CSV] [--search SEARCH] [--workspace WS] [--id ID] [--limit LIMIT] [--export EXPORT]
```

Les paramètres sont:

- `FILE`               : Identifiant du rapport à lister - Obligatoire (s'il n'est pas indiqué, la liste des rapports est affichée)
- `--csv`/`-c`         : Exporte la liste des erreurs sous forme de fichier CSV - Optionnel
- `--search`/`-s`      : Filtre de recherche plein texte permettant de limiter la liste des erreurs affichées (ex.: `-s commune_actuelle`) - Optionnel
- `--workspace`/`-w`   : Filtre de recherche permettant de limiter la liste des erreurs à afficher en fonction du workspace pour les rapport de type WMS et WFS (ex.: `-w geograndest`) - Optionnel
- `--limit`/`-l`       : Limite du nombre d'erreurs à retourner dans la liste - Optionnel
- `--id`/`-i`          : Identifiant de l'erreur à afficher - Optionnel
- `--export`/`-e`      : Exporte le résultat de la requête au format TXT - Optionnel

Exemple d'utilisation:

``` bash
> errors                              # affiche la liste des rapports disponibles
> errors 0                            # affiche la liste des erreurs du rapport n°0
> errors 0 -c wms_report.csv          # exporte la liste des erreurs sous la forme d'un fichier CSV nommé 'wms_report.csv'
> errors 0 -s commune_actuelle        # affiche la liste des erreurs contenant le terme 'commune_actuelle'
> errors 0 -s commune_actuelle -l 2   # affiche les 2 premières erreurs contenant le terme 'commune_actuelle'
> errors 0 -w region-grand-est -l 5   # affiche les 5 premières erreurs appartenant au workspace 'region-grand-est'
> errors 0 -i 395                     # affiche l'erreur n°395
> errors 0 -i 395 -e result.txt       # affiche l'erreur n°395 puis l'exporte vers le fichier 'result.txt'
```

### `layers`

Permet de lister les layers d'un rapport et éventuellement les erreurs associées.
La commande générale est:

``` bash
layers FILE [--csv CSV] [--search SEARCH] [--workspace WS] [--id ID] [--limit LIMIT] [--export EXPORT]
```

Les paramètres sont:

- `FILE`               : Identifiant du rapport à lister - Obligatoire (s'il n'est pas indiqué, la liste des rapports est affichée)
- `--csv`/`-c`         : Exporte la liste des layers sous forme de fichier CSV - Optionnel
- `--search`/`-s`      : Filtre de recherche plein texte permettant de limiter la liste des layers affichés (ex.: `-s commune_actuelle`) - Optionnel
- `--workspace`/`-w`   : Filtre de recherche permettant de limiter la liste des layers à afficher en fonction du workspace pour les rapport de type WMS et WFS (ex.: `-w geograndest`) - Optionnel
- `--limit`/`-l`       : Limite du nombre de layers à retourner dans la liste - Optionnel
- `--id`/`-i`          : Identifiant du layer à afficher - Optionnel
- `--export`/`-e`      : Exporte le résultat de la requête au format TXT - Optionnel

Exemple d'utilisation:

``` bash
> layers                              # affiche la liste des rapports disponibles
> layers 0                            # affiche la liste des layers du rapport n°0
> layers 0 -c wms_report.csv          # exporte la liste des layers sous la forme d'un fichier CSV nommé 'wms_report.csv'
> layers 0 -s commune_actuelle        # affiche la liste des layers contenant le terme 'commune_actuelle'
> layers 0 -s commune_actuelle -l 2   # affiche les 2 premiers layers contenant le terme 'commune_actuelle'
> layers 0 -w region-grand-est -l 5   # affiche les 5 premiers layers appartenant au workspace 'region-grand-est'
> layers 0 -i 395                     # affiche le layer n°395 de la liste des layers et le détail des erreurs associées
> layers 0 -i 395 -e result.txt       # affiche le layer n°395 de la liste des layers et le détail des erreurs associées puis l'exporte vers le fichier 'result.txt'
```

### `ws`

Permet de lister les différents workspaces des layers d'un rapport.
La commande générale est:

``` bash
ws FILE [--search SEARCH] [--limit LIMIT] [--export EXPORT]
```

Les paramètres sont:

- `FILE`               : Identifiant du rapport à lister - Obligatoire (s'il n'est pas indiqué, la liste des rapports est affichée)
- `--search`/`-s`      : Filtre de recherche plein texte permettant de limiter la liste des workspaces affichés (ex.: `-s region`) - Optionnel
- `--limit`/`-l`       : Limite du nombre de workspaces à retourner dans la liste - Optionnel
- `--export`/`-e`      : Exporte le résultat de la requête au format TXT - Optionnel

Exemple d'utilisation:

``` bash
> ws                             # affiche la liste des rapports disponibles
> ws 0                           # affiche la liste des workspaces du rapport n°0
> ws 0 -s ddt                    # affiche la liste des workspaces contenant le terme 'ddt'
> layers 0 -s ddt -l 5           # affiche les 5 premiers workspaces contenant le terme 'ddt'
> layers 0 -s ddt -e ws_ddt.txt  # affiche la liste des workspaces contenant le terme 'ddt' et l'exporte vers le fichier 'ws_ddt.txt'
```

## Exemple de résultats

``` bash
python.exe .\report.py reports

Liste des fichiers
Nb. reports: 3/3
+----+------------------+------+---------------------------------------------------+
| ID |       NAME       | TYPE |                        URL                        |
+----+------------------+------+---------------------------------------------------+
| 0  | WMS DataGrandEst | wms  | https://www.datagrandest.fr/public/wms-report.log |
| 1  | WFS DataGrandEst | wfs  | https://www.datagrandest.fr/public/wfs-report.log |
| 2  | CSW DataGrandEst | csw  | https://www.datagrandest.fr/public/csw-report.log |
+----+------------------+------+---------------------------------------------------+
```

``` bash
python.exe .\report.py reports 0

Report name: WMS DataGrandEst
Report type: wms
Report URL: https://www.datagrandest.fr/public/wms-report.log

Summary:
+------------------+------+
| nb_layers        | 1917 |
| nb_layers_ok     |   75 |
| nb_layers_errors | 1842 |
| nb_total_errors  | 1941 |
+------------------+------+
```

``` bash
python.exe .\report.py errors 0 -i 2

Report name: WMS DataGrandEst
Report type: wms
Report URL: https://www.datagrandest.fr/public/wms-report.log

Nb. errors: 1/2016
Id parameter: 2
Limit parameter: 10
Errors:
+------+-------------+----------------------+----------+---------------+--------------------------------------------------------------+
|   ID | WORKSPACE   | NAME                 | STATUS   | ERROR CODE    | MESSAGE                                                      |
+======+=============+======================+==========+===============+==============================================================+
|    2 | geograndest | CIGAL_BD_OCS_V2_2000 | ERROR    | ERROR_MD_LINK | Metadata https://www.datagrandest.fr/geonetwork/srv/fre/cata |
|      |             | _ALSACE              |          |               | log.search#/metadata/FR-236700019-BdOCS2000-CIGAL-V2 not     |
|      |             |                      |          |               | found or invalid for layer                                   |
|      |             |                      |          |               | 'geograndest:CIGAL_BD_OCS_V2_2000_ALSACE': Unable to parse   |
|      |             |                      |          |               | the text/xml metadata: mismatched tag: line 22, column 5     |
+------+-------------+----------------------+----------+---------------+--------------------------------------------------------------+
```

``` bash
python.exe .\report.py layers 0

Report name: WMS DataGrandEst
Report type: wms
Report URL: https://www.datagrandest.fr/public/wms-report.log

Nb. layers: 1917/1917
Limit parameter: 10
Layers:
+----+----------------------------------------------+--------+--------+
| ID | NAME                                         | STATUS | ERRORS |
+----+----------------------------------------------+--------+--------+
|  0 | geograndest:BDEA-2019                        | ERROR  | 7      |
|  1 | geograndest:BDEA-2019+                       | ERROR  | 7      |
|  2 | geograndest:CIGAL_BD_OCS_V2_2000_ALSACE      | ERROR  | 1      |
|  3 | geograndest:CIGAL_BD_OCS_V2_2008_ALSACE      | ERROR  | 1      |
|  4 | geograndest:CIGAL_BD_OCS_V2_2011_2012_ALSACE | ERROR  | 1      |
|  5 | geograndest:CIGAL_BD_ZDH_2008                | ERROR  | 1      |
|  6 | geograndest:DGE_Sentinel_2018_OSM            | ERROR  | 1      |
|  7 | geograndest:DGE_Sentinel_2019_OSM            | ERROR  | 1      |
|  8 | geograndest:DGE_Sentinel_2020_OSM            | ERROR  | 1      |
|  9 | geograndest:DGE_Sentinel_2021_OSM            | ERROR  | 1      |
+----+----------------------------------------------+--------+--------+
```

``` bash
python.exe .\report.py layers 0 -s commune_actuelle -l 2

Report name: WMS DataGrandEst
Report type: wms
Report URL: https://www.datagrandest.fr/public/wms-report.log

Nb. layers: 4/1917
Search parameter: commune_actuelle
Limit parameter: 2
Layers:
+-----+----------------------------------------+--------+--------+
|  ID | NAME                                   | STATUS | ERRORS |
+-----+----------------------------------------+--------+--------+
| 395 | region-grand-est:commune_actuelle      | ERROR  | 1      |
| 396 | region-grand-est:commune_actuelle_3857 | ERROR  | 1      |
+-----+----------------------------------------+--------+--------+
```

``` bash
python.exe .\report.py layers 0 -i 1  

Report name: WMS DataGrandEst
Report type: wms
Report URL: https://www.datagrandest.fr/public/wms-report.log

Nb. layers: 1/1917
Layers:
+----+------------------------+--------+--------+
| ID | NAME                   | STATUS | ERRORS |
+----+------------------------+--------+--------+
|  1 | geograndest:BDEA-2019+ | ERROR  | 7      |
+----+------------------------+--------+--------+

Errors:
+------+---------------+----------------------------------------------------------------------------------+
|   ID | CODE          | MESSAGE                                                                          |
+======+===============+==================================================================================+
| 0    | ERROR_MD_LINK | Metadata https://www.datagrandest.fr/geonetwork/srv/fre/catalog.search#/metadata |
|      |               | /FR-200052264-GGE-BD-EA-PLUS-D88-2019 not found or invalid for layer             |
|      |               | 'geograndest:BDEA-2019+': Unable to parse the text/xml metadata: mismatched tag: |
|      |               | line 22, column 5                                                                |
+------+---------------+----------------------------------------------------------------------------------+
| 1    | ERROR_MD_LINK | Metadata https://www.datagrandest.fr/geonetwork/srv/fre/catalog.search#/metadata |
|      |               | /FR-200052264-GGE-BD-EA-PLUS-D54-2019 not found or invalid for layer             |
|      |               | 'geograndest:BDEA-2019+': Unable to parse the text/xml metadata: mismatched tag: |
|      |               | line 22, column 5                                                                |
+------+---------------+----------------------------------------------------------------------------------+
| 2    | ERROR_MD_LINK | Metadata https://www.datagrandest.fr/geonetwork/srv/fre/catalog.search#/metadata |
|      |               | /FR-200052264-GGE-BD-EA-PLUS-D68-2019 not found or invalid for layer             |
|      |               | 'geograndest:BDEA-2019+': Unable to parse the text/xml metadata: mismatched tag: |
|      |               | line 22, column 5                                                                |
+------+---------------+----------------------------------------------------------------------------------+
| 3    | ERROR_MD_LINK | Metadata https://www.datagrandest.fr/geonetwork/srv/fre/catalog.search#/metadata |
|      |               | /FR-200052264-GGE-BD-EA-PLUS-D08-2019 not found or invalid for layer             |
|      |               | 'geograndest:BDEA-2019+': Unable to parse the text/xml metadata: mismatched tag: |
|      |               | line 22, column 5                                                                |
+------+---------------+----------------------------------------------------------------------------------+
| 4    | ERROR_MD_LINK | Metadata https://www.datagrandest.fr/geonetwork/srv/fre/catalog.search#/metadata |
|      |               | /FR-200052264-GGE-BD-EA-PLUS-D57-2019 not found or invalid for layer             |
|      |               | 'geograndest:BDEA-2019+': Unable to parse the text/xml metadata: mismatched tag: |
|      |               | line 22, column 5                                                                |
+------+---------------+----------------------------------------------------------------------------------+
| 5    | ERROR_MD_LINK | Metadata https://www.datagrandest.fr/geonetwork/srv/fre/catalog.search#/metadata |
|      |               | /FR-200052264-GGE-BD-EA-PLUS-D67-2019 not found or invalid for layer             |
|      |               | 'geograndest:BDEA-2019+': Unable to parse the text/xml metadata: mismatched tag: |
|      |               | line 22, column 5                                                                |
+------+---------------+----------------------------------------------------------------------------------+
| 6    | ERROR_MD_LINK | Metadata https://www.datagrandest.fr/geonetwork/srv/fre/catalog.search#/metadata |
|      |               | /FR-200052264-GGE-BD-EA-PLUS-D10-2019 not found or invalid for layer             |
|      |               | 'geograndest:BDEA-2019+': Unable to parse the text/xml metadata: mismatched tag: |
|      |               | line 22, column 5                                                                |
+------+---------------+----------------------------------------------------------------------------------+
```

## Déploiement de l'application

Après avoir cloné le dépôt, il est conseillé d'utiliser un environnement virtuel Python.

Sous Windows:

``` bash
python.exe -m venv venv
.\venv\Scripts\activate
python.exe .\report.py
```

Sous linux:

``` bash
python -m venv venv
source .\venv\bin\activate
python .\report.py
```
