
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile1 , Post , Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm 





class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Write your comment here...', 'style': 'width: 300px; margin: 0;'})
    )
    class Meta:
        model = Comment
        fields = ['content']  





class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Ваше имя', 'style': 'width: 300px; margin: 0;'})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Фамилия', 'style': 'width: 300px; margin: 0;'})
    )
    avatar = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'custom-file-input'})
    )
    phone_number = forms.CharField(
        max_length=17,
        validators=[UserProfile1.phone_regex],
        widget=forms.TextInput(attrs={'placeholder': 'Номер телефона', 'style': 'width: 300px; margin: 0;'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Введите вашу почту', 'style': 'width: 300px; margin: 0;'})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Выберите имя пользователя', 'style': 'width: 300px; margin: 0;'})
    )
    password1 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Введите новый пароль', 'style': 'width: 300px; margin: 0;'})
    )
    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Повторите новый пароль', 'style': 'width: 300px; margin: 0;'})
    )

    class Meta:
        model = UserProfile1
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'avatar']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['email'].disabled = True

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 or password2:
            if password1 != password2:
                raise forms.ValidationError("Пароли не совпадают.")
        return cleaned_data

class Register(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Ваше имя', 'style': 'width: 300px; margin: 0;'})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Фамилия', 'style': 'width: 300px; margin: 0;'})
    )
    avatar = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'custom-file-input'})
    )
    phone_number = forms.CharField(
        max_length=17,
        validators=[UserProfile1.phone_regex],
        widget=forms.TextInput(attrs={'placeholder': 'Номер телефона', 'style': 'width: 300px; margin: 0;'})
    )

    class Meta:
        model = UserProfile1
        fields = ['first_name', 'last_name', 'avatar', 'phone_number']

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        return phone_number

class CodeForm(forms.Form):
    key = forms.IntegerField(
        label='Код подтверждения',
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите код',
            'style': 'width: 300px; margin: 0;',
            'required': 'required',
        })
    )

class FormReg(UserCreationForm):
    email = forms.EmailField(       
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email','style' :'width: 300px ;margin: 0;'})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Choose a username','style' : 'width: 300px ; margin: 0;'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter a strong password','style' : 'width: 300px ; margin: 0;'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Repeat your password','style' : 'width: 300px ; margin: 0;'})
    )

    class Meta:
        model = UserProfile1
        fields = ['username', 'email', 'password1', 'password2']
    def __init__(self, *args, **kwargs):
        super(FormReg, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''



# class FormLogin(AuthenticationForm):
#     username = forms.CharField(
#         label = '',
#         widget=forms.TextInput(attrs={'placeholder': 'Username',
#                                       'style' : 'width: 300px ; margin: 0;'})
#     )
#     password = forms.CharField(
#         label = '',
#         widget=forms.PasswordInput(attrs={'placeholder': 'Password',
#                                       'style' : 'width: 300px ; margin: 0;'})
#     )

class FormLogin(AuthenticationForm):
    username = forms.CharField(label='', max_length=30)
    password = forms.CharField(label='', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "password")

    def __init__(self, *args, **kwargs):
        super(FormLogin, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Имя пользователя' , 'id': 'id_login_username' })
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Пароль' , 'id': 'id_login_password'})

class UserForm(AuthenticationForm):
    class Meta:
        model = User
        fields =  ['username', 'password' ]


class CreatePostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ['title','image', 'content']

    def __init__(self, *args, **kwargs):
        super(CreatePostForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['placeholder'] = 'Введите заголовок поста'
        self.fields['image'].widget.attrs['placeholder'] = 'Выберите изображение (необязательно)'
        self.fields['content'].widget.attrs['placeholder'] = 'Введите содержание поста'
