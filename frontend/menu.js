document.getElementById('plotButton').addEventListener('click', () => {
    xSize = parseInt(document.getElementById('xSize').value);
    ySize = parseInt(document.getElementById('ySize').value);
    zSize = parseInt(document.getElementById('zSize').value);

    let base1 = parseInt(document.getElementById('base1').value);
    let base2 = parseInt(document.getElementById('base2').value);
    let base3 = parseInt(document.getElementById('base3').value);
    let base4 = parseInt(document.getElementById('base4').value);
    let base5 = parseInt(document.getElementById('base5').value);

    spread = parseFloat(document.getElementById('spreadPercent').value);
    connection  = parseFloat(document.getElementById('baseConnection').value);
    gamVal = parseFloat(document.getElementById('gamma').value);
    cVal = parseFloat(document.getElementById('c').value);
    lVal = parseFloat(document.getElementById('lambda').value);
    tC = parseFloat(document.getElementById('timeConstant').value);

    initializeArray(base1,base2,base3,base4,base5);
    createGridLines();
    createSpheres();
    
});

document.getElementById('simulateButton').addEventListener('click', () => {
    // Fetch new data every 100 milliseconds
    sendInitialData();
    const left = document.getElementById('hideL');
    const right = document.getElementById('hideR');
    left.classList.toggle('unclickable');
    right.classList.toggle('unclickable');
    const simB = document.getElementById('simulateButton');
    simB.classList.toggle('unclickable');

});

document.getElementById('pauseButton').addEventListener('click', () => {
    pauseSim();
    const graphButton = document.getElementById('openGraphButton');
    graphButton.classList.toggle('unclickable');
});

document.getElementById('resumeButton').addEventListener('click', () => {
    resumeSim();  
    const graphButton = document.getElementById('openGraphButton');
    graphButton.classList.toggle('unclickable');
});

document.getElementById('endButton').addEventListener('click', () => {
    endSim();
    const graphButton = document.getElementById('openGraphButton');
    graphButton.classList.toggle('unclickable');
});

document.getElementById('resetButton').addEventListener('click', () => {
    resetSim();  
    const left = document.getElementById('hideL');
    const right = document.getElementById('hideR');
    left.classList.toggle('unclickable');
    right.classList.toggle('unclickable');
    const graphButton = document.getElementById('openGraphButton');
    graphButton.classList.toggle('unclickable');
    const simB = document.getElementById('simulateButton');
    simB.classList.toggle('unclickable');

    xSize;
    ySize;
    zSize;
    tauArray;
    tauType = 0;
    spread = 0.4;
    connection = 1;
    gamVal = 0;
    cVal = 0;
    lVal = 0;

    intervalID;
    currentTimestep = 0;
    tauOverTime = [];

});

document.getElementById('setButton').addEventListener('click', () => {

    let x1 = parseInt(document.getElementById('x1').value);
    let y1 = parseInt(document.getElementById('y1').value);
    let z1 = parseInt(document.getElementById('z1').value);
    let m11 = parseInt(document.getElementById('m11').value);
    let m12 = parseInt(document.getElementById('m12').value);
    let m13 = parseInt(document.getElementById('m13').value);
    let m14 = parseInt(document.getElementById('m14').value);
    let m15 = parseInt(document.getElementById('m15').value);

    tauArray[x1-1][y1-1][z1-1] = [m11,m12,m13,m14,m15];

    let x2 = parseInt(document.getElementById('x2').value);
    let y2 = parseInt(document.getElementById('y2').value);
    let z2 = parseInt(document.getElementById('z2').value);
    let m21 = parseInt(document.getElementById('m21').value);
    let m22 = parseInt(document.getElementById('m22').value);
    let m23 = parseInt(document.getElementById('m23').value);
    let m24 = parseInt(document.getElementById('m24').value);
    let m25 = parseInt(document.getElementById('m25').value);

    tauArray[x2-1][y2-1][z2-1] = [m21,m22,m23,m24,m25];
    createSpheres();

});