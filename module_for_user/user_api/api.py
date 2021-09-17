import hashlib
import re
import requests
from colorama import init, Fore


init(autoreset=True)

RE_EXCEPTION_PARSER = r"<p>[\w\s.,]*</p>"

ONLY_USERNAME_URL = "http://127.0.0.1:5000/check_username"
CREDENTIALS_URL = "http://127.0.0.1:5000/check_username_and_password"


def _check_only_username(service_name: str, username: str, with_log: bool) -> bool:
    """
    Проверяет только username на скомпрометированность в облачном сервисе.

    :param service_name: Имя сервиса, username от которого нужно проверить в облачном сервисе.
                         Поддерживаются только ['ebay', 'facebook', 'google', 'instagram', 'twitter'].
    :param username: Имя пользователя, которое нужно проверить по облачном сервисе.
    :param with_log: Значение True включает режим логирования запросов.
    :return: Ответ от облачного сервиса.
    """
    data_for_request = {'service_name': service_name,
                        'username': username}

    if with_log:
        print(f"-- Проверка только логина [ЗАПРОС]; data={data_for_request}; url={ONLY_USERNAME_URL}")

    response = requests.post(ONLY_USERNAME_URL, data=data_for_request)

    if response.status_code == 400:
        exception_as_str = re.findall(RE_EXCEPTION_PARSER, response.text)[0][3:-4]
        print(Fore.RED + exception_as_str)
        raise ValueError(exception_as_str)

    response_as_dict = response.json()
    if with_log:
        print(f"-- Проверка только логина [ОТВЕТ]; data={response_as_dict}; url={ONLY_USERNAME_URL}")

    return response_as_dict['need_password']


def check_credentials(service_name: str, username: str, password: str, with_log: bool = False) -> None:
    """
    Проверяет username и password на скомпрометированность в облачном сервисе.

    :param service_name: Имя сервиса, учетные данные от которого нужно проверить в облачном сервисе.
                         Поддерживаются только ['ebay', 'facebook', 'google', 'instagram', 'twitter'].
    :param username: Имя пользователя, которое нужно проверить по облачном сервисе.
    :param password: Пароль пользователя, которое нужно проверить по облачном сервисе.
    :param with_log: Значение True включает режим логирования запросов.
    :return: None.
    """
    answer_of_cloud_service = _check_only_username(service_name, username, with_log=with_log)

    if answer_of_cloud_service:
        part_of_password_hash = hashlib.sha512(password.encode()).hexdigest()[:64]
        data_for_request = {'service_name': service_name,
                            'username': username,
                            'part_of_password_hash': part_of_password_hash}

        if with_log:
            print(f"-- Проверка логина и пароля [ЗАПРОС]; data={data_for_request}; url={CREDENTIALS_URL}")

        response = requests.post(CREDENTIALS_URL, data=data_for_request)
        if response.status_code == 400:
            exception_as_str = re.findall(RE_EXCEPTION_PARSER, response.text)[0][3:-4]
            print(Fore.RED + exception_as_str)
            raise ValueError(exception_as_str)

        response_as_dict = response.json()
        if with_log:
            print(f"-- Проверка логина и пароля [ОТВЕТ]; data={response_as_dict}; url={CREDENTIALS_URL}")

        if response_as_dict['account_was_compromised']:
            print(Fore.RED + "Your credentials is compromised!\n\n")
        else:
            print(Fore.GREEN + "Your credentials is not compromised!\n\n")
    else:
        print(Fore.GREEN + "Your credentials is not compromised!\n\n")


