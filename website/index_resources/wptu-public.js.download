(function($) {
	
	wptu_ticker_init();

	/* Beaver Builder Compatibility for Accordion */
	$(document).on('click', '.fl-accordion-item', function() {

		var cls_ele		= $(this).closest('.fl-accordion');
		var ele_control	= cls_ele.find('.fl-accordion-button').attr('aria-controls');
		var ticker_wrap	= $('#'+ele_control).find('.wptu-news-ticker');

		/* Tweak for ticker */
		if( ticker_wrap.length > 0 ) {
			$(window).trigger('resize');
		}
	});

	/* Divi Builder Compatibility for Accordion & Toggle */
	$(document).on('click', '.et_pb_toggle', function() {

		var acc_cont	= $(this).find('.et_pb_toggle_content');
		var ticker_wrap	= acc_cont.find('.wptu-news-ticker');

		/* Tweak for ticker */
		if( ticker_wrap.length > 0 ) {
			$(window).trigger('resize');
		}
	});

})(jQuery);

/* Function to Initialize Ticker */
function wptu_ticker_init() {

	// Initialize news ticker
	jQuery( '.wptu-news-ticker' ).each(function( index ) {
		var ticker_id	= jQuery(this).attr('id');
		var ticker_conf	= jQuery.parseJSON( jQuery(this).attr('data-conf'));

		if( typeof(ticker_id) != 'undefined' && ticker_id != '' && ticker_conf != 'undefined' ) {

			if (ticker_conf.fontstyle == "italic") {
				jQuery(this).addClass("wpos-italic");
			}
			if (ticker_conf.fontstyle == "bold") {
				jQuery(this).addClass("wpos-bold");
			}
			if (ticker_conf.fontstyle == "bold-italic") {
				jQuery(this).addClass("wpos-bold wpos-italic");
			}

			jQuery('#'+ticker_id).breakingNews({
				stopOnHover	: true,
				effect		: ticker_conf.effect,
				delayTimer	: parseInt( ticker_conf.timer ),
				play		: ( ticker_conf.autoplay == 'false' )	? false	: true,
				borderWidth	: ( ticker_conf.border == 'false' )		? 0		: 2,
			});
		}
	});
}