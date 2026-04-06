from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.vault.views import HiddenVaultView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.auth_app.urls')),
    path('api/diary/', include('apps.diary.urls')),
    path('api/letters/', include('apps.letters.urls')),
    path('api/vault/', include('apps.vault.urls')),
    path('api/checkins/', include('apps.checkins.urls')),
    path('api/timeline/', include('apps.timeline.urls')),
    path('api/presence/', include('apps.presence.urls')),
    path('s/<slug:slug>/', HiddenVaultView.as_view(), name='hidden-vault'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)