var map = L.map('map').setView([35.6895, 51.3896], 16);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 12,
}).addTo(map);

function sendCoordinates() {
    $.ajax({
        type: "POST",
        url: "/api_weather/",
        data: {
            'latitude': document.getElementsByName('latitude')[0].value,
            'longitude': document.getElementsByName('longitude')[0].value,
            'csrfmiddlewaretoken': csrfToken
        },
        success: function (data) {
            $('#city').text(data.city);
            $('#clock').text(data.myTime);
            $('#current_temp').text(data.current_temp + '°C');
            $('#current_wind_speed').text(data.current_wind_speed + 'km/h :سرعت باد');
            $('#humidity').text(data.humidity + '% :رطوبت هوا');
            if (data.is_day == 1) {
                $('#day_night_image').attr('src', dayImage);
            } else {
                $('#day_night_image').attr('src', nightImage);
            }
        }
    });
}

map.on('click', function (e) {
    var latitude = e.latlng.lat;
    var longitude = e.latlng.lng;
    document.getElementsByName('latitude')[0].value = latitude;
    document.getElementsByName('longitude')[0].value = longitude;
    sendCoordinates()
});

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function (position) {
                var lat = position.coords.latitude;
                var lng = position.coords.longitude;

                document.getElementsByName('latitude')[0].value = lat;
                document.getElementsByName('longitude')[0].value = lng;

                sendCoordinates();

            },
            function (error) {
                alert("Error: " + error.message);
            }
        );
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

$(document).ready(function () {
    getLocation();
});
