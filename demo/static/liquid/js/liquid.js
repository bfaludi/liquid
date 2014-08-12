var site = site || {};

site.main = (function($) {
    'use strict';

    // Change select field
    $('select').dropkick({
        mobile: true
    });

    // Remove error messages on change
    $('input.error').change( function( e ) {
        $(e.target).removeClass('error');
    });

})(jQuery);