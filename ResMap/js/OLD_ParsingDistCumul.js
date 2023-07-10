function parsingDistCumulXML(xmlToParse) {

    // Récupération des éléments des balises <station> 
    let levesSpeciauxMO = xmlDoc.getElementsByTagName("levesSpeciauxMO")[0];
    let leveSpecialList = levesSpeciauxMO.getElementsByTagName("leveSpecial");

    // obtenir la topologie de chaque levé ortho
    let topologieAllDistCumul = [];
    for (i = 0; i < leveSpecialList.length; i++) {
        typeLeve = leveSpecialList[i].getAttribute("typeLeve");
        if (typeLeve == "DISTANCES CUMUL") {
            let leveXml = leveSpecialList[i];
            let ptsXmlList = leveXml.getElementsByTagName('point')
            let topologieLeve = [];
            for (j = 0; j < ptsXmlList.length; j++) {
                ptName = ptsXmlList[j].getAttribute('name')
                topologieLeve.push(ptName)
            };
            topologieAllDistCumul.push(topologieLeve)
        };
    };

    // Création du layer levé ortho
    distCumulLayer = new ol.layer.Vector({});

    // création de la source du layer pour l'ajout des géomètries
    distCumulSource = new ol.source.Vector({});

    // ajout de la géométrie de chaque levé ortho
    for (i = 0; i < topologieAllDistCumul.length; i++) {
        let topologieDistCumul  = topologieAllDistCumul[i]
        let geometryDistCumul = [];
        for (j = 0; j < topologieDistCumul.length; j++){
            let E = parseFloat(listAllPoints.get(topologieDistCumul[j])[0])
            let N = parseFloat(listAllPoints.get(topologieDistCumul[j])[1])
            geometryDistCumul.push([E,N])
        };
        // Création de la feature 
        let featureDistCumul = new ol.Feature({
            geometry: new ol.geom.LineString(geometryDistCumul),
        });
        // Ajout de la feature à la Source
        distCumulSource.addFeature(featureDistCumul);
    };

    // Création du style rectangles
    let styleDistCumul = new ol.style.Style({
        stroke: new ol.style.Stroke({ color: '#F443FF', width: 4, lineDash: [7,7] }),
    });

    // ajout à la carte
    distCumulLayer.setSource(distCumulSource);
    distCumulLayer.setStyle(styleDistCumul);
    distCumulLayer.setOpacity(100.0)
    distCumulLayer.setZIndex(5);
    distCumulLayer.setVisible(false);
    map.addLayer(distCumulLayer);
    console.log("Distances cumulées ont été ajoutés à la carte")


}