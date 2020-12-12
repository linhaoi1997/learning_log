from django import forms

from .models import Topic, Entry


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': '你想记录的内容'}


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['describe', 'text']
        labels = {'text': '你想记录的内容', 'describe': "对你想记录的主题写一个大概的描述吧"}
        widgets = {'text': forms.Textarea(attrs={'cols': 80}),
                   'describe': forms.Textarea(attrs={'rows': 2})}
