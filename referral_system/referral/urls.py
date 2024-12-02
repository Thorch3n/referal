from django.urls import path
from .views import AuthView, VerifyCodeView, ProfileView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from .api_views import AuthAPIView, VerifyCodeAPIView, ProfileAPIView

urlpatterns = [
    path('auth/', AuthView.as_view(), name='auth_phone'),
    path('verify/', VerifyCodeView.as_view(), name='verify_phone'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('api/auth/', AuthAPIView.as_view(), name='api_auth'),
    path('api/verify/', VerifyCodeAPIView.as_view(), name='api_verify'),
    path('api/profile/', ProfileAPIView.as_view(), name='api_profile'),
    # Схема OpenAPI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # ReDoc документация
    path('api/docs/', SpectacularRedocView.as_view(url_name='schema'),
         name='redoc'),

    # Swagger UI (по желанию)
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'),
         name='swagger-ui'),
]
