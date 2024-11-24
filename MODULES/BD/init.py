import sqlite3

from MODULES.MESSAGE_CREATOR import show_mesage


class DB_connection:
    def __init__(self, db_file=None):

        print(f" > CONNECTING TO DB ......... ", end="")
        try:
            if not db_file:
                self.conn = sqlite3.connect("DATA/Dbase.db3", check_same_thread=False)
            else:
                self.conn = sqlite3.connect(db_file, check_same_thread=False)
            print("DONE")
        except Exception as Except_:
            print(Except_)
            exit()

        print(f" > CREATING DB CURSOR ....... ", end="")
        try:
            self.cursor = self.conn.cursor()
            print("DONE")
        except Exception as Except_:
            print(Except_)
            exit()

    def db_get_settings(self, get_strik=False):
        if not get_strik:
            self.cursor.execute("SELECT PARAM from settings WHERE NAME = ?", ("enable_messages", ))
            msg_enable = self.cursor.fetchall()[0][0]

            self.cursor.execute("SELECT PARAM from settings WHERE NAME = ?", ("message_timeout", ))
            msg_timout = self.cursor.fetchall()[0][0]

            self.cursor.execute("SELECT PARAM from settings WHERE NAME = ?", ("message_time_behind_deadline", ))
            msg_deadline_timeout = self.cursor.fetchall()[0][0]

            self.cursor.execute("SELECT PARAM from settings WHERE NAME = ?", ("messages_about_dont_completed_tasks", ))
            msg_tasks = self.cursor.fetchall()[0][0]

            self.cursor.execute("SELECT PARAM from settings WHERE NAME = ?", ("run_on_system_startup", ))
            ru_st = self.cursor.fetchall()[0][0]

            return msg_enable, msg_timout, msg_deadline_timeout, msg_tasks, ru_st

        else:
            self.cursor.execute("SELECT PARAM from settings WHERE NAME = ?", ("streak_day",))
            days = self.cursor.fetchall()[0][0]
            return days

    def settings_write(self, msg_enable, msg_timout, msg_deadline_timeout, msg_tasks, ru_st):
        self.cursor.execute("UPDATE settings SET PARAM = ? WHERE NAME = ?",
                            (msg_enable, "enable_messages",))

        self.cursor.execute("UPDATE settings SET PARAM = ? WHERE NAME = ?",
                            (msg_timout, "message_timeout",))

        self.cursor.execute("UPDATE settings SET PARAM = ? WHERE NAME = ?",
                            (msg_deadline_timeout, "message_time_behind_deadline",))

        self.cursor.execute("UPDATE settings SET PARAM = ? WHERE NAME = ?",
                            (msg_tasks, "messages_about_dont_completed_tasks",))

        self.cursor.execute("UPDATE settings SET PARAM = ? WHERE NAME = ?",
                            (ru_st, "run_on_system_startup",))

        self.conn.commit()

    def check_first_time_run(self):
        self.cursor.execute("SELECT PARAM from settings WHERE NAME = ?",
                            ("first_time_run",))
        state = self.cursor.fetchall()[0][0]
        self.cursor.execute("UPDATE settings SET PARAM = ? WHERE NAME = ?",
                            (0, "first_time_run",))
        self.conn.commit()
        return state

    def happy_write(self, date, happy_number, comment):

        if self.get_today(date):
            show_mesage(msg="Вы уже записали свое настроение")

        else:
            self.cursor.execute("INSERT INTO happy_calendar (data, happy, comments) VALUES (?, ?, ?)",
                                (date, happy_number, comment))
            self.conn.commit()


            self.strick_add()
            stric_days = self.db_get_settings(get_strik=True)
            show_mesage(msg=f"Молодец, теперь у тебя {stric_days} стрик(ов) подряд")


    def write_task(self, title, description, deadline_date, deadline_state, today_date, task_id=None):
        if not task_id:
            self.cursor.execute(
                "INSERT INTO task_list (deadline, deadlineEnable, name, date_create, description) VALUES (?, ?, ?, ?, ?)",
                (deadline_date, deadline_state, title, today_date, description))
            self.conn.commit()

            show_mesage(msg="Задача созданна, обязательно напопомним, если дедлайн не сегодня ^_^")

        else:
            self.cursor.execute("UPDATE task_list SET deadline = ?, deadlineEnable = ?, name = ?, date_create = ?, description = ? WHERE id = ?",
                                (deadline_date, deadline_state, title, today_date, description, task_id))
            self.conn.commit()
            show_mesage(msg="Задача изменена, обязательно напопомним, если дедлайн не сегодня ^_^")

    def get_today(self, date=None, all_days=False):
        if all_days:
            self.cursor.execute("SELECT * from happy_calendar")
            days_with_data = self.cursor.fetchall()

            return days_with_data
        elif not all_days and date:
            self.cursor.execute("SELECT * from happy_calendar WHERE data = ?",
                                (date,))
            day_with_data = self.cursor.fetchall()

            return day_with_data

    def get_tasks(self, task_id=None, notif=False):
        if not task_id:
            if not notif:
                self.cursor.execute("SELECT * from task_list")
                task_list = self.cursor.fetchall()

                return task_list
            else:
                self.cursor.execute("SELECT * from task_list WHERE notified = 0 and deadlineEnable = 1")
                task_list = self.cursor.fetchall()

                return task_list
        else:
            self.cursor.execute("SELECT * from task_list WHERE id = ?", (task_id,))
            task_info = self.cursor.fetchall()[0]

            return task_info

    def del_task(self, t_id):
        self.cursor.execute(
            "DELETE FROM task_list WHERE id = ?",
            (t_id,))
        self.conn.commit()

        show_mesage(msg="Задача удалена, возвращайтесь еще )")

    def strick_add(self, annulise=False):
        stric_days = int(self.db_get_settings(get_strik=True))
        if annulise:
            self.cursor.execute("UPDATE settings SET PARAM = ? WHERE NAME = ?",
                                (0, "streak_day",))

            self.conn.commit()
        else:
            self.cursor.execute("UPDATE settings SET PARAM = ? WHERE NAME = ?",
                                (stric_days+1, "streak_day",))

            self.conn.commit()

    def notif_task(self, tid):
        self.cursor.execute("UPDATE task_list SET notified = 1 WHERE id = ?", (tid,))
        self.conn.commit()
