from django.contrib.auth import logout

def delete_user(request):
    """
    Delete user account and all its related data
    """
    user = request.user
    logout(request)
    user.delete()

