from django.shortcuts import render, redirect
from .forms import CreatePoll
from .models import Poll
from django.http import HttpResponse


def home(req):
    polls = Poll.objects.all()
    context = {'polls': polls}
    return render(req, 'core/home.html', context)


def create(request):
    if request.method == 'POST':
        form = CreatePoll(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CreatePoll()
    context = {'form': form}
    return render(request, 'core/create.html', context)


def vote(req, poll_id):
    poll = Poll.objects.get(id=poll_id)
    if req.method == 'POST':
        selected = req.POST['poll']
        if selected == 'option1':
            poll.option_one_count += 1
        elif selected == 'option2':
            poll.option_two_count += 1
        elif selected == 'option3':
            poll.option_three_count += 1
        else:
            return HttpResponse(400, 'Invalid Form')
        poll.save()
        return redirect('results', poll_id)
    context = {'poll': poll}
    return render(req, 'core/vote.html', context)


def results(req, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    context = {'poll': poll}
    return render(req, 'core/results.html', context)
