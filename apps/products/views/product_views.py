# from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime, timezone
from typing import Any, Dict

from django.forms.models import BaseModelForm
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from apps.products.forms import ProductCreateForm, ProductUpdateForm
from apps.products.models import Product
from utils.helpers import is_ajax


class ProductListView(ListView):
    model = Product
    paginate_by = 8
    template_name = "products/product_list.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["product_list"] = Product.objects.filter(
            created_by=self.request.user.id
        )
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        product = form.save(commit=False)
        product.created_by = self.request.user
        product.company = self.request.user.company
        product.save()
        return super().form_valid(form)


product_list = ProductListView.as_view()


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductUpdateForm
    template_name = "products/product_update.html"

    def form_valid(self, form):
        product = form.save(commit=False)
        product.updated_by = self.request.user
        product.updated_at = datetime.now()
        product.save()
        return redirect("products:product_list")

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


product_update = ProductUpdateView.as_view()


class ProductDeleteView(DeleteView):
    model = Product

    def get_success_url(self):
        return reverse_lazy("products:product_list")


product_delete = ProductDeleteView.as_view()


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_detail.html"


product_detail = ProductDetailView.as_view()


class ProductAddView(CreateView):
    model = Product
    form_class = ProductCreateForm
    template_name = "products/product_add.html"

    def form_valid(self, form):
        product = form.save(commit=False)
        product.created_by = self.request.user
        product.company = self.request.user.company
        product.created_at = datetime.now()
        product.save()
        return redirect("products:product_list")


product_add = ProductAddView.as_view()
