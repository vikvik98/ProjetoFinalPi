from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import View

from postagens.forms import AddPostForm
from postagens.models import Post
from django.contrib import messages

class AddPostView(View):
    template_post = 'add_post.html'

    def get(self, request):
        form = AddPostForm()
        return render(request, self.template_post, {'form': form})

    def post(self, request):
        add_postform = AddPostForm(request.POST)

        if add_postform.is_valid():
            post = Post(profile=request.user.profile)
            text = add_postform.cleaned_data['text']
            photo = add_postform.cleaned_data['photo']
            if text:
                post.content = text
            if photo:
                post.photo = photo
            post.save()
            messages.success(request, _("Post added successfully."))
            return redirect('index')

        return render(request, self.template_post, {'form': add_postform})

class SharePostView(View):
    template_post = 'add_post.html'

    def get(self, request, post_id):
        form = AddPostForm()
        return render(request, self.template_post, {'form': form})

    def post(self, request, post_id):
        add_postform = AddPostForm(request.POST)
        if post_id:
            shared_post = Post.objects.get(id= post_id)
            if add_postform.is_valid():
                post = Post(profile=request.user.profile)
                text = add_postform.cleaned_data['text']
                photo = add_postform.cleaned_data['photo']
                if text:
                    post.content = text
                if photo:
                    post.photo = photo
                post.shared_post = shared_post
                post.save()
                messages.success(request, _("Post added successfully."))
                return redirect('index')
        else:
            if add_postform.is_valid():
                post = Post(profile=request.user.profile)
                text = add_postform.cleaned_data['text']
                photo = add_postform.cleaned_data['photo']
                if text:
                    post.content = text
                if photo:
                    post.photo = photo
                post.save()
                messages.success(request, _("Post added successfully."))
                return redirect('index')
            return render(request, self.template_post, {'form': add_postform})

        return render(request, self.template_post, {'form': add_postform})


@login_required
def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if post.profile == request.user.profile or request.user.is_superuser:
        post.delete()
        messages.success(request, _("Successfully deleted post."))
        return redirect('index')
    raise PermissionError(_("You don't have permission to this operation."))

