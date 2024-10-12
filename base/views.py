from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Student, Book
from django.core.files.storage import FileSystemStorage
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.urls import reverse
from django.contrib import messages
from django.template.loader import render_to_string
from django.db.models import Q  # Make sure to import Q for queries
#from .forms import NoteForm
from .models import Note
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.mail import send_mail

import json

# Create your views here.

@login_required
def home(request):
    search_category = request.GET.get('category', '')
    search_item = request.GET.get('selected_item', '')
    
    # Use Q to filter books based on category and selected item
    if search_category or search_item:
        data = Book.objects.filter(
            Q(category__icontains=search_category) & 
            Q(selected_item__icontains=search_item)
        )
    else:
        data = Book.objects.all()

    context = {
        "data": data, 
        "search_category": search_category, 
        "search_item": search_item
    }
    return render(request, "home.html", context)
@login_required
def logout_view(request):
    logout(request)
    return redirect('basel:ogin')  

def authView(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect("base:login")
    else:
        form = UserCreationForm()
    
    return render(request, "registration/signup.html", {"form": form})

def my_view(request):
    return render(request, 'signup.html')

def view_cart(request):
    return render(request,"view_cart.html")




def insertData(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')

        # Render HTML content from the template
        html_content = render_to_string('emails/email_template.html', {
            'firstname': firstname,
            'lastname': lastname,
        })

        # Create the email with both plain text and HTML versions
        subject = "Thank You for Submitting Your Details"
        sender_email = 'your-email@gmail.com'
        email_message = EmailMultiAlternatives(
            subject=subject,
            body=f"Hi {firstname} {lastname},\n\nThank you for filling out the form.\n\nBest Regards,\nYour Team",
            from_email=sender_email,
            to=[email],
        )
        email_message.attach_alternative(html_content, "text/html")

        try:
            # Send the email
            email_message.send()
            messages.success(request, 'Your details were submitted, and an email receipt has been sent.')
        except Exception as e:
            messages.error(request, 'There was an error sending the email.')

        # Redirect to avoid resubmitting form on page refresh
        return redirect('base:insertData')

    return render(request, 'details.html')
    
#def note(request):
   # if re
    
def details(request):
    return render(request, "details.html")

def btech(request):
    # Fetch all approved BTech books
    
    
   
    return render(request, "btech.html")


def Addbook(request):
    return render(request, "addbook.html")

def insert_book(request):
    if request.method == "POST":
        title = request.POST.get("title")
        author = request.POST.get("author")
        description = request.POST.get("description")
        category = request.POST.get('category')
        selected_item = request.POST.get('selected_item')
        image = request.FILES.get("photo")  
        pdf_file = request.FILES.get("pdfFile")  

        book = Book(
            title=title,
            author=author,
            description=description,
            image=image,
            category=category,
            selected_item=selected_item,
            pdf=pdf_file,
            is_approved=False  # Initially not approved
        )
        book.save() 
        print(f"Book Image URL: {book.image.url}")
        print(f"PDF File URL: {book.pdf.url}")

        # Build approval and rejection links
        approval_link = request.build_absolute_uri(
            reverse('base:approve_book', args=[book.approval_token])
        )
        rejection_link = request.build_absolute_uri(
            reverse('base:reject_book', args=[book.approval_token])
        )

        # Prepare and send email
        subject = f"New Book Submission: {book.title}"
        html_content = render_to_string('emails/approval_email.html', {
            'book': book,
            'approval_link': approval_link,
            'rejection_link': rejection_link,
            'request': request,
        })
        text_content = render_to_string('emails/approval_email.txt', {
            'book': book,
            'approval_link': approval_link,
            'rejection_link': rejection_link,
            'request': request,
        })

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.ADMIN_EMAIL],
        )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)

        return render(request, "addbook.html", {"message": "Book submitted successfully and is pending admin approval!"})
    
    return render(request, "addbook.html")

# Approving and Rejecting Books
def approvebook(request, token):
    book = get_object_or_404(Book, approval_token=token)
    if not book.is_approved:
        book.is_approved = True
        book.save()
        return render(request, "approval_status.html", {"message": "Book has been approved and is now available in the library."})
    else:
        return render(request, "approval_status.html", {"message": "Book is already approved."})


import logging

logger = logging.getLogger(__name__)

def rejectbook(request, token):
    book = get_object_or_404(Book, approval_token=token)
    if not book.is_approved:
        logger.info(f"Rejecting book: {book.title} with token: {token}")
        book.delete()
        return render(request, "approval_status.html", {"message": "Book submission has been rejected and removed."})
    else:
        logger.warning(f"Book {book.title} is already approved and cannot be rejected.")
        return render(request, "approval_status.html", {"message": "Book is already approved and cannot be rejected."})

