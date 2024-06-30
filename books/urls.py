from django.urls import path
from .views import BookDetailView
from transactions.views import BorrowBookView, ReturnBookView

urlpatterns = [
    path('details/<int:id>/', BookDetailView.as_view(), name='book_details'),
    path('borrow/<int:id>/', BorrowBookView.as_view(), name='borrow_book'),
    path('return/<int:id>/', ReturnBookView.as_view(), name='return_book'),
]