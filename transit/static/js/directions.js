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

}

(function(){
    initialize();
})();
