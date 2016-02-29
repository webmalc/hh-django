/*jslint browser: true*/
/*global $, Cookies*/
$(document).ready(function () {
    'use strict';

    $('.input-daterange').datepicker({todayBtn: "linked"});

    (function () {
        var form = $('#search-form'),
            results = $('#search-results-body'),
            overlay = $('#search-results-overlay'),
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