from django.dispatch import receiver
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from app.models import Question, Answer, Tag, Profile
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from app.forms import LoginForm, SignUpForm, QuestionForm, SettingsForm, AnswerForm, AvatarForm
from django.db.models.signals import post_save


TAGS = Tag.objects.get_popular()

def index(request):
    questions = Question.objects.new_questions()
    page = paginate(questions, request, per_page=5)
    return render(request, 'index.html',
                  context={'questions': page.object_list, 'page_obj': page, 'tags': TAGS})


def hot(request):
    hot_questions = Question.objects.hot_questions()
    page = paginate(hot_questions, request, per_page=5)
    return render(request, 'hot.html',
                context={'questions': page.object_list, 'page_obj': page, 'tags': TAGS})


def question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    user_profile = None
    if request.user.is_authenticated:
        user_profile = get_object_or_404(Profile, user=request.user)

    answers = Answer.objects.get_answer(question)
    form = AnswerForm(request.POST or None)
    page = paginate(answers, request, per_page=3)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            form.add_error('text', 'Please log in in order to submit answers.')
        elif form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.user = user_profile
            answer.save()
            return redirect(
                reverse('one_question', kwargs={'question_id': question.id}) + f'?page={page.paginator.num_pages}')

    return render(request, 'one_question.html',
                  context={'question': question, 'page_obj': page,
                           "answers": answers, 'tags': TAGS, 'form': form})

def login(request):
    form = LoginForm
    continue_url = request.GET.get('continue')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user:
                auth.login(request, user)
                if continue_url:
                    return redirect(continue_url)
                return redirect('index')
    return render(request, "login.html", {'tags': TAGS, 'form': form})


def logout(request):
    auth.logout(request)
    continue_url = request.POST.get('continue')
    if continue_url:
        return redirect(continue_url)
    return redirect('index')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)


def registration(request):
    form = SignUpForm
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            return redirect(reverse('index'))

    return render(request, "registration.html", {'tags': TAGS, 'form': form})


def settings(request):
    success_message = None
    if request.method == 'POST':
        user_form = SettingsForm(request.POST, instance=request.user, request_user=request.user)
        avatar_form = AvatarForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and avatar_form.is_valid():
            user_form.save()
            avatar_form.save()
            success_message = "Your account details have been successfully updated!"
            return render(request, 'settings.html', {'tags': TAGS,
                'user_form': user_form,
                'avatar_form': avatar_form,
                'user_profile': request.user.profile,
                'success_message': success_message
            })
    else:
        user_form = SettingsForm(instance=request.user, request_user=request.user)
        avatar_form = AvatarForm(instance=request.user.profile)
    return render(request, 'settings.html', {'user_form': user_form,
                                            'avatar_form': avatar_form,
                                             'user_profile': request.user.profile,
                                             'success_message': success_message, 'tags': TAGS})


@login_required
def ask(request):
    if not request.user.is_authenticated:
        continue_url = request.POST.get('continue', reverse('ask'))
        request.session['continue_url'] = continue_url
        return redirect(reverse('login'))
    else:
        user = request.user
        user_profile = get_object_or_404(Profile, user=user)
        form = QuestionForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                question = form.save(get_object_or_404(Profile, user=request.user))
                return redirect('one_question', question_id=question.id)
            else:
                return render(request, 'ask.html', {'form': form, 'user_profile': user_profile, 'tags': TAGS})
        return render(request, 'ask.html', {'form': form, 'user_profile': user_profile, 'tags': TAGS})


def tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    tag_questions = Question.objects.get_by_tag(tag)
    page = paginate(tag_questions, request, per_page=5)
    return render(request, 'tag.html', {'questions': page.object_list, 'page_obj': page,
                            'tag_name': tag.name, 'tags': TAGS})

def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, 5)
    page_num = request.GET.get('page', 1)
    try:
        page = paginator.page(page_num)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page