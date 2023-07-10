
// Initialisation du popUp et ajout en Overlay sur la map
const element = document.getElementById('popup');
const popup = new ol.Overlay({
  element: element,
  positioning: 'bottom-center',
  stopEvent: false,
});
map.addOverlay(popup);


// display popup on click (event)
map.on('click', function (evt) {
  const feature = map.forEachFeatureAtPixel(evt.pixel, function (feature) {
    return feature;
  });
  $(element).popover('dispose'); 

  // Si on a bien cliquer à proximité d'une feature
  if (feature) {

    
    //Récupérer les propriétés des obs. de distances et directions
    if (feature.getProperties().properties.includes('RI') || feature.getProperties().properties.includes('DP') ) {
      let noObsStr =   feature.getProperties().properties.split('/')[0];
      let typeObsStr = feature.getProperties().properties.split('/')[1];
      let ziStr =      feature.getProperties().properties.split('/')[2];
      let wiStr =      String(parseFloat(feature.getProperties().properties.split('/')[3]).toFixed(2));
      let nablaStr =   feature.getProperties().properties.split('/')[4];
      let viStr =      feature.getProperties().properties.split('/')[5];

      if (viStr.length <= 4) { // Si préanalyse, pas de v
          viStr="-";
      };
      if (wiStr == "NaN") { // si préanalyse ou zi=0%
          wiStr="-";
      };

      if (typeObsStr == "RI" | typeObsStr == "DP") { // Uniq. pour dir. et distances

          // Position du popup au coords du clic
          popup.setPosition(evt.coordinate);

          // Création du popUp
          $(element).popover({
              placement: 'top',
              html: true,
              content: `
              <div class="popUpTitre">Obs n° &nbsp;&nbsp;${noObsStr}</div>
              <div class="popUpTitre">Type &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;${typeObsStr}</div>
              <hr>
              <div>zi &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;${ziStr}</div>
              <div>wi &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;${wiStr}</div>
              <div>∇li &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;${nablaStr}</div>
              <div>v &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;${viStr}</div>
              `
              });
          
          $(element).popover('show');
      };

    // CLIC SUR UN POINT
    } else if (feature.getProperties().properties.includes('Point fixe') || 
               feature.getProperties().properties.includes('Point nouveau')) {

      let typePt = feature.getProperties().properties.split('/')[0];
      let noPt =   feature.getProperties().properties.split('/')[1];
      let elemsPlani = feature.getProperties().properties.split('/')[2];
      let E = feature.getProperties().properties.split('/')[3];
      let N = feature.getProperties().properties.split('/')[4];

      // POINTS FIXES
      if(typePt == 'Point fixe'){

        // Position du popup au coords du clic
        popup.setPosition(evt.coordinate);
        // Création du popUp
        $(element).popover({
            placement: 'top',
            html: true,
            content: `
            <div class="popUpTitre">Type &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;${typePt}</div>
            <div class="popUpTitre">Nom&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;${noPt}</div>
            <hr>
            <div>Elem. plani. &nbsp;&nbsp;&nbsp;${elemsPlani}</div>
            <div>E &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;${E}</div>
            <div>N &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;${N}</div>
             `
            });
        $(element).popover('show');
      };

      // POINTS NOUVEAUX
      if(typePt == 'Point nouveau'){

        // indicateurs
        let a = feature.getProperties().properties.split('/')[5];
        let NA = feature.getProperties().properties.split('/')[6];
        let idObsRespNA = feature.getProperties().properties.split('/')[7];
        let dE = feature.getProperties().properties.split('/')[8];
        let dN = feature.getProperties().properties.split('/')[9];

        // Position du popup au coords du clic
        popup.setPosition(evt.coordinate);
        // Création du popUp
        $(element).popover({
            placement: 'top',
            html: true,
            content: `
            <div class="popUpTitre">Type &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;${typePt}</div>
            <div class="popUpTitre">Nom&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;${noPt}</div>
            <hr>
            <div>Elem. plani. &nbsp;&nbsp;&nbsp;${elemsPlani}</div>
            <div>E &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;${E}</div>
            <div>N &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;${N}</div>
            <div>EMA 1σ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;${a}</div>
            <div>NA&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;${NA}</div>
            <div>idRespNA&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;${idObsRespNA}</div>
            <div>dE&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;${dE}</div>
            <div>dN&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;${dN}</div>
            `
            });
        $(element).popover('show');
      };





      
    } else if (feature.getProperties().properties.includes('LY,LX')){
      console.log(feature.getProperties().properties)

    }


  } else { // Si on ne clique pas sur une feature -> coordonnée du clic 
        
        // Position du popup au coords du clic
        popup.setPosition(evt.coordinate);
        evtStr = String(evt.coordinate);
        let E = String(parseFloat(evtStr.split(",")[0]).toFixed(1));
        let N = String(parseFloat(evtStr.split(",")[1]).toFixed(1));
        let coordsStr = E+"&nbsp;&nbsp;"+N;

        // Création du popUp
        $(element).popover({
            placement: 'top',
            html: true,
            content: `
            <div>${coordsStr}</div>
            `
        });

    $(element).popover('show');
  }
});


// Close the popup when the map is moved
map.on('movestart', function () {
  $(element).popover('dispose');
});


