from django.shortcuts import render, redirect
from django.views.generic import CreateView

from .forms import NewGoalForm

class GoalCreateView(CreateView):

    template_name = 'new_goal.html'
    form_class = NewGoalForm

    def form_valid(self, form):

        # ********** DELETE IN PRODUCTION **********
        data = {
            'title': form.instance.title,
            'description': form.instance.description,
            'price': form.instance.price,
            'goal': form.instance.goal,
        }
        print(data)
        # ********** ******* ** ********** *********

        form.save()
        return redirect('home')