.PHONY: run-api

run-api:
	uv run uvicorn api.fast:app --reload
