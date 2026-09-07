let xSize;
let ySize;
let zSize;
let tauArray;
let tauType = 0;
let spread = 0.4;
let connection = 1;
let gamVal = 0;
let cVal = 0;
let lVal = 0;
let tC = 1;

let intervalID;
let currentTimestep = 0;
let tauOverTime = [];


// Initialize a 10x10x10 array
function initializeArray(base1,base2,base3,base4,base5) {
   tauArray = Array.from({ length: xSize }, () =>
        Array.from({ length: ySize }, () =>
            Array.from({ length: zSize }, () => [base1,base2,base3,base4,base5])
        )
    );
}



async function fetchNewData() {
    try {
        const response = await fetch("http://127.0.0.1:5001/simulator", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(1)  // Send a request payload if needed
        });

        if (response.ok) {
            //data has two things ina list: timestep at 0 and 3d array with 5 points at 1
            const res = await response.json();
            
            const timestep = res[0];

            if (timestep > currentTimestep) {
                //changes timestep on screen
                currentTimestep = timestep
                tauArray = res[1];
                tauOverTime.push(tauArray);
                
                const label = document.getElementById("step");
                label.textContent = "Timestep: " + timestep;

                
                createSpheres();
            }
            


            
        } else {
            console.error("Failed to fetch data");
        }
    } catch (err) {
        console.error(err);
    }
}

async function sendInitialData() {

    //sends all needed parameters to python
    let dataDictionary = {
        x:xSize,
        y:ySize,
        z:zSize,
        concentrationArray:tauArray,
        baseConnection: connection,
        spreadPercent: spread,
        gamma: gamVal,
        c: cVal,
        lambda: lVal,
        timeConstant: tC
    }
    try {
        const response = await fetch("http://127.0.0.1:5001/initial", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(dataDictionary)  // Send a request payload if needed
        });

        if (response.ok) {

            //start simulation request loop after recieving confirmation signal of 1
            const res = await response.json()
            tauOverTime.push(tauArray);
            intervalID = setInterval(fetchNewData, 100);
            
            

        } else {
            console.error("Failed to fetch data");
        }
    } catch (err) {
        console.error(err);
    }
}


async function pauseSim() {
    try {
        const response = await fetch("http://127.0.0.1:5001/pause", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(1)  // Send a request payload if needed
        });

        if (response.ok) {

            //pause simulation on frontend
            const result = await response.json();
            if (result==1) {
                clearInterval(intervalID);;
            }
            

        } else {
            console.error("Failed to fetch data");
        }
    } catch (err) {
        console.error(err);
    }

}

async function resumeSim() {

    try {

        //server ip = 10.239.186.239
        //localhost = 127.0.0.1
        const response = await fetch("http://127.0.0.1:5001/resume", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(1)  // Send a request payload if needed
        });

        if (response.ok) {

            //resume simulation request loop after recieving confirmation signal of 1
            const result = await response.json();
            if (result==1) {
                intervalID = setInterval(fetchNewData, 100);
            }
            

        } else {
            console.error("Failed to fetch data");
        }
    } catch (err) {
        console.error(err);
    }
}

async function endSim() {
    try {
        const response = await fetch("http://127.0.0.1:5001/end", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(1)  // Send a request payload if needed
        });

        if (response.ok) {

            
            const result = await response.json();
            if (result==1) {
                clearInterval(intervalID);;
            }


        } else {
            console.error("Failed to fetch data");
        }
    } catch (err) {
        console.error(err);
    }
}


async function resetSim() {
    try {
        const response = await fetch("http://127.0.0.1:5001/reset", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(1)  // Send a request payload if needed
        });

        if (response.ok) {

            const result = await response.json();

        } else {
            console.error("Failed to fetch data");
        }
    } catch (err) {
        console.error(err);
    }
}


function handleSelectionChange() {
    const selectElement = document.getElementById('mySelect');
    const selectedValue = selectElement.value;
    tauType = parseInt(selectedValue, 10); // Parse the selected value as an integer
    createSpheres();
}



//data to send: Production Constant (c)
//lambda
//collision probability (overall)
