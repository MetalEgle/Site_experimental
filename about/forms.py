from django import forms

class NameForm(forms.Form):
    name = forms.CharField(min_length=3, max_length=50)
    category = forms.CharField(min_length=1)
    price = forms.IntegerField(min_value=1)

    
    # email = forms.EmailField()
    # def clean_username(self):
    #     name = self.cleaned_data["username"]

        # if any(char.isdigit() for char in username):
        #     raise forms.ValidationError("Имя не должно содержать цифр")
        # if  username[0].islower():
        #     raise forms.ValidationError("Должно начинаться с большой буквы")
        # return username
class SearchForm(forms.Form):
    name = forms.CharField( max_length=50, required=False)