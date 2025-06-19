from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('account/', views.account_view, name='account'),
    path('about/', views.about, name='about'),
    path('index/', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('application/', views.application, name='application'),
    path('geographical_information_system/', views.geographical_information_system, name='geographical_information_system'),
    path('remote-sensing/', views.remote_sensing, name='remote_sensing'),
    path('rainfall-map/', views.rainfall_map_page, name='rainfall-map'),
    path('temperature/', views.temperature_view, name='temperature'),
    path('farm/', views.farm_view, name='farm'),
    path('zao/', views.zao_view, name='zao'),
    path('ph/', views.ph_view, name='ph'),
    path('type/', views.soil_view, name='type'),
    path('capability/', views.capability_view, name='capability'),
    path('classify/', views.upload_folder, name='classify'),
    path('weather/', views.weather_view, name='weather'),
    path('For/', views.For_view, name='For_view'),
    path('Forecast/', views.Forecast_view, name='Forecast_view'),
    path('rukwa/', views.rukwa_view, name='rukwa_view'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

