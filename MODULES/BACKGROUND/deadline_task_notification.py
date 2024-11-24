import datetime
import threading
import time

from MODULES.MESSAGE_CREATOR import show_mesage
from MODULES.BD.init import DB_connection

UPDATE_TIME = 1*60*60


def task_not_compleated():
    db = DB_connection("./DATA/Dbase.db3")
    while True:
        static = db.db_get_settings()
        t_m = static[2]
        enable = static[3]

        if enable == 1:
            tasks = db.get_tasks(notif=True)

            for task in tasks:
                today = str(datetime.date.today()).split("-")
                deadline = task[1].split("-")

                if today[0] == deadline[0] and today[1] == deadline[1] and int(deadline[2]) - int(today[2]) <= t_m:
                    show_mesage(title="Напоминание: HaPPy", msg="напоминаем вам о незавершенной задаче")
                    db.notif_task(task[0])
                    time.sleep(20)


        time.sleep(UPDATE_TIME)


notification2 = threading.Thread(target=task_not_compleated)