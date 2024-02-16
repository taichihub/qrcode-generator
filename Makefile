REGISTRY := registry.sasio.net
APP_NAME := qrcode-generator
TAG := latest
IMAGE_BASE=${REGISTRY}/${APP_NAME}

.PHONY: build
build:
	docker build -t ${IMAGE_BASE}:${TAG} .

.PHONY: push
push:
	docker push ${IMAGE_BASE}:${TAG}

