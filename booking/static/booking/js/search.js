/*jslint browser: true*/
/*global $, Cookies, hh*/
$(document).ready(function () {
    'use strict';

    $('.input-daterange').datepicker({
        startDate: new Date(),
        todayBtn: "linked"
    });

    //Search results
    (function () {
        var form = $('#search-form'),
            maxRooms = form.attr('data-max-rooms-in-order'),
            results = $('#search-results-body'),
            overlay = $('#search-results-overlay'),
            checkRooms = function () {
                var rows = $('.search-result-rooms tbody > tr'),
                    roomsCount = $('.search-results-room-input:checked').length;
                rows.removeClass('info');
                rows.each(function () {
                    if ($(this).find('.search-results-room-input:checked').val()) {
                        $(this).addClass('info');
                    }
                });
                $('#search-results-form-submit button').prop('disabled', !roomsCount);
                $('#search-results-rooms-counter').html(roomsCount);
                if (roomsCount >= maxRooms) {
                    $('.search-results-room-input').not(':checked').iCheck('disable');
                    $('.icheckbox_square-blue.disabled').tooltip({
                        title: 'Уже выбрано максимальное количество комнат для одной заявки.',
                        placement: 'left'
                    });
                } else {
                    $('.search-results-room-input').not(':checked').iCheck('enable');
                }
            },
            sendOrder = function () {
                var orderForm = $('#search-results-form'),
                    orderOverlay = $('#order-form-overlay'),
                    orderFormWrapper = $('#order-form-modal-body'),
                    sendButton = $('#send-order-form');

                if (!orderFormWrapper.html()) {
                    orderOverlay.hide();
                    orderFormWrapper.load('/booking/order/create');
                }

                orderForm.submit(function (e) {
                    e.preventDefault();
                    $.ajax({
                        type: 'POST',
                        url: '/booking/order/create',
                        data: orderForm.serialize(),
                        success: function (response) {
                            orderOverlay.hide();
                            orderFormWrapper.html(response);
                            if ($('#id_first_name').length) {
                                sendButton.prop('disabled', false);
                            } else {
                                hh.secondsCounter()
                                setTimeout(function () {
                                    location.reload();
                                }, 30 * 1000);
                            }
                        },
                        beforeSend: function () {
                            sendButton.prop('disabled', true)
                            orderOverlay.show();
                            orderFormWrapper.html('Подождите...');
                        }
                    });
                });
            },
            sendForm = function (scroll) {
                scroll = scroll === 'undefined' ? false : scroll;
                var data = form.find('input[name!=csrfmiddlewaretoken], select').serialize();
                $.ajax({
                    type: 'POST',
                    url: '/booking/search/results',
                    data: form.serialize(),
                    beforeSend: function () {
                        overlay.show();
                        results.html('Подождите...');
                    },
                    success: function (response) {
                        overlay.hide();
                        results.html(response);
                        window.history.pushState(data, '', '/booking/search/?' + data);
                        hh.readmore().icheck().select2().makeRequired();
                        checkRooms();
                        sendOrder();
                        $('.search-results-room-input').on('ifChanged change', checkRooms);
                        $('#search-results-form-submit').affix({
                            offset: {
                                top: function () {
                                    return $('#search-results-body').offset().top;
                                }
                            }
                        });
                        if (scroll) {
                            $('html, body').animate({
                                scrollTop: $("#search-results-form").offset().top
                            }, 300);
                        }
                    }
                });

            };
        if (!form.length) {
            return;
        }
        form.submit(function (event) {
            event.preventDefault();
            sendForm(true);
        });
        sendForm();
    }());
});