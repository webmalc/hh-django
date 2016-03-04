/*jslint browser: true*/
/*global $, Cookies, hh*/
$(document).ready(function () {
    'use strict';

    $('.input-daterange').datepicker({
        startDate: new Date(),
        todayBtn: "linked"
    });

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
            sendForm = function () {
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
                        hh.readmore();
                        hh.icheck();
                        checkRooms();
                        $('.search-results-room-input').on('ifChanged change', checkRooms);
                        $('#search-results-form-submit').affix({
                            offset: {
                                top: function () {
                                    return $('#search-results-body').offset().top;
                                }
                            }
                        });
                    }
                });

            };
        if (!form.length) {
            return;
        }
        form.submit(function (event) {
            event.preventDefault();
            sendForm();
        });
        sendForm();
    }());
});