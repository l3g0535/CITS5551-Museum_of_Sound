var x = document.getElementById("location");
function getLocation() {
  if(x!=null){
      if (navigator.geolocation) {
      console.log('processing');
        navigator.geolocation.getCurrentPosition(showPosition);
      } else {
      console.log('sort of worked');
        x.innerHTML = "Geolocation is not supported by this browser.";
      }
  }
  console.log('fail');
  //If x is null, don't execute the code. Currently there are no plans to add an error message
}

function showPosition(position) {
     let lat = position.coords.latitude;
     let long = position.coords.longitude;
     $("input[name='lat']").val(lat);
     $("input[name='lat']").val(long);
     let url_str = 'https://maps.googleapis.com/maps/api/geocode/json?latlng='+lat+','+long+'&key=AIzaSyC4pppaQX9oFbQIj4lY0gMLDXzq1Ym-jn4'
    $.getJSON(url_str, function(data) {
          console.log(data);
          x.innerHTML = data;
      });
}