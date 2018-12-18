/**
 * Created by ivsemionov on 27.06.2017.
 */
(function ($) {
    function create(target, options) {
        $(target).combo({
            width: 100,
            panelWidth: 300
        });


        $(target).combo({onChange: options.onChange});


        var panel = $(target).combo('panel').panel({
            footer: $('<div style="padding:2px 5px;"><button class="b-ok">Ok</button><button class="b-cancel" style="margin-left:5px">Cancel</button></div>')
        });
        panel.panel('footer').find('.b-ok,.b-cancel').linkbutton({
            width: '20%',
            onClick: function (e) {
                if ($(this).hasClass('b-ok')) {
                    var c1 = panel.find('.c1');
                    var c2 = panel.find('.c2');
                    var d1 = $.fn.datebox.defaults.formatter(c1.calendar('options').current);
                    var d2 = $.fn.datebox.defaults.formatter(c2.calendar('options').current);
                    var v = [d1, d2].join('-');
                    $(target).combo('setValue', v).combo('setText', v);
                }
                else if ($(this).hasClass('b-cancel')) {
                     $(target).combo('setValue', '').combo('setText', '');
                }
                $(target).combo('hidePanel');

            }
        });
        var c = $('<div style="display:block;height:100%"><div class="c1" style="width:50%;float:left"></div><div class="c2" style="width:50%;float:right"></div></div>').appendTo(panel);
        c.find('.c1,.c2').calendar({
            width: '50%',
            height: '100%'
        });
    }

    $.fn.daterangebox = function (options) {
        options = options || {};
        return this.each(function () {
            create(this, options);
        })
    };
    $.parser.plugins.push('daterangebox');
})(jQuery);


