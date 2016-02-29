/*jslint browser: true*/
/*global $, Cookies*/
$(document).ready(function () {
    'use strict';
    (function () {
        var metro = $('select#id_metro_stations'),
            city = $('select#id_city'),
            switchMetro = function () {
                if (city.length && $.inArray(city.val(), ['347', '201']) > -1) {
                    metro.prop('disabled', false).trigger('change');
                } else {
                    metro.prop('disabled', true);
                    //metro.val(null).trigger('change');
                }
            };
        if (!city.length || !metro.length) {
            return;
        }

        switchMetro();
        city.change(switchMetro);
    }());
});
