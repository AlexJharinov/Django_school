from rest_framework.routers import SimpleRouter
from users.views import PaymentViewSet

router = SimpleRouter()
router.register(r"payments", PaymentViewSet, basename="payment")

urlpatterns = router.urls