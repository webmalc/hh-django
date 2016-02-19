/*jslint browser: true*/
/*global $, Cookies*/
$(document).ready(function () {
    'use strict';
    // Position
    (function () {
        var search = $('.geoposition-search input'),
            city = $('select#id_city'),
            address = $('textarea#id_address'),
            setAddress = function () {
                var cityText = city.select2('data')[0] === undefined ? '' : city.select2('data')[0].text + ', ';
                search.val(cityText + address.val()).trigger('keydown');
            };
        search.attr('placeholder', 'Начните вводить адрес ...');
        city.change(function () {
            setAddress();
        });
        address.keyup(function () {
            setAddress();
        });
    }());
});
