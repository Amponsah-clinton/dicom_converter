from django.contrib import admin
from django.urls import path
from converter import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.convert_to_dicom, name='convert_to_dicom'),
]
