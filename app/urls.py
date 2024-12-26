from django.urls import path
from app import views

app_patterns = [
    path('', views.index, name='index'),
    path('hot/', views.hot, name='hot'),
    path('question/<int:question_id>', views.question, name='one_question'),
    path("login/", views.login, name="login"),
    path("registration/", views.registration, name="registration"),
    path("settings/", views.settings, name="settings"),
    path("ask/", views.ask, name="ask"),
    path("tag/<str:tag_name>/", views.tag, name="tag"),
]