# SharePoint Office365-REST-Python-Client

## Installation

```bash
pip install -r requirements.txt
```

## Start app

```bash
python app.py
```

## APIs

1. List all folders in folder_path

```bash
curl -X 'POST' \
  'http://localhost:8000/folders' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "folder_path": "Shared Documents/TOI Session Archive/VTtT 2021 1H"
}'
```

2. List all files in folder_path

```bash
curl -X 'POST' \
  'http://localhost:8000/files' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "folder_path": "Shared Documents/TOI Session Archive/VTtT 2021 1H"
}'
```