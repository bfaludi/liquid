var site = site || {};

site.main = (function($) {
    'use strict';

    $('input.error').change( function( e ) { $(e.target).removeClass('error'); });
})(jQuery);