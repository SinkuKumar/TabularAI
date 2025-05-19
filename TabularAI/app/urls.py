from django.urls import path
from .views import file_upload_view, ask_question

urlpatterns = [
    path('', file_upload_view, name='upload'),
    path('ask/', ask_question, name='ask'),
]
