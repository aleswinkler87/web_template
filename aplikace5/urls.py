from django.contrib import admin
from django.urls import path
from aplikace5.views import ovladani_view, tabulecka_view, vysledky_view

urlpatterns = [
    path('ovladani/', ovladani_view, name='ovladani'),
    path('tabulecka/', tabulecka_view, name='tabulecka'),
    path('vysledky/', vysledky_view, name='vysledky'),
]
