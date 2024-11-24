import datetime
import threading
from datetime import datetime as dt
import time

from MODULES.BD.init import DB_connection
from MODULES.MESSAGE_CREATOR import show_mesage

UPDATE_TIME = 1*60*60


def happy_not_written():
    db = DB_connection("./DATA/Dbase.db3")
    while True:
        static = db.db_get_settings()
        upd_msg = static[1]
        enable = static[0]

        if enable == 1:

            while not db.get_today(date=datetime.date.today()):
                now_hour = int(dt.today().strftime("%H"))
                if now_hour >= 16:
                    show_mesage(msg="Не забудьте заполнить настроение  ^-^")
                time.sleep(upd_msg*60)
        time.sleep(UPDATE_TIME)


notification1 = threading.Thread(target=happy_not_written)