/*jslint browser: true*/
/*global $, Cookies, hh*/
$(document).ready(function () {
    'use strict';

    // Orders countdown
    $('.order-ends-at').each(function () {
        var clock = $(this);
        clock.countdown(clock.html(), function (event) {
            var totalHours = event.offset.totalDays * 24 + event.offset.hours,
                output = totalHours > 0 ? totalHours + ' ч %M мин. %S сек.' : '%M мин. %S сек.';
            $(this).html(event.strftime('через ' + output));
        });
    });

    // Order confirmation modal
    (function () {
        var orderTotalInput = $('#order-confirmation-total'),
            orderConfirmationForm = $('#order-confirmation-form'),
            orderOverlay = $('#order-confirmation-form-overlay'),
            sendButton = $('#send-order-confirmation-form'),
            errorWrapper = $('#order-confirmation-total-error');

        $('.order-confirmation-link').click(function () {
            var total = $(this).attr('data-total');
            orderTotalInput.val(total).attr('max', total);
            $('#order-confirmation-total-help').html($.number(total, 0, '.', ' '));
            orderConfirmationForm.attr('action', $(this).attr('data-url'));
            sendButton.prop('disabled', false);
            errorWrapper.hide().html('');
        });

        orderConfirmationForm.submit(function (e) {
            e.preventDefault();
            $.ajax({
                type: 'GET',
                url: orderConfirmationForm.attr('action'),
                dataType: "json",
                data: orderConfirmationForm.serialize(),
                success: function (response) {
                    if (response.success) {
                        window.location.reload();
                    } else {
                        orderOverlay.hide();
                        errorWrapper.show().html(response.message);
                        sendButton.prop('disabled', false);
                    }
                },
                beforeSend: function () {
                    sendButton.prop('disabled', true)
                    orderOverlay.show();
                }
            });
        });
    }());
});