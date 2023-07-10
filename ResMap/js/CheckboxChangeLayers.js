
function changeLayerVisibilityFixedPoints() {

    if (document.getElementById("checkboxPointsFixes").checked === false) {
        pointsLayer.setVisible(false);
    };
    if (document.getElementById("checkboxPointsFixes").checked === true) {
        pointsLayer.setVisible(true);
    }; 
};

function changeLayerVisibilityVariablePoints() {

    if (document.getElementById("checkboxPointsNouv").checked === false) {
        pointsVariableLayer.setVisible(false);
    };
    if (document.getElementById("checkboxPointsNouv").checked === true) {
        pointsVariableLayer.setVisible(true);
    };
};

function changeLayerVisibilityNotCalculatedPoints(){

    if (document.getElementById("checkboxPointsNotCalculated").checked === false) {
        notCalculatedPointsLayer.setVisible(false);
    };
    if (document.getElementById("checkboxPointsNotCalculated").checked === true) {
        notCalculatedPointsLayer.setVisible(true);
    };

};

function changeLayerVisibilityDistances() {

    if (document.getElementById("checkboxDistances").checked === false) {
        distanceLayer.setVisible(false);
    };
    if (document.getElementById("checkboxDistances").checked === true) {
        distanceLayer.setVisible(true);
    };
};


function changeLayerVisibilityDirections() {

    if (document.getElementById("checkboxDirections").checked === false) {
        directionLayer.setVisible(false);
    };
    if (document.getElementById("checkboxDirections").checked === true) {
        directionLayer.setVisible(true);
    };
};


function changeLayerVisibilityEllipses() {

    if (document.getElementById("checkboxEllipses").checked === false) {
        ellipseLayer.setVisible(false);
    };
    if (document.getElementById("checkboxEllipses").checked === true) {
        ellipseLayer.setVisible(true);
    };
};


function changeLayerVisibilityEllipsesRela() {

    if (document.getElementById("checkboxEllipsesRela").checked === false) {
        ellipseRelaLayer.setVisible(false);
    };
    if (document.getElementById("checkboxEllipsesRela").checked === true) {
        ellipseRelaLayer.setVisible(true);
    };
};



function changeLayerVisibilityRectangles() {

    if (document.getElementById("checkboxRectangles").checked === false) {
        rectangleLayer.setVisible(false);
    };
    if (document.getElementById("checkboxRectangles").checked === true) {
        rectangleLayer.setVisible(true);
    };
};



function changeLayerVisibilityRectanglesRela() {

    if (document.getElementById("checkboxRectanglesRela").checked === false) {
        rectangleRelaLayer.setVisible(false);
    };
    if (document.getElementById("checkboxRectanglesRela").checked === true) {
        rectangleRelaLayer.setVisible(true);
    };
};



function changeLayerVisibilityGnss() {

    if (document.getElementById("checkboxGnss").checked === false) {
        gnssLayer.setVisible(false);
    };
    if (document.getElementById("checkboxGnss").checked === true) {
        gnssLayer.setVisible(true);
    };
};


function changeLayerVisibilitySysLoc() {

    if (document.getElementById("checkboxSysLoc").checked === false) {
        sysLocLayer.setVisible(false);
    };
    if (document.getElementById("checkboxSysLoc").checked === true) {
        sysLocLayer.setVisible(true);
    };
};


function changeLayerVisibilityCotes() {

    if (document.getElementById("checkboxCotes").checked === false) {
        cotesLayer.setVisible(false);
    };
    if (document.getElementById("checkboxCotes").checked === true) {
        cotesLayer.setVisible(true);
    };
};

function changeLayerVisibilityAlignement() {

    if (document.getElementById("checkboxAlignement").checked === false) {
        alignementLayer.setVisible(false);
    };
    if (document.getElementById("checkboxAlignement").checked === true) {
        alignementLayer.setVisible(true);
    };
};

