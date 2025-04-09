from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import StudentUser, Profile

class postInput(forms.Form):
    post_title = forms.CharField(
        max_length = 500,
        widget = forms.Textarea(attrs={"id":"enter_title"}),
        label="Post Title"
    )
    
    post_body = forms.CharField( 
        max_length = 40000,
        widget = forms.Textarea(attrs ={"class":"enter_post"}
            ),
            label = "Body"
    )

class replyInput(forms.Form):
    reply_text = forms.CharField(
        max_length = 10000,
        widget = forms.Textarea(attrs ={"class":"enter_reply"}
            ),
        label = "Enter your reply..."
    )

class signUpForm(UserCreationForm):
    select_year = ["2006","2007","2008","2009","2010","2011","2012","2013","2014"]
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254, required=True)
    birth_date = forms.DateField(
        widget=forms.SelectDateWidget(years=select_year))

    class Meta:
        model = StudentUser
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'birth_date', 'password2')
        help_texts = {
            'username': None
        }

class StudentUserUpdate(forms.ModelForm):
    select_year = ["2006","2007","2008","2009","2010","2011","2012","2013","2014"]
    birth_date = forms.DateField(widget=forms.SelectDateWidget(years=select_year), label = "Birthday")
    class Meta:
        model = StudentUser
        fields = ["username", "first_name", "last_name", "email", "birth_date"]
        help_texts = {
            'username': None
        }


class ProfileForm(forms.ModelForm):
    biography = forms.CharField( 
        max_length = 500,
        widget = forms.Textarea(attrs ={"id":"bio_entry"}
            ),
            label = "Biography (Max 500 words)"
    )

    class Meta:
        model = Profile
        fields = ["biography", "avatar"]
        