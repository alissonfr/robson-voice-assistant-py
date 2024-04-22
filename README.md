python3 -m venv .venv
./.venv/scripts/Activate
pip install -r requirements.txt | python3 -m pip install -r requirements.txt

coverage run -m unittest discover
coverage report
coverage html
