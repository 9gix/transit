function initialize(){
    var opt = {
        center: new google.maps.LatLng(1.35188,103.820114),
        zoom: 11,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map(document.getElementById('map'), opt);

    var kmlLayersArray = [];

    function addKmlLayer(serv_no_serv_dir) {
        kmlLayer = new google.maps.KmlLayer('http://dqbug.com/static/kml/'+serv_no_serv_dir+'.kml');
        kmlLayer.setMap(map);
        kmlLayersArray.push(kmlLayer);
    }

    function deleteKmlLayer(serv_no_serv_dir){
        url = 'http://dqbug.com/static/kml/'+serv_no_serv_dir+'.kml';
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

    var options = {
        componentRestrictions: {country: 'sg'}
    };
    var markerA = new google.maps.Marker({
        map: map
    });
    var markerB = new google.maps.Marker({
        map: map
    });


    var input_from = $('#id_direction_from')[0];
    var input_to = $('#id_direction_to')[0];
    var autocomplete_from = new google.maps.places.Autocomplete(input_from, options);
    var autocomplete_to = new google.maps.places.Autocomplete(input_to, options);
    autocomplete_from.bindTo('bounds', map);
    autocomplete_to.bindTo('bounds', map);
    google.maps.event.addListener(autocomplete_from, 'place_changed', function() {
        var place = autocomplete_from.getPlace();
        markerA.setVisible(false);
        markerA.setPosition(place.geometry.location);
        markerA.setVisible(true);     
        $('#geo_from').val(place.geometry.location);
    });
    google.maps.event.addListener(autocomplete_to, 'place_changed', function() {
        var place = autocomplete_to.getPlace();
        markerB.setVisible(false);
        markerB.setPosition(place.geometry.location);
        markerB.setVisible(true);     
        $('#geo_to').val(place.geometry.location);
    });
    var geo_from = $('#geo_from').val();
    geo_from = geo_from.replace('(','').replace(')','').split(',');
    geo_from = new google.maps.LatLng(geo_from[0], geo_from[1]);

    var geo_to = $('#geo_to').val();
    geo_to = geo_to.replace('(','').replace(')','').split(',');
    geo_to = new google.maps.LatLng(geo_to[0], geo_to[1]);

    markerA.setPosition(geo_from);
    markerB.setPosition(geo_to);
    markerA.setVisible(true);     
    markerB.setVisible(true);     
}

google.maps.event.addDomListener(window, 'load', function(){
    initialize();
});
