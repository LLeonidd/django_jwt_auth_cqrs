from rest_framework_simplejwt.tokens import RefreshToken


class CustomToken(RefreshToken):
    @property
    def access_token(self):
        """
        Добавление кастомного поля в закодированный токен, например
        access['custom'] = 'custom_field'
        :return:
        """
        access = super().access_token
        return access

    @classmethod
    def for_user(cls, user):
        """
        Добаляем кастомные данные о пользователе в закодированный токен, например:
        token['user_group'] = dict(user.groups.values_list())
        """
        token = super().for_user(user)
        return token

