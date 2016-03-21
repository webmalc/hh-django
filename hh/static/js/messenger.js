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
                    items.push('<div class="callout callout-' + v.type + '"><i class="' + v.icon + '"></i> ' + v.content + '</div>');
                });
                modal.find('.modal-body').html(items.join(''));
                $('#messages-modal').modal('show');
            }
        });
    };
    setTimeout(getMessages, 500);
    setInterval(getMessages, 1000 * 60 * 3);
});