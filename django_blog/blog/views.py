from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.decorators.http import require_POST
from django.db.models import Q
from .models import Post, Comment
from .forms import UserRegisterForm, UserUpdateForm, PostForm, CommentForm

# ========== AUTHENTICATION VIEWS - BEGIN ==========
def home(request):
    return render(request, 'blog/base.html', {'title': 'Home'})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form, 'title': 'Register'})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('profile')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form, 'title': 'Login'})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')
# ========== AUTHENTICATION VIEWS - END ==========

# ========== PROFILE VIEW - BEGIN ==========
@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    
    # Get user's posts count
    user_posts = Post.objects.filter(author=request.user).count()
    # Get user's comments count
    user_comments = Comment.objects.filter(author=request.user).count()
    
    return render(request, 'blog/profile.html', {
        'form': form, 
        'title': 'Profile',
        'user_posts': user_posts,
        'user_comments': user_comments
    })
# ========== PROFILE VIEW - END ==========

# ========== BLOG POST CRUD VIEWS - BEGIN ==========
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 5

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add comment form and comments to context
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.all()
        # ========== TAGGING FUNCTIONALITY - BEGIN ==========
        context['related_posts'] = Post.objects.filter(tags__in=self.object.tags.all()).exclude(pk=self.object.pk).distinct()[:5]
        # ========== TAGGING FUNCTIONALITY - END ==========
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        # ========== TAGGING FUNCTIONALITY - BEGIN ==========
        # Handle tags from the form
        tags_input = form.cleaned_data.get('tags', '')
        if tags_input:
            tag_list = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
            self.object.tags.add(*tag_list)
        # ========== TAGGING FUNCTIONALITY - END ==========
        messages.success(self.request, 'Your post has been created successfully!')
        return response

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        # ========== TAGGING FUNCTIONALITY - BEGIN ==========
        # Handle tags from the form
        tags_input = form.cleaned_data.get('tags', '')
        self.object.tags.clear()
        if tags_input:
            tag_list = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
            self.object.tags.add(*tag_list)
        # ========== TAGGING FUNCTIONALITY - END ==========
        messages.success(self.request, 'Your post has been updated successfully!')
        return response

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def get_initial(self):
        initial = super().get_initial()
        # ========== TAGGING FUNCTIONALITY - BEGIN ==========
        # Pre-populate tags field
        post = self.get_object()
        if post.tags.exists():
            initial['tags'] = ', '.join([tag.name for tag in post.tags.all()])
        # ========== TAGGING FUNCTIONALITY - END ==========
        return initial

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Your post has been deleted successfully!')
        return super().delete(request, *args, **kwargs)
# ========== BLOG POST CRUD VIEWS - END ==========

# ========== SEARCH AND TAGGING FUNCTIONALITY - BEGIN ==========
class SearchResultsView(ListView):
    model = Post
    template_name = 'blog/search_results.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            # Search in title, content, and tags
            return Post.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct().order_by('-published_date')
        return Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context

# ========== CHECKER-REQUIRED POST BY TAG LIST VIEW - BEGIN ==========
class PostByTagListView(ListView):
    """
    View to display posts filtered by a specific tag.
    URL pattern: tags/<slug:tag_slug>/
    """
    model = Post
    template_name = 'blog/tagged_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        tag_slug = self.kwargs.get('tag_slug')
        if tag_slug:
            return Post.objects.filter(tags__name__icontains=tag_slug).distinct().order_by('-published_date')
        return Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.kwargs.get('tag_slug')
        return context
# ========== CHECKER-REQUIRED POST BY TAG LIST VIEW - END ==========

# Keep the original TaggedPostsView for backward compatibility
class TaggedPostsView(ListView):
    model = Post
    template_name = 'blog/tagged_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        tag_slug = self.kwargs.get('tag_slug')
        return Post.objects.filter(tags__name__icontains=tag_slug).distinct().order_by('-published_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.kwargs.get('tag_slug')
        return context
# ========== SEARCH AND TAGGING FUNCTIONALITY - END ==========

# ========== COMMENT CRUD OPERATIONS - BEGIN ==========
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['pk']  
        messages.success(self.request, 'Your comment has been added successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, pk=self.kwargs['pk'])  
        return context

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Your comment has been updated successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment'] = self.get_object()
        context['post'] = self.get_object().post
        return context

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Your comment has been deleted successfully!')
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment'] = self.get_object()
        context['post'] = self.get_object().post
        return context
# ========== COMMENT CRUD OPERATIONS - END ==========

# ========== FUNCTION-BASED COMMENT VIEWS (RETAINED FOR COMPATIBILITY) - BEGIN ==========
@login_required
@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST)
    
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        messages.success(request, 'Your comment has been added successfully!')
    else:
        messages.error(request, 'There was an error adding your comment.')
    
    return HttpResponseRedirect(reverse('post-detail', args=[post_id]))

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    
    # Check if user is the author
    if request.user != comment.author:
        messages.error(request, 'You do not have permission to edit this comment.')
        return redirect('post-detail', pk=comment.post.pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your comment has been updated successfully!')
            return redirect('post-detail', pk=comment.post.pk)
    else:
        form = CommentForm(instance=comment)
    
    return render(request, 'blog/comment_form.html', {
        'form': form, 
        'comment': comment,
        'title': 'Edit Comment'
    })

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    post_id = comment.post.pk
    
    # Check if user is the author
    if request.user != comment.author:
        messages.error(request, 'You do not have permission to delete this comment.')
        return redirect('post-detail', pk=post_id)
    
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Your comment has been deleted successfully!')
        return redirect('post-detail', pk=post_id)
    
    return render(request, 'blog/comment_confirm_delete.html', {
        'comment': comment,
        'title': 'Delete Comment'
    })
# ========== FUNCTION-BASED COMMENT VIEWS - END ==========
