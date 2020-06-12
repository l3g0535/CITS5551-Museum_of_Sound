
function getLocation() {
    var loc_field = document.getElementById("location");
  if (navigator.geolocation) {
  console.log('processing');
    navigator.geolocation.getCurrentPosition(showPosition);
  } else {
  console.log('failed');
    loc_field.innerHTML = "Automatic geolocation is not supported by this browser.";
  }
}

function showPosition(pos) {
     let lat = pos.coords.latitude;
     let long = pos.coords.longitude;
     $("input[name='lat']").val(lat);
     $("input[name='lat']").val(long);
     let url_str = 'https://maps.googleapis.com/maps/api/geocode/json?latlng='+lat+','+long+'&key=AIzaSyC4pppaQX9oFbQIj4lY0gMLDXzq1Ym-jn4'
    $.getJSON(url_str, function(data) {
          var res = '';
          for (index = 0; index < data['results'].length; ++index) {
            if(data['results'][index]['types'].includes('political')){
                res = data['results'][index]['formatted_address'];
                break;
            }
          }
          loc_field.innerHTML = res;
      });
}