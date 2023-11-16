from django.contrib import admin
from django.urls import path
from first.views import home_view
from first.views import speech_view
from first.views import output_speech
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name="home"),
    path('speech.html', speech_view, name='speech_page'),
    path('output_speech/', output_speech, name='output_speech'),  # Corrected name
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)