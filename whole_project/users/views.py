from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, reverse

from django.views.generic.edit import FormView
from django.views import View, generic

from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib import messages

from django.urls import reverse_lazy

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.db.models import Q

from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, DeleteAccountForm
from .models import Profile, Subscribers

from blog.models import Blog, Tag, Categories

User = get_user_model()


# ----- Register and login views -----
class UsersLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid login or password')
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse_lazy('home')


class UsersRegisterView(FormView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.save()
        if user:
            Profile.objects.get_or_create(user=user)
            login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('home')


class UsersLogoutView(LogoutView):
    def get_success_url(self):
        return reverse_lazy('home')


# ----- End register and login views----

# Settings user profile view
class UsersProfileSettingsView(LoginRequiredMixin, View):
    def get(self, request):
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

        context = {
            'user_form': user_form,
            'profile_form': profile_form,
        }

        return render(request, 'users/profile_settings.html', context=context)

    def post(self, request):
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.profile.email_verified = False
            user.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated')
            return redirect('profile-settings')
        else:
            context = {
                'user_form': user_form,
                'profile_form': profile_form,
            }
            messages.error(request, 'Error updating your profile')

            return render(request, 'users/profile_settings.html', context=context)


# ----- End settings user profile view -----

# ----- Verify email views -----
class SendVerificationEmailView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        if not user.profile.email_verified:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            verification_url = reverse('verify_email', kwargs={'uidb64': uid, 'token': token})
            email_subject = 'Please verify your email'
            email_body = render_to_string('users/verify_email.html',
                                          {'verification_url': verification_url, 'domain': request.get_host(),
                                           'protocol': 'http' if not request.is_secure() else 'https'})
            email = EmailMessage(email_subject, email_body, to=[user.email])
            email.send()
        return redirect('confirm_wait')


class VerifyEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.profile.email_verified = True
            user.profile.save()
            login(request, user)
            messages.success(request, 'You successful verify your email')
            return redirect('home')
        else:
            return redirect('login')


# ----- End verify email views -----

# ----- User delete account view -----

class UsersDeleteAccountView(LoginRequiredMixin, View):
    def get(self, request):
        delete_form = DeleteAccountForm()
        context = {
            'form': delete_form,
        }
        return render(request, 'users/delete_account.html', context=context)

    def post(self, request):
        delete_form = DeleteAccountForm(data=request.POST)
        if delete_form.is_valid():
            user = User.objects.get(username=request.user.username)
            if user.id == self.request.user.id:
                password = delete_form.cleaned_data['password']
                if user.check_password(password):
                    user = request.user
                    token = default_token_generator.make_token(user)
                    uid = urlsafe_base64_encode(force_bytes(user.pk))
                    verification_url = reverse('verify_delete_account', kwargs={'uidb64': uid, 'token': token})
                    email_subject = 'Please confirm that you want delete your account'
                    email_body = render_to_string('users/verify_delete_account.html',
                                                  {'verification_url': verification_url,
                                                   'domain': request.get_host(),
                                                   'protocol': 'http' if not request.is_secure() else 'https'})
                    email = EmailMessage(email_subject, email_body, to=[user.email])
                    email.send()
                    return redirect('confirm_wait')

        context = {
            'form': delete_form
        }
        messages.error(request, 'Invalid password')
        return render(request, 'users/delete_account.html', context=context)


class UsersDeleteAccountVerifyView(LoginRequiredMixin, View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(force_str(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            return render(request, 'users/confirm_delete_account.html')

    def post(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(force_str(uidb64))
            user = User.objects.get(pk=uid)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.delete()
            messages.success(request, 'You successful delete your account')
            return redirect('home')


# ----- End user delete account view -----

# ----- User Profile View -----

class AuthorDetailView(generic.DetailView):
    model = User
    template_name = 'users/author.html'
    context_object_name = 'author'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()

        blogs = Blog.objects.filter(author=user).order_by('-id')
        blogs_last = Blog.objects.filter(author=user).order_by('-id')[:3]

        tags = Tag.objects.filter(blog__author=user).distinct()
        category = Categories.objects.filter(blog__author=user).distinct()

        followers = Subscribers.objects.filter(subscribers=user)

        following = Subscribers.objects.filter(user=user)
        context['blogs'] = blogs
        context['blogs_last'] = blogs_last
        context['tags'] = tags
        context['category'] = category

        context['followers'] = followers.count()
        context['following'] = following.count()
        context['user'] = self.request.user

        query = self.request.GET.get('q')
        if query:
            context['blogs'] = Blog.objects.filter(
                Q(title__icontains=query) | Q(author__username__icontains=query))
            context['q'] = query

        try:
            sub = Subscribers.objects.get(user=self.request.user, subscribers=user)
            context['subscribed'] = True
        except ObjectDoesNotExist:
            context['subscribed'] = False

        return context

    def post(self, *args, **kwargs):
        user = self.request.user
        author = self.get_object()

        try:
            sub = Subscribers.objects.get(user=user, subscribers=author)
            sub.delete()
            messages.error(self.request, f'Unsubscribe - {author}')
            return redirect('author-view', pk=author.pk)
        except ObjectDoesNotExist:
            Subscribers.objects.create(user=user, subscribers=author)
            messages.success(self.request, f'Subscribe - {author}')
            return redirect('author-view', pk=author.pk)
    # ----- End User Profile View ----


class UserPasswordResetView(LoginRequiredMixin, PasswordResetView):
    template_name = 'users/password_reset.html'

    def form_valid(self, form):

        if form.cleaned_data['email'] == self.request.user.email:
            response = super().form_valid(form)
            messages.success(self.request, 'Password reset email has been sent.')
            return redirect('password_reset_done')
        else:
            messages.error(self.request, 'Wrong email')
            return redirect('password-reset')

