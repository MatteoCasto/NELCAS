function parsingViseesXML(jsonRes) {

  /* 

  This function parses the PRNx file (XML) to get
  all the points from the projects (approximate coordinates)
  and add them on the ol map

  INPUT: XML toparse, coming from fr.result (FileReader method)
  OUPUT: None
  
  */


  // Récupération des éléments des balises <station> 
  if (jsonRes['network']['polar']){
    stationsList = jsonRes['network']['polar']['station'];
    stationsList = [].concat(stationsList);
  } else {return};

  // Création du layer distance et de sa source
  distanceLayer = new ol.layer.Vector({});
  distanceLineSource = new ol.source.Vector({});
  // Création du layer distance
  directionLayer = new ol.layer.Vector({});
  directionLineSource = new ol.source.Vector({});


  for (i = 0; i < stationsList.length; i++) {

    let noSt = stationsList[i]['stationName'];

    // Si la station n'existe pas, ne pas l'ajouter (ni ses visées)
    if (listAllPoints.has(noSt)){

      let E_st = listAllPoints.get(noSt)[0];
      let N_st = listAllPoints.get(noSt)[1];
      
      let listObs = stationsList[i]['stationData']['measure'];

      for (j = 0; j < listObs.length; j++) {

        let noVis = listObs[j]['pointName'];

        // Si le point n'existe pas, ne pas l'ajouter
        if(listAllPoints.has(noVis)){

          let E_Vis = listAllPoints.get(noVis)[0];
          let N_Vis = listAllPoints.get(noVis)[1];
          let coordArray_i = [ [E_st,N_st], [E_Vis,N_Vis] ];


          // ---- DISTANCES ----.
          // Si après estimation
          if (listObs[j]['DP']){
            DP = listObs[j]['DP'];
          } else if (listObs[j]['DS']){ // Si avant estimation
            DP = listObs[j]['DS'];
          } 
          let DP_zi = DP['zi'];
          let DP_noObs = DP['idObsPlani'];
          let DP_ecarte = DP['discarded'];
          let DP_wi = DP['wi'];
          let DP_nabla_rzi = DP['nablaLi'];
          let DP_vi = DP['vi'];
          
          

          // calculs pour faire figurer les traits épais de 10% à 20% du vecteur
          let dE_inf = (coordArray_i[1][0] - coordArray_i[0][0])*0.1
          let dE_sup = (coordArray_i[1][0] - coordArray_i[0][0])*0.2
          let dN_inf = (coordArray_i[1][1] - coordArray_i[0][1])*0.1
          let dN_sup = (coordArray_i[1][1] - coordArray_i[0][1])*0.2
          let coordArray_i_epais = [ [dE_inf+coordArray_i[0][0] , dN_inf+coordArray_i[0][1]] ,
                                    [dE_sup+coordArray_i[0][0] , dN_sup+coordArray_i[0][1]] ];

          // Création de la feature pour la symbologie de distance (sinon transparent pour obs. supp)
          featureDistanceEpais = new ol.Feature({
            geometry: new ol.geom.LineString(coordArray_i_epais),
            properties: DP_noObs + "/DP/" + (DP_zi*100).toFixed(1) + " %" + "/" + DP_wi + "/" + (DP_nabla_rzi*1000).toFixed(1) + " mm" + "/" + DP_vi*1000 + " mm"// "noObs/dist//zi/wi/nabla_rzi/v"
          });
          if (DP_ecarte != "true") { // si l'obs n'est pas écartée
            featureDistanceEpais.setStyle( new ol.style.Style({
              stroke: new ol.style.Stroke({ color: '#000000', width: 5, lineCap: "square" })
            }) )
          } else { // si obs. supp.
            featureDistanceEpais.setStyle( new ol.style.Style({
              stroke: new ol.style.Stroke({ color: 'rgba(0, 0, 0, 0.0)', width: 0})
              }) )
          };

          // Ajout des features
          let featureDistance = new ol.Feature({
            geometry: new ol.geom.LineString(coordArray_i),
            properties: DP_noObs + "/DP/" + (DP_zi*100).toFixed(1) + " %" + "/" + DP_wi + "/" + (DP_nabla_rzi*1000).toFixed(1) + " mm" + "/" + DP_vi*1000 + " mm"// "noObs/dist//zi/wi/nabla_rzi/v"
          });
          if (DP_ecarte == "true") { // si l'obs. est écartée
            distanceStyle = new ol.style.Style({
              stroke: new ol.style.Stroke({ color: 'rgba(0, 0, 0, 0.0)', width: 0, })
            });
            // nbObsSuppr += 1;
          } else { // Si l'obs a un numéro = elle est gardée
            distanceStyle = new ol.style.Style({
              stroke: new ol.style.Stroke({ color: '#000000', width: 1 })
            });
          };
          featureDistance.setStyle(distanceStyle);
          distanceLineSource.addFeature(featureDistance);
          distanceLineSource.addFeature(featureDistanceEpais);
          
          





          // ---- DIRECTIONS ----

          let RI = listObs[j]['RI'];
          let RI_zi = RI['zi'];
          let RI_noObs = RI['idObsPlani'];
          let RI_ecarte = RI['discarded'];
          let RI_wi = RI['wi'];
          let RI_nabla_rzi = RI['nablaLi'];
          let RI_vi = RI['vi'];

          // Calculs pour faire figurer les traits pleins jusqu'à 70% de la visée
          let RI_dE_sup = (coordArray_i[1][0] - coordArray_i[0][0])*0.7
          let RI_dN_sup = (coordArray_i[1][1] - coordArray_i[0][1])*0.7
          let coordArray_i_plein = [ [RI_dE_sup+coordArray_i[0][0],RI_dN_sup+coordArray_i[0][1]] ,
                                  [coordArray_i[0][0],coordArray_i[0][1]] ];

          // Création de la feature pour la symbologie de direction (trait plein)
          let featureDirPlein = new ol.Feature({
            geometry: new ol.geom.LineString(coordArray_i_plein),
            properties: RI_noObs + "/RI/" + (RI_zi*100).toFixed(1) + " %" + "/" + RI_wi + "/" + (RI_nabla_rzi*10000).toFixed(1) + " cc" + "/" + RI_vi*1000 + " cc"// "noObs/dir//zi/wi/nabla_rzi/v"
          });
          if (RI_ecarte != "true") {
            featureDirPlein.setStyle( new ol.style.Style({
              stroke: new ol.style.Stroke({ color: '#717171', width: 1 })
              }) )
          } else {
            featureDirPlein.setStyle( new ol.style.Style({
              stroke: new ol.style.Stroke({ color: 'rgba(0, 0, 0, 0.0)', width: 0 })
              }) )
          };
          // Création de la feature pour une direction (traittillés)
          let featureDirection = new ol.Feature({
            geometry: new ol.geom.LineString(coordArray_i),
            properties: RI_noObs + "/RI/" + (RI_zi*100).toFixed(1) + " %" + "/" + RI_wi + "/" + (RI_nabla_rzi*10000).toFixed(1) + " cc" + "/" + RI_vi*1000 + " cc"// "noObs/dir//zi/wi/nabla_rzi/v"
          });
          if (RI_ecarte == "true") { // si l'obs. a pas de numéro, elle sera transparente
            directionStyle = new ol.style.Style({
              stroke: new ol.style.Stroke({ color: 'rgba(0, 0, 0, 0.0)', width: 0, })
            });
            // nbObsSuppr += 1;
          }
          else { // Si l'obs a un numéro = elle est figurée normalement
            directionStyle = new ol.style.Style({
              stroke: new ol.style.Stroke({ color: '#717171', width: 1, lineDash: [15,7]})
            });
          };


          featureDirection.setStyle(directionStyle);
          directionLineSource.addFeature(featureDirection);
          directionLineSource.addFeature(featureDirPlein);
          




        };
      };
    };

  };

  // création des layers dist. et dir.
  distanceLayer.setSource(distanceLineSource);
  map.addLayer(distanceLayer);
  distanceLayer.setVisible(false);
  console.log("Distances have been added to map")

  directionLayer.setSource(directionLineSource);
  map.addLayer(directionLayer);
  directionLayer.setVisible(false)
  console.log("Directions have been added to map")

  // Passer en dessous du reste (dist. au dessus des dir.)
  distanceLayer.setZIndex(2);
  directionLayer.setZIndex(1);

  




  


  







};