function changeLayerVisibilityPerpendiculaire() {

    if (document.getElementById("checkboxPerpendiculaire").checked === false) {
        perpendicularLayer.setVisible(false);
    };
    if (document.getElementById("checkboxPerpendiculaire").checked === true) {
        perpendicularLayer.setVisible(true);
    };
};





function changeLayerVisibilityCoordE() {

    if (document.getElementById("checkboxCoordE").checked === false) {
        obsCoordELayer.setVisible(false);
    };
    if (document.getElementById("checkboxCoordE").checked === true) {
        obsCoordELayer.setVisible(true);
    };
};


function changeLayerVisibilityCoordN() {

    if (document.getElementById("checkboxCoordN").checked === false) {
        obsCoordNLayer.setVisible(false);
    };
    if (document.getElementById("checkboxCoordN").checked === true) {
        obsCoordNLayer.setVisible(true);
    };
};


function changeLayerVisibilityFiabLoc() {
    
    if (document.getElementById("checkboxFiabLoc").checked === false) {
        fiabLocalLayer.setVisible(false);
    };
    if (document.getElementById("checkboxFiabLoc").checked === true) {
        fiabLocalLayer.setVisible(true);
        document.getElementById("checkboxResidusNormes").checked = false;
        document.getElementById("checkboxDistances").checked = false;
        document.getElementById("checkboxDirections").checked = false;
        if (xmlDoc.getElementsByTagName("biggestWi").length != 0) {  // seulement si pas pré-analyse
            wiLayer.setVisible(false);
        };
        distanceLayer.setVisible(false);
        directionLayer.setVisible(false);
    };
};


function changeLayerVisibilityWi() {
    
    if (document.getElementById("checkboxResidusNormes").checked === false) {
        wiLayer.setVisible(false);
    };
    if (document.getElementById("checkboxResidusNormes").checked === true) {
        wiLayer.setVisible(true);
        document.getElementById("checkboxFiabLoc").checked = false;
        document.getElementById("checkboxDistances").checked = false;
        document.getElementById("checkboxDirections").checked = false;
        fiabLocalLayer.setVisible(false);
        distanceLayer.setVisible(false);
        directionLayer.setVisible(false);
        
    };
};


function changeLayerVisibilityVect() {
    
    if (document.getElementById("checkboxVect").checked === false) {
        vectLayer.setVisible(false);
    };
    if (document.getElementById("checkboxVect").checked === true) {
        vectLayer.setVisible(true);
    };
};

function changeLayerVisibilityVectPF() {
    
    if (document.getElementById("checkboxVectRattach").checked === false) {
        vectLayerPF.setVisible(false);
    };
    if (document.getElementById("checkboxVectRattach").checked === true) {
        vectLayerPF.setVisible(true);
    };
};







function changeLayerVisibilityTextFixedPoints() {

    if (document.getElementById("checkboxPointsFixesNo").checked === true) {

        map.removeLayer(pointsLayer);
        delete pointsLayer;

        pointsLayer = new ol.layer.Vector({
            source: fixedPointsSource,
            // Si le point est à cacher on lui attribue le style avec ou sans opacité
            style:  function (feature) {
                        if (!listePtsToHide.includes(feature.getId())){
                            stylePointsFixedLayer.getText().setText(feature.getId());
                            return stylePointsFixedLayer; 
                        } else {
                            stylePointsFixedLayerWithOpacity.getText().setText(feature.getId());
                            return stylePointsFixedLayerWithOpacity;
                            }
                    }         
        });
        pointsLayer.setZIndex(99);
        changeLayerVisibilityFixedPoints();
        map.addLayer(pointsLayer);
    };

    if (document.getElementById("checkboxPointsFixesNo").checked === false) {

        map.removeLayer(pointsLayer);
        delete pointsLayer;

        pointsLayer = new ol.layer.Vector({
            source: fixedPointsSource,
            // Si le point est à cacher on lui attribue le style avec ou sans opacité
            style:  function (feature) {
                        if (!listePtsToHide.includes(feature.getId())){
                            stylePointsFixedLayer.getText().setText(" ");
                            return stylePointsFixedLayer; 
                        } else {
                            stylePointsFixedLayerWithOpacity.getText().setText(" ");
                            return stylePointsFixedLayerWithOpacity;
                            }
                    }         
        });
        pointsLayer.setZIndex(99);
        changeLayerVisibilityFixedPoints();
        map.addLayer(pointsLayer);
    };

};







