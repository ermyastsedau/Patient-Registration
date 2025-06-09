$(document).ready(function() {
    // Toggle sidebar
    $("#menu-toggle").click(function(e) {
        e.preventDefault();
        $("#wrapper").toggleClass("toggled");
    });
    
    // Initialize submenus
    $('.sidebar-nav .dropdown-toggle').click(function(e) {
        // Only prevent default if it has a submenu
        if ($(this).next('.collapse').length) {
            e.preventDefault();
        }
    });
    
    // Close all submenus when in toggled-2 mode
    $("#menu-toggle-2").click(function(e) {
        e.preventDefault();
        $("#wrapper").toggleClass("toggled-2");
        $('.sidebar-nav .collapse').collapse('hide');
    });
});