# Dropdown filter
def dropfilter(request):
    if request.method == "POST":
        searchcategory = request.POST.get("category")
        searchSelectItem = request.POST.get("SelectItem")
        booksearch = Book.objects.filter(category=searchcategory, selected_item=searchSelectItem)  # Fixed filtering
        return render(request, "home.html", {"data": booksearch})

def book_list(request):
    books = Book.objects.all()  # Fetch all book records from the database
    return render(request, 'your_template.html', {'books': books})







from .models import Book, Note

def book_details(request, pk):
    book = get_object_or_404(Book, pk=pk, is_approved=True)
    logger.info(f"Accessing PDF at: {book.pdf.url}")
    
    # Fetch the existing note for the user and book, if any
    existing_note = ''
    if request.user.is_authenticated:
        try:
            note = Note.objects.get(user=request.user, book=book)
            existing_note = note.text
        except Note.DoesNotExist:
            existing_note = ''
    
    context = {
        'book': book,
        'existing_note': existing_note,
    }
    return render(request, 'btech.html', context)


"""

def add_to_cart(request, book_id):
    cart = request.session.get('cart', {})
    cart[book_id] = cart.get(book_id, 0) + 1  # Increment the count if already in cart
    request.session['cart'] = cart
    messages.success(request, 'Book added to cart!')
    return redirect('base:cart') 


def view_cart(request):
    cart = request.session.get('cart', {})
    books = []

    for book_id, quantity in cart.items():
        try:
            book = Book.objects.get(id=book_id)
            books.append(book)
        except Book.DoesNotExist:
            pass  # Optionally handle the case where the book no longer exists

    context = {
        'books': books,
        'cart': cart,
    }

    return render(request, 'cart.html', context)

def remove_from_cart(request, book_id):
    cart = request.session.get('cart', {})
    if book_id in cart:
        del cart[book_id]
        request.session['cart'] = cart
        messages.success(request, 'Book removed from cart!')
    return redirect('base:cart')
    





#note
@login_required
def create_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            # If associating with a user or book, set those fields here
            # note.user = request.user
            # note.book = get_object_or_404(Book, id=book_id)
            note.save()
            return redirect('your_app:note_detail', note_id=note.id)
    else:
        form = NoteForm()
    return render(request, 'your_app/create_note.html', {'form': form})


@csrf_exempt  # Use with caution. Prefer including CSRF tokens in requests.
@login_required
@require_POST
def add_note(request, book_id):
    try:
        data = json.loads(request.body)
        text = data.get('text', '').strip()

        if text == "":
            return JsonResponse({"success": False, "message": "Note content cannot be empty."}, status=400)

        book = get_object_or_404(Book, id=book_id)
        note = Note.objects.create(user=request.user, book=book, text=text)

        return JsonResponse({"success": True, "message": "Note saved successfully."})
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "message": "Invalid JSON."}, status=400)
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)
    
    """

@require_POST
@login_required
def save_note(request, book_id):
    try:
        data = json.loads(request.body)
        note_text = data.get('text', '').strip()
        
        if not note_text:
            return JsonResponse({'error': 'Note text cannot be empty.'}, status=400)
        
        book = get_object_or_404(Book, id=book_id, is_approved=True)
        
        # Get or create the note
        note, created = Note.objects.get_or_create(user=request.user, book=book)
        note.text = note_text  # Overwrite existing text
        note.save()
        
        return JsonResponse({'message': 'Note saved successfully.', 'updated_at': note.updated_at.strftime('%Y-%m-%d %H:%M:%S')})
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    
@login_required
@require_POST
def delete_note(request, book_id):
    try:
        book = get_object_or_404(Book, id=book_id, is_approved=True)
        note = Note.objects.get(user=request.user, book=book)
        note.delete()
        return JsonResponse({'message': 'Note cleared successfully.'})
    except Note.DoesNotExist:
        return JsonResponse({'error': 'No existing note to delete.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

from django.core.mail import EmailMessage

def send_receipt_email(user_email):
    subject = 'Your Receipt from E.Book Community'
    message = 'Thank you for uploading your book details. Here is your receipt...'
    from_email = 'admin@example.com'  # Replace with your actual admin email
    recipient_list = [user_email]

    email = EmailMessage(
        subject,
        message,
        from_email,  # This is the actual admin email
        recipient_list
    )
    
    # Set the name that will show in the "From" field
    email.extra_headers = {'Reply-To': 'E.Book Community <no-reply@example.com>'}  # Modify as needed

    email.send()
