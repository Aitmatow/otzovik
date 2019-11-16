
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import  ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView,DeleteView

from webapp.forms import ReviewForm
from webapp.models import Product, Review


class IndexView(ListView):
    model = Product
    template_name = 'index.html'

    def get_queryset(self):
        return Product.objects.all()



class ProductView(DetailView):
    model = Product
    template_name = 'product/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        product = Product.objects.get(pk=self.request.path.split('/')[-2])
        context['form'] = ReviewForm(initial={'author':self.request.user, 'product' : product})
        return context



class ProductCreateView(PermissionRequiredMixin, CreateView):
    model = Product
    template_name = 'product/create.html'
    fields = ('name', 'category', 'description', 'photo')
    permission_required = 'webapp.add_product'
    permission_denied_message = '403 Доступ запрещён!'

    def get_success_url(self):
        return reverse('webapp:product_detail', kwargs={'pk': self.object.pk})


class ProductUpdateView(PermissionRequiredMixin, UpdateView):
    model = Product
    template_name = 'product/update.html'
    fields = ('name', 'category', 'description', 'photo')
    context_object_name = 'product'
    permission_required = 'webapp.change_product'
    permission_denied_message = '403 Доступ запрещён!'

    def get_success_url(self):
        return reverse('webapp:product_detail', kwargs={'pk': self.object.pk})

class ProductDeleteView(PermissionRequiredMixin, DeleteView):
    model = Product
    template_name = 'product/delete.html'
    success_url = reverse_lazy('webapp:index')
    context_object_name = 'product'
    permission_required = 'webapp.delete_product'
    permission_denied_message = '403 Доступ запрещён!'

class ReviewCreateView(LoginRequiredMixin,CreateView):
    model = Review
    template_name = 'review/create.html'
    form_class = ReviewForm

    def get_form(self, form_class=None):
        form = super(ReviewCreateView,self).get_form()
        product = Product.objects.filter(id=self.request.path.split('/')[-1])
        form.fields['author'].queryset = User.objects.filter(username = self.request.user)
        form.fields['product'].queryset = product
        return form

    def form_valid(self, form):
        product = Product.objects.get(id=self.request.path.split('/')[-1])
        Review.objects.create(
            author=form.cleaned_data['author'],
            product=form.cleaned_data['product'],
            text=form.cleaned_data['text'],
            rating=form.cleaned_data['rating']
        )
        return redirect('webapp:product_detail', product.id)

class ReviewUpdateView(LoginRequiredMixin,UpdateView):
    model = Review
    template_name = 'review/update.html'
    form_class = ReviewForm


    def get_form(self, form_class=None):
        form = super(ReviewUpdateView, self).get_form()
        product = Product.objects.filter(id=self.request.path.split('/')[-1])
        form.fields['author'].queryset = User.objects.filter(username=self.request.user)
        form.fields['product'].queryset = product
        return form

    def form_valid(self, form):
        product = Product.objects.get(id=self.request.path.split('/')[-1])
        review = Review.objects.get(id=self.kwargs['pk'])
        review.text = form.cleaned_data['text']
        review.rating = form.cleaned_data['rating']
        review.save()
        return redirect('webapp:product_detail', product.id)

    def get(self, *args, **kwargs):
        if self.request.user == Review.objects.get(pk=self.kwargs['pk']).author or self.request.user.has_perm('webapp.change_review'):
            return super().get(*args, **kwargs)
        raise PermissionDenied()

class ReviewDeleteView(LoginRequiredMixin,DeleteView):
    model = Review
    template_name = 'review/delete.html'
    context_object_name = 'product'

    def get_success_url(self):
        return reverse('webapp:product_detail', kwargs={'pk': self.kwargs['id']})

    def get(self, *args, **kwargs):
        if self.request.user == Review.objects.get(pk=self.kwargs['pk']).author or self.request.user.has_perm('webapp.delete_review'):
            return super().get(*args, **kwargs)
        raise PermissionDenied()