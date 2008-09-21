# encoding: utf-8

from django import forms
from django.contrib.comments.forms import CommentForm

from nerdcaptcha import NerdCaptcha, make_random_expr_items, check_answer

class NerdCommentForm(CommentForm):
    captcha_answer = forms.IntegerField(label="CAPTCHA")
    captcha_token = forms.CharField(widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super(NerdCommentForm, self).__init__(*args, **kwargs)
        self.captcha = NerdCaptcha(make_random_expr_items(3, 4),
                                   hidden_repr='<i>x</i>')
        if not self.data:
            self.initial['captcha_token'] = self.captcha.token
            
    def clean(self):
        answer = self.cleaned_data['captcha_answer']
        token = self.cleaned_data['captcha_token']
        if not check_answer(str(answer), token):
            raise forms.ValidationError("Bad CAPTCHA answer")
        return self.cleaned_data
