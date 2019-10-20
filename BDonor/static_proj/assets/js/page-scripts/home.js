// Map Detect User Current Location
(function ($, google) {
    $(document).ready(function () {
        $.geolocate({
                loading: "detecting....",
                formatted_address: true,
                name: "long_name", // "short_name", "long_name"
                components: [
                    "country"
                ],
                delimeter: ", ",
                enableHighAccuracy: true,
                timeout: 5000,
                maximumAge: 0
            })
        .done(function (result) {
            if ((result != "Could not an address for your location.") && (result != "")) {
                $.ajax({
                    url: '/utils/set/user/country/',
                    data: {
                        'location': result
                    },
                    dataType: 'json',
                    // success: function (data) {
                    //     if (data.location) {
                    //         console.log("from console-" + data.location);
                    //     }
                    // }
                });
            } else {
                // Something
            }
        });
    });
})(jQuery, google);