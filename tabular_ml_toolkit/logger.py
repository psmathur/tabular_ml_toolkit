# AUTOGENERATED! DO NOT EDIT! File to edit: logger.ipynb (unless otherwise specified).

__all__ = ['handler', 'logger']

# Cell
import logging

# Cell
handler = logging.StreamHandler()
# set custom formatting settings for info
handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))

# now create logger
logger = logging.getLogger("tmlt")
logger.addHandler(handler)
logger.setLevel(logging.INFO)