SHELL := /bin/bash
include .env

create_environment:
	python3 -m venv env

delete_environment:
	rm -rf env

install:
	pip install --upgrade pip
	pip install -r requirements.txt

run:
	python manage.py runserver

migration:
	python manage.py makemigrations

migrate:
	python manage.py migrate

demo:
	rm -f db.sqlite3
	make migration
	make migrate
	python manage.py demo_data
	python manage.py createsuperuser --noinput

deploy:
	gcloud builds submit --config cloudmigrate.yaml \
    --substitutions _INSTANCE_NAME=postgresql,_REGION=us-central1
	gcloud run deploy turage \
    --platform managed \
    --region us-central1 \
    --image gcr.io/${PROJECT_ID}/turage
