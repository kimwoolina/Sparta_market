from django import forms
from .models import Product, Comment, Tag


class ProductForm(forms.ModelForm):
    tags = forms.CharField(required=False, help_text="해시태그를 입력하고 #로 구분하세요.")

    class Meta:
        model = Product
        fields = "__all__"
        exclude = ("author", "like_users", "view_cnt")

    def __init__(self, *args, **kwargs):
        # 기존의 태그를 표시하기 위해 인스턴스를 전달받아 초기화합니다.
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            tags = self.instance.tags.values_list('name', flat=True)
            self.initial['tags'] = '#'.join(tags)

    def clean_tags(self):
        tags = self.cleaned_data.get('tags', '')
        tag_names = [tag.strip() for tag in tags.split('#') if tag.strip()]
        unique_tags = set(tag_names)

        if len(unique_tags) != len(tag_names):
            raise forms.ValidationError("중복된 해시태그가 포함되어 있습니다.")
        
        # Check if the tags are already in the database
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
