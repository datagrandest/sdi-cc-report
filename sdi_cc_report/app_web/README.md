# SDI CC REPORT WEB

Application Python permettant de générer une API de consultation des rapports issus du script ["SDI Consistence Check"](https://github.com/georchestra/sdi-consistence-check).

## Déploiement de l'application

Après avoir cloné le dépôt, il est conseillé d'utiliser un environnement virtuel Python.

Sous Windows:

``` bash
python.exe -m venv venv
.\venv\Scripts\activate
pip.exe install -r .\sdi_cc_report\app_web\requirements_web.txt
python.exe .\report.py
```

Sous linux:

``` bash
python -m venv venv
source ./venv/bin/activate
pip install -r ./sdi_cc_report/app_web/requirements_web.txt
python ./report.py
```

## Utilisation

L'application fonctionne grâce à un serveur web basé sur "bottle". Elle permet notamment de pouvoir développer et héberger une application en ligne. Cette dernière devra être déposée dans le dossier "./sdi_cc_report/app_web/ui/dist".
Elle peut être lancée selon plusieurs modes:

``` bash
python.exe .\report.py web [prod]   # mode production par défaut. L'application s'ouvre dans webview
python.exe .\report.py web dev      # mode développement (debug=True). L'application s'ouvre dans webview
python.exe .\report.py web browser  # mode navigateur: l'application s'ouvre dans le navigateur
python.exe .\report.py web wsgi     # mode WSGI pour l'utilisation sur certains serveurs
```

Par défaut le serveur propose une page, avec d'une part des liens vers les réponses de l'API notamment, et d'autre part des tableaux de bords simples connectés directement à l'API.

## API

### `reports`

Fournit, au format JSON, la liste des rapports disponibles (configurés dans "./sdi_cc_report/config.yaml") ou les statistiques d'un rapport spécifique.

Exemple: liste des rapports disponibles

URL: <http://127.0.0.1:8001/reports>

Resultat:

``` json
[
  {
    "name": "WMS DataGrandEst",
    "type": "wms",
    "url": "https://www.datagrandest.fr/public/wms-report.log",
    "id": 0
  },
  {
    "name": "WFS DataGrandEst",
    "type": "wfs",
    "url": "https://www.datagrandest.fr/public/wfs-report.log",
    "id": 1
  },
  {
    "name": "CSW DataGrandEst",
    "type": "csw",
    "url": "https://www.datagrandest.fr/public/csw-report.log",
    "id": 2
  }
]
```

Exemple: statistiques du rapport n°0

URL: <http://127.0.0.1:8001/reports/0>

Resultat:

``` json
[
  {
    "nb_errors": 2017,
    "nb_layers": 1918,
    "nb_layers_ok": 75,
    "nb_layers_error": 1843,
    "nb_workspaces": 61,
    "report_name": "WMS DataGrandEst",
    "report_type": "wms",
    "report_url": "https://www.datagrandest.fr/public/wms-report.log"
  }
]
```

### 'errors'

Fournit, au format JSON, la liste des erreurs du rapport spécifié.

Les paramètres d'URL sont:

- `search=`: permet de filtrer la liste retournée selon un texte libre.
- `ws=`: permet de filtrer la liste retournée selon un workspace spécifique
- `name=`: permet de filtrer la liste retournée selon le nom d'un layer
- `id=`: permet de filtrer la liste retournée selon l'identifiant d'un layer
- `limit=`: permet de limiter le nombre de résultats retournés
- `offset=`: permet de définir le nombre de résultats retournés
- 'details=': permet de récupéré uniquement la iste des erreurs (par défaut) ou également les statistiques des erreurs retournées

Exemple: liste les erreurs du workspace 'geograndest' du rapport n°0

URL: <http://127.0.0.1:8001/errors/0?ws=geograndest>

Resultat:

``` json
[
  {
    "id": "0",
    "workspace": "geograndest",
    "name": "BDEA-2019",
    "error": 1,
    "error_code": "ERROR_MD_LINK",
    "message": "Metadata https://www.datagrandest.fr/geonetwork/srv/fre/catalog.search#/metadata/FR-200052264-GGE-BD-EA-D54-2019 not found or invalid for layer 'geograndest:BDEA-2019': Unable to parse the text/xml metadata: mismatched tag: line 22, column 5",
    "search": "0 | geograndest | BDEA-2019 | ERROR_MD_LINK | Metadata https://www.datagrandest.fr/geonetwork/srv/fre/catalog.search#/metadata/FR-200052264-GGE-BD-EA-D54-2019 not found or invalid for layer 'geograndest:BDEA-2019': Unable to parse the text/xml metadata: mismatched tag: line 22, column 5"
  },
  {
    "id": "0",
    "workspace": "geograndest",
    "name": "BDEA-2019",
    "error": 1,
    "error_code": "ERROR_MD_LINK",
    "message": "Metadata https://www.datagrandest.fr/geonetwork/srv/fre/catalog.search#/metadata/FR-200052264-GGE-BD-EA-D68-2019 not found or invalid for layer 'geograndest:BDEA-2019': Unable to parse the text/xml metadata: mismatched tag: line 22, column 5",
    "search": "0 | geograndest | BDEA-2019 | ERROR_MD_LINK | Metadata https://www.datagrandest.fr/geonetwork/srv/fre/catalog.search#/metadata/FR-200052264-GGE-BD-EA-D68-2019 not found or invalid for layer 'geograndest:BDEA-2019': Unable to parse the text/xml metadata: mismatched tag: line 22, column 5"
  },
  ...
  {
    "id": "1917",
    "workspace": "cc-thann-cernay",
    "name": "raepa_reparaep_p",
    "error": 1,
    "error_code": "ERROR_MD_LINK",
    "message": "Metadata https://www.datagrandest.fr/metadata/cc-thann-cernay/FR-20003646500124-01-raepa_reparaep_p_cc_thann_cernay.xml not found or invalid for layer 'cc-thann-cernay:raepa_reparaep_p': 'text/xml' Metadata not found (HTTP 404): 404 Client Error: Not Found for url: https://www.datagrandest.fr/metadata/cc-thann-cernay/FR-20003646500124-01-raepa_reparaep_p_cc_thann_cernay.xml",
    "search": "1917 | cc-thann-cernay | raepa_reparaep_p | ERROR_MD_LINK | Metadata https://www.datagrandest.fr/metadata/cc-thann-cernay/FR-20003646500124-01-raepa_reparaep_p_cc_thann_cernay.xml not found or invalid for layer 'cc-thann-cernay:raepa_reparaep_p': 'text/xml' Metadata not found (HTTP 404): 404 Client Error: Not Found for url: https://www.datagrandest.fr/metadata/cc-thann-cernay/FR-20003646500124-01-raepa_reparaep_p_cc_thann_cernay.xml"
  }
]
```

Exemples:

URL: <http://127.0.0.1:8001/errors/0?ws=geograndest&details=1>   # Liste les erreurs du workspace 'geograndest' du rapport n°0

Resultat:

``` json
{
  "nb_errors": 2017,
  "errors": [...],
  "report": {
    "name": "WMS DataGrandEst",
    "type": "wms",
    "url": "https://www.datagrandest.fr/public/wms-report.log",
    "id": 0
  },
  "search": null,
  "workspace": "geograndest",
  "name": null,
  "id": null,
  "limit": null,
  "offset": null,
  "nb_errors_return": 343
}
```

### 'layers'

Fournit, au format JSON, la liste des layers du rapport spécifié.

Les paramètres d'URL sont:

- `search=`: permet de filtrer la liste retournée selon un texte libre.
- `ws=`: permet de filtrer la liste retournée selon un workspace spécifique
- `name=`: permet de filtrer la liste retournée selon le nom d'un layer
- `id=`: permet de filtrer la liste retournée selon l'identifiant d'un layer
- `limit=`: permet de limiter le nombre de résultats retournés
- `offset=`: permet de limiter le nombre de résultats retournés
- 'details=': permet de récupéré uniquement la iste des erreurs (par défaut) ou également les statistiques des erreurs retournées

Exemple: liste les layers du workspace 'geograndest' du rapport n°0

URL: <http://127.0.0.1:8001/layers/0?ws=geograndest&limit=10>

Resultat:

``` json
[
  {
    "id": "0",
    "workspace": "geograndest",
    "name": "BDEA-2019",
    "error": 1,
    "nb_errors": 7,
    "errors": [
      {
        "error_id": 1,
        "error_code": "ERROR_MD_LINK",
        "error_message": "Metadata https://www.datagrandest.fr/geonetwork/srv/fre/catalog.search#/metadata/FR-200052264-GGE-BD-EA-D54-2019 not found or invalid for layer 'geograndest:BDEA-2019': Unable to parse the text/xml metadata: mismatched tag: line 22, column 5"
      },
      { ... },
      {
        "error_id": 7,
        "error_code": "ERROR_MD_LINK",
        "error_message": "Metadata https://www.datagrandest.fr/geonetwork/srv/fre/catalog.search#/metadata/FR-200052264-GGE-BD-EA-D57-2019 not found or invalid for layer 'geograndest:BDEA-2019': Unable to parse the text/xml metadata: mismatched tag: line 22, column 5"
      }
    ],
    "search": "0 | geograndest | BDEA-2019 | ERROR_MD_LINK | Metadata https://www.datagrandest.fr/geonetwork/srv/fre/catalog.search#/metadata/FR-200052264-GGE-BD-EA-D54-2019 not found or invalid for layer 'geograndest:BDEA-2019': Unable to parse the text/xml metadata: mismatched tag: line 22, column 5 | ..."
  },
  {...},
  {...},
  {...},
  {...},
  {...},
  {...},
  {...},
  {...},
  {...}
]
```

Exemple: Liste les 10 premimiers layers et les statistiques du workspace 'geograndest' du rapport n°0

URL: <http://127.0.0.1:8001/layers/0?limit=10&details=1>

Resultat:

``` json
{
  "nb_layers": 1918,
  "layers": [],
  "report": {
    "name": "WMS DataGrandEst",
    "type": "wms",
    "url": "https://www.datagrandest.fr/public/wms-report.log",
    "id": 0
  },
  "search": null,
  "workspace": null,
  "name": null,
  "id": null,
  "limit": "10",
  "offset": 0,
  "nb_layers_return": 10
}
```

### 'workspaces'

Fournit, au format JSON, la liste des erreurs du rapport spécifié.
Cette API n'est disponible que pour les rapports de type WMS et WFS.

Les paramètres d'URL sont:

- `search=`: permet de filtrer la liste retournée selon le nom du workspace.
- `limit=`: permet de limiter le nombre de résultats retournés
- `offset=`: permet de limiter le nombre de résultats retournés
- 'details=': permet de récupéré uniquement la iste des erreurs (par défaut) ou également les statistiques des erreurs retournées

Exemple: liste l'ensembldes workspaces du rapport n°0

URL: <http://127.0.0.1:8001/workspaces/0>

Resultat:

``` json
[
  {
    "id": 0,
    "workspace": "geograndest",
    "nb_errors": 316,
    "nb_layers": 267,
    "nb_layers_ok": 15,
    "nb_layers_error": 252
  },
  {
    "id": 1,
    "workspace": "ems",
    "nb_errors": 59,
    "nb_layers": 61,
    "nb_layers_ok": 3,
    "nb_layers_error": 58
  }, 
  {...}
]
```

Exemple: Liste les 10 premimiers workspaces et les statistiques du workspace 'geograndest' du rapport n°0

URL: <http://127.0.0.1:8001/workspaces/0?search=geograndest&details=1>

Resultat:

``` json
{
  "nb_workspaces": 61,
  "workspaces": [
    {
      "id": 0,
      "workspace": "geograndest",
      "nb_errors": 316,
      "nb_layers": 267,
      "nb_layers_ok": 15,
      "nb_layers_error": 252
    }
  ],
  "report": {
    "name": "WMS DataGrandEst",
    "type": "wms",
    "url": "https://www.datagrandest.fr/public/wms-report.log",
    "id": 0
  },
  "search": "geograndest",
  "limit": null,
  "offset": null,
  "nb_workspaces_return": 1
}
```
