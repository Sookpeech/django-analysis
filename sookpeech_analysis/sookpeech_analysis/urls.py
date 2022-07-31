from django.contrib import admin
from django.urls import path
from analysis import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('analysis/<int:user_id>/<int:practice_id>/<int:rand>/<str:gender>', views.analysis, name='analysis'),
]
