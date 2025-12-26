build-image:
	docker build -t nucleus/auth-service:dev .

load-k8:
	kind load docker-image nucleus/auth-service:dev --name nucleus 2>&1 && kubectl rollout restart deployment/auth-service -n nucleus-dev 2>&1

port-forward:
	kubectl port-forward deployment/auth-service 8080:8080 -n nucleus-dev
