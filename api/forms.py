from django import forms

from .models import ApiDescribe


class ApiDescribeForm(forms.ModelForm):
    class Meta:
        model = ApiDescribe
        fields = ['name', 'describe', 'url', 'method', 'input_para', 'return_value', 'status_code', 'attention']
        labels = {'name': '名称', 'describe': "描述", "url": "URL", "method": "调用方法", "input_para": "传入参数",
                  "return_value": "返回值", "status_code": "状态码", "attention": "说明"}
        widgets = {'name': forms.Textarea(attrs={'rows': 1}),
                   'describe': forms.Textarea(attrs={'rows': 4}),
                   'url': forms.Textarea(attrs={'rows': 1}),
                   'method': forms.Textarea(attrs={'rows': 1}),
                   'input_para': forms.Textarea(attrs={'rows': 6}),
                   'return_value': forms.Textarea(attrs={'rows': 4}),
                   'status_code': forms.Textarea(attrs={'rows': 6}),
                   'attention': forms.Textarea(attrs={'rows': 4}), }
