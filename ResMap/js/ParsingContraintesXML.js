function parsingContraintesXML(jsonRes) {

  /* 

  This function parses the XML file to get
  all the constraints from the project
  and add them on the ol map

  INPUT: JSON (coming from XML parsing) of fusionned results
  OUPUT: None
  
  */


  // Récupération des éléments des balises <station> 
  if (jsonRes['network']['constraints']) {
    contraintesListe = jsonRes['network']['constraints']['constraint']
    contraintesListe = [].concat(contraintesListe);
  } else {return};

  // Création du layer Alignement
  alignementLayer = new ol.layer.Vector({});
  alignementLineSource = new ol.source.Vector({});

  // Création du layer Perpendiculaire
  perpendicularLayer = new ol.layer.Vector({});
  perpendicularLineSource = new ol.source.Vector({});

  for (i = 0; i < contraintesListe.length; i++) {

    // Parcourir les points concernés par la contrainte et récupérer les nom de point
    for (j=0; j < contraintesListe[i]['point'].length; j++) {
      if (contraintesListe[i]['point'][j]['pointTypeInConstraint'] == "A") {
        noA = contraintesListe[i]['point'][j]['pointName'];
      };
      if (contraintesListe[i]['point'][j]['pointTypeInConstraint'] == "B") {
        noB = contraintesListe[i]['point'][j]['pointName'];
      };
      if (contraintesListe[i]['point'][j]['pointTypeInConstraint'] == "P") {
        noP = contraintesListe[i]['point'][j]['pointName'];
      };
    };

    // Si lun des pts n'existe pas, ne pas l'ajouter
    if(listAllPoints.has(noA) && listAllPoints.has(noB) && listAllPoints.has(noP) ){
      let E_A = listAllPoints.get(noA)[0];
      let N_A = listAllPoints.get(noA)[1];
      let E_B = listAllPoints.get(noB)[0];
      let N_B = listAllPoints.get(noB)[1];
      let E_P = listAllPoints.get(noP)[0];
      let N_P = listAllPoints.get(noP)[1];

      if (contraintesListe[i]['discarded'] != 'true'){
        // Création de la feature reliant A, B et P
        featureContrainte = new ol.Feature({
          geometry: new ol.geom.LineString([[E_A,N_A],[E_P,N_P],[E_B,N_B]]),
          properties: "A IMPLEMENTER",
        });
        // Création d'un cercle du point P
        featurePointP = new ol.Feature({
          geometry: new ol.geom.Point([E_P,N_P]),
          name: "P",
          properties: "A IMPLEMENTER",
          });

        // Styles pour les 2 types de contraintes
        alignementPointPstyle = new ol.style.Style({
          image: new ol.style.Circle({
            radius: 15, 
            stroke: new ol.style.Stroke({
            color: '#00DF00', width: 4 
            })
          })
        });
        perpendicularPointPstyle = new ol.style.Style({
          image: new ol.style.Circle({
            radius: 10, 
            stroke: new ol.style.Stroke({
            color: '#BA00DF', width: 5 
            })
          })
        });
        alignementStyle = new ol.style.Style({
          stroke:  new ol.style.Stroke({ color: '#00DF00', width: 4 })
        });
        perpendicularStyle = new ol.style.Style({
          stroke:  new ol.style.Stroke({ color: '#BA00DF', width: 7 })
        });

        // Coloration dépend du type
        if (contraintesListe[i]['constraintType'] == "alignment") {
          featureContrainte.setStyle(alignementStyle);
          featurePointP.setStyle(alignementPointPstyle);
          alignementLineSource.addFeature(featureContrainte);
          alignementLineSource.addFeature(featurePointP);
        };
        if (contraintesListe[i]['constraintType'] == "perpendicular") {
          featureContrainte.setStyle(perpendicularStyle);
          featurePointP.setStyle(perpendicularPointPstyle);
          perpendicularLineSource.addFeature(featureContrainte);
          perpendicularLineSource.addFeature(featurePointP);
        }; 
      };
    };
  };

  // création du layer Alignement
  alignementLayer.setSource(alignementLineSource);
  map.addLayer(alignementLayer);
  alignementLayer.setVisible(false);
  console.log("Alignement constraints have been added to map")
  alignementLayer.setZIndex(20);

  // création du layer Perpendiculaire
  perpendicularLayer.setSource(perpendicularLineSource);
  map.addLayer(perpendicularLayer);
  perpendicularLayer.setVisible(false);
  console.log("Perpendicular constraints have been added to map")
  perpendicularLayer.setZIndex(18);


};
