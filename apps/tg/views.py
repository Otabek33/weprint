from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .chat import polToWebhook


@csrf_exempt
def webhook(request):
    polToWebhook(request)
    return JsonResponse({"message": "OK"}, status=200)
