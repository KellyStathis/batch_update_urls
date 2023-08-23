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

- ACCOUNT_ID: DataCite Repository account ID.
- ACCOUNT_PASS: DataCite Repostiory account password.
- PROD: Set to "true" for production environment; default is "false" for test environment.
- FIND: String to find in the URL.
- REPLACE: String to replace with in the URL.

## Usage

python batch_update.py

## Limitations
This was created quickly for an internal migration of a small repository. It retrieves the most recent 1000 DOIs from a repository, though it could be adapted to retrieve and update more.

As this code was not officially reviewed or tested by the DataCite engineering team, please take care to check for errors when using it.
