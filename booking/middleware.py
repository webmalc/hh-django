from booking.models import Order


class IncomingOrdersMiddleware(object):

    def process_request(self, request):
        user = request.user
        request.incoming_orders = None
        if user.is_authenticated() and user.is_partner():
            request.incoming_orders = Order.objects.filter_for_hotelier(request.user).filter(status='process').count()
