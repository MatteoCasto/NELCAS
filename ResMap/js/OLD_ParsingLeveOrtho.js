function parsingLeveOrthoXML(xmlToParse) {

    // Récupération des éléments des balises <station> 
    let levesSpeciauxMO = xmlDoc.getElementsByTagName("levesSpeciauxMO")[0];
    let leveSpecialList = levesSpeciauxMO.getElementsByTagName("leveSpecial");

    // obtenir la topologie de chaque levé ortho
    let topologieAllLevesOrtho = [];
    for (i = 0; i < leveSpecialList.length; i++) {
        typeLeve = leveSpecialList[i].getAttribute("typeLeve");
        if (typeLeve == "LEVE ORTHO") {
            let leveXml = leveSpecialList[i];
            let ptsXmlList = leveXml.getElementsByTagName('point')
            let topologieLeve = [];
            for (j = 0; j < ptsXmlList.length; j++) {
                ptName = ptsXmlList[j].getAttribute('name')
                if (topologieLeve.includes(ptName) == false) {
                    topologieLeve.push(ptName)
                };
            };
            topologieAllLevesOrtho.push(topologieLeve)
        };
    };
   
    // Création du layer levé ortho
    leveOrthoLayer = new ol.layer.Vector({});

    // création de la source du layer pour l'ajout des géomètries
    leveOrthoSource = new ol.source.Vector({});

    // ajout de la géométrie de chaque levé ortho
    for (i = 0; i < topologieAllLevesOrtho.length; i++) {
        let topologieLeveOrtho  = topologieAllLevesOrtho[i]
        let geometryLeveOrtho = [];
        for (j = 0; j < topologieLeveOrtho.length; j++){
            if(j==0){ // premier et dernier point
                EB = parseFloat(listAllPoints.get(topologieLeveOrtho[j])[0])
                NB = parseFloat(listAllPoints.get(topologieLeveOrtho[j])[1])
                EP = parseFloat(listAllPoints.get(topologieLeveOrtho[topologieLeveOrtho.length-1])[0])
                NP = parseFloat(listAllPoints.get(topologieLeveOrtho[topologieLeveOrtho.length-1])[1])
                vE = EP-EB
                vN = NP-NB
                normV = (vE**2+vN**2)**0.5
                geometryLeveOrtho.push([EB,NB]) // ajout du premier point à la geom
            } else { // autres points à projeter
                EA = parseFloat(listAllPoints.get(topologieLeveOrtho[j])[0])
                NA = parseFloat(listAllPoints.get(topologieLeveOrtho[j])[1])
                BH = ((EA-EB)*vE+(NA-NB)*vN) / (normV)
                EH = EB + (BH/normV)*vE
                NH = NB + (BH/normV)*vN
                geometryLeveOrtho.push([EH,NH]) // ajout du point projeté à la geom
                geometryLeveOrtho.push([EA,NA]) // ajout du point réel
                geometryLeveOrtho.push([EH,NH]) // re-ajout du point projeté à la geom
            }; 
        };
        // Création de la feature 
        let featureLeveOrtho = new ol.Feature({
            geometry: new ol.geom.LineString(geometryLeveOrtho),
        });
        // Ajout de la feature à la Source
        leveOrthoSource.addFeature(featureLeveOrtho);
    };

    // Création du style rectangles
    let styleLeveOrtho = new ol.style.Style({
        stroke: new ol.style.Stroke({ color: '#0006B6', width: 4, lineDash: [7,7] }),
    });

    // ajout à la carte
    leveOrthoLayer.setSource(leveOrthoSource);
    leveOrthoLayer.setStyle(styleLeveOrtho);
    leveOrthoLayer.setOpacity(100.0)
    leveOrthoLayer.setZIndex(5);
    leveOrthoLayer.setVisible(false);
    map.addLayer(leveOrthoLayer);
    console.log("Levés orthogonaux ont été ajoutés à la carte")






};