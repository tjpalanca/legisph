# AUTOGENERATED! DO NOT EDIT! File to edit: ../notebooks/00-core.ipynb.

# %% auto 0
__all__ = ['logger']

# %% ../notebooks/00-core.ipynb 3
import logging

logging.basicConfig()
logger = logging.getLogger("legisph")
logger.setLevel(logging.INFO)
