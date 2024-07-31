.PHONY: lint

lint:
	pants lint ::
	pants fmt ::
	pants check src/mistralai src/mistralai/models
