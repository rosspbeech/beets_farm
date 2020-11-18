from django.urls import path
from beets import views

app_name = 'beets'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('persona/<slug:persona_name_slug>/',
         views.show_persona, name='show_persona'),
    path('add_persona/', views.add_persona, name='add_persona'),
    path('persona/<slug:persona_name_slug>/add_beet/', views.add_beet, name='add_beet'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('personas', views.personas, name='talent'),
    path('new_sound/', views.RandomSongView.as_view(), name='new_sound'),
    path('userHub/', views.userHub, name='hub'),
    path('persona/<slug:persona_name_slug>/edit_persona/', views.edit_persona, name='edit_persona'),
    path('edit_beet/<int:beet_id>/', views.edit_beet, name="edit_beet"),
]
