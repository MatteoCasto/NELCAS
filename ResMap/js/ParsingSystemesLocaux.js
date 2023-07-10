function getRandomColor() {
    let letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
  }

function getRandomSize(min, max) {
    
    return Math.random() * (max - min + 1) + min;;
  }


function parsingSystemesLocaux(jsonRes) {

    /* 

    This function parses the PRNx file (XML) to get
    all the localSystem sessions, add them to the map
    and style them with forms and/or color

    INPUT: XML toparse, coming from fr.result (FileReader method)
    OUPUT: None

    */

    // Récupération des éléments des balises <station> 
    if (jsonRes['network']['localSystems']){
      
      sessionsList = jsonRes['network']['localSystems']['localSystem'];
      sessionsList = [].concat(sessionsList);
    } else {return}
    

    // Initialisation du Vector Source
    let localSystemSource = new ol.source.Vector({});
    let localSystemStyle = new ol.style.Style({});
    let listPointsLeves = [] // -> savoir si un point est relevé plus d'une fois (2 pentagones dans ce cas)

    // Parcourir les sessions
    for (let i = 0; i < sessionsList.length; i++) {
    
        let colorStyleSession = getRandomColor();
        let sizeStyleSession = getRandomSize(10,20);
        let sessionlocalSystem = sessionsList[i];
        let listObs = sessionlocalSystem['measure'];
        let radius = 0.08;

        for (let j = 0; j < listObs.length; j++) {

          let noVis = listObs[j]['pointName'];
          // Si le point n'existe pas, ne pas l'ajouter
          if(listAllPoints.has(noVis)){
            let E_Vis = listAllPoints.get(noVis)[0];
            let N_Vis = listAllPoints.get(noVis)[1];
            let coordArray_i = [ E_Vis,N_Vis ] ;
            
            // Création d'une Feature ol pour chaque point de la session localSystem et ajout à la source
            featurePointlocalSystem = new ol.Feature({
                geometry: new ol.geom.Point(coordArray_i),
                name: noVis,
                properties: "A IMPLEMENTER",
            });
            localSystemStyle = new ol.style.Style({
                image: new ol.style.Circle({
                    radius: sizeStyleSession, // taille aléatoire par système
                    stroke: new ol.style.Stroke({
                      color: colorStyleSession, width: 4 // couleur aléatoire par système
                    })
                  })
            });
            featurePointlocalSystem.setStyle(localSystemStyle);

            if (listObs[j]['LY']['discarded'] != 'true' || listObs[j]['LX']['discarded'] != 'true'){
              localSystemSource.addFeature(featurePointlocalSystem);
            };
          };

        };
    };

    sysLocLayer = new ol.layer.Vector({
        source: localSystemSource,
        style: localSystemStyle,
        opacity: 1.0,
    });

    map.addLayer(sysLocLayer);
    changeLayerVisibilitySysLoc();
    sysLocLayer.setZIndex(50);
    console.log("Local systems have been added to map");

    


    


    
    










};


