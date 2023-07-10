function parsingGNSS(xmlToParse) {

    /* 

    This function parses the PRNx file (XML) to get
    all the GNSS sessions, add them to the map
    and style them with forms and/or color

    INPUT: XML toparse, coming from fr.result (FileReader method)
    OUPUT: None

    */

    
    let planimetricAbriss = xmlDoc.getElementsByTagName("planimetricAbriss")[0];
    let stationsList = planimetricAbriss.getElementsByTagName("sessionGNSS");
    
    // Initialisation du Vector Source
    let gnssSource = new ol.source.Vector({});
    let gnssStyle = new ol.style.Style({});
    let sessionNo = 0
    let listPointsLeves = []

    // Récupérer les numéros de points de chaque session GNSS et les stocker dans une liste (listPointsNameOfSession)
    for (let i = 0; i < stationsList.length; i++) {
        
        if (stationsList[i].getAttribute("typeLeve") == "sessionGNSS") {
            let sessionGNSS = stationsList[i];
            let listObs = sessionGNSS.getElementsByTagName("obs");
            let Listradius = [0.08,0.10];
            let listColorSession = ["#0164FF"];
            
            for (let j = 0; j < listObs.length; j++) {
                if (listObs[j].getAttribute("obsType") === "LY") { // uniq. une fois (si LY, alors LX aussi)
                    let pointName_i = listObs[j].getAttribute("target");
                    let E = listAllPoints.get(pointName_i)[0];
                    let N = listAllPoints.get(pointName_i)[1];
                    
                    // Création d'une Feature ol pour chaque point de la session GNSS et ajout à la source
                    featurePointGnss = new ol.Feature({
                        geometry: new ol.geom.Point([parseFloat(E), parseFloat(N)]),
                        name: pointName_i,
                        properties: "Session n° " + "A IMPLEMENTER" + "/" ,
                    });
                    gnssStyle = new ol.style.Style({
                        // stroke: new ol.style.Stroke({ color: listColorSession[sessionNo], width: 4}),
                        image: new ol.style.Icon(/** @type {olx.style.IconOptions} */ ({
                            src: './img/Pentagon_bleu_simple.svg',
                            scale: Listradius[0],
                            opacity: 1.0
                        })),
                    });
                    // Si point relevé 2 fois ou plus, deux polygones
                    if (listPointsLeves.includes(pointName_i)){
                        gnssStyle = new ol.style.Style({
                            // stroke: new ol.style.Stroke({ color: listColorSession[sessionNo], width: 4}),
                            image: new ol.style.Icon(/** @type {olx.style.IconOptions} */ ({
                                src: './img/Pentagon_bleu_double.svg',
                                scale: Listradius[0],
                                opacity: 1.0
                            })),
                        });
                    };
                    listPointsLeves.push(pointName_i)
                    featurePointGnss.setStyle(gnssStyle);
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


