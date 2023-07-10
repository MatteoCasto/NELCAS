//  Définition d'une variable globale
//  qui donne la liste des points à masquer (et leurs indicateurs)
listePtsToHide = []





function applyFilter() {

    /**
     Fonction qui lance l'application du filtre.
     Elle poermet de remplir la liste des no de points à masquer.
     S'active au clic sur "Ajouter"
     */


    let filtreSur = document.getElementById("filtreSur").value;
    let filtreOperateur = document.getElementById("filtreOperateur").value;
    let filtreValeur = document.getElementById("filtreValeur").value;



    // Filtre sur la taille des ellipses d'EM
    if (filtreSur == 'demi-grand axe a [mm]') {
        filtreSurIndicateur(ellipseLayer, filtreOperateur, parseFloat(filtreValeur));

        // Ajout à la liste des filtres actifs
        remplirFiltresActifs('demi-grand axe a [mm]', filtreOperateur, filtreValeur)
        // adapter panel au contenu
        adaptPanelToContent();

        

    };

    // ----- Filtre sur la taille des vecteurs de fiab. ext. NA
    if (filtreSur == 'vecteurs NA [mm]') {
        filtreSurIndicateur(rectangleLayer, filtreOperateur, parseFloat(filtreValeur));

        // Ajout à la liste des filtres actifs
        remplirFiltresActifs('vecteurs NA [mm]', filtreOperateur, filtreValeur)
        // adapter panel au contenu
        adaptPanelToContent();
    };
1
    // ---- Filtre sur la taille des vecteurs dE/dN pts nouveaux
    if (filtreSur == 'vecteurs dE/dN [mm]') {
        filtreSurIndicateur(vectLayer, filtreOperateur, parseFloat(filtreValeur));

        // Ajout à la liste des filtres actifs
        remplirFiltresActifs('vecteurs dE/dN [mm]', filtreOperateur, filtreValeur)
        // adapter panel au contenu
        adaptPanelToContent();
    };


    hidePtsFromList();


};




function filtreSurIndicateur (layerToFilter, filtreOperateur, filtreValeur, filtreASupp = false) {

    /**Fonction qui parcours chaque entité de la couche en input (couche d'indic. = ellipses et vect.)
    et tester la valeur de a [mm].
    Si elle ne satisfait pas au filtre, la fonction d'ajoute à la 
    liste globale des points à masquer. **/

    // Liste utile pour la suppression des points concernés par un filtre
    let listePts = [];

    // parcourir les entitié des filtres d'indicateurs (en input)
    layerToFilter.getSource().forEachFeature(function (feature) {

        // récupérer valeur en mm (sans la mention "mm")
        let val = parseFloat(feature.get('properties').split('/')[0].split('mm')[0]);

        // pour les vecteurs NA, si infini, attribuer une grande valeur
        // -> les faire apparaître sans alourdir le code
        if (val=="inf."){
            val = 999999999
        };

        // Opérateur "="
        if (filtreOperateur == '='){
            if (val != filtreValeur && val != undefined && val != null){
                // Ajotuer le no de pt à la var. globale des points à cacher
                listePtsToHide.push(feature.get('id'))
                listePts.push(feature.get('id')); // Si on on supprimer le filtre 
            };
        };

        // Opérateur >=
        if (filtreOperateur == "≥"){
            if (val < filtreValeur && val != undefined && val != null){
                // Ajotuer le no de pt à la var. globale des points à cacher
                listePtsToHide.push(feature.get('id'))
                listePts.push(feature.get('id')); // Si on on supprimer le filtre 
            };
        };

        // Opérateur <=
        if (filtreOperateur == "≤"){
            if (val > filtreValeur && val != undefined && val != null){
                // Ajotuer le no de pt à la var. globale des points à cacher
                listePtsToHide.push(feature.get('id'))
                listePts.push(feature.get('id')); // Si on on supprimer le filtre 

            };
        };


    });

    // si pour une suppression du filtre (réafficher ces points)
    if (filtreASupp){
        return listePts
    };
  
};









function remplirFiltresActifs(nomFiltre, op, val){

    // Ajout à la liste des filtres actifs (a, b, c -> String)
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
    let cell1 = newRow.insertCell();
    cell1.innerText = nomFiltre;
    let cell2 = newRow.insertCell();
    cell2.innerText = op;
    let cell3 = newRow.insertCell();
    cell3.innerText = val;
};






function viderFiltresActifs() {

    // Vider le tableau des filtres actifs
    let table = document.getElementById('listeFiltresActifs')
    let rowCount = table.rows.length;
    for (let i = rowCount - 1; i > 0; i--) {
        table.deleteRow(i);
    }



}


