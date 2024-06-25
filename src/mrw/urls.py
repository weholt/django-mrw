from django.urls import path

from .views import ParseChatView, WriteChangesView, clean_up, delete_prompt, save_prompt

app_name = "mrw"

urlpatterns = [
    path("", ParseChatView.as_view(), name="parse_chat"),
    path("write-changes/", WriteChangesView.as_view(), name="write_changes"),
    path("save_prompt/", save_prompt, name="save_prompt"),
    path("delete_prompt", delete_prompt, name="delete_prompt"),
    path("clean_up/", clean_up, name="clean_up"),
]
