from rest_framework import routers
from django.urls import path, include
from . import views

router = routers.DefaultRouter()
router.register(r"conversations", views.ConversationViewSet,
                basename="conversations")
router.register(r"messages", views.MessageViewSet, basename="messages")


urlpatterns = [
    path("", include(router.urls))
]
