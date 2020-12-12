from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from learning_logs.models import Topic, Entry
from django.contrib.auth.models import User
from django.db.utils import DataError

# Create your views here.
from .models import ApiDescribe
from .forms import ApiDescribeForm


def show_all_api(request):
    """显示所有暴露的api"""
    apis = ApiDescribe.objects.all()

    context = {'apis': apis}
    return render(request, 'api/index.html', context)


def new_api(request):
    """添加新接口"""
    if request.method != 'POST':
        # 未提交数据，创建一个新表单
        form = ApiDescribeForm()
    else:
        # POST提交了数据，对数据进行处理
        form = ApiDescribeForm(request.POST)
        if form.is_valid():
            _new_topic = form.save()
            return HttpResponseRedirect(reverse('api:show_all_api'))

    context = {'form': form}
    return render(request, 'api/new_api.html', context)


def edit_api(request, api_id):
    """编辑既有接口"""
    api = ApiDescribe.objects.get(id=api_id)

    if request.method != 'POST':
        form = ApiDescribeForm(instance=api)
    else:
        form = ApiDescribeForm(instance=api, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('api:show_all_api'))

    context = {'api': api, 'form': form}
    return render(request, 'api/edit_api.html', context)


def add_topic(request):
    username = request.POST.get('username', '')
    text = request.POST.get('text', '')

    if username == '' or text == '':
        return JsonResponse({'status': 10021, 'message': 'parameter error'})

    user = User.objects.filter(username=username)
    if not user:
        return JsonResponse({'status': 10020, 'message': 'no such user error'})

    result = Topic.objects.filter(owner_id=user[0].id, text=text)
    if result:
        return JsonResponse({'status': 10022, 'message': 'topic already exists'})

    try:
        Topic.objects.create(owner_id=user[0].id, text=text)
    except DataError as e:
        return JsonResponse({'status': 10023, 'message': 'Data too long for column "text" at row 1'})
    except Exception as e:
        return JsonResponse({'status': 10024, 'message': 'data formatting error'})

    return JsonResponse({'status': 200, 'message': 'add topic success'})


def add_entry(request):
    username = request.POST.get('username', '')
    topic_name = request.POST.get('topic_name', '')
    describe = request.POST.get('describe', '')
    text = request.POST.get('text', '')

    if username == '' or text == '' or topic_name == '' or describe == '':
        return JsonResponse({'status': 10021, 'message': 'parameter error'})

    user = User.objects.filter(username=username)
    if not user:
        return JsonResponse({'status': 10020, 'message': 'no such user error'})

    result = Topic.objects.filter(owner_id=user[0].id, text=topic_name)
    if not result:
        return JsonResponse({'status': 10022, 'message': 'no such topic error'})

    result = Entry.objects.filter(text=text, topic_id=result[0].id, describe=describe)
    if result:
        return JsonResponse({'status': 10024, 'message': 'entry already exists'})

    try:
        Entry.objects.create(topic_id=result[0].id, text=text, describe=describe)
    except DataError as e:
        return JsonResponse({'status': 10023, 'message': 'Data too long for column "text" at row 1'})
    except Exception as e:
        return JsonResponse({'status': 10024, 'message': 'data formatting error'})

    return JsonResponse({'status': 200, 'message': 'add entry success'})


def get_topic_lists(request):
    username = request.GET.get('username', '')

    if username == '':
        return JsonResponse({'status': 10021, 'message': 'parameter error'})

    user = User.objects.filter(username=username)
    if not user:
        return JsonResponse({'status': 10020, 'message': 'no such user error'})

    result = Topic.objects.filter(owner_id=user[0].id)
    if not result:
        return JsonResponse({'status': 10022, 'message': 'query result is empty '})
    else:
        data = []
        for i in result:
            data.append(i.text)
        return JsonResponse({'status': 200, 'message': 'success', 'data': data})


def get_entry_lists(request):
    username = request.GET.get('username', '')
    topic_name = request.GET.get('topic_name', '')

    if username == '' or topic_name == '':
        return JsonResponse({'status': 10021, 'message': 'parameter error'})

    user = User.objects.filter(username=username)
    if not user:
        return JsonResponse({'status': 10020, 'message': 'no such user error'})

    result = Topic.objects.filter(owner_id=user[0].id, text=topic_name)
    if not result:
        return JsonResponse({'status': 10022, 'message': 'no such topic'})

    result = Entry.objects.filter(topic_id=result[0].id)
    if not result:
        return JsonResponse({'status': 10024, 'message': 'query result is empty'})
    else:
        data = []
        for i in result:
            data.append({'text': i.text, 'describe': i.describe, 'topic_name': topic_name, 'user': username})
        return JsonResponse({'status': 200, 'message': 'success', 'data': data})


def delete_topic(request):
    username = request.GET.get('username', '')
    topic_name = request.GET.get('topic_name', '')

    if username == '' or topic_name == '':
        return JsonResponse({'status': 10021, 'message': 'parameter error'})

    user = User.objects.filter(username=username)
    if not user:
        return JsonResponse({'status': 10020, 'message': 'no such user error'})

    result = Topic.objects.filter(owner_id=user[0].id, text=topic_name)
    if not result:
        return JsonResponse({'status': 10022, 'message': 'no such topic error'})
    else:
        del_num, del_dict = result.delete()
        return JsonResponse({'status': 200, 'message': 'success', 'del_num': del_num, 'del_items': del_dict})


def delete_entry(request):
    username = request.GET.get('username', '')
    topic_name = request.GET.get('topic_name', '')
    describe = request.GET.get('describe', '')

    if username == '' or topic_name == '':
        return JsonResponse({'status': 10021, 'message': 'parameter error'})

    user = User.objects.filter(username=username)
    if not user:
        return JsonResponse({'status': 10020, 'message': 'no such user error'})

    result = Topic.objects.filter(owner_id=user[0].id, text=topic_name)
    if not result:
        return JsonResponse({'status': 10022, 'message': 'no such topic error'})

    result = Entry.objects.filter(topic_id=result[0].id, describe=describe)
    if not result:
        return JsonResponse({'status': 10024, 'message': 'no such entry'})
    else:
        del_num, del_dict = result.delete()
        return JsonResponse({'status': 200, 'message': 'success', 'del_num': del_num, 'del_items': del_dict})

