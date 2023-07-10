listePtsToHide = [];


function addFilter(){

    // Ajout à la liste des filtres actifs (a, b, c -> String)

    let nomFiltre= document.getElementById('filtreSur').value
    let op = document.getElementById('filtreOperateur').value
    let val = document.getElementById('filtreValeur').value

    let table = document.getElementById('listeFiltresActifs')
    let newRow = table.insertRow(-1);
    
    // Bouton "retirer le filtre"
    let cell0 = newRow.insertCell();
    cell0.innerHTML = `
    <button class="btn btn-outline-secondary btn-sm py-0 px-1" 
    onclick="deleteOneFilter(this)">
    X
    </button>
    `
    // Remplissage du reste des tableaux des filtres
    let cell1 = newRow.insertCell();
    cell1.innerText = nomFiltre;
    let cell2 = newRow.insertCell();
    cell2.innerText = op;
    let cell3 = newRow.insertCell();
    cell3.innerText = val;

    adaptPanelToContent();
    updateFilter();
    

};



function adaptPanelToContent(){

    // Fonction simple qui permet d'apater la hauteur
    // du left panel (filtre) à son contenu
    let panel = document.getElementById('leftPanel');
    panel.style.maxHeight = panel.scrollHeight + "1px"; 

};


function updateFilter(){

    // init. liste des no de points à masquer (var globale)
    listePtsToHide = [];
    hidePtsFromList(); // réaffiche rapidement tous les pts précédents


    // get le tableau des filtres
    let table = document.getElementById('listeFiltresActifs');

    for (let i = 1, row; row = table.rows[i]; i++) {  // i=1 pour pas prendre en-tête
        
        let nomFiltre = row.cells[1].innerText;
        let op = row.cells[2].innerText;
        let val = row.cells[3].innerText;

        // get la liste des pts à masquer
        if (nomFiltre == "demi-grand axe a [mm]"){
            filtreSurIndicateur (ellipseLayer, op, val);
        } else if (nomFiltre == "vecteurs NA [mm]"){
            filtreSurIndicateur (rectangleLayer, op, val);
        } else if (nomFiltre == "vecteurs dE/dN [mm]"){
            filtreSurIndicateur (vectLayer, op, val);
            filtreSurIndicateur (vectLayerPF, op, val);


        // filtres sémantiques sur les balises ad-hoc
        } else {
            filtreSurBalises(nomFiltre, op, val);
        };

    };

    listePtsToHide = Array.from(new Set(listePtsToHide)); // no de pts apparaissent une seule fois
    
    // Cacher les points concernés par les filtres actifs après update
    hidePtsFromList();

    // Opacité des points cachés (uniqument les couches de pts nouveaux et fixes, pas les indic.)
    setOpacityOfHiddenPoints();
}



function filtreSurIndicateur (layerToFilter, filtreOperateur, filtreValeur) {

    /**Fonction qui parcours chaque entité de la couche en input (couche d'indic. = ellipses et vect.)
    et tester la valeur [mm].
    Si elle ne satisfait pas au filtre, la fonction d'ajoute à la 
    liste des points à masquer. **/


    // Tester la valeur en float -> sinon NaN et aucun point de satisfait le filtre
    let filtreValeurFloat = parseFloat(filtreValeur);

    // parcourir les entitié des filtres d'indicateurs (en input)
    layerToFilter.getSource().forEachFeature(function (feature) {

        // récupérer valeur en mm (sans la mention "mm")
        let val = parseFloat(feature.get('properties').split('/')[0].split('mm')[0]);
        
        // pour les vecteurs NA, si infini, attribuer une grande valeur
        // -> les faire apparaître sans alourdir le code
        if (val=="inf."){
            val = 99999999999
        };

        // Opérateur "="
        if (filtreOperateur == '='){
            if (val != filtreValeurFloat || isNaN(filtreValeurFloat) || isNaN(val) ){
                // Ajotuer le no de pt à la var. globale des points à cacher
                listePtsToHide.push(feature.get('id'))
            };
        };

        // Opérateur >=
        if (filtreOperateur == "≥"){
            if (val < filtreValeurFloat || isNaN(filtreValeurFloat) || isNaN(val) ){
                // Ajotuer le no de pt à la var. globale des points à cacher
                listePtsToHide.push(feature.get('id'))
            };
        };

        // Opérateur <=
        if (filtreOperateur == "≤"){
            if (val > filtreValeurFloat || isNaN(filtreValeurFloat) || isNaN(val) ){
                // Ajotuer le no de pt à la var. globale des points à cacher
                listePtsToHide.push(feature.get('id'))
            };
        };
    });
};



