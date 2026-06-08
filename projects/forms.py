from django.forms import ModelForm,widgets
from django import forms
from .models import Project,Review ##Helps in importing models
## for creating forms 

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'featured_image', 'description', 'demo_link', 'source_link']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    # 1. Properly align __init__ directly under the main class
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        
        # 2. Loop through every field to inject the CSS classes dynamically
        for name, field in self.fields.items():
                field.widget.attrs.update({'class': 'input'})



class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']

        labels = {
            'value': 'Place your vote',
            'body': 'Add a comment with your vote'
        }
          
    # SHIFT LEFT: This def must align directly with 'class Meta:'
    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        
        # Shifted left accordingly to match the new scope
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
     