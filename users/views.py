from django.views.generic import TemplateView, UpdateView, RedirectView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages


class PasswordChangeRedirectView(RedirectView):
    """
    Password change done redirect
    """
    permanent = False
    url = reverse_lazy('users:profile')

    def get_redirect_url(self, *args, **kwargs):
        messages.success(self.request, 'Пароль успешно сохранен.')

        return super(PasswordChangeRedirectView, self).get_redirect_url(*args, **kwargs)


class Profile(TemplateView):
    """
    Profile view
    """

    template_name = 'users/profile.html'


class UserUpdate(SuccessMessageMixin, UpdateView):
    """
    User update view
    """
    model = User
    fields = ['last_name', 'first_name']
    success_url = reverse_lazy('users:profile')
    success_message = "Профиль успешно сохранен"
    template_name = 'users/profile_edit.html'

    def get_object(self):
        return self.request.user
