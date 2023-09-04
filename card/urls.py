from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework import routers
from card.views import CheckInView, WorkshopAddView, WorkshopOverviewView

router = routers.SimpleRouter()
router.register(r'checkin', CheckInView)
router.register(r'workshop/(?P<workshop_id>[\d]+)/card', WorkshopAddView)
router.register(r'workshops', WorkshopOverviewView)

urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += router.urls
