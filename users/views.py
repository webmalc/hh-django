from django.views.generic import TemplateView, UpdateView, RedirectView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from users.forms import PartnershipOrderForm, OrganizationForm
from users.models import Organization, PartnershipOrder


class PartnershipOrderCreate(TemplateView):
    """
    PartnershipOrder add view
    """
    template_name = 'users/add_partner.html'
    success_url = reverse_lazy('users:partner_add')

    def get_context_data(self, **kwargs):
        context = super(PartnershipOrderCreate, self).get_context_data(**kwargs)
        user = self.request.user
        context['not_completed_orders_count'] = PartnershipOrder.objects.filter(
                created_by=user, status__in=('new', 'in_work')
        ).count()
        order_form_initial = {'first_name': user.first_name, 'last_name': user.last_name}

        if user.get_profile():
            order_form_initial.update({
                'patronymic': user.profile.patronymic,
                'phone': user.profile.phone,
                'type': user.profile.type,
                'city': user.profile.city,
                'experience': user.profile.experience,
            })

        context['order_form'] = PartnershipOrderForm(
                prefix='order_form',
                initial=order_form_initial,

                data=self.request.POST if self.request.POST else None)
        context['organization_form'] = OrganizationForm(
                instance=user.profile.organization if user.get_profile() else None,
                prefix='organization_form',
                data=self.request.POST if self.request.POST else None
        )
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        # Get organization from request
        if context['organization_form'].is_valid():
            new_organization = context['organization_form'].save(commit=False)
            organizations = Organization.objects.filter(name=new_organization.name, type=new_organization.type)

            if not organizations:
                new_organization.save()
                organization = new_organization
            else:
                organization = organizations[0]

        else:
            organization = None

        # Save order
        if context['order_form'].is_valid():
            order = context['order_form'].save(commit=False)
            order.organization = organization
            order.save()
            messages.success(
                    request,
                    'Заявка #{} успешно создана. Наши менеджеры свяжутся с Вами в ближайшее время'.format(
                            order.pk)
            )
            return redirect(self.success_url)
        else:
            messages.error(request, 'Во время создания заяки произошли ошибки, исправьте их и попробуйте снова')

        return self.render_to_response(context)


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
