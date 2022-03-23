NAMESPACE=default

WORKDIR=$(shell pwd)

export WORKDIR

up:
	docker-compose up -d --build

down:
	docker-compose down --remove-orphans

import-images:
	docker build -t cicadatesting/demo-api-app:local .
	docker build -t cicadatesting/demo-api-flyway:local -f flyway.dockerfile .
	k3d image import cicadatesting/demo-api-app:local
	k3d image import cicadatesting/demo-api-flyway:local

install-kube:
	kubectl apply -f kube-app.yaml

uninstall-kube:
	kubectl delete -f kube-app.yaml
