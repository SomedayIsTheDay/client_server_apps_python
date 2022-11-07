import logging
from logging import handlers
import os

logger = logging.getLogger("app.main")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s - %(message)s")

f_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.server.log")
t_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.server.time.log")
fh = logging.FileHandler(f_PATH, encoding="utf-8")

fh.setFormatter(formatter)
fh.setLevel(logging.DEBUG)

th = handlers.TimedRotatingFileHandler(t_PATH, when="s", interval=10, encoding="utf-8")

logger.addHandler(th)
logger.addHandler(fh)
