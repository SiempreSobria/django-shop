from django import forms

class OrderCreateForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=100)
    phone = forms.CharField(label='Телефон', max_length=20)
    address = forms.CharField(label='Адрес', max_length=255)
    comment = forms.CharField(label='Комментарий', widget=forms.Textarea, required=False)
