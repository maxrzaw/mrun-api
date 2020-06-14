#!/bin/bash
# Stop on Errors
set -Eeuo pipefail

# Remove database
rm -f db.sqlite3
# Remove migrations
rm -r api/migrations/

# Make migrations
python manage.py makemigrations api
# Migrate
python manage.py migrate

# Create Superuser
python manage.py createsuperuser --email admin@example.com --username admin