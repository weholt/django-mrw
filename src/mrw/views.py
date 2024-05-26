import re
import os
import shutil
import time
from urllib.parse import unquote

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import InputForm, PromptForm
from .services import parse_chat
from .models import Prompt


def camelcase2snakecase(s: str) -> str:
    "Converts CamelCase to snake-case, ie. CamelCase -> camel_case"
    return re.sub(r"(?<!^)(?=[A-Z])", "_", s).lower()


class ParseChatView(View):
    def get(self, request):
        return render(
            request,
            "mrw/parse_chat.html",
            {
                "prompt_form": PromptForm(),
                "prompts": Prompt.objects.all().order_by("-created_at"),
                "form": InputForm(),
            },
        )

    def post(self, request):
        form = InputForm(request.POST)
        if form.is_valid():
            app_name = camelcase2snakecase(form.cleaned_data["app_name"])
            root_folder = form.cleaned_data.get(
                "root_folder",
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            )
            content = request.POST.get("editor_content", "")
            content = unquote(content)  # Decode the content
            parsed_data = parse_chat(content, app_name, root_folder)
            return JsonResponse(parsed_data, safe=False)
        return JsonResponse({"error": f"Invalid form data: {form.errors}"}, status=400)


class WriteChangesView(View):
    def post(self, request):
        app_name = camelcase2snakecase(request.POST.get("app_name", ""))
        if not app_name:
            return JsonResponse({"status": f"Missing app-name"})

        root_folder = request.POST.get(
            "root_folder", os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        selected_code_blocks = request.POST.getlist("code_blocks")
        content = request.POST.get("editor_content", "")
        content = request.POST.get("editor_content", "")
        content = unquote(content)  # Decode the content
        parsed_data = parse_chat(content, app_name, root_folder)

        for file_path, file_content in parsed_data.items():
            if not any([f in file_path for f in selected_code_blocks]):
                continue

            file_path = file_path.replace("\\", os.sep).replace("/", os.sep)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            if os.path.exists(file_path):
                shutil.move(file_path, file_path + f"_{int(time.time())}.bak")

            with open(file_path, "w", encoding="utf-8") as file:
                file.write(file_content)

        return JsonResponse(
            {
                "status": f"Selected elements written successfully to {os.path.join(root_folder, app_name)}"
            }
        )


def save_prompt(request):
    if request.method == "POST":
        form = PromptForm(request.POST)
        if form.is_valid():
            prompt = form.save()
            return JsonResponse(
                {
                    "id": prompt.id,
                    "name": prompt.name,
                    "prompt": prompt.prompt,
                }
            )
    return JsonResponse({"error": "Invalid form"}, status=400)


def delete_prompt(request):
    if request.method == "POST":
        pk = request.POST.get("id")
        prompt = Prompt.objects.get(pk=pk)
        prompt.delete()
        return JsonResponse({"status": "deleted"})
    return JsonResponse({"error": "Invalid request"}, status=400)