function filtreSurBalises(typeFilter, filtreOperateur, filtreValeur){

    // Récupération des éléments des balises <point> des coordonnées
    for (let i = 0; i < pointList.length; i++) {

        // ---- get les balises du point
        let pointName = pointList[i]['pointName']; 

        // get les balises ad-hoc du point (éléments en communs des 2 listes)
        let listeAllBalisesDuPt = Object.keys(pointList[i]);
        let balisesSupplDuPt = listeAllBalisesDuPt.filter(x => !listeBalisesParDefaut.includes(x));
        baliseFound = false

        for (let j = 0; j < balisesSupplDuPt.length; j++){

            
            let balise = balisesSupplDuPt[j];
            if (balise == typeFilter){

                baliseFound = true
                
                // val. dans XML
                let valeurBalise = pointList[i][balise];
        
                // Opérateur "=" 
                if (filtreOperateur == '='){
                    if (valeurBalise != filtreValeur ){
                        // Ajotuer le no de pt à la var. globale des points à cacher
                        listePtsToHide.push(pointName);
                    };
                };

                // Opérateur ">=" 
                if (filtreOperateur == '≥'){
                    if (valeurBalise < filtreValeur){
                        // Ajotuer le no de pt à la var. globale des points à cacher
                        listePtsToHide.push(pointName);
                    };
                };

                // Opérateur "<=" 
                if (filtreOperateur == '≤'){
                    if (valeurBalise > filtreValeur){
                        // Ajotuer le no de pt à la var. globale des points à cacher
                        listePtsToHide.push(pointName);
                    };
                };

            };  
        };

        if (baliseFound == false){ // cacher le point si pas de balise trouvée pour le test
            listePtsToHide.push(pointName);
        }

    };
    
};








function hidePtsFromList(){

    hideIndicatorsOfHiddenPoints(ellipseLayer);
    hideIndicatorsOfHiddenPoints(rectangleLayer);
    hideIndicatorsOfHiddenPoints(vectLayer);
    hideIndicatorsOfHiddenPoints(vectLayerPF);
};


function hideIndicatorsOfHiddenPoints(layer){

    // parcourir toutes les features d'un layer d'indicateur et cache selon la 
    // liste global des pts à cacher

    layer.getSource().forEachFeature(function (feature) {

        // Si le no de pt rattaché à l'indicateur est présent dans la 
        // liste des pts à cacher (no de pt stocké en dernier dans les properties)
        let id = feature.get('id'); // id = no de pt
        if (listePtsToHide.includes(id)){

            // Cacher l'entité
            feature.setStyle(new ol.style.Style({}));

        } else {
            feature.setStyle(null);
        }
    });
};



function viderFiltresActifs() {

    // Vider le tableau des filtres actifs
    let table = document.getElementById('listeFiltresActifs')
    let rowCount = table.rows.length;
    for (let i = rowCount - 1; i > 0; i--) {
        table.deleteRow(i);
    };

    // réafficher tout
    listePtsToHide = [];
    adaptPanelToContent();
    hidePtsFromList();
    setOpacityOfHiddenPoints();
};






function deleteOneFilter(btn){

    // récupérer index de la ligne du bouton cliqué
    let row = btn.parentNode.parentNode;
    let rowIndex = row.rowIndex; // avec en-tête comprise

    // suprrimer la ligne à l'index du tableau des filtres actifs
    let table = document.getElementById('listeFiltresActifs');

    // supprimer de la liste déroulante des filtres
    table.deleteRow(rowIndex);

    adaptPanelToContent();
    updateFilter();

};


function setOpacityOfHiddenPoints(){



    // ---- POINTS NOUVEAUX ----
    // on réinitialise le layer des pts pour un nouveau style
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
    // Ajout du Vector Layer à la carte
    pointsVariableLayer.setZIndex(90);
    map.addLayer(pointsVariableLayer);
    changeLayerVisibilityVariablePoints();
    changeLayerVisibilityTextVariablePoints();




    // ---- POINTS FIXES (ou rattach. en LA) ----
    // on   réinitialise le layer des pts pour un nouveau style
    map.removeLayer(pointsLayer);
    delete pointsLayer;

    pointsLayer = new ol.layer.Vector({
        source: fixedPointsSource,
        // Si le point est à cacher on lui attribue le style avec ou sans opacité
        style:  function (feature) {
                    if  (!listePtsToHide.includes(feature.getId())){
                        stylePointsFixedLayer.getText().setText(feature.getId());
                        return stylePointsFixedLayer; 
                    } else {
                        stylePointsFixedLayerWithOpacity.getText().setText(feature.getId());
                        return stylePointsFixedLayerWithOpacity;
                        }
                }         
    });
    // -> Ajout du Vector Layer à la carte
    pointsLayer.setZIndex(99);
    map.addLayer(pointsLayer);
    changeLayerVisibilityFixedPoints();
    changeLayerVisibilityTextFixedPoints();




    // ---- POINTS NON-CALCULES ----
    // on   réinitialise le layer des pts pour un nouveau style
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
    // Ajout du Vector Layer à la carte
    map.addLayer(notCalculatedPointsLayer);
    notCalculatedPointsLayer.setZIndex(95);
    changeLayerVisibilityNotCalculatedPoints();
    changeLayerVisibilityTextNotCalculatedPoints();



    
};










