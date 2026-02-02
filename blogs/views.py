from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from .models import Post
from django.urls import reverse_lazy

class PostListView(ListView):
    model = Post
    template_name = "post_list.html"
    ordering = ["-updated_at"]
class PostDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"
class PostUpdateView(UpdateView):
    model = Post
    fields = ("title", "content", "cover_image", "status")
    template_name = "post_update.html"
class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy("post_list")
    template_name = "post_delete.html"
class PostCreateView(CreateView):
    model = Post
    template_name = "post_create.html"
    fields = ("title", "content", "cover_image", "status")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)