from django.shortcuts import render,redirect, get_object_or_404, redirect
from .models import Post, Comment
from .models import Contact
from django.contrib.auth.forms import UserCreationForm


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
        if form.is_valid():
            form.save()
            return redirect("login")
    
    else:
        form = UserCreationForm()
    return render(request, "signup.html", {"form": form})