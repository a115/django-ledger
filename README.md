# django-ledger
Python / Django-based double entry accounting ledger

# Toy project for the refactor of the MainRD project

In this project we will create the django models for the ledger. For more information see the SQL in https://gist.github.com/jordan-dimov/67cf99a3f2ffd400c2140a956d587a86

## Getting started with local development

Make a virtualenv with Python 3.8 and pip install `requirements/dev.txt`

To run the Django project, you will need to set some environment variables. You could put those in the `bin/postactivate` script in your virtualenv so they are loaded automatically each time you activate the virtualenv:

    export EXTRA_ALLOWED="localhost"
    export DJANGO_DEBUG=TRUE
    export DJANGO_SECRET_KEY="-generate-a-secret-key-for-your-instance-"
    export PG_DB_NAME="your-mainrd-db-name"
    export PG_USER="your-mainrd-db-user"
    export PG_PASS="your-mainrd-db-password"
    export PG_HOST="127.0.0.1"
    export BRAND_NAME="Localhost"
    export OWN_CRN="08438306"
    export MAINRD_SITE_ID=5
