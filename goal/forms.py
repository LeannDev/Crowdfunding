from django import forms

from .models import GoalModel

class NewGoalForm(forms.ModelForm):

    class Meta:

        model = GoalModel
        fields = ['title', 'description', 'price', 'goal']
        labels = {
            'title': 'Title',
            'description': 'Description',
            'price': 'Price',
            'goal': 'Goal',
        }