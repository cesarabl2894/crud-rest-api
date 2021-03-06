from services.UtilService import check_fields_existance_in_payload
import services.MessageService as MessageService
import services.AuthService as AuthService
import dao.UserDao as UserDao


def add_user(payload):
    try:
        fields_exist = check_fields_existance_in_payload(payload, 'first_name', 'email', 'gamertag', 'password')

        if fields_exist:
            __set_optional_fields(payload, 'last_name', 'address', 'profile_picture', 'role')
            user = UserDao.create_user(payload)

            if user:
                return MessageService.generate_success_message('User created', user.to_dictionary())
            else:
                return MessageService.generate_custom_message('The user could not be added', 500)
        else:
            return MessageService.missing_fields_request

    except Exception as e:
        return MessageService.generate_internal_server_error(e)


def get_user(gamertag, token):
    try:
        data = AuthService.decode_token(token)

        if data['role'] == 'admin':
            gamertag_to_look = gamertag
        else:
            gamertag_to_look = data['gamertag']

        data = UserDao.retrieve_user(gamertag_to_look)

        if data:
            return MessageService.generate_success_message('', data.to_dictionary())
        else:
            return MessageService.generate_custom_message('No user was found with that gamertag', {})

    except Exception as e:
        return MessageService.generate_internal_server_error(e)


def get_all_users():
    try:
        result = UserDao.get_users()
        response = []
        for user in result:
            response.append(user.to_dictionary())

        if len(response):
            return MessageService.generate_success_message('', response)
        else:
            return MessageService.generate_custom_message('No users were found', {})

    except Exception as e:
        return MessageService.generate_internal_server_error(e)


def modify_user(payload):
    try:
        result = UserDao.check_email_gamertag_duplication(payload['id'], payload['email'], payload['gamertag'])

        if result:
            return MessageService.user_info_duplication

        if check_fields_existance_in_payload(payload, 'id', 'first_name', 'last_name', 'email', 'address', 'gamertag',
                                             'profile_picture'):
            user = UserDao.update_user(payload)
            if user:
                return MessageService.generate_success_message('', user.to_dictionary())
            else:
                MessageService.generate_custom_message('No user was found', {})
        else:
            return MessageService.missing_fields_request

    except Exception as e:
        return MessageService.generate_internal_server_error(e)


def remove_user(payload):
    try:
        if check_fields_existance_in_payload(payload, 'id'):
            user = UserDao.delete_user(payload['id'])

            if user:
                return MessageService.generate_success_message('', user.to_dictionary())
            else:
                return MessageService.generate_custom_message('No user was found', {})
        else:
            return MessageService.missing_fields_request

    except Exception as e:
        return MessageService.generate_internal_server_error(e)


def login(payload):
    if not check_fields_existance_in_payload(payload, 'email', 'password'):
        return MessageService.missing_fields_request

    try:
        result = UserDao.login_user(payload)

        if not result:
            return MessageService.authentication_failed

        token = AuthService.generate_token(result)
        data = {'token': 'Bearer ' + token}

        return MessageService.generate_success_message('', data)

    except Exception as e:
        return MessageService.generate_internal_server_error(e)


def __set_optional_fields(payload, *fields):
    for field in fields:
        if field not in payload.keys():
            if field == 'role':
                payload[field] = 'customer'
            else:
                payload[field] = ''
