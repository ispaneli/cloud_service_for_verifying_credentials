import csv
import hashlib


SERVICE_MAP = {'ebay': "db/ebay.csv",
               'facebook': "db/facebook.csv",
               'google': "db/google.csv",
               'instagram': "db/instagram.csv",
               'twitter': "db/twitter.csv"}


def check_username_in_csv_db(filename: str, username: str) -> bool:
    """
    Проверяет, есть ли учетная запись с таким username в базе
    скомпрометированных аккаунтов конкретного сервиса.

    :param filename: Имя csv-таблицы с логинами и пароля конкретного сервиса (демонстрационный вариант БД).
    :param username: Имя пользователя, которое нужно проверить по БД.
    :return: Ответ на вопрос: "В БД есть такой username?".
    """
    with open(filename, 'r') as csv_db:
        db_data = list(csv.reader(csv_db))

        for row in db_data[1:]:
            if username == row[0]:
                return True

        return False


def check_password_in_csv_db(filename: str, username: str, part_of_password_hash: str) -> bool:
    """
    Проверяет, есть ли учетная запись с таким username и password
    в базе скомпрометированных аккаунтов конкретного сервиса.

    :param filename: Имя csv-таблицы с логинами и пароля конкретного сервиса (демонстрационный вариант БД).
    :param username: Имя пользователя, которое нужно проверить по БД.
    :param part_of_password_hash: Половина хэша пароля пользователя.
    :return: Ответ на вопрос: "В БД есть username с паролем, дающий такой хэш?".
    """
    with open(filename, 'r') as csv_db:
        db_data = list(csv.reader(csv_db))

        for row in db_data[1:]:
            if username == row[0]:
                real_hash_as_str = hashlib.sha512(row[1].encode()).hexdigest()
                return part_of_password_hash == real_hash_as_str[:64]

        return False
