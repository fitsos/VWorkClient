
var geocoder;
var map;
var marker;
var infowindow = new google.maps.InfoWindow();
var directionsDisplay;
var directionsService = new google.maps.DirectionsService();

// Get user lat/lng position
function userPos(){
	if(navigator.geolocation){
		navigator.geolocation.getCurrentPosition(
			function(position){
				var user_lat = parseFloat(position.coords.latitude);
				var	user_lng = parseFloat(position.coords.longitude);
				console.log(user_lat);
				console.log(user_lng);
				initialize(user_lat, user_lng);
				codeLatLng(user_lat, user_lng);	
		});
	} else {
		alert("Geolocation is not supported or turned off");
	}
}
userPos();

//initialize map passing user lat/lng
function initialize(user_lat, user_lng){
	geocoder = new google.maps.Geocoder();
	directionsDisplay = new google.maps.DirectionsRenderer();
	var latlng = new google.maps.LatLng(user_lat,user_lng);
	var mapOptions = {
		zoom: 13,
		center: latlng,
		mapTypeId: 'roadmap'
	};
	map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
	marker = new google.maps.Marker({
		position: latlng,
		map: map,
		draggable: true	
		});
	directionsDisplay.setMap(map);
}

//set autocomplete
function autoComplete(){
	var input = (document.getElementById('searchTextField'));
	var autocomplete = new google.maps.places.Autocomplete(input);
	google.maps.event.addListener(autocomplete, 'place_changed', function(){
		infowindow.close();
		input.className = '';
		var place = autocomplete.getPlace();
		// advise if place not found
		if(!place.geometry){
			input.className = 'notfound';
			return;
		}
		//if place has geommetry then show on map... working?
		if(place.geometry.viewport){
			map.fitBounds(place.geometry.viewport);
		} else {
			console.log("bounds?");
			map.setCenter(place.geometry.location);
			map.setZoom(15);
		}
		//custom drop off location icon
		marker.setIcon(({
			url: place.icon,
			size: new google.maps.Size(65, 65),
			origin: new google.maps.Point(0, 0),
			anchor: new google.maps.Point(17, 34),
			scaledSize: new google.maps.Size(35, 35)
		}));
		marker.setPosition(place.geometry.location);
		marker.setVisible(true);
		calcRoute();
		//autocomplete address components and set infowindow
		var address = "";
		if(place.address_components){
			address = [
				(place.address_components[0] && place.address_components[0].short_name || ""),
				(place.address_components[1] && place.address_components[1].short_name || ""),
				(place.address_components[2] && place.address_components[2].short_name || "")
			].join(" ");
		}
		infowindow.setContent(address);
		infowindow.open(map, marker);
	});
}
autoComplete();

//reverse geocoder user lat/lng to address
function codeLatLng(user_lat, user_lng){	
	var latlng = new google.maps.LatLng(user_lat, user_lng);
	geocoder.geocode({'latLng': latlng}, function(results, status){
		if(status == google.maps.GeocoderStatus.OK){
			if(results[0]){
				map.setZoom(15);
				var results = results[0].formatted_address;
				infowindow.setContent(results);
				infowindow.open(map, marker);
				dragMarker(results);
				setAddr(results);
			} else {
				alert("No results found");
			}
		} else {
			console.log("Geocoder failed due to: "+status);
		}
	});
}

//event listener for dragging marker 
function dragMarker(results){
	google.maps.event.addListener(marker, 'dragend', function(event){
		console.log('new position is '+event.latLng.lat()+','+event.latLng.lng());
		var lat = parseFloat(event.latLng.lat());
		console.log(lat);
		var lng = parseFloat(event.latLng.lng());
		console.log(lng);
		codeLatLng(lat,lng);	
	});
}

//show optimal driving route on map
function calcRoute() {
  var start = document.getElementById('pickup-loc').value;
  console.log(start);
  var end = document.getElementById('searchTextField').value;
  console.log(end);
  var request = {
      origin:start,
      destination:end,
      travelMode: google.maps.DirectionsTravelMode.DRIVING
  };
  directionsService.route(request, function(response, status) {
    if (status == google.maps.DirectionsStatus.OK) {
      directionsDisplay.setDirections(response);
    }
  });
}

//populate pickup location field
function setAddr(results){
	$('#pickup-loc').val(results);
}

google.maps.event.addDomListener(window, 'load', initialize);

