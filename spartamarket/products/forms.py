from django import forms
from .models import Product, Tag, Comment


class ProductForm(forms.ModelForm):
    tags = forms.CharField(required=False, help_text="해시태그를 입력하고 #로 구분하세요.")

    class Meta:
        model = Product
        fields = ['title', 'content', 'price', 'image', 'tags']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            tags = self.instance.tags.values_list('name', flat=True)
            self.initial['tags'] = '#'.join(tags)

    def clean_tags(self):
        tags = self.cleaned_data.get('tags', '')
        tag_names = [tag.strip() for tag in tags.split('#') if tag.strip()]

        # 해시태그 유효성 검사
        for tag_name in tag_names:
            if ' ' in tag_name or any(char in tag_name for char in "#@!$%^&*()"):
                raise forms.ValidationError("해시태그는 띄어쓰기와 특수문자를 포함할 수 없습니다.")

        unique_tags = set(tag_names)
        if len(unique_tags) != len(tag_names):
            raise forms.ValidationError("중복된 해시태그가 포함되어 있습니다.")

        tag_objects = []
        for tag_name in unique_tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            tag_objects.append(tag)

        return tag_objects

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = "__all__"
        exclude = ("product", "user")


# 검색 폼
class SearchForm(forms.Form):
    query = forms.CharField(label='검색어', max_length=100, required=False)       