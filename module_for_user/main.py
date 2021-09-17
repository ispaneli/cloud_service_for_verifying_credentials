from user_api import check_credentials


WITH_LOG = True


if __name__ == '__main__':
    # Uncompromised account.
    service_name_1 = 'ebay'
    username_1 = 'uncompromised_username'
    password_1 = 'uncompromised_password'
    check_credentials(service_name_1, username_1, password_1, with_log=WITH_LOG)

    # Compromised account (only username).
    service_name_2 = 'instagram'
    username_2 = 'jaxona'
    password_2 = 'uncompromised_password'
    check_credentials(service_name_2, username_2, password_2, with_log=WITH_LOG)

    # Compromised account (username and password).
    service_name_3 = 'google'
    username_3 = 'oralishaniew'
    password_3 = 'mmANy4w9qUkJw'
    check_credentials(service_name_3, username_3, password_3, with_log=WITH_LOG)

