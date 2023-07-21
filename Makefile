# install Python dependencies
init:
	poetry install

# run cli
run:
	poetry run python src/app.py

# clean python caching files..
clean:
	rm -rf src/__pycache__

