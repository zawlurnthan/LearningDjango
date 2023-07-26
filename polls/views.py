from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Choice, Question


# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list }
#     return render(request, 'polls/base_site.html', context)
#
#
# def detail(request, question_id):
#     # below method will raise 404 if object doesn't exist
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})
#
#
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        # return the last five published questions (not including those set to be published in the future).
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    # view need to know what model is going to use and expect the primary key value is captured from url.
    # context variable as question is provided to the template automatically by Django Generic view class.
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        :return:
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # redisplay the question voting form
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice."
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # redirect after successfully vote, to avoid voiding twice
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))

