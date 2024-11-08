from datetime import timezone
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from .forms import UserRegistrationForm
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Borrowing
from .forms import DepositForm
from .models import UserProfile
from books_app.models import Book
from django.utils import timezone





def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)  
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user, balance=0.0)
            login(request, user)  
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'users_app/register.html', {'form': form})




def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  
    else:
        form = AuthenticationForm()
    return render(request, 'users_app/login.html', {'form': form})





@login_required
def profile(request):
    profile = request.user.profile  
    borrowing_history = Borrowing.objects.filter(user=request.user)

    return render(request, 'users_app/profile.html', {
        'profile': profile,
        'borrowing_history': borrowing_history,
    })






from django.core.mail import send_mail
from django.conf import settings

def send_deposit_email(user, amount):
    subject = 'Deposit Successful'
    message = f'Hello {user.username},\n\nYour deposit of {amount} Taka has been successfully processed.\n\nThank you for using our service!'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)



@login_required
def deposit(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            profile.balance += amount  
            profile.save()

        
            send_deposit_email(request.user, amount)
            messages.success(request, f'{amount} has been added to your balance.')
            return redirect('profile')
    else:
        form = DepositForm()
    
    return render(request, 'users_app/deposit.html', {'form': form})





@login_required
def borrow_book(request, book_id):
    book = Book.objects.get(id=book_id)  
    user_profile = request.user.profile  

    
    if user_profile.balance >= book.borrowing_price:
       
        user_profile.balance -= book.borrowing_price
        user_profile.save()

        borrowing = Borrowing.objects.create(
            user=request.user,
            book=book,
            borrowing_price=book.borrowing_price
        )

        messages.success(request, f'You have borrowed "{book.title}".')
        return redirect('profile')  
    else:
        
        context = {'message': 'You do not have enough balance to borrow this book.'}
        return render(request, './users_app/error.html', context)










def return_book(request, borrowing_id):
   
    try:
        borrowing = Borrowing.objects.get(id=borrowing_id)
    except Borrowing.DoesNotExist:
        messages.error(request, "Borrowing record not found.")
        return redirect('profile')

    if borrowing.user == request.user:
        profile = request.user.profile
        profile.balance += borrowing.borrowing_price
        profile.save()

        borrowing.returned = True
        borrowing.return_date = timezone.now()  
        borrowing.save()

        messages.success(request, "Book returned successfully!")
        return redirect('profile')
    else:
       
        messages.error(request, 'You cannot return this book.')
        return redirect('profile')





def user_logout(request):
    logout(request)
    return redirect('home')