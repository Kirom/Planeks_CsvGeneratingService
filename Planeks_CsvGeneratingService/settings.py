"""Separating local and production settings."""
from .prod_conf import ProdConf  # noqa

try:
    from .local_conf import LocalConf  # noqa
except ImportError:
    pass

# export DJANGO_CONFIGURATION=LocalConf
# export DJANGO_SETTINGS_MODULE=Planeks_CsvGeneratingService.settings
# celery -A Planeks_CsvGeneratingService worker -l INFO -c 4 -B