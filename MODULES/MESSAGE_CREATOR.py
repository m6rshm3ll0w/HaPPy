from win10toast import ToastNotifier

toast = ToastNotifier()


def show_mesage(title: str = "HaPPy", msg: str = "", duration: int = 1):
    try:
        toast.show_toast(
            title=title,
            msg=msg,
            duration=duration,
            icon_path="",
            threaded=True,
        )
    except Exception as E:
        print("")

# show_mesage("Не потеряй комбо", "привет, сегодня ты не заполнил настроение")
