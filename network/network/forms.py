from django import forms

from .models import User,Post


class PostForm(forms.Form):
    new_post = forms.CharField(required=True,max_length="1000",min_length="2")

class CommentForm(forms.Form):
    post_id = forms.DecimalField(required=True)
    comment = forms.CharField(required=True,max_length="1000",min_length="2")
    
    def clean_post_id(self):
        post_id = self.cleaned_data["post_id"]

        post = Post.objects.get(id=post_id)
        if post : 
            return post_id
        else:
            raise forms.ValidationError("Invalid listing")

