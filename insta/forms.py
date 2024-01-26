from django import forms
from .models import Profile,Post

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo', 'gender', 'bio'] 
        
