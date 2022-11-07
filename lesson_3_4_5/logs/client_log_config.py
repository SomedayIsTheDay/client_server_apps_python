import logging
import os

logger = logging.getLogger("app.main")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s - %(message)s")

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.client.log")
fh = logging.FileHandler(PATH, encoding="utf-8")
sh = logging.StreamHandler()

fh.setFormatter(formatter)
fh.setLevel(logging.DEBUG)
sh.setFormatter(formatter)
sh.setLevel(logging.INFO)

logger.addHandler(fh)
logger.addHandler(sh)
