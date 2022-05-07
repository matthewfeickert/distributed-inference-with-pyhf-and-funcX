default: image

all: image

image:
	docker pull python:3.8-buster
	docker build . \
	--file Dockerfile \
	--tag pyhf-funcx-endpoint:pyhf-funcx-endpoint \
	--tag pyhf-funcx-endpoint:pyhf-funcx-endpoint-python3.8 \
	--tag pyhf-funcx-endpoint:latest
