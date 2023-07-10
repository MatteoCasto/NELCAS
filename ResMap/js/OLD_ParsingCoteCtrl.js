function parsingCoteCtrlXML(xmlToParse) {

    // Récupération des éléments des balises <station> 
    let levesSpeciauxMO = xmlDoc.getElementsByTagName("levesSpeciauxMO")[0];
    let leveSpecialList = levesSpeciauxMO.getElementsByTagName("leveSpecial");

    // Création du layer levé ortho
    coteCtrlLayer = new ol.layer.Vector({});

    // création de la source du layer pour l'ajout des géomètries
    coteCtrlSource = new ol.source.Vector({});

    // obtenir la topologie de chaque cote de ctrl
    let topologieAllCotesCtrl = [];
    for (i = 0; i < leveSpecialList.length; i++) {
        typeLeve = leveSpecialList[i].getAttribute("typeLeve");
        if (typeLeve == "COTE CTRL") {
            let leveXml = leveSpecialList[i];
            let pt1Xml = leveXml.getElementsByTagName('point')[0]
            let pt2Xml = leveXml.getElementsByTagName('point')[1]
            let ptName1 = pt1Xml.getAttribute("name")
            let ptName2 = pt2Xml.getAttribute("name")
            let topologieLeve = [ptName1,ptName2];
            topologieAllCotesCtrl.push(topologieLeve)
        };
    };

    
    // Création du layer levé ortho
    coteCtrlLayer = new ol.layer.Vector({});

    // création de la source du layer pour l'ajout des géomètries
    coteCtrlSource = new ol.source.Vector({});

    // ajout de la géométrie de chaque levé ortho
    for (i = 0; i < topologieAllCotesCtrl.length; i++) {
        let topologieCoteCtrl  = topologieAllCotesCtrl[i]
        let geometryCoteCtrl = [];
        for (j = 0; j < topologieCoteCtrl.length; j++){
            let E = parseFloat(listAllPoints.get(topologieCoteCtrl[j])[0])
            let N = parseFloat(listAllPoints.get(topologieCoteCtrl[j])[1])
            geometryCoteCtrl.push([E,N])
        };
        // Création de la feature 
        let featureCoteCtrl = new ol.Feature({
            geometry: new ol.geom.LineString(geometryCoteCtrl),
        });
        // Ajout de la feature à la Source
        coteCtrlSource.addFeature(featureCoteCtrl);
    };

    // Création du style rectangles
    let styleCoteCtrl = new ol.style.Style({
        stroke: new ol.style.Stroke({ color: '#FFC432', width: 4 }),
    });

    coteCtrlLayer.setSource(coteCtrlSource);
    coteCtrlLayer.setStyle(styleCoteCtrl);
    coteCtrlLayer.setOpacity(100.0)
    coteCtrlLayer.setZIndex(0);
    coteCtrlLayer.setVisible(false);
    map.addLayer(coteCtrlLayer);
    console.log("Cotes de contrôle ont été ajoutés à la carte")

};