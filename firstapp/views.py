# from django.urls import reverse
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Question, Choice


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    print(latest_question_list)
    # output = ','.join([q.question_text for q in latest_question_list])
    context = {
        'latest_question_list':latest_question_list
    }
    return render(request, 'firstapp/index.html',context)

def detail(request, question_id):
    # try:
    #     question = Question.objects.get(id=question_id)
    # except Question.DoesNotExist:
    #     raise Http404('Question does not exist!')
    question = get_object_or_404(Question,pk=question_id)
    return render(request,'firstapp/detail.html',locals())
    # return HttpResponse("You're looking at question {}.".format(question_id))

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'firstapp/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question,pk=question_id)
    try:
        result = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'firstapp/detail.html',{'question':question,
                                                       'error_message': "You didn't select a choice.",})
    else:
        result.votes += 1
        result.save()
    return HttpResponseRedirect(reverse('firstapp:results', args=(question.id,)))