function deleteAllFilters(){

    listePtsToHide = []; // vider la liste des pts à cacher
    hidePtsFromList();
    viderFiltresActifs();
    adaptPanelToContent();
}





function removeItem(array, item) {

    // supprime toutes les occurence d'un element dans une liste
    let i = array.length;
    while (i--) {
      if (array[i] === item) {
        array.splice(i, 1);
      }
    }
  }
  





function deleteOneFilter(btn){

    
    // récupérer index de la ligne du bouton cliqué
    let row = btn.parentNode.parentNode;
    let rowIndex = row.rowIndex; // avec en-tête comprise

    // suprrimer la ligne à l'index du tableau des filtres actifs
    let table = document.getElementById('listeFiltresActifs');



    // récupération des éléments du filtre à supprimer
    let typeFiltre = row.cells[1].innerText;
    let filtreOperateur = row.cells[2].innerText;
    let filtreValeur = row.cells[3].innerText;

    // Détermination des points à ré-afficher par type de filtre, op. et val.
    if (typeFiltre == 'demi-grand axe a [mm]'){

        // récupérer les points concernés par ce filtre pour les ré-afficher
        listePtsAreafficher = filtreSurIndicateur (ellipseLayer, filtreOperateur, filtreValeur, true)
        
        // suppression des pts à cacher
        listePtsToHide = listePtsAreafficher.filter( function( el ) {
            return !listePtsAreafficher.includes( el );
        } );
        hidePtsFromList();
        



    } else if (typeFiltre == 'vecteurs NA [mm]'){

        // récupérer les points concernés par ce filtre pour les ré-afficher
        listePtsAreafficher = filtreSurIndicateur (rectangleLayer, filtreOperateur, filtreValeur, true)
    
    } else if (typeFiltre == 'vecteurs dE/dN [mm]'){

        // récupérer les points concernés par ce filtre pour les ré-afficher
        listePtsAreafficher1 = filtreSurIndicateur (vectLayer, filtreOperateur, filtreValeur, true)
        listePtsAreafficher2 = filtreSurIndicateur (vectLayerPF, filtreOperateur, filtreValeur, true)

        // fusion des 2 listes (vect PF et pts nouv.)
        listePtsAreafficher = listePtsAreafficher1.concat(listePtsAreafficher2)
    };


    





    // supprimer de la liste déroulante des filtres
    table.deleteRow(rowIndex);


    

    

    


    


    

    
    



};









function hidePtsFromList(){

    hideIndicatorsOfHiddenPoints(pointsVariableLayer);
    hideIndicatorsOfHiddenPoints(pointsLayer);
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



function schowIndicatorsOfPoints(layer, listePtsAreafficher){

    // parcourir toutes les features d'un layer d'indicateur et réaffiche selon la
    // suppression d'un filtre

    layer.getSource().forEachFeature(function (feature) {

        // Si le no de pt rattaché à l'indicateur est présent dans la 
        // liste des pts à réafficher
        let id = feature.get('id'); // id = no de pt
        if (listePtsAreafficher.includes(id)){
            console.log(id)
            feature.setStyle(null);
        };
    });
};



function adaptPanelToContent(){

    // Fonction simple qui permet d'apater la hauteur
    // du left panel (filtre) à son contenu
    let panel = document.getElementById('leftPanel');
    panel.style.maxHeight = panel.scrollHeight + "1px"; 

}


















    // if (filtreSur == "type"){ // balise <type> à compléter pour permettre une sélection
    //     layerFilter(pointsVariableLayer, 10);
    //     layerFilter(pointsLayer, 5);
    //     layerFilter(ellipseLayer, 1);
    //     layerFilter(rectangleLayer, 1);
    //     layerFilter(vectLayer, 1);
    //     layerFilter(vectLayerPF, 1);
    // }







    // function layerFilter(filterLayer, i) {

    //     /**  
    //     filterLayer : Layer à filter
    //     i : indice où se trouve l'élément à filter dans "properties" de la feature
        
    //     Cette fonction permet de gérer l'affichage des éléments selon le filtre appliqué
    //     sur un layer en argument.
    
    //     **/
    
    
    
    //     // parcourir toutes les features de layer
    //     filterLayer.getSource().forEachFeature(function (feature) {
    
    //         // get la propriété
    //         let type = feature.get('properties').split('/')[i]
    
    //         // Si un filtre est sélectionné (autre que '-')
    //         if (document.getElementById("filtreType").value != '-'){
    
    //             if (type != document.getElementById("filtreType").value) {
    //                 feature.setStyle(new ol.style.Style({}));
    //             } else {
    //                 feature.setStyle(null);
    //             };
            
    //         // Sinon on revient à tout afficher
    //         } else {
    //             feature.setStyle(null);
    //         };
        
    
    //     });
    
    
    
    // };


    



















