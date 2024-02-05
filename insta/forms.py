from django import forms
from .models import Profile, Message

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo', 'gender', 'bio'] 
        
        
class MessageForm(forms.ModelForm): 
    class Meta:      
        model = Message
        fields = [ 'message']
    
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['message'].widget.attrs.update({'class': 'form-control  rounded-pill','aria-label':'Message','id':"messageInput",'style':"height:45px;" ,'placeholder':"Message......"})
