from .models import *

def layout_context(request):
    if request.user.is_authenticated:
        user = User.objects.get(pk=int(request.user.id))
        watchlist_count = Watchlist.objects.filter(user=user).count()
    else:
        watchlist_count = 0
    context = {
        "watchlist_count": watchlist_count
    }
    return context