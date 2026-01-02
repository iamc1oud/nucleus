db-forward:
	kubectl port-forward svc/postgres 5432:5432 -n nucleus-dev
