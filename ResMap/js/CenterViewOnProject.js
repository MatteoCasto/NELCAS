listCoordsProject = []

function logMapElements(value, key, map) {
    listCoordsProject.push(value);
};

function centerViewOnProject(listAllPoints,URLstr) {

    if (URLstr.split('#map=')[1] == undefined) {
    // Function that sets  view and zoom on the zone of the project (mean of coords)
        listAllPoints.forEach(logMapElements);
        extentProject = ol.extent.boundingExtent(listCoordsProject);
        bufferProject = ol.extent.buffer(extentProject,0);
        view.fit(bufferProject)
    };
};

function centerViewOnURL(URLstr) {
    // Function that sets view and zoom on the zone of the URL
    if (URLstr.split('#map=')[1] != undefined) {
        let params = URLstr.split('#map=')[1]
        let coord = [parseFloat(params.split('/')[0]),parseFloat(params.split('/')[1])]
        let zoom = parseFloat(params.split('/')[2])
        view.setCenter(coord);
        view.setZoom(zoom)
    };
};




function centerViewOnPoint(){
    // Function that sets the current view on the point describe in the input field id="inputPointSearch"
    let noPointToSearch = document.getElementById("inputPointSearch").value;
    // Parcours de tous les points et stockage des correspondances
    let listeFound = [];
    for (i = 0; i < pointList.length; i++) {
        // Condition de recherche
        if(pointList[i]['pointName'].includes(noPointToSearch)){
            listeFound.push(pointList[i])
        };
    

    };
    for (i = 0; i < listeFound.length; i++) {
        view.setCenter([parseFloat(listeFound[i]['E']), parseFloat(listeFound[i]['N'])]);
        view.setZoom(25); 
        return // s'arrête à la 1ere itération (possibilité de fonctionnalité qui fait "next" en prenant le point d'après)
    };
};