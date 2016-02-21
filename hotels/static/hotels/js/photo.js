/*jslint browser: true*/
/*global $, Cookies*/
$(document).ready(function () {
    'use strict';

    //photo field
    (function () {
        var wrapper = $('#div_id_photo .controls'),
            oldLink = wrapper.find('a'),
            link = $('<a href="' + oldLink.attr('href') + '" class="photo-preview">текущее фото</a>'),
            input = wrapper.find('input');

        if (oldLink.length) {
            link.fancybox();
            wrapper.html('');
            wrapper.append();
            wrapper.append(link, input);
        }
        //$('#div_id_photo a').css('visibility', 'visible');
    }());
});