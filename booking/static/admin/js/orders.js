/*jslint browser: true*/
/*global $*/
$(document).ready(function () {
    'use strict';

    //Set color for td.field-status
    $('td.field-status:contains("Завершена") a').css('color', '#00a65a');
    $('td.field-status:contains("Отменена") a').css('color', '#dd4b39');
    $('td.field-status:contains("Обрабатывается") a').css('color', '#f39c12');
});