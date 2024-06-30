from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView,ListView
from .constants import DEPOSIT,BORROW, RETURN
from .models import Transaction
from .forms import DepositForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from books.models import Book
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views import View
# Create your views here.

def send_transaction_mail(user,amount,subject,template):
    mail_subject=subject
    message=render_to_string(template,{
        'user':user,
        'amount':amount,
        })
    send_email=EmailMultiAlternatives(mail_subject,'',to=[user.email])
    send_email.attach_alternative(message,"text/html")
    send_email.send()

class TransactionViewMixin(LoginRequiredMixin,CreateView):
    template_name='transactions/transaction_form.html'
    model=Transaction
    title=''
    # success_url=reverse_lazy('transaction_report')
    success_url=reverse_lazy('profile')

    def get_form_kwargs(self):
        kwargs=super().get_form_kwargs()
        kwargs.update({
            'account':self.request.user.account,
        })
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title':self.title
        })
        return context

class DepositMoneyView(TransactionViewMixin):
    form_class=DepositForm
    title='Deposit'

    def get_initial(self):
        initial={'transaction_type':DEPOSIT}
        return initial
    
    def form_valid(self,form):
        amount=form.cleaned_data.get('amount')
        account=self.request.user.account
        account.balance += amount
        account.save(
            update_fields=['balance']
        )
        messages.success(self.request,f"{amount}$ was deposited to your account successfully")
        send_transaction_mail(self.request.user,amount,"Deposit Message",'transactions/deposit_mail.html')
        return super().form_valid(form)
    



class BorrowBookView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        book = get_object_or_404(Book, id=id)
        borrowing_cost=book.price

        if request.user in book.borrower.all():
            messages.warning(request, "You have already borrowed this book.")
            return HttpResponseRedirect(reverse_lazy('home'))
        if request.user.account.balance < borrowing_cost:
            messages.error(self.request, "Insufficient balance to borrow the book.")
            return HttpResponseRedirect(reverse_lazy('deposit'))

        book.borrower.add(request.user)
        request.user.account.balance -= borrowing_cost
        request.user.account.save(update_fields=['balance'])
        Transaction.objects.create(
            account=request.user.account,
            amount=borrowing_cost,
            balance_after_transaction=request.user.account.balance,
            transaction_type=BORROW,
        )
        messages.success(request, f"You have successfully borrowed the book: {book.title}")
        send_transaction_mail(self.request.user,borrowing_cost,"Book Borrow Message",'transactions/borrow_mail.html')
        return HttpResponseRedirect(reverse_lazy('profile'))



class ReturnBookView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        book = get_object_or_404(Book, id=id)
        borrowing_cost=book.price

        if request.user not in book.borrower.all():
            messages.warning(request, "You have already returned this book.")
            return HttpResponseRedirect(reverse_lazy('home'))

        book.borrower.remove(request.user)
        request.user.account.balance += borrowing_cost
        request.user.account.save(update_fields=['balance'])
        Transaction.objects.create(
            account=request.user.account,
            amount=borrowing_cost,
            balance_after_transaction=request.user.account.balance,
            transaction_type=RETURN,
        )
        messages.success(request, f"You have successfully returned the book: {book.title}")
        send_transaction_mail(self.request.user,borrowing_cost,"Return Borrow Message",'transactions/return_mail.html')
        return HttpResponseRedirect(reverse_lazy('profile'))


class TransactionReportView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'transactions/transaction_report.html'
    context_object_name = 'data'

    def get_queryset(self):
        return Transaction.objects.filter(account=self.request.user.account)