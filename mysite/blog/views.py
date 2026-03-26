from django.shortcuts import render,redirect, get_object_or_404
from .models import Post, Comment
from .models import Contact
from django.contrib.auth.forms import UserCreationForm 
from django.core.mail import send_mail
from django.contrib.auth import login


def home(request):
    posts = Post.objects.all()
    return render(request, "home.html", {"posts": posts})


def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    comments = Comment.objects.filter(post=post).order_by('-created_at')

    if request.method == "POST":
        name = request.POST.get("name")
        content = request.POST.get("content")

        if name and content:
            Comment.objects.create(
                post=post,
                name=name,
                content=content
            )
            return redirect(f"/post/{id}/")  # 🔥 prevents duplicate submission

    return render(request, "post_detail.html", {
        "post": post,
        "comments": comments
    })


def about(request):
    return render(request, "about.html")


def contact(request):
    success = False

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        if name and email and message:
            Contact.objects.create(
                name=name,
                email=email,
                message=message
            )

            success = True  # ✅ show success message

    return render(request, "contact.html", {"success": success})


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        email = request.POST.get("email")

        if form.is_valid():
            user = form.save(commit=False)  # don't save yet
            user.email = email              # add email
            user.save() 
            
            login(request, user)

            send_mail('Welcome to My Health Blog',
                'Your account was created successfully!',
                'your_email@gmail.com',   # change this
                [email],
                fail_silently=True,
            )
            
            return redirect("home")
    
    else:
        form = UserCreationForm()
    return render(request, "signup.html", {"form": form})

