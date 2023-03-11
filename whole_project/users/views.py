from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


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
    success_url = reverse_lazy('home')
    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.save()
        if user:
            login(self.request, user)
        return super().form_valid(form)


class UsersLogoutView(LogoutView):
    def get_success_url(self):
        return reverse_lazy('home')


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
            user_form.save()
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
