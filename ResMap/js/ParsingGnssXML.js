function parsingGNSS(jsonRes) {

    /* 

    This function parses the PRNx file (XML) to get
    all the GNSS sessions, add them to the map
    and style them with forms and/or color

    INPUT: XML toparse, coming from fr.result (FileReader method)
    OUPUT: None

    */

    // Récupération des éléments des balises <station> 
    if (jsonRes['network']['gnss']) {
        sessionsList = jsonRes['network']['gnss']['session']
        sessionsList = [].concat(sessionsList);
    } else {return }; // sinon fin de la fonction

    

    // Initialisation du Vector Source
    let gnssSource = new ol.source.Vector({});
    let gnssStyle = new ol.style.Style({});
    let listPointsLeves = [] // -> savoir si un point est relevé plus d'une fois (2 pentagones dans ce cas)

    // Parcourir les sessions
    for (let i = 0; i < sessionsList.length; i++) {
    
        let sessionGNSS = sessionsList[i];
        let listObs = sessionGNSS['measure'];
        let radius = 0.08;

        for (let j = 0; j < listObs.length; j++) {

            let noVis = listObs[j]['pointName'];
            
            // Si le point n'existe pas, ne pas l'ajouter
            if(listAllPoints.has(noVis)){

                let E_Vis = listAllPoints.get(noVis)[0];
                let N_Vis = listAllPoints.get(noVis)[1];
                let coordArray_i = [ E_Vis,N_Vis ] ;
                
                // Création d'une Feature ol pour chaque point de la session GNSS et ajout à la source
                featurePointGnss = new ol.Feature({
                    geometry: new ol.geom.Point(coordArray_i),
                    name: noVis,
                    properties: "A IMPLEMENTER",
                });
                gnssStyle = new ol.style.Style({
                    // stroke: new ol.style.Stroke({ color: listColorSession[sessionNo], width: 4}),
                    image: new ol.style.Icon(/** @type {olx.style.IconOptions} */ ({
                        src: './img/Pentagon_bleu_simple.svg',
                        scale: radius,
                        opacity: 1.0
                    })),
                });
                // Si point relevé 2 fois ou plus, deux polygones
                if (listPointsLeves.includes(noVis)){
                    gnssStyle = new ol.style.Style({
                        // stroke: new ol.style.Stroke({ color: listColorSession[sessionNo], width: 4}),
                        image: new ol.style.Icon(/** @type {olx.style.IconOptions} */ ({
                            src: './img/Pentagon_bleu_double.svg',
                            scale: radius,
                            opacity: 1.0
                        })),
                    });
                };
                listPointsLeves.push(noVis)
                featurePointGnss.setStyle(gnssStyle);

                if (listObs[j]['LY']['discarded'] != 'true' || listObs[j]['LX']['discarded'] != 'true'){
                    gnssSource.addFeature(featurePointGnss);
                };
            };

        };
    };


    gnssLayer = new ol.layer.Vector({
        source: gnssSource,
        style: gnssStyle,
        opacity: 1.0,
    });


    map.addLayer(gnssLayer);
    changeLayerVisibilityGnss();
    gnssLayer.setZIndex(80);
    console.log("GNSS sessions has been added to map");

    


    


    
    










};


