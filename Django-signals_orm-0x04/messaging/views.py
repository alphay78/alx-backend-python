from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

User = get_user_model()

@login_required
def delete_user(request):
    """
    Allow a logged-in user to delete their account.
    Triggers the post_delete signal to clean up related data.
    """
    user = request.user
    username = user.username
    user.delete()  # this will fire the post_delete signal
    return HttpResponse(f"User {username} and all related data have been deleted.")
