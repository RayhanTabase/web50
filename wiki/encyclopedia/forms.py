from django import forms

class WikiForm(forms.Form):
    title = forms.CharField(label="title", max_length="100", strip="True")
    content = forms.CharField(
                widget=forms.Textarea(
                    attrs={
                            'placeholder':"Enter content in markdown"
                        }
                )  
            )
