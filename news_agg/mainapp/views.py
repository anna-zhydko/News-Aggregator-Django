from django.http import JsonResponse
from django.shortcuts import render
from mainapp.rss_parser import get_trends
from .tasks import get_trends_task


def index(request):
    task = get_trends_task.delay()
    return render(request, 'mainapp/index.html', {'task_id': task.id})


def get_task_info(request):
    task_id = request.GET.get('task_id', None)
    task_data = get_trends_task.AsyncResult(task_id)

    if task_data.ready():
        print(task_data.result)
        return JsonResponse({'result': task_data.result})
    else:
        print('NOT READYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY')

    return JsonResponse({'result': False})
