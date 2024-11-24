import datetime
import sys

from PyQt6 import uic
from PyQt6.QtCore import QCoreApplication, Qt, QTimer, QDate, QUrl
from PyQt6.QtGui import QIcon, QAction, QPixmap
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QApplication, QWidget, QSystemTrayIcon, QMenu, QMessageBox, QSlider, QVBoxLayout, QLabel, \
    QPushButton, QFrame, QHBoxLayout, QMainWindow, QFileDialog

from MODULES.BD.init import DB_connection
from MODULES.OTHER.init_all import init_all, VERSION, By
from MODULES.MESSAGE_CREATOR import show_mesage
from MODULES.STATISTICS.graph import render_graph
from MODULES.STATISTICS.CSV_EXPORT import csv_export


# noinspection PyUnresolvedReferences
class Hello(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('DATA/ui/hello.ui', self)
        self.initUI()

    def initUI(self):
        self.version_label.setText(f"{VERSION} & {By}")
        self.closeButton.clicked.connect(lambda: self.hide())
        self.setWindowTitle("Привет!!!")
        self.setWindowIcon(QIcon('DATA/icon.png'))

        pixmap = QPixmap('./DATA/icon.png')
        self.limage.setPixmap(pixmap)
        self.limage.setScaledContents(True)


    def closeEvent(self, event):
        event.ignore()
        self.hide()


####################################################
def graph_show():
    global wv
    days = db.get_today(all_days=True)

    dates = []
    happyes = []
    comments = []

    for day in days:
        data, happy, comment = day
        dates.append(data)
        happyes.append(happy)
        comments.append(comment)

    render_graph(dates, happyes, comments)

    wv.destroy()
    wv = WebView()
    wv.show()


def happy_show():
    global happy_window
    happy_window.destroy()
    happy_window = Write_happy()
    happy_window.show()


def task_show(task_data=None):
    global task_creator_window
    task_creator_window.destroy()
    task_creator_window = Task_create()
    if not task_data:
        task_creator_window.show()
    else:
        task_creator_window.edit_task(task_data)
        task_creator_window.show()


def settings_show():
    global settings_window
    settings_window.destroy()
    settings_window = Settings()
    settings_window.show()


def task_mgr_show():
    global task_mgr_window
    task_mgr_window.destroy()
    task_mgr_window = Task_manager()
    task_mgr_window.show()
####################################################


# DONE
# noinspection PyUnresolvedReferences
class WebView(QMainWindow):
    def __init__(self):
        try:
            super().__init__()

            self.browser = QWebEngineView()
            self.setWindowIcon(QIcon('./DATA/icon.png'))
            self.setWindowTitle("График настроения")

            self.browser.setUrl(QUrl('file:///DATA/graph.html'))

            layout = QVBoxLayout()
            layout.addWidget(self.browser)

            container = QWidget()
            container.setLayout(layout)
            self.setCentralWidget(container)

            self.resize(1024, 750)
        except Exception as E:
            print(E)

    def closeEvent(self, event):
        event.ignore()
        self.hide()


# DONE
# noinspection PyUnresolvedReferences
class Tray_icon(QWidget):
    def __init__(self):
        super().__init__()
        self.uiINIT()

    def uiINIT(self):
        self.tray_icon_set()

    def tray_icon_set(self, ):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("./DATA/icon.png"))

        menu = QMenu()

        add_happy = QAction("Записать настроение", self)
        add_happy.triggered.connect(lambda: happy_show())
        menu.addAction(add_happy)

        stats = QAction("Статистика настроения", self)
        stats.triggered.connect(lambda: graph_show())
        menu.addAction(stats)

        settings = QAction("Открыть настройки", self)
        settings.triggered.connect(lambda: settings_show())
        menu.addAction(settings)

        add_task = QAction("Добавить задачу", self)
        add_task.triggered.connect(lambda: task_show())
        menu.addAction(add_task)

        show_welcome = QAction("Приветственное окно", self)
        show_welcome.triggered.connect(lambda: welcome_window.show())
        menu.addAction(show_welcome)

        show_calendar = QAction("Просмотр Задач", self)
        show_calendar.triggered.connect(lambda: task_mgr_show())
        menu.addAction(show_calendar)

        exit_action = QAction("Выход", self)
        exit_action.triggered.connect(lambda: self.app_quit())
        menu.addAction(exit_action)

        self.tray_icon.setContextMenu(menu)
        self.tray_icon.show()

    def app_quit(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Подтверждение")
        dlg.setText("Вы точно хотите выйти из приложения?")
        dlg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        dlg.setIcon(QMessageBox.Icon.Question)
        dlg.setWindowIcon(QIcon("./DATA/icon.png"))
        button = dlg.exec()

        if button == QMessageBox.StandardButton.Yes:
            QCoreApplication.quit()
        else:
            dlg1 = QMessageBox(self)
            dlg1.setWindowTitle("Инфо")
            dlg1.setText("Выход отменен!")
            dlg1.setStandardButtons(QMessageBox.StandardButton.Ok)
            dlg1.setIcon(QMessageBox.Icon.Information)
            dlg1.setWindowIcon(QIcon("./DATA/icon.png"))
            dlg1.exec()

    def closeEvent(self, event):
        event.ignore()
        self.hide()


# FULL DONE
# noinspection PyUnresolvedReferences
class Task_manager(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_tasks()

    def initUI(self):
        uic.loadUi('DATA/ui/task_manage.ui', self)
        self.setWindowTitle("Просмотр Задач")
        self.setWindowIcon(QIcon('./DATA/icon.png'))

        self.updateButton.clicked.connect(lambda: self.load_tasks())

    def load_tasks(self):

        task_list = db.get_tasks()

        self.widget = QWidget()
        self.vbox = QVBoxLayout()

        a = self.size().width() - 30
        self.widget.setMinimumWidth(a)
        self.widget.setMaximumWidth(a)

        for task in task_list:
            date_of_create = QLabel(f"Созданно: {task[4]}")
            self.vbox.addWidget(date_of_create)

            name = QLabel(f"Тема: {task[3]}")
            self.vbox.addWidget(name)

            if not task[5] or task[5] == "":
                description = QLabel(f"Описание: нет")
            else:
                description = QLabel(f"Описание: {task[5]}")

            self.vbox.addWidget(description)

            if task[2] == 1:
                deadline = QLabel(f"Дедлайн: {task[1]}")
            else:
                deadline = QLabel(f"Дедлайн: нет")

            self.vbox.addWidget(deadline)

            buttons = QHBoxLayout()

            b1 = QPushButton("Изменить")
            b2 = QPushButton("Выполнено")

            b1.clicked.connect(lambda _, task_id=task[0]: self.task_edit(task_id))
            b2.clicked.connect(lambda _, task_id=task[0]: self.done_task_delete(task_id))

            buttons.addWidget(b1)
            buttons.addWidget(b2)

            self.vbox.addLayout(buttons)

            line = QFrame()
            line.setFrameShape(QFrame.Shape.HLine)
            line.setFrameShadow(QFrame.Shadow.Sunken)
            line.setLineWidth(2)

            self.vbox.addWidget(line)

        self.widget.setLayout(self.vbox)

        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.scroll.setWidgetResizable(False)
        self.scroll.setWidget(self.widget)

    def done_task_delete(self, task_id):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Подтверждение")
        dlg.setText("Вы точно хотите удалить эту задачу?")
        dlg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        dlg.setIcon(QMessageBox.Icon.Question)
        button = dlg.exec()

        if button == QMessageBox.StandardButton.Yes:
            db.del_task(task_id)
            self.load_tasks()
        else:
            pass

    def task_edit(self, task_id):
        task_data = db.get_tasks(task_id=task_id)
        task_show(task_data=task_data)

    def closeEvent(self, event):
        event.ignore()
        self.hide()


# FULL DONE
# noinspection PyUnresolvedReferences
class Task_create(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('DATA/ui/task_create.ui', self)
        self.setWindowIcon(QIcon('./DATA/icon.png'))
        self.setWindowTitle("Создание Задачи")
        self.initUI()

    def initUI(self):
        self.deadline_data.setMinimumDate(QDate.currentDate())
        self.deadline_data.setDisplayFormat("yyyy.MM.dd")

        self.deadlineEnable.setCheckState(Qt.CheckState.Checked)
        self.deadlineEnable.stateChanged.connect(lambda: self.set_deadline())

        self.closeButton.clicked.connect(lambda: self.hide())
        self.create.clicked.connect(lambda: self.write2db())

    def set_deadline(self):
        if self.deadlineEnable.isChecked() is True:
            self.deadline_data.setEnabled(True)
        else:
            self.deadline_data.setEnabled(False)

    def write2db(self, task_id=None, today_date=None):

        title = self.task_name.text()
        if title == "":
            show_mesage(msg="пожалуйста, укажите название")
            return 0
        description = self.comment.toPlainText()
        deadline_state = self.deadlineEnable.isChecked()
        deadline_date = self.deadline_data.date()

        deadline_date = f"{deadline_date.year()}-{deadline_date.month()}-{deadline_date.day()}"

        if not task_id:
            today = datetime.date.today().strftime('%Y-%m-%d')
            db.write_task(title, description, deadline_date, deadline_state, today)

            task_mgr_window.load_tasks()


        else:
            today = today_date
            db.write_task(title, description, deadline_date, deadline_state, today, task_id)

            task_mgr_window.load_tasks()

        QTimer().singleShot(1000, lambda: self.hide())

    def edit_task(self, data):
        task = data[0]
        deadline: str = data[1]
        deadlineEnabled = data[2]
        title = data[3]
        creation_data = data[4]
        description = data[5]

        if deadlineEnabled == 1:
            self.deadlineEnable.setCheckState(Qt.CheckState.Checked)
        else:
            self.deadlineEnable.setCheckState(Qt.CheckState.Unchecked)

        self.comment.setPlainText(description)
        self.task_name.setText(title)

        self.create.setText('Обновить')

        self.deadline_data.setDate(QDate.fromString(deadline, "yyyy-MM-dd"))
        self.create.clicked.disconnect()
        self.create.clicked.connect(lambda: self.write2db(task_id=task, today_date=creation_data))

    def closeEvent(self, event):
        event.ignore()
        self.hide()


# FULL DONE
# noinspection PyUnresolvedReferences
class Settings(QWidget):
    def __init__(self):
        super().__init__()

        self.time2 = None
        self.time1 = None

        uic.loadUi('DATA/ui/settings.ui', self)
        self.setWindowIcon(QIcon('./DATA/icon.png'))
        self.setWindowTitle("Настройки")

        self.initUI()
        self.load_from_db()
        self.edit_params()

    def initUI(self):
        self.time_selector.setMinimum(15)
        self.time_selector.setSingleStep(2)

        self.time_selector_2.setMinimum(1)
        self.time_selector_2.setSingleStep(1)
        self.time_selector_2.setMaximum(7)

        time_selector: QSlider

        self.time_selector.valueChanged.connect(self.update_slider1)
        self.time_selector_2.valueChanged.connect(self.update_slider2)

        self.close_conf.clicked.connect(lambda: self.hide())
        self.apply_conf.clicked.connect(lambda: self.write2db())
        self.enable_message.stateChanged.connect(lambda: self.edit_params())
        self.dont_compleated_task.stateChanged.connect(lambda: self.edit_params())

        self.export2csv.clicked.connect(lambda: self.export())

    def export(self):
        try:
            file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "", "CSV Files (*.csv);;All Files (*)")
            csv_export(file_path)

            dlg = QMessageBox(self)
            dlg.setWindowTitle("ОК")
            dlg.setText("Файл Сохранен!!!")
            dlg.setStandardButtons(QMessageBox.StandardButton.Ok)
            dlg.setIcon(QMessageBox.Icon.Information)
            dlg.show()

        except Exception as E:
            print(E)

    def load_from_db(self):
        msg_enable, msg_timout, msg_deadline_timeout, msg_tasks, ru_st = db.db_get_settings()

        if msg_enable == 1:
            self.enable_message.setCheckState(Qt.CheckState.Checked)
        else:
            self.enable_message.setCheckState(Qt.CheckState.Unchecked)

        if msg_tasks == 1:
            self.dont_compleated_task.setCheckState(Qt.CheckState.Checked)
        else:
            self.dont_compleated_task.setCheckState(Qt.CheckState.Unchecked)

        self.time_selector.setValue(msg_timout)
        self.time_selector_2.setValue(msg_deadline_timeout)

    def edit_params(self):
        if not self.enable_message.isChecked():
            self.time_selector.setEnabled(False)
        else:
            self.time_selector.setEnabled(True)

        if not self.dont_compleated_task.isChecked():
            self.time_selector_2.setEnabled(False)
        else:
            self.time_selector_2.setEnabled(True)

    def write2db(self):

        msg_enable = self.enable_message.isChecked()
        msg_timout = self.time1
        msg_deadline_timeout = self.time2
        msg_tasks = self.dont_compleated_task.isChecked()

        db.settings_write(msg_enable, msg_timout, msg_deadline_timeout, msg_tasks, 0)
        show_mesage(msg="Параметры приложения были применены")

    def update_slider1(self, value):
        self.time1 = value
        self.show_time.setText(f"{value}")

    def update_slider2(self, value):
        self.time2 = value
        self.days_show.setText(f"{value} день(дней) до дедлайна")

    def closeEvent(self, event):
        event.ignore()
        self.hide()


# FULL DONE
# noinspection PyUnresolvedReferences
class Write_happy(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('DATA/ui/write_happy.ui', self)
        self.setWindowTitle("Запись Настроения")
        self.setWindowIcon(QIcon('./DATA/icon.png'))

        self.write_happy.clicked.connect(lambda: self.write2db())
        self.closeButton.clicked.connect(lambda: self.hide())

    def write2db(self):
        if self.one.isChecked():
            happy = 1
        elif self.two.isChecked():
            happy = 2
        elif self.three.isChecked():
            happy = 3
        elif self.four.isChecked():
            happy = 4
        elif self.five.isChecked():
            happy = 5
        elif self.six.isChecked():
            happy = 6
        elif self.seven.isChecked():
            happy = 7
        elif self.eight.isChecked():
            happy = 8
        elif self.nine.isChecked():
            happy = 9
        elif self.ten.isChecked():
            happy = 10
        else:
            show_mesage(msg="выбери настроение")
            return 0

        date_now = datetime.date.today()
        comment_happy = self.comment.toPlainText()

        db.happy_write(date_now, happy, comment_happy)
        QTimer().singleShot(1000, lambda: self.hide())

    def closeEvent(self, event):
        event.ignore()
        self.hide()


# Импортировать уведомления о не выполненных задачах
if __name__ == '__main__':
    init_all()
    app = QApplication(sys.argv)

    db = DB_connection()

    welcome_window = Hello()
    settings_window = Settings()
    task_creator_window = Task_create()
    task_mgr_window = Task_manager()
    happy_window = Write_happy()
    tray_widget = Tray_icon()
    wv = WebView()

    if db.check_first_time_run() == 1:
        welcome_window.show()
    else:
        show_mesage(msg="приложение запущено в фоновом режиме")

    sys.exit(app.exec())
