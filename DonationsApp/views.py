from django.views import View
from django.shortcuts import render
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from goal.models import GoalModel

class HomeView(View):
    # Define the name of the template to be used
    template_name = 'home.html'

    def get(self, request):
        # Retrieve the latest goal object
        goals = GoalModel.objects.last()
        # Retrieve all paid donations associated with the latest goal object, and order them by the most recent
        donations = goals.donation.filter(paid=True).order_by('-updated_at')
        # Paginate the donations, displaying 2 donations per page
        paginator = Paginator(donations, 10)
        # Get the current page number from the request
        page_number = request.GET.get('page')

        try:
            # Get the page object for the current page number
            page_obj = paginator.get_page(page_number)

        except PageNotAnInteger:
            page_obj = paginator.get_page(1)

        except EmptyPage:
            # If the page number is out of range, return the last page
            page_obj = paginator.get_page(paginator.num_pages)

        if goals:
            # Encode the ID of the latest goal object
            goal_id = urlsafe_base64_encode(force_bytes(goals.id))
            # Calculate the percentage of the goal completed
            percentage = (goals.progress * 100) / goals.goal
        else:
            # If there are no goal objects, set goal_id to None and percentage to 0
            goal_id = None
            percentage = 0

        # Use get_elided_page_range() to get a list of page numbers to display in the template
        page_range = page_obj.paginator.get_elided_page_range(number=page_obj.number, on_each_side=3, on_ends=3)

        # Create a dictionary of variables to be used in the template
        context = {
            'goals': goals,
            'donations': page_obj,
            'percentage': percentage,
            'goal_id': goal_id,
            'page_range': page_range,  # Pass the page range to the template
        }

        # Render the template with the context variables
        return render(request, self.template_name, context)