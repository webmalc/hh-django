import logging
from django.conf import settings
from hashlib import md5
from payments.models import Payment
from users.tasks import mail_user_task, add_message_user_task


class Rbk(object):
    """
    RBK payment system service
    """

    @staticmethod
    def get_form_data(order):
        """
        Get rbk form params
        :param order: payment
        :type order: payments.models.Payment
        :return: form params
        :rtype: dict
        """
        data = {
            'eshopId': settings.HH_RBK_SHOP_ID,
            'orderId': order.id,
            'serviceName': 'Заказ #{}. Пополнение счета HostelHunt'.format(order.id),
            'recipientAmount': order.total,
            'recipientCurrency': 'RUR',
            'user_email': order.created_by.get_first_email(),
        }
        data['hash'] = Rbk.get_hash([
            data['eshopId'], data['recipientAmount'], data['recipientCurrency'],
            data['user_email'], data['serviceName'], data['orderId'], settings.HH_RBK_KEY
        ]).hexdigest()
        return data

    @staticmethod
    def process_request(request):
        """
        Process request from RBK
        :param request: django.http.HttpRequest
        :type request: django.http.HttpRequest
        :return: payment of False
        :rtype: payments.models.Payment | False
        """
        logging.getLogger('hh').info('POST from RBK : {}'.format(request.POST))

        eshop_id = request.POST.get('eshopId')
        order_id = request.POST.get('orderId')
        service_name = request.POST.get('serviceName')
        eshop_account = request.POST.get('eshopAccount')
        recipient_amount = float(request.POST.get('recipientAmount'))
        recipient_currency = request.POST.get('recipientCurrency')
        payment_status = int(request.POST.get('paymentStatus'))
        user_name = request.POST.get('userName')
        user_email = request.POST.get('userEmail')
        payment_data = request.POST.get('paymentData')
        request_signature = request.POST.get('hash')

        if not eshop_id or not payment_status or not request_signature or payment_status != 5:
            return False

        signature = Rbk.get_hash([
            eshop_id, order_id, service_name, eshop_account, recipient_amount, recipient_currency,
            payment_status, user_name, user_email, payment_data, settings.HH_RBK_KEY
        ]).hexdigest()

        if signature != request_signature:
            return False

        payment = Payment.objects.filter(pk=order_id, is_completed=False).first()

        if not payment or payment.total != recipient_amount:
            return False

        payment.is_completed = True
        payment.save()
        user = payment.created_by

        mail_user_task.delay(
            subject='Баланс успешно пополнен',
            template='emails/user_add_funds_completed.html',
            data={'id': payment.id, 'total': payment.total},
            email=user.get_first_email()
        )
        add_message_user_task.delay(
            user_id=user.id,
            template='messages/user_add_funds_completed.html',
            data={'id': payment.id, 'total': payment.total},
            subject='Баланс пополнен на {} р.'.format(payment.total),
            message_type='success'
        )

        return payment

    @staticmethod
    def get_hash(data):
        """
        Generate rbk hash
        :param data: params for hash generation
        :type data: list
        :return: md5
        :rtype: md5
        """
        signature = '::'.join(map(str, data))
        return md5(signature.encode('utf-8'))
