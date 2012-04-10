
function initialize(map_id, lat, longi) {
    var latlng = new google.maps.LatLng(lat, longi);
    var myOptions = {
	zoom: 8,
	center: latlng,
	mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map(document.getElementById(map_id),
				  myOptions);
    var marker = new google.maps.Marker( {
        map: map,
        position: latlng});
}