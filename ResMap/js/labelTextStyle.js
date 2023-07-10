 
//  // <------ POINTS NOUVEAUX ----->
 
 // Création du style labelText pt nouv
 textStyleVariablePoints = new ol.style.Text({
    textAlign: "center",
    textBaseline: "middle",
    font: "bold 13px Calibri",
    fill: new ol.style.Fill({
      color: "red"
    }),
    stroke: new ol.style.Stroke({
      color: "#ffffff", width: 3
    }),
    offsetX: 20.0,
    offsetY: -10.0,
    rotation: 0
});
// Création du style de Layer pour points nouveaux
stylePointsVariableLayer = new ol.style.Style({
    image: new ol.style.Icon(/** @type {olx.style.IconOptions} */ ({
    src: './img/redDot_icon.png',
    scale: '0.005',
})),
    text: textStyleVariablePoints,
});


// >>>>>> VERSION OPACITY=0.2

// Création du style labelText pt nouv AVEC opacité
textStyleVariablePointsWithOpacity = new ol.style.Text({
    textAlign: "center",
    textBaseline: "middle",
    font: "bold 13px Calibri",
    fill: new ol.style.Fill({
        color: 'rgba(255, 0, 0, 0.2)'
    }),
    stroke: new ol.style.Stroke({
        color: "#ffffff", width: 3
    }),
    offsetX: 20.0,
    offsetY: -10.0,
    rotation: 0
});
// Style AVEC opacité de l'icone
styleVariablePointsWithOpacity = new ol.style.Style({
    image: new ol.style.Icon(/** @type {olx.style.IconOptions} */ ({
        src: './img/redDot_icon.png',
        scale: '0.005',
        opacity: '0.2'
    })),
    text: textStyleVariablePointsWithOpacity,
});











// <------ POINTS FIXES ------>

// Création du style labelText pt fixe
textStyleFixedPoints = new ol.style.Text({
textAlign: "center",
textBaseline: "middle",
font: "bold 13px Calibri",
fill: new ol.style.Fill({
    color: "blue"
}),
stroke: new ol.style.Stroke({
    color: "#ffffff", width: 3
}),
offsetX: 25.0,
offsetY: -15.0,
rotation: 0
});
// Création du style de Layer pour points fixes
stylePointsFixedLayer = new ol.style.Style({
    image: new ol.style.Icon(/** @type {olx.style.IconOptions} */ ({
    src: './img/blueTriangle.png',
    scale: '0.06',
    })),
    text: textStyleFixedPoints,
});


// >>>>>> VERSION OPACITY=0.2

// Création du style labelText pt fixe
textStyleFixedPointsWithOpacity = new ol.style.Text({
    textAlign: "center",
    textBaseline: "middle",
    font: "bold 13px Calibri",
    fill: new ol.style.Fill({
        color: 'rgba(0, 0, 255, 0.2)'
    }),
    stroke: new ol.style.Stroke({
        color: "#ffffff", width: 3
    }),
    offsetX: 25.0,
    offsetY: -15.0,
    rotation: 0
    });
    // Création du style de Layer pour points fixes
    stylePointsFixedLayerWithOpacity = new ol.style.Style({
        image: new ol.style.Icon(/** @type {olx.style.IconOptions} */ ({
        src: './img/blueTriangle.png',
        scale: '0.06',
        opacity: '0.2'
        })),
        text: textStyleFixedPointsWithOpacity,
    });











  // <------ POINTS NON-CALCULES ------>

// Création du style labelText pt nouv
textStyleNotCalculatedPoints = new ol.style.Text({
    textAlign: "center",
    textBaseline: "middle",
    font: "bold 13px Calibri",
    fill: new ol.style.Fill({
      color: "rgba(112, 48, 160)"
    }),
    stroke: new ol.style.Stroke({
      color: "#ffffff", width: 3
    }),
    offsetX: 25.0,
    offsetY: -15.0,
    rotation: 0
  });
// Création du style de Layer pour points variables
stylePointsNotCalculatedPoints = new ol.style.Style({
      image: new ol.style.Icon(/** @type {olx.style.IconOptions} */ ({
      src: './img/purpleCross.png',
      scale: '0.04',
    })),
    text: textStyleNotCalculatedPoints,
  });


  // >>>>>> VERSION AVEC OPACITE=0.2

// Création du style labelText pt nouv
textStyleNotCalculatedPointsWithOpacity = new ol.style.Text({
    textAlign: "center",
    textBaseline: "middle",
    font: "bold 13px Calibri",
    fill: new ol.style.Fill({
        color: "rgba(112, 48, 160, 0.2)"
    }),
    stroke: new ol.style.Stroke({
        color: "#ffffff", width: 3
    }),
    offsetX: 25.0,
    offsetY: -15.0,
    rotation: 0
    });
    // Création du style de Layer pour points variables
    stylePointsNotCalculatedPointsWithOpacity = new ol.style.Style({
        image: new ol.style.Icon(/** @type {olx.style.IconOptions} */ ({
        src: './img/purpleCross.png',
        scale: '0.04',
        opacity: '0.2'
    })),
    text: textStyleNotCalculatedPointsWithOpacity,
    });

















