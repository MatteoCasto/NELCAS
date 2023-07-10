// Init. de la variable globale non-modifiable des balises par défaut dans le XML résultats
const listeBalisesParDefaut = [
    'pointName',
    'E', 'N', 'H',
    'planimetricElems', 'altimetricElems',
    'idUnkH', 'idUnkE', 'idUnkN',
    'stdErrEllipse', 'externalReliabilityPlaniVector',
    'deltaPlani',
    'altiStdError', 'externalReliabilityAlti',
    'deltaAlti'
]

listeAllBalisesToAdd = []

function detectionBalisesSupplPoints(pointXML){

    /* Cette fonction va parser le fichier XML et proposer des balises à filtrer 
    dans la liste à choix prévue dans les filtres */
    
    // get la liste des balises du point XML
    let listeBalisesDuPt = Object.keys(pointXML);

    // différence entre les 2 arrays (=> balises supplémentaires à proposer)
    let balisesSuppl = listeBalisesDuPt.filter(x => !listeBalisesParDefaut.includes(x));

    
    // Ajouter la balises uniquement si pas déjà présent dans les balises suppl.
    for (let i=0; i < balisesSuppl.length; i++){
        if (listeAllBalisesToAdd.indexOf(balisesSuppl[i]) === -1) {
            listeAllBalisesToAdd.push(balisesSuppl[i])
        };
    };

};


function addSupplBalisesToSelectFilters(){

    // get le "select" des types de filtres
    let select = document.getElementById('filtreSur');

    // Y ajouter les balises supplémentaires
    for (let i=0; i < listeAllBalisesToAdd.length; i++){
        let option = document.createElement("option");
        option.text = listeAllBalisesToAdd[i];
        select.add(option)
    };
};