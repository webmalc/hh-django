/*jslint browser: true*/
/*global $*/
$(document).ready(function () {
    'use strict';

    // Show partner form
    (function () {
        $('#show-partner-add-form').click(function (e) {
            e.preventDefault();
            $('#partner-add-form').removeClass('hidden');
            $(this).hide();
            $('#partner-info-table').hide();
        });
    }());


});