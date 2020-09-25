"""Celery's config file."""
from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Planeks_CsvGeneratingService.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", "LocalConf")
import configurations  # noqa
from configurations import importer

configurations.setup()

importer.install()

app = Celery("Planeks_CsvGeneratingService")
app.config_from_object("django.conf:settings")

app.autodiscover_tasks()
