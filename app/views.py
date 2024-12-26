import copy

from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse

QUESTIONS = [
  {
    'title': 'title '  + str(i+1),
    'id': i,
    'text': 'text' + str(i+1)
  } for i in range(30)
]

ANSWERS = [
  {
    'title': 'answer '  + str(i+1),
    'id': i,
    'text': 'some advice about your problem #' + str(i+1)
  } for i in range(5)
]

TAGS = [
  {
    'name': 'la' * i,
    'id': i
  } for i in range(5)
]

def index(request):
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(QUESTIONS, 5)
    page = paginator.page(page_num)
    return render(request, 'index.html',
                  context={'questions': page.object_list, 'page_obj': page})


def hot(request):
    page_num = int(request.GET.get('page', 1))
    hot_questions = copy.deepcopy(QUESTIONS)
    hot_questions.reverse()
    paginator = Paginator(hot_questions, 5)
    page = paginator.page(page_num)
    return render(request, 'hot.html',
                context={'questions': page.object_list, 'page_obj': page})


def question(request, question_id):
    one_question = QUESTIONS[question_id]
    answer = ANSWERS
    return render(request, 'one_question.html',
                {'item': one_question, 'answers': answer})


def login(request):
    return render(request, "login.html")


def registration(request):
    return render(request, "registration.html")


def settings(request):
    return render(request, "settings.html")


def ask(request):
    return render(request, "ask.html")


def tag(request, tag_name):
    tag = copy.deepcopy(TAGS)
    return render(request, "tag.html", {'tags': tag, 'tag_name': tag_name})


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