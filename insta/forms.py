from django import forms
from .models import Profile, Message

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo', 'gender', 'bio'] 
        
        
class MessageForm(forms.ModelForm): 
    class Meta:      
        model = Message
        fields = ['receiver', 'message']
        
