from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from .models import Post, Like, Tag
from .forms import CommentForm, LikeForm, TagForm

class PostListView(ListView):
    model = Post
    template_name = "post_list.html"
    ordering = ["-updated_at"]

    def get_queryset(self):
        queryset = super().get_queryset()
        tag_slug = self.request.GET.get("tag")  # query string ?tag=slug
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # add likes count and user liked info for each post
        for post in context['object_list']:
            post.likes_count = post.likes.count()
            post.user_liked = post.likes.filter(user=self.request.user).exists() if self.request.user.is_authenticated else False
        # pass current tag (optional: for UI)
        context['current_tag'] = self.request.GET.get("tag", "")
        return context



class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "post_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        context["like_form"] = LikeForm()  
        context["comments"] = self.object.comments.all()
        context["likes_count"] = self.object.likes.count()
        context["user_liked"] = self.object.likes.filter(user=self.request.user).exists()
        context["tags"] = self.object.tags.all()  # ✅ indha line important
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if "comment_submit" in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = self.object
                comment.author = request.user
                comment.save()
                return redirect("post_detail", pk=self.object.pk)

        elif "like_submit" in request.POST:
            like = self.object.likes.filter(user=request.user).first()
            if like:
                like.delete()  # unlike
            else:
                self.object.likes.create(user=request.user)  # like
            return redirect("post_detail", pk=self.object.pk)

        context = self.get_context_data()
        context["form"] = CommentForm()
        return self.render_to_response(context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "post_create.html"
    fields = ("title", "content", "cover_image", "status", "tags")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ("title", "content", "cover_image", "status", "tags")
    template_name = "post_update.html"

    def test_func(self):
        return self.get_object().author == self.request.user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("post_list")
    template_name = "post_delete.html"

    def test_func(self):
        return self.get_object().author == self.request.user
