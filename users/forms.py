__author__ = 'eric'
import account.forms
from django import forms
from models import UserProfile, DependantProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms.extras.widgets import SelectDateWidget

class UserProfileForm (forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        return super(UserProfileForm, self).save(*args, **kwargs)

    class Meta:
        model = UserProfile
        exclude = ('user', 'Updated_at','created_at', "height_field", "width_field")


class DependantProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DependantProfileForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        return super(DependantProfileForm, self).save(*args, **kwargs)

    class Meta:
        model = DependantProfile
        exclude = ('user', 'Updated_at','created_at', "height_field", "width_field", "Dependant", "Parent")


class SignupForm(UserCreationForm):
    """User Creation form that uses bootrasp CSS"""
    GENDER_CHOICES = (('m', 'Male'), ('f', 'Female'))
    firstname= forms.CharField(label=("First Name"), max_length=120,
                               widget=forms.TextInput({
                                   'class':'form-control'
                                   }))

    lastname = forms.CharField(label=("Last Name"), max_length=120,
                                widget=forms.TextInput({
                                    'class': 'form-control'
                                }))
    username = forms.CharField(label=("Username"), max_length=120,
                                widget=forms.TextInput({
                                    'class': 'form-control'
                                }))
    password1 = forms.CharField(label=("Password"), max_length=120,
                                widget=forms.PasswordInput({
                                    'class': 'form-control'
                                }))
    password2 = forms.CharField(label=("Password(Again)"), max_length=120,
                                widget=forms.PasswordInput({
                                    'class': 'form-control'
                                }))
    email = forms.CharField(label=("Email Address"), max_length=120,
                                widget=forms.EmailInput({
                                    'class': 'form-control'
                                }))

    # profilepic = forms.ImageField()



    Residence= forms.CharField(label=("Residence"), max_length=120,
                               widget=forms.TextInput({
                                   'class':'form-control'
                                   }))

    email = forms.EmailField(label=("Email Address"), max_length=120,
                               widget=forms.TextInput({
                                   'class':'form-control'}))

    Weight = forms.IntegerField(label=("Weight"),
                                widget=forms.widgets.NumberInput({
                                    'class': 'form-control'}),
                                )



    Height = forms.IntegerField(label=("Height"),
                                widget=forms.widgets.NumberInput({
                                   'class':'form-control'}),
                                )

    Phone_Number = forms.CharField(label=("Phone No."), max_length=12,
                                   widget=forms.NumberInput({
                                       'class': 'form-control'
                                   }))
    National_ID = forms.CharField(label=("National ID No."), max_length=12,
                                  widget=forms.NumberInput({
                                      'class': 'form-control'}))

    Date_of_birth = forms.DateField(widget=SelectDateWidget(years=range(1910, 2016)))

    Gender = forms.ChoiceField(label="Sex",
                               choices=GENDER_CHOICES,
                               widget=forms.Select(),
                               required=True)

    # def __init__(self, custom_choices=None, *args, **kwargs):
    #     sum(SignupForm, self).__init__(*args, **kwargs)
    #     if custom_choices:
    #         self.Gender['fie']

    class Meta:
        model=User
        fields=('firstname', 'lastname', 'username', 'email', 'password1', 'password2')

    def clean_username(self): # check if username dos not exist before
        try:
            User.objects.get(username=self.cleaned_data['username']) #get user from user model
        except User.DoesNotExist :
            return self.cleaned_data['username']

        raise forms.ValidationError("this user exist already")

    def clean(self):
        """
        Verifies that the values entered into the password fields match
        NOTE: Errors wil appear in 'non_field_errors()'' because it applies to more than one field.
        """
        cleaned_data=super(SignupForm, self).clean()
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("Passwords don't match. Please enter both fields again")
            return self.cleaned_data

    def save(self, commit=True):
        user=super(UserCreationForm, self).save(commit=False)
        user.email=self.cleaned_data['email']
        user.username=self.cleaned_data['username']
        user.first_name =self.cleaned_data['firstname']
        user.last_name = self.cleaned_data['lastname']
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

