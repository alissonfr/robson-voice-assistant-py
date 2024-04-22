./.venv/scripts/Activate

coverage run -m unittest discover
coverage report
coverage html
