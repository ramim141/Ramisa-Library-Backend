from django.urls import reverse_lazy
from django.views.generic import FormView,ListView
from .models import UserAccount
from .forms import UserRegistrationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from books.models import Book
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class UserRegistrationView(FormView):
    template_name='accounts/signup_login.html'
    model=UserAccount
    form_class=UserRegistrationForm
    success_url=reverse_lazy('profile')

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['type']='SignUp'
        return context

    def form_valid(self,form):
        user=form.save()
        login(self.request,user)
        messages.success(self.request,'You Have Signed up Successfully')
        return super().form_valid(form)

class UserLoginView(LoginView):
    template_name="accounts/signup_login.html"

    def form_valid(self,form):
        messages.success(self.request,'You Have Logged In Successfully')
        return super().form_valid(form)
    
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['type']='Login'
        return context

    def get_success_url(self):
        return reverse_lazy('home')



class UserLogoutView(LogoutView):
    template_name = 'index.html'

    def dispatch(self, request, *args, **kwargs):
        messages.success(self.request, 'You Have Logged Out Successfully')
        return super().dispatch(request, *args, **kwargs)

class UserProfileView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'accounts/user_profile.html'
    context_object_name = 'data'

    def get_queryset(self):
        return Book.objects.filter(borrower=self.request.user)