.PHONY: run-api

run-api:
	uv run uvicorn api.fast:app --reload

docker_build:
	docker build --platform amd64/linux -t ${IMAGE_NAME} .

docker_build_local:
	docker build \
		-t ${IMAGE_NAME}:dev .

docker_build_cloud:
	docker build \
		--platform linux/amd64 \
		-t ${GAR_IMAGE_NAME}:prod .

docker_image_name:
	@echo ${GAR_IMAGE_NAME}

auth_docker:
	gcloud auth configure-docker ${GCP_REGION}-docker.pkg.dev

create_docker_repo:
	gcloud artifacts repositories create ${DOCKER_REPO_NAME} \
		--repository-format=docker \
		--location=${GCP_REGION} \
		--description="Repository for storing Docker images"

docker_run:
	docker run \
	-p 8001:8080 \
	--env-file .env \
	${IMAGE_NAME}:dev

docker_run_with_gcs:
	docker run \
	-p 8001:8080 \
	--env-file production.env \
	-v ~/.config/gcloud/application_default_credentials.json:/tmp/keys/gackey.json:ro \
	-e GOOGLE_APPLICATION_CREDENTIALS=/tmp/keys/gackey.json \
	${IMAGE_NAME}:dev

docker_run_with_gcs2:
	docker run \
	-p 8001:8000 \
	--env-file production.env \
	-v ~/.config/gcloud/application_default_credentials.json:/tmp/keys/gackey.json:ro \
	-e GOOGLE_APPLICATION_CREDENTIALS=/tmp/keys/gackey.json \
	${IMAGE_NAME}:dev

docker_push:
	docker push ${GAR_IMAGE_NAME}:prod

docker_deploy:
	gcloud run deploy ${CLOUD_RUN_SERVICE_NAME} \
		--image ${GAR_IMAGE_NAME}:prod \
		--allow-unauthenticated \
		--env-vars-file production.env \
		--region ${GCP_REGION}
