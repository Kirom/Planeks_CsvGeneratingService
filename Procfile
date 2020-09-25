web: gunicorn Planeks_CsvGeneratingService.wsgi --bind:0.0.0.0:80 --log-file -
celery: celery -A Planeks_CsvGeneratingService worker -l INFO -c 4 -B