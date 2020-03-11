var loc_field = document.getElementById("location");
function getLocation() {
  if(x!=null){
      if (navigator.geolocation) {
      console.log('processing');
        navigator.geolocation.getCurrentPosition(showPosition);
      } else {
      console.log('sort of worked');
        loc_field.innerHTML = "Geolocation is not supported by this browser.";
      }
  }
  //If x is null, don't execute the code. Currently there are no plans to add an error message
}

//TODO will need to clean this section up
function showPosition(position) {
     let lat = position.coords.latitude;
     let long = position.coords.longitude;
     $("input[name='lat']").val(lat);
     $("input[name='lat']").val(long);
     let url_str = 'https://maps.googleapis.com/maps/api/geocode/json?latlng='+lat+','+long+'&key=AIzaSyC4pppaQX9oFbQIj4lY0gMLDXzq1Ym-jn4'
    $.getJSON(url_str, function(data) {
          var res = '';
          for (index = 0; index < data['results'].length; ++index) {
            //console.log(data['results'][index]['formatted_address']);
            //console.log(data['results'][index]['types']);
            if(data['results'][index]['types'].includes('political')){
                res = data['results'][index]['formatted_address'];
                break;
            }
          }
          loc_field.innerHTML = res;
      });
}