from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic.base import View

from postagens.forms import AddPostForm
from postagens.models import Post


class AddPostView(View):
    template_post = 'add_post.html'

    def get(self, request):
        return render(request, self.template_post)

    def post(self, request):
        add_postform = AddPostForm(request.POST)
        if add_postform.is_valid():
            print(add_postform.cleaned_data['text'])
            post = Post(content=add_postform.cleaned_data['text'])
            post.profile = request.user.profile
            post.save()
            return redirect('index')

        return render(request, self.template_post, {'form': add_postform})


@login_required
def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    logged_profile = request.user.profile
    logged_profile.delete_post(post)
    return redirect('index')
