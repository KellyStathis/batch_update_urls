# Batch Update URLs
A simple batch update script to update URLs for up to 1000 DataCite DOIs.

## Setup

Create an .env file in the root directory with the following variables:
```
ACCOUNT_ID=
ACCOUNT_PASS=
PROD=
FIND=
REPLACE=
```

- ACCOUNT_ID: DataCite Repository account ID
- ACCOUNT_PASS: DataCite Repostiory account pass
- PROD: Set to "true" for production environment; default is "false" for test environment.
- FIND: String to find in the URL.
- REPLACE: String to replace with in the URL.

## Usage

python batch_update.py
