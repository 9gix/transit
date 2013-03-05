function initialize(){
    var opt = {
        center: new google.maps.LatLng(1.35188,103.820114),
        zoom: 11,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map(document.getElementById('map'), opt);

    var kmlLayersArray = [];

    function addKmlLayer(serv_no_serv_dir) {
        kmlLayer = new google.maps.KmlLayer('http://publictransport.sg/kml/busroutes/'+serv_no_serv_dir+'.kml');
        kmlLayer.setMap(map);
        kmlLayersArray.push(kmlLayer);
    }

    function deleteKmlLayer(serv_no_serv_dir){
        url = 'http://publictransport.sg/kml/busroutes/'+serv_no_serv_dir+'.kml';
        kmlLayers = $.grep(kmlLayersArray, function(kmlLayer){
            return kmlLayer.url === url;
        });
        $.each(kmlLayers, function(i, kmlLayer){
            kmlLayer.setMap(null);
        });
    }

    $(".bus_chkbox").each(function(){
        $(this).click(function(){
            if (this.checked){
                addKmlLayer(this.value);
            }else{
                deleteKmlLayer(this.value);
            }
        });
    });

    var inputs = $('input');
    var options = {
        componentRestrictions: {country: 'sg'}
    };
    $.each(inputs, function(i, input){
        var marker = new google.maps.Marker({
            map: map
        });
        var autocomplete = new google.maps.places.Autocomplete(input, options);
        autocomplete.bindTo('bounds', map);
        google.maps.event.addListener(autocomplete, 'place_changed', function() {
            var place = autocomplete.getPlace();
            marker.setVisible(false);
            marker.setPosition(place.geometry.location);
            marker.setVisible(true);     
        });
    });
}

google.maps.event.addDomListener(window, 'load', function(){
    initialize();
});
