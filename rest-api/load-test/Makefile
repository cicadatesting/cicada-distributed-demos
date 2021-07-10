TEST_IMAGE=cicadatesting/cicada-distributed-demo-load-test:local

run-local:
	ENV=local cicada-distributed --debug run --dockerfile local.dockerfile

run-dev:
	ENV=dev cicada-distributed --debug run --dockerfile dev.dockerfile

run:
	cicada-distributed --debug run

import-kube-local:
	docker build -t ${TEST_IMAGE} -f local.dockerfile .
	k3d image import ${TEST_IMAGE}

import-kube-dev:
	docker build -t ${TEST_IMAGE} -f dev.dockerfile .
	k3d image import ${TEST_IMAGE}

import-kube:
	docker build -t ${TEST_IMAGE} .
	k3d image import ${TEST_IMAGE}

run-kube:
	cicada-distributed --debug run --mode=KUBE --image=${TEST_IMAGE}
