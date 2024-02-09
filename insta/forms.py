from django import forms
from .models import Profile, Message

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo', 'gender', 'bio'] 
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['photo'].widget.attrs.update({'class': 'form-control'})
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gender'].widget.attrs.update({'class': 'form-control'})  
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bio'].widget.attrs.update({'class': 'form-control','aria-label':'bio'})
        
        
class MessageForm(forms.ModelForm): 
    class Meta:      
        model = Message
        fields = [ 'message']
    
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['message'].widget.attrs.update({'class': 'form-control  rounded-pill','aria-label':'Message','id':"messageInput",'style':"height:45px;" ,'placeholder':"Message......"})
