/*jslint browser: true*/
/*global $, Cookies, hh*/
$(document).ready(function () {
    'use strict';

    // Order confirmation modal
    (function () {
        var orderTotalInput = $('#order-confirmation-total');
        $('.order-confirmation-link').click(function () {
            var total = $(this).attr('data-total');
            orderTotalInput.val(total).attr('max', total);
            $('#order-confirmation-total-help').html($.number(total, 0, '.', ' '));
        });
    }());
});