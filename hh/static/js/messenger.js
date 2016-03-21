/*jslint browser: true*/
/*global $*/

$(document).ready(function () {
    'use strict';

    var getMessages = function () {
        $.getJSON('/users/messages', function (data) {
            if (data.length) {
                var items = [],
                    modal = $('#messages-modal');
                $.each(data, function (k, v) {
                    items.push('<p class="callout callout-' + v.type + '"><i class="' + v.icon + '"></i> ' + v.content + '</p>');
                });
                modal.find('.modal-body').html(items.join(''));
                $('#messages-modal').modal('show');
            }
        });
    };
    setTimeout(getMessages, 500);
    setInterval(getMessages, 1000 * 60 * 3);
});