/*jslint browser: true*/
/*global $*/

$(document).ready(function () {
    'use strict';

    $.notification.requestPermission(function () {return; });

    var getMessages = function () {
        $.getJSON('/users/messages', function (data) {
            if (data.length) {
                var items = [],
                    modal = $('#messages-modal');
                $.each(data, function (k, v) {
                    if (v.subject) {
                        $.notification({
                            iconUrl: '/static/img/logo-png-white.png',
                            title: 'HostelHunt.ru',
                            body: v.subject
                        });
                    }
                    items.push('<div class="callout callout-' + v.type + '"><i class="' + v.icon + '"></i> ' + v.content + '</div>');
                });
                modal.find('.modal-body').html(items.join(''));
                modal.find('.messages-modal-link').remove();
                $('#messages-modal').modal('show');
            }
        });
    };
    setTimeout(getMessages, 500);
    setInterval(getMessages, 1000 * 60 * 3);
});