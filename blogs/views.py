from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from .models import Post
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class PostListView(ListView):
    model = Post
    template_name = "post_list.html"
    ordering = ["-updated_at"]
class PostDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ("title", "content", "cover_image", "status")
    template_name = "post_update.html"

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("post_list")
    template_name = "post_delete.html"

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "post_create.html"
    fields = ("title", "content", "cover_image", "status")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)