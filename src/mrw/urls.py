from django.urls import path

from .views import ParseChatView, WriteChangesView, save_prompt, delete_prompt

app_name = "mrw"

urlpatterns = [
    path("parse-chat/", ParseChatView.as_view(), name="parse_chat"),
    path("write-changes/", WriteChangesView.as_view(), name="write_changes"),
    path('save_prompt/', save_prompt, name='save_prompt'),
    path('delete_prompt', delete_prompt, name='delete_prompt'),    
]
