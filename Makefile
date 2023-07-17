tests:
	@echo "\n ======= Running Tests ======="
	@pytest -v .

bump_version:
	@echo "\n ======= Bumping Version ======="

deploy:
	@echo "\n ======= Deploying Application ======="
	git push heroku main

run:
	@echo "\n ======= Running Application Locally ======="
	python -m flask run