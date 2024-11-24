from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from .models import Article


class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = "article_list.html"


class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = "article_detail.html"


class ArticleUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Article
    fields = (
        "title",
        "body",
    )
    template_name = "article_edit.html"

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class ArticleDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Article
    success_url = reverse_lazy("article_list")
    template_name = "article_delete.html"

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    fields = ("title", "body")
    template_name = "article_create.html"
    success_url = reverse_lazy("article_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
