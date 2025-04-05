from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect, render
from .models import Item, Comment
from .forms import ItemForm, CommentForm

class ItemListView(ListView):
    model = Item
    template_name = "item_list.html"
    context_object_name = "items"

class ItemDetailView(DetailView):
    model = Item
    template_name = "item_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = self.object.comments.all()
        context["form"] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.item = self.object
            comment.save()
            return redirect("item_detail", pk=self.object.pk)
        return self.get(request, *args, **kwargs)

class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    form_class = ItemForm
    template_name = "item_form.html"
    success_url = reverse_lazy("item_list")

class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model = Item
    form_class = ItemForm
    template_name = "item_form.html"
    success_url = reverse_lazy("item_list")

class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model = Item
    template_name = "item_confirm_delete.html"
    success_url = reverse_lazy("item_list")
