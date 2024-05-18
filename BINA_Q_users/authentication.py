from django.contrib.auth.backends import BaseBackend
from BINA_Q_users.models import User


class BinaQIDBackend(BaseBackend):
    def authenticate(self, request, bina_q_id=None, password=None, **kwargs):
        try:
            user = User.objects.get(bina_q_id=bina_q_id)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
