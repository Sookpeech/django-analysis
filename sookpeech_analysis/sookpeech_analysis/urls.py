from django.contrib import admin
from django.urls import path
from analysis import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('analysis/<int:user_id>/<int:practice_id>/<str:gender>/<int:pose_sensitivity>/<int:eyes_sensitivity>', views.analysis, name='analysis'),
]
