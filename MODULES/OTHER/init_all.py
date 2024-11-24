import sys

from MODULES.BACKGROUND.deadline_task_notification import notification2
from MODULES.BACKGROUND.strike_notification import notification1
from dotenv import dotenv_values


try:
    config = dotenv_values("./DATA/globals.txt")
    VERSION = config["version"]
    By = config["by"]
except Exception as e:
    print(f".env error: {e}")
    sys.exit()



def init_all():
    notification1.start()
    notification2.start()
