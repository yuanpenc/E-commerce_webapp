from django.contrib.auth import authenticate
from django import forms
from django.contrib.auth.models import User

from information.models import Profile

MAX_UPLOAD_SIZE = 2500000


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, required=True,
                               label="Username",
                               widget=forms.TextInput(attrs={'class': 'happy', 'placeholder': 'Username'}))
    password = forms.CharField(max_length=200, label="Password",
                               widget=forms.TextInput(attrs={'class': 'happy', 'placeholder': 'Password'}))

    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super().clean()

        # Confirms that the two password fields match
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Invalid username/password")

        # We must return the cleaned data we got from our parent.
        return cleaned_data


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20, label="Username",
                               widget=forms.TextInput(attrs={'class': 'happy', 'placeholder': 'Username'}))
    password = forms.CharField(max_length=200,
                               label='Password',
                               widget=forms.TextInput(attrs={'class': 'happy', 'placeholder': 'Password'}))
    confirm_password = forms.CharField(max_length=200,
                                       label='Confirm password',
                                       widget=forms.TextInput(
                                           attrs={'class': 'happy', 'placeholder': 'Confirm Password'}))
    email = forms.CharField(max_length=50,
                            widget=forms.TextInput(attrs={'class': 'happy', 'placeholder': 'Email'}))

    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super().clean()

        # Confirms that the two password fields match
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords did not match.")

        # We must return the cleaned data we got from our parent.
        return cleaned_data

    # Customizes form validation for the username field.
    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        # We must return the cleaned data we got from the cleaned_data
        # dictionary
        return username


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('picture', 'birthday', 'gender', 'address')

        widgets = {
            'picture': forms.FileInput(attrs={'id': 'id_profile_picture'}),
            'birthday': forms.TextInput(attrs={"type": "date"})
        }

    # def clean_picture(self):
    #     picture = self.cleaned_data['picture']
    #     if not picture:
    #         raise forms.ValidationError('You must upload a picture')
    #     try:
    #         if not picture or not hasattr(picture, 'content_type'):
    #             raise forms.ValidationError('You must upload a picture')
    #         if not picture.content_type or not picture.content_type.startswith('image'):
    #             raise forms.ValidationError('File type is not image')
    #         if picture.size > MAX_UPLOAD_SIZE:
    #             raise forms.ValidationError('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
    #         return picture
    #     except:
    #         raise forms.ValidationError("Please upload an image")
    #
    # def clean_birthday(self):
    #     birthday = self.cleaned_data['birthday']
    #     if not isinstance(birthday, str):
    #         raise forms.ValidationError('You must provide a str')

    def clean_gender(self):
        gender = self.cleaned_data['gender']
        if not isinstance(gender, str):
            raise forms.ValidationError('You must provide a str')

        return gender

    def clean_address(self):
        address = self.cleaned_data['address']
        if not isinstance(address, str):
            raise forms.ValidationError('You must provide a str')

        return address
