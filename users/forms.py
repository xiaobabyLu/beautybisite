from django.contrib.auth.forms import UserCreationForm
from .models import User,BeautyUsers
from django import forms


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model=User
        fields = ('username','email')


class UserListForm(forms.ModelForm):
    # user_id = forms.IntegerField(label='用户id')
    # nickname = forms.CharField(label='用户名',max_length=100)
    username = forms.CharField(label='用户名：',max_length=100)
    # password = forms.CharField(label='密码：',widget=forms.PasswordInput())

    class Meta:
        model = BeautyUsers
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UserListForm, self).__init__(*args, **kwargs)
        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs.update({"class":"form-control"})