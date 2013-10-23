function driver(){
    var driver_lat = localStorage.getItem('driver_lat');
    var driver_lng = localStorage.getItem('driver_lng');
    document.write(driver_lat);
    document.write(driver_lng);
}
driver()