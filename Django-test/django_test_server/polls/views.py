from django.shortcuts import render
from django.http import HttpResponse, Http404
from polls.models import Question
from django.shortcuts import render, get_object_or_404

# Create your views here.

def detail(request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        return render(request,'polls/detail.html', {'question': question})

def results(request, question_id):
    response = "You'r looking result of question %s"
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You'r voting on question %s" % question_id)

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'polls/index.html', context)