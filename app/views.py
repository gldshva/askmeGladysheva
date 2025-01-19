import copy

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from app.models import Question, Answer, Tag


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
    answers = Answer.objects.get_answer(question)
    page = paginate(answers, request, per_page=3)
    return render(request, 'one_question.html',
                  context={'question': question, 'page_obj': page,
                           "answers": answers, 'tags': TAGS})


def login(request):
    return render(request, "login.html", {'tags': TAGS})


def registration(request):
    return render(request, "registration.html", {'tags': TAGS})


def settings(request):
    return render(request, "settings.html", {'tags': TAGS})


def ask(request):
    return render(request, "ask.html", {'tags': TAGS})


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