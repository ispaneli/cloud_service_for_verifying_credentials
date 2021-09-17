from flask import Flask, request, abort

from credentials_checkers import SERVICE_MAP, check_username_in_csv_db, check_password_in_csv_db


app = Flask(__name__)


@app.route('/check_username', methods=['POST'])
def check_username():
    """
    Проверяет username по базе скомпрометированных аккаунтов.

    :return: Если в БД нет такого username - вернет {'need_password': False};
             если есть - то вернет {'need_password': True}, что означает: "Требуется провести проверку с паролем".
    """
    service_name = request.values['service_name']
    username = request.values['username']

    if service_name not in SERVICE_MAP.keys():
        return abort(400, "Unknown service name.")

    answer = check_username_in_csv_db(SERVICE_MAP[service_name], username)
    return {'need_password': answer}


@app.route('/check_username_and_password', methods=['POST'])
def check_username_and_password():
    """
    Проверяет username и часть хэша пароля по базе скомпрометированных аккаунтов.

    :return: Если в БД нет таких учетных данных - вернет {'account_was_compromised': False};
             если есть - то вернет {'account_was_compromised': True}.
    """
    service_name = request.values['service_name']
    username = request.values['username']
    part_of_password_hash = request.values['part_of_password_hash']

    if service_name not in SERVICE_MAP.keys():
        return abort(400, "Unknown service name.")

    if len(part_of_password_hash) != 64:
        return abort(400, "Invalid length of the part of password hash.")

    answer = check_password_in_csv_db(SERVICE_MAP[service_name], username, part_of_password_hash)
    return {'account_was_compromised': answer}


if __name__ == '__main__':
    app.run()







