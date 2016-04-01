from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.core.exceptions import ValidationError
from django.forms import model_to_dict
from django.core.urlresolvers import reverse_lazy
from booking.forms import SearchForm, OrderPersonForm
from booking.models import Order, OrderRoom
from hotels.models import Room
from booking.calculation import calc_commission
from booking.tasks import mail_order_hoteliers_task, get_order_email_data


class SearchView(FormView):
    """
    Search form view
    """
    template_name = 'booking/search.html'
    form_class = SearchForm

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context['max_rooms'] = settings.HH_BOOKING_MAX_ORDER_ROOMS
        return context

    def get_initial(self):
        initial = super(SearchView, self).get_initial()
        initial.update(self.request.GET.dict())

        return initial


class SearchResultsView(FormView):
    """
    Search results view
    """
    template_name = 'booking/search_results.html'
    form_class = SearchForm

    def form_valid(self, form):
        data = form.cleaned_data
        user = self.request.user
        rooms = Room.objects.search(**data)[:settings.HH_SEARCH_RESULTS_PER_PAGE]
        duration = (data['end'] - data['begin']).days
        is_partner = self.request.user.is_partner()

        for room in rooms:
            room.total = room.calc_price(data['places'], duration)
            if is_partner:
                room.commission = calc_commission(room, room.total)

        return render_to_response(self.template_name, {
            'rooms': rooms,
            'form': data,
            'duration': duration,
            'order_lifetime': settings.HH_BOOKING_ORDER_LIFETIME,
            'can_booking': Order.objects.user_can_booking(user)
        }, RequestContext(self.request))


class OrderCreateSuccessView(TemplateView):
    """
    Order success message
    """
    template_name = 'booking/order_person_form_success.html'


class OrderCreateView(FormView):
    """
    Order creation form view
    """
    form_class = OrderPersonForm
    template_name = 'booking/order_person_form.html'

    def get_success_url(self):
        return reverse_lazy('booking:order_create_success')

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super(OrderCreateView, self).get_initial()
        user = self.request.user

        try:
            last_order = Order.objects.filter(created_by=self.request.user).latest('created_at')
            data = model_to_dict(last_order, exclude={'comment'})
        except Order.DoesNotExist:
            data = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            }
        initial.update(data)
        return initial

    def form_valid(self, form):
        error_response = render_to_response('booking/order_person_form_error.html')

        if not Order.objects.user_can_booking(self.request.user):
            return error_response
        rooms = self.request.POST.getlist('rooms')
        if len(rooms) > settings.HH_BOOKING_MAX_ORDER_ROOMS or len(rooms) == 0:
            return error_response

        order = form.instance
        order.places = self.request.POST['places']
        order.begin = self.request.POST['begin']
        order.end = self.request.POST['end']
        try:
            order.full_clean()
            order.save()
            for room_id in rooms:
                room = Room.objects.filter(pk=int(room_id)).first()
                if room:
                    order_room = OrderRoom()
                    order_room.total = room.calc_price(order.places, order.get_duration())
                    order_room.room = room
                    order_room.order = order

                    order_room.full_clean()
                    order_room.save()

            mail_order_hoteliers_task.delay(
                order_id=order.id,
                subject='Новая заявка на бронирование #{id}'.format(id=order.id),
                template='emails/hotelier_booking_order_new.html',
                data=get_order_email_data(order, True),
            )

        except ValidationError:
            return error_response
        return super(OrderCreateView, self).form_valid(form)
