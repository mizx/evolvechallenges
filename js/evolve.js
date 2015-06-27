/*!
 * Start Bootstrap - Grayscale Bootstrap Theme (http://startbootstrap.com)
 * Code licensed under the Apache License v2.0.
 * For details, see http://www.apache.org/licenses/LICENSE-2.0.
 */

// jQuery to collapse the navbar on scroll
/*
$(window).scroll(function() {
    if ($(".navbar").offset().top > 50) {
        $(".navbar-fixed-top").addClass("top-nav-collapse");
    } else {
        $(".navbar-fixed-top").removeClass("top-nav-collapse");
    }
});*/

// jQuery for page scrolling feature - requires jQuery Easing plugin
/*
$(function() {
    $('a.page-scroll').bind('click', function(event) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: $($anchor.attr('href')).offset().top
        }, 1500, 'easeInOutExpo');
        event.preventDefault();
    });
});*/

// Closes the Responsive Menu on Menu Item Click
$('.navbar-collapse ul li a').click(function() {
    $('.navbar-toggle:visible').click();
});

// Google Maps Scripts
// When the window has finished loading create our google map below
//google.maps.event.addDomListener(window, 'load', init);

function init() {
    // Basic options for a simple Google Map
    // For more options see: https://developers.google.com/maps/documentation/javascript/reference#MapOptions
    /*
    var mapOptions = {
        // How zoomed in you want the map to start at (always required)
        zoom: 15,

        // The latitude and longitude to center the map (always required)
        center: new google.maps.LatLng(40.6700, -73.9400), // New York

        // Disables the default Google Maps UI components
        disableDefaultUI: true,
        scrollwheel: false,
        draggable: false,

        // How you would like to style the map. 
        // This is where you would paste any style found on Snazzy Maps.
        styles: [{
            "featureType": "water",
            "elementType": "geometry",
            "stylers": [{
                "color": "#000000"
            }, {
                "lightness": 17
            }]
        }, {
            "featureType": "landscape",
            "elementType": "geometry",
            "stylers": [{
                "color": "#000000"
            }, {
                "lightness": 20
            }]
        }, {
            "featureType": "road.highway",
            "elementType": "geometry.fill",
            "stylers": [{
                "color": "#000000"
            }, {
                "lightness": 17
            }]
        }, {
            "featureType": "road.highway",
            "elementType": "geometry.stroke",
            "stylers": [{
                "color": "#000000"
            }, {
                "lightness": 29
            }, {
                "weight": 0.2
            }]
        }, {
            "featureType": "road.arterial",
            "elementType": "geometry",
            "stylers": [{
                "color": "#000000"
            }, {
                "lightness": 18
            }]
        }, {
            "featureType": "road.local",
            "elementType": "geometry",
            "stylers": [{
                "color": "#000000"
            }, {
                "lightness": 16
            }]
        }, {
            "featureType": "poi",
            "elementType": "geometry",
            "stylers": [{
                "color": "#000000"
            }, {
                "lightness": 21
            }]
        }, {
            "elementType": "labels.text.stroke",
            "stylers": [{
                "visibility": "on"
            }, {
                "color": "#000000"
            }, {
                "lightness": 16
            }]
        }, {
            "elementType": "labels.text.fill",
            "stylers": [{
                "saturation": 36
            }, {
                "color": "#000000"
            }, {
                "lightness": 40
            }]
        }, {
            "elementType": "labels.icon",
            "stylers": [{
                "visibility": "off"
            }]
        }, {
            "featureType": "transit",
            "elementType": "geometry",
            "stylers": [{
                "color": "#000000"
            }, {
                "lightness": 19
            }]
        }, {
            "featureType": "administrative",
            "elementType": "geometry.fill",
            "stylers": [{
                "color": "#000000"
            }, {
                "lightness": 20
            }]
        }, {
            "featureType": "administrative",
            "elementType": "geometry.stroke",
            "stylers": [{
                "color": "#000000"
            }, {
                "lightness": 17
            }, {
                "weight": 1.2
            }]
        }]
    };
    

    // Get the HTML DOM element that will contain your map 
    // We are using a div with id="map" seen below in the <body>
    var mapElement = document.getElementById('map');

    // Create the Google Map using out element and options defined above
    var map = new google.maps.Map(mapElement, mapOptions);

    // Custom Map Marker Icon - Customize the map-marker.png file to customize your icon
    var image = 'img/map-marker.png';
    var myLatLng = new google.maps.LatLng(40.6700, -73.9400);
    var beachMarker = new google.maps.Marker({
        position: myLatLng,
        map: map,
        icon: image
    });
    */
}
var clock_text;
var clock, jClock, timeleft, start, end, date_start, date_end;
$(function() {

	setTimeout(updateProgressBar, 750);
	
    clock = document.getElementById('clock');
	if (clock == null) 
		return
    jClock = $(clock);
    timeleft = "";
    start = jClock.attr('data-start');
    end = jClock.attr('data-end');
    date_start = new Date(0);
    date_start.setUTCSeconds(challenge['start']);
    date_end = new Date(0);
    date_end.setUTCSeconds(challenge['end']);
    total_time = date_end - date_start;
    
    clock_text = new ProgressBar.Circle(clock, {
        duration: 100,
        trailColor: "#FF391D",
        color: "#000",
        strokeWidth: 4,
        trailWidth: 3,
        text: {
            color: '#FFF',
            className: 'clock_label',
            
        }
    });

    /*
    setInterval(function() {
        var second = new Date().getSeconds();
        seconds.animate(second / 60, function() {
            seconds.setText(second);
        });
    }, 1000);
    */
    
    
    $("#clock_text").countdown(date_end, function(event) {
        var str_format = "%-Dd %-Hh";
        if ( ! event.offset.totalDays) {
            str_format = "%-Hh %-Mm";
        }
        clock_text.setText(event.strftime(str_format));
        timeleft = event.strftime("%-D days %-H hours %M mins remaining");
    });
    
    $(clock).tooltip({
        'title': function() {
            return timeleft;
        },
    });
    
    setInterval(function() {
        var now = new Date();
        var timeleft = date_end - now;
        var percent_left = timeleft / total_time;
        clock_text.animate(1 - percent_left)
    });
    
});

function updateProgressBar() {
    
    var i = 0;
    var bars = challenge.progress / 20;
    $('.health_progress .placeholder').each(function() {
        var floor = Math.floor(bars);
        var progress = 0;
        if (i < floor) {
            progress = 100;
            $(this).find('.bar_border').removeClass('active');
        } else if (i == floor && bars != 0) {
            progress = challenge.progress % 20 * 5;
            $(this).find('.bar_border').delay(750 * (i + 1)).queue(function() {
                $(this).addClass('active');
            });
        }
        
        if (progress) {
            $(this).find('.bar_progress').delay(750 * i).queue(function() {
                $(this).css('width', progress + '%')
            })
        }
        i++;
    });
}