from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from app.urls import urlpatterns as app_urls

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('api/v1/', include(app_urls)),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                                         document_root=settings.STATIC_ROOT)
