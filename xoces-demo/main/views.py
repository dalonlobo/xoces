from django.shortcuts import render, render_to_response
import json

def index(request):
    book = request.GET.get('book', 'murphy')
    context = {}
    DATA_PATH = "/home/dalonlobo/xoces-demo/xoces-demo/main/static/data/"
    mapped_file_name = book + "_mapped.json"
    with open(DATA_PATH + mapped_file_name, "r") as f:
        data = json.load(f)
    context["data"] = json.dumps(data)
    return render_to_response("main/index.html", context)