from django import forms
from .models import Product, Comment, Tag


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        exclude = ("author","like_users", "view_cnt")

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        tag_ids = [tag.id for tag in tags]
        if len(tag_ids) != len(set(tag_ids)):
            raise forms.ValidationError("중복된 해시태그가 포함되어 있습니다.")
        return tags

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = "__all__"
        exclude = ("product", "user")
