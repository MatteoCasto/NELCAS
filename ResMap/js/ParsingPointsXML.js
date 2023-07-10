// simple function used to create an array with steps
// between 2 values
function range(start, stop, step){
  step = step || 1;
  var arr = [];
  for (var i=start;i<stop;i+=step){
     arr.push(i);
  }
  return arr;
};


// Fonction utilisée pour la rotation d'array de coordonnées (ellipses) (ATTENTION: gons et sens mathématique (inv. horaire))
function rotatePoint(x, y, centerx, centery, gons) {
  var newx = (x - centerx) * Math.cos(gons * Math.PI / 200) - (y - centery) * Math.sin(gons * Math.PI / 200) + centerx;
  var newy = (x - centerx) * Math.sin(gons * Math.PI / 200) + (y - centery) * Math.cos(gons * Math.PI / 200) + centery;
  return [newx, newy];
}



function parsingPointsXML(jsonRes) {

  /* 

  This function parses the PRNx file (XML) to get
  all the points from the projects
  and add them to the ol map

  INPUT: XML toparse, coming from fr.result (FileReader method)
  OUPUT: [ Id list for fixed points, Id list for variable points ] (2D Array)

  */


  // Récupération des éléments des balises <point> des coordonnées
  pointList = jsonRes['points']['point']

  // Liste des PF pour attribuer la bonne symbologie lors d'une libre-ajustée
  listePF = [];
  try {
    if (jsonRes['globalResults']['planimetry']['stochasticNetwork']){
      for (i = 0; i < jsonRes['globalResults']['planimetry']['stochasticNetwork']['point'].length; i++){
        listePF.push(jsonRes['globalResults']['planimetry']['stochasticNetwork']['point'][i]['pointName'])
      };
    };
  } catch{

  }
  





  // ------- Initialisation des Vector Layer des points nouveaux et fixes ------- 
  fixedPointsSource = new ol.source.Vector({});
  variablesPointsSource = new ol.source.Vector({});
  notCalculatedPointsSource = new ol.source.Vector({});
  pointsListId = []
  listAllPoints = new Map();
  // Points fixes


  

  // ------- Initialisation des Vector Layer des ELLIPSES ------- 
  let ellipsesLineSource = new ol.source.Vector({});

  // ------- Initialisation des Vector Layer des VECTEURS FIAB -------
  let vectorsReliabilityLineSource = new ol.source.Vector({});

  // ------- Initialisation des Vector Layer des DY/DX vecteurs -------
  let vectLineSource = new ol.source.Vector({});
  let vectLineSourcePF = new ol.source.Vector({});


  // Niveau de confiance des ellipes
  let nivConfianceEllipses = "39%";
  let kSigma = 1.0;
  document.getElementById("nivConfiance").textContent = "Niveau de confiance des ellipses → " + String(nivConfianceEllipses)

  

  // Parcours de tous les points 
  for (i = 0; i < pointList.length; i++) {

    // ---- Généralités
    pointName_i = pointList[i]['pointName'];
    E_i = parseFloat(pointList[i]['E']);
    N_i = parseFloat(pointList[i]['N']);
    listAllPoints.set(pointName_i,[E_i,N_i]);

    // détection de balise suuplémentaire pour les proposer dans la liste à choix
    // des éléments
    detectionBalisesSupplPoints(pointList[i]);

    // ---- Indicateurs pour les POINTS NOUVEAUX
    if ( pointList[i]['idUnkE'] != null) {

      // --- ELLIPSES
      a = parseFloat(pointList[i]['stdErrEllipse']['a']); // en [m]
      let b = parseFloat(pointList[i]['stdErrEllipse']['b']); // en [m]
      let gisA = parseFloat(pointList[i]['stdErrEllipse']['bearA']); // en [g]
      // Initialisation des boucles pour création d'ellipses
     let t = range(0, 420, 20);
      let listXYellipse = [];
      t.forEach(alpha => listXYellipse.push( [ a*kSigma*echelleEllipses*Math.cos(alpha*Math.PI/200.0),
                                               b*kSigma*echelleEllipses*Math.sin(alpha*Math.PI/200.0)  ]  ) )

      // t.forEach(gis => listENellipse.push( [parseFloat(a*kSigma*echelleEllipses*Math.cos((gis)*Math.PI/200.0)+E_i),
      //                                       parseFloat(b*kSigma*echelleEllipses*Math.sin((gis)*Math.PI/200.0)+N_i)] ) ) 
      
      listENellipse = []
      for (let j = 0; j < listXYellipse.length; j++){
        let E = rotatePoint(listXYellipse[j][0], listXYellipse[j][1], 0, 0, -gisA + 100)[0] + E_i;
        let N = rotatePoint(listXYellipse[j][0], listXYellipse[j][1], 0, 0, -gisA + 100)[1] + N_i;
        listENellipse.push([E, N]);
      }

      let featureEllipse = new ol.Feature({
        geometry: new ol.geom.LineString(listENellipse),
        id: pointName_i, // rattaché à un pt
        properties: String((a*1000.0).toFixed(1)) + "mm"
                    + '/'+pointName_i,
      })
      gisArad = gisA* Math.PI / 200.0 // en rad

      
      // featureEllipse.getGeometry().rotate(gisArad, [E_i, N_i]);
      ellipsesLineSource.addFeature(featureEllipse);


      // --- VECTEURS DE FIABILITE EXTERNE
      NA = parseFloat(pointList[i]['externalReliabilityPlaniVector']['NA']); // en [m]
      let gisNA = parseFloat(pointList[i]['externalReliabilityPlaniVector']['bearNA']); // en [m]
      idObsRespNA = pointList[i]['externalReliabilityPlaniVector']['idObsRespNA']; // string (identifiant)
      if (isNaN(NA)== false) { // uniquement si une valeur de fiabilité est calculée
        // FLECHES DES VECTEURS
        let Earrow = E_i+echelleEllipses*NA*Math.sin(gisNA*Math.PI/200.0);
        let Narrow = N_i+echelleEllipses*NA*Math.cos(gisNA*Math.PI/200.0);
        // Calcul des éléments pour la flèches  du vecteur [g] et [m]
        let gisArrow1 = gisNA + 200.0 + 50.0;
        let gisArrow2 = gisNA + 200.0 - 50.0;
        let Ea1 = 0.001*echelleEllipses*Math.sin(gisArrow1*Math.PI/200.0) + Earrow;
        let Na1 = 0.001*echelleEllipses*Math.cos(gisArrow1*Math.PI/200.0) + Narrow;
        let Ea2 = 0.001*echelleEllipses*Math.sin(gisArrow2*Math.PI/200.0) + Earrow;
        let Na2 = 0.001*echelleEllipses*Math.cos(gisArrow2*Math.PI/200.0) + Narrow;

        // Coordonnées du vecteur avec la flèche et feature
        let listENvect = [ [E_i,N_i] , [Earrow, Narrow] , [Ea1, Na1] , [Earrow, Narrow] , [Ea2, Na2] ];
        let featureVectorReliability = new ol.Feature({
          geometry: new ol.geom.LineString(listENvect),
          id: pointName_i, // rattaché à un pt
          properties: String((NA*1000.0).toFixed(1)) + "mm"
                      + '/'+pointName_i,
        })
        vectorsReliabilityLineSource.addFeature(featureVectorReliability);
      
      } else { // si NA = NaN (infini)
        // Point et texte "inf"
        let featureVectorReliability = new ol.Feature({
          geometry: new ol.geom.Point([E_i, N_i]),
          id: pointName_i, // rattaché à un pt
          properties: "inf."
                      +'/'+pointName_i,

                     
        })
        vectorsReliabilityLineSource.addFeature(featureVectorReliability);
      };


      // --- VECTEURS DY/DX
      dE = parseFloat(pointList[i]['deltaPlani']['dE']) // en [m]
      dN = parseFloat(pointList[i]['deltaPlani']['dN']) // en [m]
      let norme = (dE**2 + dN**2)**0.5
      let gisVect = (Math.atan2(dE,dN))*200.0/Math.PI; // Gisement du vecteur en [g] (pour dessin flèche)
      if (gisVect<0) {
          gisVect = gisVect + 400.0;
      };
      // Flèche des vecteurs
      let Earrow = E_i+echelleEllipses*dE;
      let Narrow = N_i+echelleEllipses*dN;
      // Calcul des éléments pour la flèches  du vecteur [g] et [m]
      let gisArrow1 = gisVect + 200.0 + 50.0;
      let gisArrow2 = gisVect + 200.0 - 50.0;
      let Ea1 = 0.001*echelleEllipses*Math.sin(gisArrow1*Math.PI/200.0) + Earrow;
      let Na1 = 0.001*echelleEllipses*Math.cos(gisArrow1*Math.PI/200.0) + Narrow;
      let Ea2 = 0.001*echelleEllipses*Math.sin(gisArrow2*Math.PI/200.0) + Earrow;
      let Na2 = 0.001*echelleEllipses*Math.cos(gisArrow2*Math.PI/200.0) + Narrow;
      // Coordonnées du vecteur avec la flèche et feature
      let listENvect = [ [E_i,N_i] , [Earrow, Narrow] , [Ea1, Na1] , [Earrow, Narrow] , [Ea2, Na2] ];
      let featureVectorDYDX = new ol.Feature({
        geometry: new ol.geom.LineString(listENvect),
        id: pointName_i, // rattaché à un pt
        properties: String((norme*1000.0).toFixed(1)) + "mm"
                    +'/'+pointName_i,
      })
      // Vecteurs sur rattachement (PF)
      if ((pointList[i]['idUnkE'] == null && parseFloat(pointList[i]['planimetricElems']) >= 2) || listePF.includes(pointName_i)) {
        vectLineSourcePF.addFeature(featureVectorDYDX);
      // Vecteurs sur points nouveaux
      } else if (parseFloat(pointList[i]['planimetricElems']) >= 2){ 
        vectLineSource.addFeature(featureVectorDYDX);
      };
      
    };

    // Création d'une Feature ol pour Point i (MN95)
    let featurePointMN95 = new ol.Feature({
      geometry: new ol.geom.Point([E_i, N_i]),
      name: pointName_i,
    });

    // Ajout de chaque geom à la source points fixes (si pas de idIncE) (et si il possède bien plus de 2 elemsPlani (vrai PF))
    if ((pointList[i]['idUnkE'] == null && parseFloat(pointList[i]['planimetricElems']) >= 2) || listePF.includes(pointName_i)) {
      featurePointMN95.setId(pointName_i)
      // ajout des proprité pour le popup
      featurePointMN95.setProperties({'properties':'Point fixe/'+pointName_i+
                                      "/"+pointList[i]['planimetricElems']+
                                      '/'+String(E_i)+
                                      '/'+String(N_i)+
                                      '/'+pointName_i})
      // featurePointMN95.setStyle(stylePointsFixedLayer)
      fixedPointsSource.addFeature(featurePointMN95);
      
    
    } else if (parseFloat(pointList[i]['planimetricElems']) >= 2){ 
      // Ajout de chaque geom à la source des points nouveaux
      // ajout des proprité pour le popup
      featurePointMN95.setId(pointName_i)
      featurePointMN95.setProperties({'properties':
        'Point nouveau/'+pointName_i+"/"+pointList[i]['planimetricElems']
        +'/'+String(E_i)+'/'+String(N_i)
        +'/'+String((a*1000).toFixed(1))+' mm'
        +'/'+String((NA*1000).toFixed(1))+' mm' 
        +'/'+idObsRespNA
        +'/'+String((dE*1000).toFixed(1))+' mm' 
        +'/'+String((dN*1000).toFixed(1))+' mm' 
        })
      // featurePointMN95.setStyle(stylePointsVariableLayer)
      variablesPointsSource.addFeature(featurePointMN95);

    };

    // POINTS NON-CALCULES
    if (pointList[i]['idUnkE'] == null && parseFloat(pointList[i]['planimetricElems']) < 2){
      featurePointMN95.setId(pointName_i)
      notCalculatedPointsSource.addFeature(featurePointMN95);
    };

    // POINTS AVANT ESTIMATION
    if (typeFile == 'pointsInput'){
      featurePointMN95.setId(pointName_i)
      variablesPointsSource.addFeature(featurePointMN95);
    };

  };







  // <------ LAYER POINTS FIXES (ou rattachement LA) ------>

  // -> Création du Vector Layer avec les points nouv
  pointsLayer = new ol.layer.Vector({
    source: fixedPointsSource,
    // la propriété style prend un callback qui doit retourner un style qui contient le label du pt
    style: function (feature) {
      // stylePointsFixedLayer.getText().setText(feature.getId());
      return stylePointsFixedLayer;
    },
  });

  // -> Ajout du Vector Layer à la carte
  pointsLayer.setZIndex(99);
  map.addLayer(pointsLayer);
  changeLayerVisibilityFixedPoints();
  changeLayerVisibilityTextFixedPoints();
  console.log("Fixed points has been added to map");






  // <------ LAYER POINTS NOUVEAUX ------>

  // -> Création du Vector Layer avec les points nouv
  pointsVariableLayer = new ol.layer.Vector({
      source: variablesPointsSource,
      //la propriété style prend un callback qui doit retourner un style qui contient le label du pt
      style: function (feature) {
        // stylePointsVariableLayer.getText().setText(feature.getId());
        return stylePointsVariableLayer;
      },
  });

  // Ajout du Vector Layer à la carte
  pointsVariableLayer.setZIndex(90);
  map.addLayer(pointsVariableLayer);
  changeLayerVisibilityVariablePoints();
  changeLayerVisibilityTextVariablePoints();
  console.log("Variable points has been added to map");






 // <------ LAYER POINTS NON-CALCULES ------>

  // -> Création du Vector Layer avec les points nouv
  notCalculatedPointsLayer = new ol.layer.Vector({
      source: notCalculatedPointsSource,
      // la propriété style prend un callback qui doit retourner un style
      style: function (feature) {
        // stylePointsNotCalculatedPoints.getText().setText(feature.getId());
          return stylePointsNotCalculatedPoints;
      },
  });
  // Ajout du Vector Layer à la carte
  map.addLayer(notCalculatedPointsLayer);
  notCalculatedPointsLayer.setZIndex(95);
  changeLayerVisibilityNotCalculatedPoints();
  changeLayerVisibilityTextNotCalculatedPoints();
  console.log("Not calculated points has been added to map");











  // <------ LAYER ELLIPSES ------>

  // Création du style labelText pour demi-grand axe a
  let textStyleEllipse = new ol.style.Text({
    textAlign: "center",
    textBaseline: "middle",
    font: "italic 13px Calibri",
    fill: new ol.style.Fill({
      color: "#FF6BF1"
    }),
    stroke: new ol.style.Stroke({
      color: "#ffffff", width: 3
    }),
    offsetX: -10,
    offsetY: 10,
    rotation: 0,
    placement: "point"
  });

  // Création du style ellipses
  let styleEllipse = new ol.style.Style({
    stroke: new ol.style.Stroke({ color: '#FF6BF1', width: 1 }),
    text: textStyleEllipse
  });

  // Création du Layer ellipses
  ellipseLayer = new ol.layer.Vector({
    source: ellipsesLineSource,
    style: function (feature) { // la propriété style prend un callback qui doit retourner un style
      styleEllipse.getText().setText(feature.get("properties").split('/')[0]); 
      return styleEllipse;
    }
  })

  map.addLayer(ellipseLayer);
  ellipseLayer.setZIndex(89)
  changeLayerVisibilityEllipses()
  // document.getElementById("AffichageEchelleEllipse").textContent = "⤷ Echelle: " + echelleEllipses + ":1";
  console.log("Ellipses have been added to map");






  
  // <------ LAYER VECTEURS FIAB. EXT. ------>

  // Création du style labelText pour demi-grand axe na du rect.
  let textStyleRectangle = new ol.style.Text({
    textAlign: "center",
    textBaseline: "middle",
    font: "italic 13px Calibri",
    fill: new ol.style.Fill({
      color: "#00AD02"
    }),
    stroke: new ol.style.Stroke({
      color: "#ffffff", width: 3
    }),
    offsetX: -10,
    offsetY: 10,
    rotation: 0,
    placement: "point"
  });

  // Création du style rectangles
  let styleRectangle = new ol.style.Style({
    stroke: new ol.style.Stroke({ color: '#00AD02', width: 1 }),
    text: textStyleRectangle
  });

  // Création du Layer rectangles
  rectangleLayer = new ol.layer.Vector({
    source: vectorsReliabilityLineSource,
    style: function (feature) { // la propriété style prend un callback qui doit retourner un style
      styleRectangle.getText().setText(feature.get("properties").split('/')[0]); 
      return styleRectangle;
    }
  });

  map.addLayer(rectangleLayer);
  rectangleLayer.setZIndex(88);
  changeLayerVisibilityRectangles();
  // document.getElementById("AffichageEchelleRectangles").textContent = "⤷ Echelle: " + echelleEllipses + ":1";
  console.log("Rectangles have been added to map");









  // <------ LAYER VECTEURS DE/DN POINTS NOUVEAUX ------>

  // Création du style labelText pour norme du vecteur DY/DX
  let textStyleVect = new ol.style.Text({
    textAlign: "center",
    textBaseline: "middle",
    font: "13px Calibri",
    fill: new ol.style.Fill({
    color: "#FF0000"
    }),
    stroke: new ol.style.Stroke({
    color: "#ffffff", width: 3
    }),
    offsetX: 10,
    offsetY: -10,
    rotation: 0,
    placement: "point"
  });

  // Création du style vecteurs
  let styleVect = new ol.style.Style({
      stroke: new ol.style.Stroke({ color: '#FF0000', width: 1 }),
      text: textStyleVect
  });

  // Création du Layer 
  vectLayer = new ol.layer.Vector({
      source: vectLineSource,
      style: function (feature) { // la propriété style prend un callback qui doit retourner un style
          styleVect.getText().setText(feature.get("properties").split('/')[0]); 
          return styleVect;
      }
  });

  // Ajout à la carte
  map.addLayer(vectLayer);
  vectLayer.setZIndex(10); // en dessous 
  changeLayerVisibilityVect();
  // document.getElementById("AffichageEchelleVect").textContent = "⤷ Echelle: " + echelleEllipses + ":1";
  console.log("Diff. vectors have been added to map");





  // <------ LAYER VECTEURS DE/DN POINTS FIXES ------>

  // Création du style labelText pour norme du vecteur DY/DX
  let textStyleVectPF = new ol.style.Text({
    textAlign: "center",
    textBaseline: "middle",
    font: "13px Calibri",
    fill: new ol.style.Fill({
    color: "#00A2FF"
    }),
    stroke: new ol.style.Stroke({
    color: "#ffffff", width: 3
    }),
    offsetX: 10,
    offsetY: -10,
    rotation: 0,
    placement: "point"
  });

  // Création du style vecteurs
  let styleVectPF = new ol.style.Style({
      stroke: new ol.style.Stroke({ color: '#00A2FF', width: 1 }),
      text: textStyleVectPF
  });

  // Création du Layer 
  vectLayerPF = new ol.layer.Vector({
      source: vectLineSourcePF,
      style: function (feature) { // la propriété style prend un callback qui doit retourner un style
          styleVectPF.getText().setText(feature.get("properties").split('/')[0]); 
          return styleVectPF;
      }
  });

  // Ajout à la carte
  map.addLayer(vectLayerPF);
  vectLayerPF.setZIndex(10); // en dessous 
  changeLayerVisibilityVectPF();
  // document.getElementById("AffichageEchelleVectPF").textContent = "⤷ Echelle: " + echelleEllipses + ":1";
  console.log("Diff. vectors have been added to map");

























    return listAllPoints;
};





  


