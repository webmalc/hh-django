from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import FormMixin
from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy
from hotels.models import Property, Room, PropertyPhoto
from hotels.forms import PropertyForm, RoomForm


class PropertyList(ListView):
    """
    User properties list
    """
    model = Property

    def dispatch(self, request, *args, **kwargs):
        if not request.user.hotels_property_created_by.count():
            return redirect('hotel:property_create')
        return super(PropertyList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return super(PropertyList, self).get_queryset().\
            filter(created_by=self.request.user).prefetch_related('metro_stations', 'propertyphoto_set', 'room_set')


class PropertyCreate(SuccessMessageMixin, CreateView):
    """
    User property create
    """
    form_class = PropertyForm
    template_name = 'hotels/property_edit.html'
    success_url = reverse_lazy('hotel:property_room_list')
    success_message = "Отель успешно добавлен. Теперь необходимо заполнить цены."


class PropertyUpdate(SuccessMessageMixin, UpdateView):
    """
    Property update
    """
    model = Property
    form_class = PropertyForm
    template_name = 'hotels/property_edit.html'
    success_message = "Данные отеля успешно обновлены."

    def get_queryset(self):
        return super(PropertyUpdate, self).get_queryset().filter(created_by=self.request.user)


class PhotoList(DetailView):
    """
    Photo list
    """
    model = Property
    template_name = 'hotels/photo_list.html'

    def get_context_data(self, **kwargs):
        context = super(PhotoList, self).get_context_data(**kwargs)
        context['photos'] = PropertyPhoto.objects.filter(property=self.object)
        return context

    def get_queryset(self):
        return super(PhotoList, self).get_queryset().filter(created_by=self.request.user)


class RoomList(DetailView):
    """
    Property photos List
    """
    model = Property
    template_name = 'hotels/room_list.html'

    def get_context_data(self, **kwargs):
        context = super(RoomList, self).get_context_data(**kwargs)
        context['rooms'] = Room.objects.filter(property=self.object)
        return context

    def get_queryset(self):
        return super(RoomList, self).get_queryset().filter(created_by=self.request.user)


class RoomUpdate(SuccessMessageMixin, UpdateView):
    """
    Property room update
    """
    model = Room
    form_class = RoomForm
    template_name = 'hotels/room_form.html'
    success_message = "Комната/цена успешно обновлена."

    def get_context_data(self, **kwargs):
        context = super(RoomUpdate, self).get_context_data(**kwargs)
        context['property'] = self.object.property
        return context

    def get_queryset(self):
        return super(RoomUpdate, self).get_queryset().filter(property__created_by=self.request.user)


class RoomCreate(SuccessMessageMixin, FormMixin, DetailView):
    """
    Property rooms create
    """
    model = Property
    template_name = 'hotels/room_form.html'
    success_message = "Комната/цена успешно добавлена."
    form_class = RoomForm

    def get_success_url(self):
        return reverse_lazy('hotel:property_room_list', kwargs={'pk': self.get_object().id})

    def get_context_data(self, **kwargs):
        context = super(RoomCreate, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        room = form.save(commit=False)
        room.property = self.get_object()
        room.save()
        return super(RoomCreate, self).form_valid(form)

    def get_queryset(self):
        return super(RoomCreate, self).get_queryset().filter(created_by=self.request.user)


