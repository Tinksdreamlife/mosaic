from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Post
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserProfile
from .forms import UserProfileForm

# Define the home view function
class Home(LoginView):
    # Send a simple HTML response
    template_name = 'home.html'

# Create your views here.

@login_required
def profile_detail(request, user_id):
    profile = UserProfile.objects.get(user__id=user_id)
    posts = Posts.objects.filter(user=profile.user)
    return render(request, 'profile/detail.html', {
        'profile': profile,
        'posts': posts
    })

@login_required
def profile_edit(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if form.is_valid():
        form.save()
        return redirect('profile_detail', user_id=request.user.id)
    else: 
        form = UserProfileForm(instance=profile)
    
    return render(request, 'profile/edit.html', {
        'form': form
    })

@login_required
def user_feed(request):
    posts = Post.objects.filter(user=request.user)
    return render(request, 'posts/user_feed.html', {'posts': posts})

def post_detail(request, post_id):  
    post = Post.objects.get(id=post_id)
    return render(request, 'posts/post_detail.html', {'post': post})
    

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
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)

# @login_required 
