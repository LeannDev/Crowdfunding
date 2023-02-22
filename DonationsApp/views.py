from django.views import View
from django.shortcuts import render
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from goal.models import GoalModel

class HomeView(View):

    template_name = 'home.html'

    def get(self, request):

        goals = GoalModel.objects.last()
        if goals:
            goal_id = urlsafe_base64_encode(force_bytes(goals.id))
            percentage = (goals.progress * 100) / goals.goal
        else:
            goal_id = None
            percentage = 0
            
        context = {
            'goals': goals,
            'donations': goals.donation.filter(paid=True).order_by('-updated_at'),
            'percentage': percentage,
            'goal_id': goal_id,
        }

        return render(request, self.template_name, context)