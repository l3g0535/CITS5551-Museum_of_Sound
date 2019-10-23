function startCounter() {
    if(!interval){
      document.getElementById('time').innerHTML = currentTimeInt; 
      interval = setInterval(newNumber, 1000) // set an interval
    }
  }
  
  // stop
  function stopCounter() {
    // clear the interval
    clearInterval(interval)
    interval = undefined;
  }
  
  // reset the timer
  function resetCounter(){
    currentTimeInt = startTimeInt;
    document.getElementById('time').innerHTML = currentTimeInt;
    //stopCounter(); startCounter();
  }
  
  
  // change the time and handle end of time event
  function newNumber(){
    currentTimeInt--; // decrement the current time
    document.getElementById('time').innerHTML = currentTimeInt; 
    if(currentTimeInt == 0){
      console.log("Done");
      stopCounter();
    }
  }