$(function() {
	var scroll;
	
	$(window).scroll(function() {
		if (scroll) {
			window.clearTimeout(scroll);
			scroll = null;
		}
		scroll = window.setTimeout(function() {
			if ($(window).scrollTop() > 70)
				$('.navbar-default').addClass('navbar-shrink');
			else $('.navbar-default').removeClass('navbar-shrink');
		}, 100);
	});
});