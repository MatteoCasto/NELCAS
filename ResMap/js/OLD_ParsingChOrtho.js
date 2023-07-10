function parsingChOrthoXML(xmlToParse) {

    // Récupération des éléments des balises <station> 
    let levesSpeciauxMO = xmlDoc.getElementsByTagName("levesSpeciauxMO")[0];
    let leveSpecialList = levesSpeciauxMO.getElementsByTagName("leveSpecial");
    
    
    // obtenir la topologie de chaque levé ortho
    let topologieAllChOrtho = [];
    for (i = 0; i < leveSpecialList.length; i++) {
        typeLeve = leveSpecialList[i].getAttribute("typeLeve");
        if (typeLeve == "CHEMINEMENT ORTHO") {
            let leveXml = leveSpecialList[i];
            let ptsXmlList = leveXml.getElementsByTagName('point')
            let topologieLeve = [];
            for (j = 0; j < ptsXmlList.length; j++) {
                ptName = ptsXmlList[j].getAttribute('name')
                topologieLeve.push(ptName)
            };
            topologieAllChOrtho.push(topologieLeve)
        };
    };

    // Création du layer levé ortho
    ChOrthoLayer = new ol.layer.Vector({});

    // création de la source du layer pour l'ajout des géomètries
    ChOrthoSource = new ol.source.Vector({});

    // ajout de la géométrie de chaque levé ortho
    for (i = 0; i < topologieAllChOrtho.length; i++) {
        let topologieChOrtho  = topologieAllChOrtho[i]
        let geometryChOrtho = [];
        for (j = 0; j < topologieChOrtho.length; j++){
            let E = parseFloat(listAllPoints.get(topologieChOrtho[j])[0])
            let N = parseFloat(listAllPoints.get(topologieChOrtho[j])[1])
            geometryChOrtho.push([E,N])
        };
        // Création de la feature 
        let featureChOrtho = new ol.Feature({
            geometry: new ol.geom.LineString(geometryChOrtho),
        });
        // Ajout de la feature à la Source
        ChOrthoSource.addFeature(featureChOrtho);

    };

    // Création du style rectangles
    let styleChOrtho = new ol.style.Style({
        stroke: new ol.style.Stroke({ color: '#50C876', width: 4 }),
    });


    ChOrthoLayer.setSource(ChOrthoSource);
    ChOrthoLayer.setStyle(styleChOrtho);
    ChOrthoLayer.setOpacity(100.0)
    ChOrthoLayer.setZIndex(5);
    ChOrthoLayer.setVisible(false);
    map.addLayer(ChOrthoLayer);
    console.log("Cheminements orthogonaux ont été ajoutés à la carte")
        
        





};