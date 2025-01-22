from django.urls import path
from app import views
from askme_gladysheva import settings
from django.conf.urls.static import static

app_patterns = [
    path('', views.index, name='index'),
    path('hot/', views.hot, name='hot'),
    path('question/<int:question_id>', views.question, name='one_question'),
    path("login/", views.login, name="login"),
    path("registration/", views.registration, name="registration"),
    path("settings/", views.settings, name="settings"),
    path("ask/", views.ask, name="ask"),
    path("tag/<str:tag_name>/", views.tag, name="tag"),
    path('logout/', views.logout, name="logout"),
    path('profile/edit/', views.settings, name = 'settings')
]

if settings.DEBUG:
    app_patterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)