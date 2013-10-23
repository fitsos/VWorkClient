<!DOCTYPE html>
<html>
<head>
<script type="text/javascript">
   window.onload = function () {
        localStorage.setItem('driver_lat', '{{lat}}' );
	    localStorage.setItem('driver_lng', '{{lng}}' );
   }
</script>
<script type="text/javascript" src="t.js"></script>
    <title></title>
</head>
<body>
    <h1>Test</h1>
    <h3>{{lat}}<br />{{lng}}<br /></h3>
</body>
</html>