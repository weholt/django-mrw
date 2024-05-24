import json
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .forms import InputForm
from .services import parse_chat
import os


from urllib.parse import unquote


class ParseChatView(View):
    def get(self, request):
        form = InputForm()
        return render(request, "mrw/parse_chat.html", {"form": form})

    def post(self, request):
        form = InputForm(request.POST)
        if form.is_valid():
            app_name = form.cleaned_data["app_name"]
            root_folder = form.cleaned_data.get("root_folder", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            content = request.POST.get("editor_content", "")
            content = unquote(content)  # Decode the content
            parsed_data = parse_chat(content, app_name, root_folder)
            return JsonResponse(parsed_data, safe=False)
        return JsonResponse({"error": "Invalid form data"}, status=400)


class WriteChangesView(View):
    def post(self, request):
        app_name = request.POST.get("app_name")
        root_folder = request.POST.get("root_folder", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        content = request.POST.get("editor_content", "")
        parsed_data = parse_chat(content, app_name, root_folder)

        for file_path, file_content in parsed_data.items():
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w") as file:
                file.write(file_content)

        return JsonResponse({"status": "Changes written successfully"})
