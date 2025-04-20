from django import forms
from . import models
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from crispy_forms.layout import Div


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

            # Added so that submit button is right aligned
            Div(
                Submit('submit', 'Submit', css_class="btn btn-primary"),
                css_class="d-flex justify-content-end"
            )
        )


class UpdateTicket(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ['status']
        labels = {
            'status': 'Status:',
        }
        widgets = {
            'status': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "mt-5"
        self.helper.layout = Layout(
            'status',
        )


class TenantUpdateTicket(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ['category', 'description', 'image']
        labels = {
            'category': 'Category',
            'description': 'Description',
            'image': 'Upload Image (optional)',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "mt-5"
        self.helper.layout = Layout(
            'category',
            'description',
            'image'
        )

class CreateComment(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['content']
        labels = {
            'content': 'Please add a description:',
        }
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add your update...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = "mt-5"
        self.helper.layout = Layout(
            'content',
        )