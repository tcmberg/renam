;(function($) {
    "use strict"; 
	
	//* Navbar Fixed  
    function navbarFixed(){
        if ( $('body').length ){ 
            $(window).on('scroll', function() {
                var scroll = $(window).scrollTop();   
                if (scroll >= 295) {
                    $(".main_header_area").addClass("navbar_fixed");
                } else {
                    $(".main_header_area").removeClass("navbar_fixed");
                }
            });   
        };
    };  
	
	//* Client Logo 
    function clSlide(){
        if ( $('.cl_slide').length ){ 
            $('.cl_slide').owlCarousel({
            	loop: true,
            	margin: 60,
            	nav: false,
				dots: false,
            	responsive: {
            		0: {
            			items: 2, 
            		}, 
            		575: {
            			items: 3, 
						margin: 30,
            		}, 
            		767: {
            			items: 4, 
						margin: 30,
            		}, 
            		991: {
            			items: 5
            		},
            		1199: {
            			items: 7
            		}
            	}
            })
        };
    };
	
	//* Counter Js 
    function counterUp(){
        if ( $('.ba_3, .countarup_area').length ){ 
            $('.counter').counterUp({
                delay: 10,
                time: 400
            });
        };
    };
	
    //* Magnificpopup js
    function magnificPopup() {
        if ($('.popup-youtube, .partner_img').length) { 
            //Video Popup
            $('.popup-youtube').magnificPopup({
                disableOn: 700,
                type: 'iframe',
                mainClass: 'mfp-fade',
                removalDelay: 160,
                preloader: false, 
                fixedContentPos: false,
            });  
			
			// Image popups
            $('.partner_img').magnificPopup({
                delegate: '.zoom_img',
                type: 'image',
                removalDelay: 500,
                callbacks: {
                    beforeOpen: function () { 
                        this.st.image.markup = this.st.image.markup.replace('mfp-figure', 'mfp-figure mfp-with-anim');
                        this.st.mainClass = this.st.el.attr('data-effect');
                    }
                },
                closeOnContentClick: true,
                midClick: true
            });
        };
    };
	
	//* Isotope js
    function protfolioIsotope(){
        if ( $('.portfolio_grid').length ){ 
            // Activate isotope in container
            $(".portfoli_inner").imagesLoaded( function() {
                $(".portfoli_inner").isotope({
                    layoutMode: 'fitRows',  
                }); 
            });  
            
            // Add isotope click function 
            $(".protfoli_filter li").on('click',function(){
                $(".protfoli_filter li").removeClass("active");
                $(this).addClass("active"); 
                var selector = $(this).attr("data-filter");
                $(".portfoli_inner").isotope({
                    filter: selector,
                    animationOptions: {
                        duration: 450,
                        easing: "linear",
                        queue: false,
                    }
                });
                return false;
            });  
        };
    };
	
	//* Select js
    function selectmenu(){
        if ( $('.post_select').length ){ 
            $('select').niceSelect();
        };
    };   
    
    // Scroll to top
    function scrollToTop() {
        if ($('.scroll-top').length) {  
            $(window).on('scroll', function () {
                if ($(this).scrollTop() > 200) {
                    $('.scroll-top').fadeIn();
                } else {
                    $('.scroll-top').fadeOut();
                }
            }); 
            //Click event to scroll to top
            $('.scroll-top').on('click', function () {
                $('html, body').animate({
                    scrollTop: 0
                }, 1000);
                return false;
            });
        }
    }
    
    // Preloader JS
    function preloader(){
        if( $('.preloader').length ){
            $(window).on('load', function() {
                $('.preloader').fadeOut();
                $('.preloader').delay(50).fadeOut('slow');  
            })   
        }
    }     
	
    /*Function Calls*/ 
    new WOW().init();
    navbarFixed ();   
	scrollToTop (); 
	clSlide ();
	counterUp ();
	magnificPopup ();
	protfolioIsotope ();
	preloader ();
    
})(jQuery);