from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication


class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        """
        Return the user referenced by the validated token
        """
        user_id = validated_token.get(settings.USER_ID_CLAIM)

        if user_id is None:
            raise AuthenticationFailed(
                "Token contained no recognizable user identification",
                code="user_id_missing"
            )
        try:
            user = self.user_model.objects.get(
                **{settings.USER_ID_FIELD: user_id})
        except self.user_model.DoesNotExist:
            raise AuthenticationFailed(
                "User not found", code="user_not_found"
            )
        if not user.is_active:
            raise AuthenticationFailed(
                "User is inactive", code="user_inactive")
        return user
