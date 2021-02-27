default: image

all: image

image:
	docker build . \
	--pull \
	--file Dockerfile \
	--tag pyhf-funcx-endpoint:pyhf-funcx-endpoint \
	--tag pyhf-funcx-endpoint:pyhf-funcx-endpoint-python3.8 \
	--tag pyhf-funcx-endpoint:latest
