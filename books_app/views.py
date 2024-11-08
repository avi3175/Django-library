# books_app/views.py
from django.shortcuts import render,redirect
from .models import Book, Category,Review
from django.contrib import messages
from users_app.models import Borrowing

def book_list(request):
    # Get all books
    books = Book.objects.all()

    # Get all categories to display in the filter
    categories = Category.objects.all()

    # Get selected category from query parameters
    selected_category = request.GET.get('category')

    if selected_category:
        books = books.filter(category__id=selected_category)

    return render(request, 'books_app/book_list.html', {
        'books': books,
        'categories': categories,
        'selected_category': selected_category,
    })


def review_book(request, book_id):
    book = Book.objects.get(id=book_id)  # Get the book
    user_profile = request.user.profile  # Get the user's profile

    # Check if the user has borrowed the book
    borrowed_book = Borrowing.objects.filter(user=request.user, book=book, returned=False).first()

    if not borrowed_book:
        messages.error(request, "You can only review books that you've borrowed.")
        return redirect('book_detail', book_id=book.id)

    if request.method == 'POST':
        review_text = request.POST['content']
        rating = int(request.POST['rating'])

        # Create the review
        review = Review.objects.create(
            user=request.user,
            book=book,
            review_text=review_text,
            rating=rating
        )

        messages.success(request, "Your review has been submitted!")
        return redirect('book_detail', book_id=book.id)

    return render(request, 'users_app/review_book.html', {'book': book})






def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)  # Get the book
    reviews = book.reviews.all()  # Get all reviews for this book
    return render(request, 'books_app/book_detail.html', {'book': book, 'reviews': reviews})
