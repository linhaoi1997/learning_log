from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse

from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required


# Create your views here.


def index(request):
    """学习笔记的首页"""
    return render(request, 'learning_logs/index.html')


@login_required
def topics(request):
    """显示所有主题"""
    topics_value = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics_value}
    return render(request, 'learning_logs/topics.html', context)


@login_required
def topic(request, topic_id):
    """显示主题下所有条目"""
    topic_value = Topic.objects.get(id=topic_id)
    # 确认请求的主题属于用户
    check_topic_owner(request, topic_value)

    entries = topic_value.entry_set.order_by('-date_added')
    context = {'topic': topic_value, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request):
    """添加新主题"""
    if request.method != 'POST':
        # 未提交数据，创建一个新表单
        form = TopicForm()
    else:
        # POST提交了数据，对数据进行处理
        form = TopicForm(request.POST)
        if form.is_valid():
            _new_topic = form.save(commit=False)
            _new_topic.owner = request.user
            _new_topic.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """在特定的主题下添加新条目"""
    _topic = Topic.objects.get(id=topic_id)
    check_topic_owner(request, _topic)

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = _topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))

    context = {'topic': _topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """编辑既有条目"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    check_topic_owner(request, topic)

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))

    context = {'topic': topic, 'form': form, 'entry': entry}
    return render(request, 'learning_logs/edit_entry.html', context)

@login_required
def delete_entry(request, entry_id):
    """删除既有条目"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    check_topic_owner(request, topic)
    entry.delete()

    return HttpResponseRedirect(reverse('learning_logs:topic',args=[topic.id]))





#工具函数

def check_topic_owner(request, topic):
    if request.user != topic.owner:
        raise Http404
