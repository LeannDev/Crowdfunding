from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from .views import HomeView
#from goal.views import GoalCreateView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    #path('goal/', GoalCreateView.as_view(), name='goal'), # MOVE TO GOAL APP !!!
    path('donate/', include('donation.urls')),
]

# Static files route
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)