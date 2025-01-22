from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

from app.models import Profile, Question, Tag, Answer


class LoginForm(forms.Form):
    username = forms.CharField(max_length=32)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)

    def clean(self):
        data = super().clean()
        username = data.get('username')
        password = data.get('password')
        if not User.objects.filter(username=username).exists():
            self.add_error('username', "User doesn't exists.")

        user = authenticate(username=username, password=password)
        if user is None:
            self.add_error('password', "Incorrect password.")

        return data


class SignUpForm(forms.ModelForm):
    username = forms.CharField(max_length=32, min_length=3)
    email = forms.EmailField()
    password = forms.CharField(max_length=32, min_length=8, widget=forms.PasswordInput)
    password_confirm = forms.CharField(max_length=32, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean(self):
        data = super().clean()
        username = data.get('username')
        email = data.get('email')

        if data['password'] != data['password_confirm']:
            self.add_error('password_confirm', "Passwords doesn't match")

        if User.objects.filter(email=email).exists():
            self.add_error('email', 'A user with this email already exists.')
        if User.objects.filter(username=username).exists():
            self.add_error('username', 'A user with this username already exists.')

        return data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user


class QuestionForm(forms.ModelForm):
    title = forms.CharField(max_length=100)
    text = forms.CharField(max_length=1000)
    tags = forms.CharField(required=True, max_length=30)

    class Meta:
        model = Question
        fields = ['title', 'text', 'tags']

    def clean_tags(self):
        tags = super().clean().get('tags', '')
        tag_names = set()

        for tag in tags.split():
            tag = tag.strip().lower()
            if tag:
                if len(tag) >= 30:
                    self.add_error('tags', 'Cannot add tags; Tags must be less than 30 symbols')
                tag_names.add(tag)

        return tag_names

    def save(self, user, commit=True):
        question = super().save(commit=False)

        if commit:
            question.user = user
            question.save()

            for tag_name in self.cleaned_data['tags']:
                tag_obj, created = Tag.objects.get_or_create(name=tag_name)
                question.tags.add(tag_obj)
            question.save()
        return question


class AnswerForm(forms.ModelForm):
    text = forms.CharField(min_length=2, max_length=500)

    class Meta:
        model = Answer
        fields = ['text']


class SettingsForm(forms.ModelForm):
    username = forms.CharField(max_length=32, min_length=3)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop('request_user')
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if (User.objects.filter(username=username).exclude(pk=self.request_user.pk).exists()):
            raise ValidationError("A user with this username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if (User.objects.filter(email=email).exclude(pk=self.request_user.pk).exists()):
            raise ValidationError("A user with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        profile = self.request_user.profile
        profile.avatar = self.cleaned_data.get('avatar', profile.avatar)
        profile.save()

        return user

class AvatarForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']