from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views.generic import ListView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import UserProfile
from .forms import UserProfileForm, CommentForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect


# Define the home view function
class Home(LoginView):
    # Send a simple HTML response
    template_name = 'home.html'

# Create your views here.

@login_required
def profile_detail(request, user_id):
    user = User.objects.get(id=user_id)
    profile, created = UserProfile.objects.get_or_create(user=user)
    posts = Post.objects.filter(user=profile.user)
    return render(request, 'profile/detail.html', {
        'profile': profile,
        'posts': posts
    })

@login_required
def profile_edit(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_detail', user_id=request.user.id)
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'profile/edit.html', {'form': form})

@login_required
def user_feed(request):
    posts = Post.objects.filter(user=request.user)
    return render(request, 'main_app/user_feed.html', {'posts': posts})


def post_detail(request, post_id):  
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all().order_by('created_at')
    form = CommentForm()  # ✅ ensures `form` always exists

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = post
            new_comment.save()
            messages.success(request, "Your comment was posted.")
            return redirect('post_detail', post_id=post.id)

    return render(request, 'main_app/post_detail.html', {
        'post': post,
        'form': form,
        'comments': comments
    })


    

class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'body', 'tags']
    # success_url = '/user_feed/'
    def form_valid(self, form):
        form.instance.user = self.request.user  
        return super().form_valid(form)


def signup(request):
    error_message=''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
        # Auto creating a blank user profile here to make sure every user has one
            UserProfile.objects.create(user=user)
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)

class PostUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'body', 'tags']
    template_name = 'main_app/post_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.user  

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)
    
class PostDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post 
    success_url = '/'
    template_name = 'main_app/post_confirm_delete.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.user

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)

class GlobalFeedView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'main_app/global_feed.html'
    context_object_name = 'posts'
    ordering = ['-created_at'] 