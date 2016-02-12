/*jslint browser: true*/
/*global $*/
$(document).ready(function () {
    'use strict';

    //Set color for td.field-color
    $('td.field-color').each(function () {
        var el = $(this);
        el.css('color', el.html());
    });
});