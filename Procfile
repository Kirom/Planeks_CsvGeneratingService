web: gunicorn Planeks_CsvGeneratingService.wsgi --log-file -
celery: celery -A Planeks_CsvGeneratingService worker -l INFO -c 4 -B