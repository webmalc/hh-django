from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import FormMixin
from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy
from hh.models import DeleteSuccessMessageMixin
from hotels.models import Property, Room, PropertyPhoto
from hotels.forms import PropertyForm, RoomForm, PhotoForm


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
    success_message = "Отель успешно добавлен. Теперь необходимо заполнить цены."

    def get_success_url(self):
        return reverse_lazy('hotel:property_room_list', kwargs={'pk': self.object.id})


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


class PhotoUpdate(SuccessMessageMixin, UpdateView):
    """
    Property photo update
    """
    model = PropertyPhoto
    fields = ['photo', 'name', 'is_default']
    template_name = 'hotels/photo_form.html'
    success_message = "Фото успешно обновлено."

    def get_context_data(self, **kwargs):
        context = super(PhotoUpdate, self).get_context_data(**kwargs)
        context['property'] = self.object.property
        return context

    def get_queryset(self):
        return super(PhotoUpdate, self).get_queryset().filter(property__created_by=self.request.user)


class PhotoCreate(SuccessMessageMixin, FormMixin, DetailView):
    """
    Property photo create
    """
    model = Property
    template_name = 'hotels/photo_form.html'
    success_message = "Фото успешно добавлено."
    form_class = PhotoForm

    def get_success_url(self):
        return reverse_lazy('hotel:property_photo_list', kwargs={'pk': self.get_object().id})

    def get_context_data(self, **kwargs):
        context = super(PhotoCreate, self).get_context_data(**kwargs)
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
        photo = form.save(commit=False)
        photo.property = self.get_object()
        photo.save()
        return super(PhotoCreate, self).form_valid(form)

    def get_queryset(self):
        return super(PhotoCreate, self).get_queryset().filter(created_by=self.request.user)


class PhotoDelete(DeleteSuccessMessageMixin, DeleteView):
    """
    Photo delete
    """
    model = PropertyPhoto
    template_name = "partials/confirm_delete.html"
    success_message = "Фото отеля успешно удалено."

    def get_success_url(self):
        return reverse_lazy('hotel:property_photo_list', kwargs={'pk': self.get_object().property.id})

    def get_queryset(self):
        return super(PhotoDelete, self).get_queryset().filter(property__created_by=self.request.user)


class RoomList(DetailView):
    """
    Property photos list
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


