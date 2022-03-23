TEST_IMAGE=cicadatesting/cicada-distributed-demo-integration-test:local
MODE=LOCAL

run-local:
	ENV=local cicada-distributed --debug run --mode=${MODE} --log-path=logs --dockerfile local.dockerfile -e FOO BAR --env-file .env

run-dev:
	ENV=dev cicada-distributed --debug run --mode=${MODE} --log-path=logs --dockerfile dev.dockerfile -e FOO BAR --env-file .env

run:
	cicada-distributed --debug run --mode=${MODE} --log-path=logs -e FOO BAR --env-file .env

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
