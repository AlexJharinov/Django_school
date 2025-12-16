from django.urls import path
from rest_framework.routers import SimpleRouter

from users.views import PaymentViewSet, RegisterView, UserViewSet  # ✅ именно так

router = SimpleRouter()
router.register(r"payments", PaymentViewSet, basename="payment")
router.register(r"users", UserViewSet, basename="user")
urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
]

urlpatterns = router.urls
