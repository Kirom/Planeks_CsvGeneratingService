"""Separating local and production settings."""
from .prod_conf import ProdConf  # noqa

try:
    from .local_conf import LocalConf  # noqa
except ImportError:
    pass
