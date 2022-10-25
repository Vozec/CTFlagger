function redirect() {
  sleep(5000).then(() => { 
    if("Scan in progress ..." == document.getElementById("type").textContent){
      sleep(5000).then(() => {location.reload();}); 
    }
    else{
      window.location.replace("/");
    }
  });
}
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
redirect();