function changeLayerVisibilityTextVariablePoints() {


    if (document.getElementById("checkboxPointsVariableNo").checked === true) {

        map.removeLayer(pointsVariableLayer);
        delete pointsVariableLayer;

        pointsVariableLayer = new ol.layer.Vector({
            source: variablesPointsSource,
            // Si le point est à cacher on lui attribue le style avec ou sans opacité
            style:  function (feature) {
                        if (!listePtsToHide.includes(feature.getId())){
                            stylePointsVariableLayer.getText().setText(feature.getId());
                            return stylePointsVariableLayer; 
                        } else {
                            styleVariablePointsWithOpacity.getText().setText(feature.getId());
                            return styleVariablePointsWithOpacity;
                            }
                    }         
        });
        pointsVariableLayer.setZIndex(90);
        changeLayerVisibilityVariablePoints();
        map.addLayer(pointsVariableLayer);
        
    };

    if (document.getElementById("checkboxPointsVariableNo").checked === false) {

        map.removeLayer(pointsVariableLayer);
        delete pointsVariableLayer;

        pointsVariableLayer = new ol.layer.Vector({
            source: variablesPointsSource,
            // Si le point est à cacher on lui attribue le style avec ou sans opacité
            style:  function (feature) {
                        if (!listePtsToHide.includes(feature.getId())){
                            stylePointsVariableLayer.getText().setText(" ");
                            return stylePointsVariableLayer; 
                        } else {
                            styleVariablePointsWithOpacity.getText().setText(" ");
                            return styleVariablePointsWithOpacity;
                            }
                    }         
        });
        pointsVariableLayer.setZIndex(90);
        changeLayerVisibilityVariablePoints();
        map.addLayer(pointsVariableLayer);
    };





};







function changeLayerVisibilityTextNotCalculatedPoints() {


    if (document.getElementById("checkboxPointsNotCalculatedNo").checked === true) {

        map.removeLayer(notCalculatedPointsLayer);
        delete notCalculatedPointsLayer;

        notCalculatedPointsLayer = new ol.layer.Vector({
            source: notCalculatedPointsSource,
            // Si le point est à cacher on lui attribue le style avec ou sans opacité
            style:  function (feature) {
                        if (!listePtsToHide.includes(feature.getId())){
                            stylePointsNotCalculatedPoints.getText().setText(feature.getId());
                            return stylePointsNotCalculatedPoints; 
                        } else {
                            stylePointsNotCalculatedPointsWithOpacity.getText().setText(feature.getId());
                            return stylePointsNotCalculatedPointsWithOpacity;
                            }
                    }         
        });
        notCalculatedPointsLayer.setZIndex(95);
        changeLayerVisibilityNotCalculatedPoints();
        map.addLayer(notCalculatedPointsLayer);
    };

    if (document.getElementById("checkboxPointsNotCalculatedNo").checked === false) {

        map.removeLayer(notCalculatedPointsLayer);
        delete notCalculatedPointsLayer;

        notCalculatedPointsLayer = new ol.layer.Vector({
            source: notCalculatedPointsSource,
            // Si le point est à cacher on lui attribue le style avec ou sans opacité
            style:  function (feature) {
                        if (!listePtsToHide.includes(feature.getId())){
                            stylePointsNotCalculatedPoints.getText().setText(" ");
                            return stylePointsNotCalculatedPoints; 
                        } else {
                            stylePointsNotCalculatedPointsWithOpacity.getText().setText(" ");
                            return stylePointsNotCalculatedPointsWithOpacity;
                            }
                    }         
        });
        notCalculatedPointsLayer.setZIndex(95);
        changeLayerVisibilityNotCalculatedPoints();
        map.addLayer(notCalculatedPointsLayer);


    };
    
};