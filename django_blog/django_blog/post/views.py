from django.shortcuts import render, redirect
from django.views import View

from post.forms import WritePostForm


class WritePostView(View):
    template_name = 'post/write_post.html'

    def get(self, request):
        return render(request, self.template_name, {'form': WritePostForm})

    def post(self, request):
        form = WritePostForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('user_profile')
