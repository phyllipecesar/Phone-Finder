var map;
var index = 1;
var poly;
function initialize(map_id, lat, longi) {
    var latlng = new google.maps.LatLng(lat, longi);
    
    var myOptions = {
	zoom: 8,
	mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    map = new google.maps.Map(document.getElementById(map_id),
				  myOptions);
	var polyOptions = {
    strokeColor: '#000000',
    strokeOpacity: 0.8,
    strokeWeight: 3
  }
  poly = new google.maps.Polyline(polyOptions);
  poly.setMap(map);
}


function add_marker(lati, longi, description) {
    var position = new google.maps.LatLng(lati, longi);
    var marker = new google.maps.Marker( {
         map: map,
         title: "teste",
         position: position});
    poly.getPath().push(position);
    map.setCenter(position);
    // Create the DIV to hold the control and call the HomeControl() constructor
    // passing in this DIV.
    var homeControlDiv = document.createElement('DIV');
    var homeControl = new HomeControl(homeControlDiv, map, position, index);
    homeControlDiv.index = index;
    index += 1;
    map.controls[google.maps.ControlPosition.TOP_RIGHT].push(homeControlDiv);

    var contentString = '<div class="Top_View" id="content">'+
    '<div id="siteNotice">'+
    '</div>'+
    '<h1 id="firstHeading" class="firstHeading">Phone Finder</h1><hr/><h3>The smartest way to find your phone!</h3>'+
    '<div id="bodyContent">'+
        description +
    '</div>'+
    '</div>';
    
    var infowindow = new google.maps.InfoWindow({
        content: contentString
    });
    google.maps.event.addListener(marker, 'click', function() {
      infowindow.open(map,marker);
    });
}
    
    
    
    
    
    
    
   
/**
 * The HomeControl adds a control to the map that simply
 * returns the user to Chicago. This constructor takes
 * the control DIV as an argument.
 */

function HomeControl(controlDiv, map, position, messageop) {

  // Set CSS styles for the DIV containing the control
  // Setting padding to 5 px will offset the control
  // from the edge of the map
  controlDiv.style.padding = '5px';

  // Set CSS for the control border
  var controlUI = document.createElement('DIV');
  controlUI.style.backgroundColor = 'white';
  controlUI.style.borderStyle = 'solid';
  controlUI.style.borderWidth = '2px';
  controlUI.style.cursor = 'pointer';
  controlUI.style.textAlign = 'center';
  controlUI.title = 'Click to set the map to ' + messageop;
  controlDiv.appendChild(controlUI);

  // Set CSS for the control interior
  var controlText = document.createElement('DIV');
  controlText.style.fontFamily = 'Arial,sans-serif';
  controlText.style.fontSize = '12px';
  controlText.style.paddingLeft = '4px';
  controlText.style.paddingRight = '4px';
  controlText.innerHTML = messageop;
  controlUI.appendChild(controlText);

  // Setup the click event listeners: simply set the map to Chicago
    google.maps.event.addDomListener(controlUI, 'click', function() {
    map.setCenter(position)
  });
}

