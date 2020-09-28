# Planeks_CsvGeneratingService
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Python test assessment by Planeks.

If you have any questions, you can contact me in telegram @Nizhdanchik or email me viktor.mironov.dev@gmail.com.

Deployment link: `https://fakecsv.herokuapp.com/` or [click](https://fakecsv.herokuapp.com/).

Authentication credentials: Username: First, Password: second123 

## Running all the stuff step by step
1. Clone repo: `git clone https://github.com/Kirom/Planeks_CsvGeneratingService.git`
2. Rename `local_conf_dev.py` to `local_conf.py`
3. Create virtualenv, for example: `python3 -m venv venv` or `virtualenv -p python3 venv`
4. Activate it `source venv/bin/activate`
5. Install all the packages `pip install -r requirements.txt`
6. Run redis `redis-server`
7. Run celery worker `celery -A Planeks_CsvGeneratingService worker -l INFO -c 4 -B`
8. Set environment variables `export DJANGO_CONFIGURATION=LocalConf`,   
`export DJANGO_SETTINGS_MODULE=Planeks_CsvGeneratingService.settings`
9. Start the app itself `./manage.py runserver`

