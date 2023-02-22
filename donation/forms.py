from django import forms

from .models import DonationModel

class DonationForm(forms.ModelForm):

    # pay method select in form
    options = (('MP', 'MercadoPago'), ('PP', 'PayPal'),)
    pay_method = forms.ChoiceField(choices=options, required=True)

    class Meta:

        model = DonationModel
        fields = ['donation', 'name', 'email', 'text', 'pay_method']
        labels = {
            'donation': 'Donation',
            'name': 'Your Name',
            'email': 'Your contact email',
            'text': 'Greetings for user',
            'pay_method': 'payment method',
        }
        widgets = {
            'donation': forms.NumberInput(attrs={
                'value':'1',
                'min':'1',
                'max':'999999999',
                'pattern':'^[1-9]\d*$'
            }),
            'name': forms.TextInput(attrs={
                'placeholder':'Anonymous (optional)',
                'pattern':'^[a-zA-ZÀ-ÿ\s]{0,40}$',
                'maxlength':'40',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder':'anonymous@email.com (optional)',
                'pattern':'^$|^.*@.*\..*$',
                'maxlength':'100',
            }),
            'text': forms.Textarea(attrs={
                'placeholder':'（っ＾▿＾） (optional)',
                'pattern':'^[a-zA-Z0-9\_\-]{0,150}$',
                'maxlength':'150',
                'rows':'5'
            })
        }

    def clean_name(self):
        # get name
        name = self.cleaned_data.get('name')

        if not name:
            name = 'Anonymous'
            
        return name
    
    def clean_text(self):
        # get text
        text = self.cleaned_data.get('text')

        if not text:
            text = '(づ￣ ³￣)づ'

        return text