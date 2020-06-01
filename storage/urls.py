from django.urls import path
from .views import home, StorageView

app_name = "storage"

urlpatterns = [
    path("", StorageView.as_view(), name="storage")
]
