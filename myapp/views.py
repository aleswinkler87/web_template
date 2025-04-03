from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Item
from .forms import ItemForm


class ItemListView(ListView):
    model = Item
    template_name = "item_list.html"
    context_object_name = "items"

class ItemDetailView(DetailView):
    model = Item
    template_name = "item_detail.html"

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
