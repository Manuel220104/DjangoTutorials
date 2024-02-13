from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View
from django.http import HttpResponseRedirect
from django import forms
from django.shortcuts import render, redirect

# Create your views here.

class HomePageView(TemplateView):
    template_name = "pages/home.html"


class AboutPageView(TemplateView):
    template_name = 'pages/about.html'

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "About us - Online Store",
            "subtitle": "About us",
            "description": "This is an about page ...",
            "author": "Developed by: Your Name",
        })

        return context


class Product:
    products = [
        {"id":"1", "name":"TV", "description":"Best TV", "price":99 },
        {"id":"2", "name":"iPhone", "description":"Best iPhone,", "price":180},
        {"id":"3", "name":"Chromecast", "description":"Best Chromecast", "price":75},
        {"id":"4", "name":"Glasses", "description":"Best Glasses", "price":120}
    ]

class ProductIndexView(View):
    template_name = 'products/index.html'

    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] =  "List of products"
        viewData["products"] = Product.products

        return render(request, self.template_name, viewData)

class ProductShowView(View):
    template_name = 'products/show.html'


    def get(self, request, id):
        viewData = {}
        if int(id) <= len(Product.products):
            product = Product.products[int(id)-1]
            viewData["title"] = product["name"] + " - Online Store"
            viewData["subtitle"] =  product["name"] + " - Product information"
            viewData["product"] = product
        else:
            return HttpResponseRedirect('http://127.0.0.1:8000/')

        return render(request, self.template_name, viewData)
    


class ProductForm(forms.Form):
    name = forms.CharField(required=True)
    price = forms.FloatField(required=True)
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError("El precio debe ser mayor a cero.")
        return price

class ProductCreateView(View):
    template_name = 'products/create.html'
    
    def get(self, request):
        form = ProductForm()
        viewData = {}
        viewData["title"] = "Create product"
        viewData["form"] = form
        return render(request, self.template_name, viewData)
    
    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            return redirect("valid")
        else:
            viewData = {}
            viewData["title"] = "Create product"
            viewData["form"] = form
            return render(request, self.template_name, viewData)

class ProductValidView(TemplateView):
    template_name = 'products/valid.html'