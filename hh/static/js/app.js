/*jslint browser: true*/
/*global $, Cookies*/
var hh = {};
hh.readmore = function () {
    'use strict';
    $('.readmore').readmore({
        collapsedHeight: 60,
        moreLink: '<a href="#" class="readmore-link">подробнее</a>',
        lessLink: '<a href="#" class="readmore-link">скрыть</a>'
    });
    return hh;
};

hh.icheck = function () {
    "use strict";
    $('input[type="radio"], input[type="checkbox"]')
        .not('#avatar-delete-form input, #avatar-choose-form input').iCheck({
            checkboxClass: 'icheckbox_square-blue',
            radioClass: 'iradio_square-blue'
        });
    return hh;
};

hh.select2 = function () {
    "use strict";
    $('select.form-control').not('.not-select2').select2();
    return hh;
};

hh.makeRequired = function () {
    "use strict";
    $('label.requiredField').each(function () {
        $(this).next('div.controls').find('input').prop('required', true);
    });
    return hh;
};

hh.secondsCounter = function () {
    "use strict";
    $('.seconds-counter').each(function () {
        var span = $(this),
            counter = parseInt(span.html(), 10);
        setInterval(function () {
            counter -= 1;
            span.html(counter);
            if (counter === 0) {
                clearInterval(counter);
            }
        }, 1000);
    });
    return hh;
};

$(document).ready(function () {
    'use strict';

    // Ajax CSRFToken
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            var csrfSafeMethod = function (method) {
                // these HTTP methods do not require CSRF protection
                return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
            };
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", Cookies.get('csrftoken'));
            }
        }
    });

    // Readmore.js
    hh.readmore();

    // Modal confirmation link
    (function () {
        $('.modal-confirm').click(function (event) {
            event.preventDefault();
            var modal = $('#messages-modal');
            modal.find('.modal-body').html('Вы уверены?');
            if (!modal.find('.messages-modal-link').length) {
                modal.find('.modal-footer')
                    .append('<a href="" class="btn btn-primary messages-modal-link">Продолжить</a>');
            }
            modal.find('.messages-modal-link').prop('href', $(this).attr('href'));

            $('#messages-modal').modal('show');
        });
    }());

    //Seconds counter
    hh.secondsCounter();

    //Datepicker
    $.fn.datepicker.defaults.format = "dd.mm.yyyy";
    $.fn.datepicker.defaults.language = "ru";
    $.fn.datepicker.defaults.daysOfWeekHighlighted = "0,6";
    $.fn.datepicker.defaults.todayHighlight = true;

    //Fancybox
    $(".fancybox").fancybox({
        openEffect: 'none',
        closeEffect: 'none'
    });
    $(".fancybox.autoplay").fancybox({
        openEffect: 'none',
        closeEffect: 'none',
        autoPlay: true
    });

    //iCheck
    hh.icheck()

    //tabs remember
    $(function () {
        $('a[data-toggle="tab"]').on('shown.bs.tab', function () {
            localStorage.setItem('last_tab', $(this).attr('href'));
        });
        var lastTab = localStorage.getItem('last_tab');
        if (lastTab) {
            $('[href="' + lastTab + '"]').tab('show');
        }
    });

    //tooltip
    $('[data-toggle="tooltip"]').tooltip();

    //select2
    $.fn.select2.defaults.set("allowClear", true);
    $.fn.select2.defaults.set("placeholder", "--------------");
    $('select.form-control').not('.not-select2').select2();

    //sidebar
    (function () {
        if ($(window).width() <= 1100) {
            localStorage.setItem('sidebar-collapse', 1);
            $('body').addClass('sidebar-collapse');
        }

        $('.sidebar-toggle').click(function () {
            if ($('body').hasClass('sidebar-collapse')) {
                localStorage.removeItem('sidebar-collapse');
            } else {
                localStorage.setItem('sidebar-collapse', 1);
            }
        });
    }());

    //Datepickers & period select
    (function () {

        $('.datepicker').datepicker({
            format: "yyyy-mm-dd",
            autoclose: true,
            todayHighlight: true
        });

        var period = $('select#id_period'),
            begin = $('input#id_begin'),
            end = $('input#id_end'),
            select = function () {
                var dates = period.val();
                if (dates) {
                    dates = dates.split("_");
                    begin.datepicker('setDate', dates[0]);
                    end.datepicker('setDate', dates[1]);
                }
            },
            periodSet = function () {
                var val = begin.val() + '_' + end.val();
                period.val(val);
            };
        period.change(select);
        begin.change(periodSet);
        end.change(periodSet);
        select();
    }());

    //Box widget
    (function () {
        var links = $('.form-group-collapse');

        links.each(function () {
            if (localStorage.getItem($(this).prop('id'))) {
                var box = $(this).closest('.box'),
                    boxBody = box.find('.box-body'),
                    icon = $(this).find('i');

                box.addClass('collapsed-box');
                boxBody.hide();
                icon.removeClass('fa-minus').addClass('fa-plus');
            }
        });
        links.click(function () {
            if ($(this).closest('.box').find('.box-body').is(':visible')) {
                localStorage.setItem($(this).prop('id'), 1);
            } else {
                localStorage.removeItem($(this).prop('id'));
            }
        });
    }());
});