function parsingCotesXML(jsonRes) {

  /* 

  This function parses the PRNx file (XML) to get
  all the points from the projects (approximate coordinates)
  and add them on the ol map

  INPUT: XML toparse, coming from fr.result (FileReader method)
  OUPUT: None
  
  */


  // Récupération des éléments des balises <station> 
  if (jsonRes['network']['simpleMeasures']){
    CotesListe = jsonRes['network']['simpleMeasures']['simpleMeasure'];
    CotesListe = [].concat(CotesListe);
  } else {return}
  


  // Création du layer distance et de sa source
  cotesLayer = new ol.layer.Vector({});
  coteLineSource = new ol.source.Vector({});


  for (i = 0; i < CotesListe.length; i++) {

    let no1 = CotesListe[i]['measure']['pointName1'];
    let no2 = CotesListe[i]['measure']['pointName2'];

    // Si un des points n'existe pas, ne pas l'ajouter
    if(listAllPoints.has(no1) && listAllPoints.has(no2)){
      let E_1 = listAllPoints.get(no1)[0];
      let N_1 = listAllPoints.get(no1)[1];
      let E_2 = listAllPoints.get(no2)[0];
      let N_2 = listAllPoints.get(no2)[1];

      // Création de la feature pour la symbologie de distance (sinon transparent pour obs. supp)
      // Figurer uiniquement les cotes non-écartées
      if (CotesListe[i]['measure']['DP']['discarded'] != "true"){
        featureCote = new ol.Feature({
          geometry: new ol.geom.LineString([[E_1,N_1],[E_2,N_2]]),
          properties: "A IMPLEMENTER",
        });
        coteStyle = new ol.style.Style({
          stroke:  new ol.style.Stroke({ color: '#FFCD00', width: 3 })
        });
        featureCote.setStyle(coteStyle);
        coteLineSource.addFeature(featureCote);
      };
    };
  };


  // création du layer
  cotesLayer.setSource(coteLineSource);
  map.addLayer(cotesLayer);
  cotesLayer.setVisible(false);
  console.log("Simple measures have been added to map")

  // Passer en dessous du reste 
  cotesLayer.setZIndex(2);

  




  


  







};
