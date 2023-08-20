from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from user.models import Account


class EmailBackend(ModelBackend, object):
    def authenticate(self, request, phone=None, password=None, ** kwargs):

        user_model = get_user_model()
        try:
            user = user_model.objects.get(phone=phone)
        except user_model.DoesNotExist:
            return None
        else:
            if not user.check_password(password):
                return user
        return None

    @staticmethod
    def get_user(id):
        try:
            return Account.objects.get(pk=id)  # <-- tried to get by email here
        except Account.DoesNotExist:
            return None
