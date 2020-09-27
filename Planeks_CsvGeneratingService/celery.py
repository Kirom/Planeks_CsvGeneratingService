"""Celery's config file."""
from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Planeks_CsvGeneratingService.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", "LocalConf")
import configurations  # noqa

configurations.setup()

app = Celery("Planeks_CsvGeneratingService")
app.config_from_object("django.conf:settings", namespace='CELERY')

app.autodiscover_tasks()
