from django.urls import reverse_lazy
from django.shortcuts import HttpResponseRedirect
from django.contrib import messages
from django.views.generic import DetailView
from .models import Book
from .forms import ReviewForm


class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_details.html'
    pk_url_kwarg = 'id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object
        reviews = book.reviews.all()
        review_form=ReviewForm()
        context["form"] = review_form
        context["reviews"] = reviews
        return context

    def post(self, request,*args, **kwargs):
        book = self.get_object()
        form = ReviewForm(self.request.POST)

        if form.is_valid():
            user = self.request.user
            if user in book.borrower.all():
                form.instance.user = user
                form.instance.book = book
                form.save()
                messages.success(self.request,"You have successfully submitted the review")
                return HttpResponseRedirect(reverse_lazy('profile'))
        messages.error(request,"In order to review, you have to borrow first")
        return self.get(*args,**kwargs)

