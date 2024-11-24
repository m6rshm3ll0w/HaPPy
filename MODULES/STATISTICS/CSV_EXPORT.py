import csv

from MODULES.BD.init import DB_connection


def csv_export(file_path):
    db = DB_connection("./DATA/Dbase.db3")
    days = db.get_today(all_days=True)

    data = []

    for day in days:
        data.append({"дата": day[0], "настроение": day[1], "комментарии": day[2]})

    with open(file_path, 'w', newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=list(data[0].keys()),
            delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        for d in data:
            writer.writerow(d)