SHELL := /bin/bash
include .env

push:
	git add .
	git commit -m '${message}'
	git push

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
	gcloud builds submit --substitutions=_SERVICE_NAME=${SERVICE_NAME},\
	_PORT=${PORT},\
	_GOOGLE_CLOUD_PROJECT=${GOOGLE_CLOUD_PROJECT},\
	_GS_BUCKET_NAME=${GS_BUCKET_NAME},\
	_REGION=${REGION},\
	_CLOUDRUN_SERVICE_URL=${CLOUDRUN_SERVICE_URL},\
	_CLOUD_SQL_INSTANCE_NAME=${CLOUD_SQL_INSTANCE_NAME},\
	_DEBUG=${DEBUG},\
	_MAX_INSTANCES=10
	--timeout=2400
# TODO: on deployment, run demo management command against dev base

set-project:
	gcloud config set project ${PROJECT_ID}

build-docker:
	docker build -t ${SERVICE_NAME} .

run-docker:
 	docker run -p ${PORT}:${PORT} ${SERVICE_NAME}


# TODO: Need to run this against the production database when needed
#python manage.py demo_data
#RUN python manage.py createsuperuser --noinput
