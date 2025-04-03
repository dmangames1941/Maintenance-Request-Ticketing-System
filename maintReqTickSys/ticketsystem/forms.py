from django import forms
from . import models
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

# class CreateTicket(forms.ModelForm):
#     class Meta:
#         model = models.Ticket
#         fields = [
#             'title', 'category', 'description', 'image',
#         ]

CATEGORY_CHOICES = [
        ('electrical', 'Electrical'),
        ('plumbing', 'Plumbing'),
        ('general', 'General'),
    ]

class CreateTicket(forms.ModelForm):
   
    class Meta:
        model = models.Ticket
        fields = ['title', 'category', 'description', 'image']
        labels = {
            'title': 'Issue Title',
            'description': 'Describe the Issue',
            'category': 'Issue Type',
            'image': 'Upload a Photo (Optional)'
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Briefly summarize the problem (e.g., "Broken door")'}),
            'description': forms.Textarea(attrs={'placeholder': 'Provide details about the problem.'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "mt-5"
        self.helper.layout = Layout(
            'title',
            'category',
            'description',
            'image',

            Submit('submit', 'Submit')
        )

class UpdateTicket(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ['status']
        labels = {
            'status': 'Ticket Status'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "mt-5"
        self.helper.layout = Layout(
            'status',

            Submit('submit', 'Submit')
        )