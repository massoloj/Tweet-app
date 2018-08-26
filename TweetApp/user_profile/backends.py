from django.conf import settings
from user_profile.models import UserProfile

class UserProfileBackend(object):
    """
    A custom authentication backend for UserProfileModels.
    """

    def authenticate(self, username=None, password=None):
        """
        Authentication method
        """
        try:
            user = UserProfile.objects.get(username=username)
            if user.password == password:
                return user
        except UserProfile.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            user = UserProfile.objects.get(pk=user_id)
            if user.is_active:
                return user
            return None
        except UserProfile.DoesNotExist:
            return None
