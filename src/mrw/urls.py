from django.urls import path
from .views import ParseChatView, WriteChangesView

app_name = 'mrw'

urlpatterns = [
    path('parse-chat/', ParseChatView.as_view(), name='parse_chat'),
    path('write-changes/', WriteChangesView.as_view(), name='write_changes'),
]
