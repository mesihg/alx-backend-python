from rest_framework import routers
from rest_framework_nested.routers import NestedDefaultRouter
from django.urls import path, include
from . import views

router = routers.DefaultRouter()
router.register(r"conversations", views.ConversationViewSet,
                basename="conversations")

conversations_router = NestedDefaultRouter(
    router, r"conversations", lookup="conversation")

# router.register(r"messages", views.MessageViewSet, basename="messages")
conversations_router.register(
    r"messages", views.MessageViewSet, basename="conversation-messages")


urlpatterns = [
    path("", include(router.urls)),
    path("", include(conversations_router.urls)),
]
