document.addEventListener('DOMContentLoaded', function () {
    // Get references to DOM elements
    const openGraphButton = document.getElementById('openGraphButton');
    const closeGraphButton = document.getElementById('closeGraphButton');
    const graphContainer = document.getElementById('graphContainer');
    const dataCheckboxes = document.querySelectorAll('.dataCheckbox');
    const ctx = document.getElementById('dataChart').getContext('2d');

    let dataArrays = [
        [],[],[],[],[]
    ];

    // Function to get the maximum value in all arrays
    function getMaxValue(arrays) {
        return Math.max(...arrays.flat(), 0); // Ensure at least 0 is considered
    }

    // Initialize the chart with static settings
    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [], // Will be updated dynamically
            datasets: []
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            layout: {
                padding: {
                    top: 10,
                    bottom: 10,
                    left: 10,
                    right: 100
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    ticks: {
                        autoSkip: true
                    }
                },
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'right'
                }
            }
        }
    });

    // Function to update the chart data based on selected checkboxes
    function updateSelectedData() {
        chart.data.datasets = [];
        dataCheckboxes.forEach((checkbox, index) => {
            if (checkbox.checked) {
                const colors = ['blue', 'green', 'red', 'yellow', 'gray'];
                chart.data.datasets.push({
                    label: `Tau ${index + 1}`,
                    data: dataArrays[index],
                    borderColor: colors[index],
                    backgroundColor: colors[index],
                    fill: false
                });
            }
        });
        chart.update();
    }

    // Event listener to open the graph modal
    openGraphButton.addEventListener('click', () => {
        graphContainer.style.display = 'flex';

        dataArrays = [[], [], [], [], []];
        console.log(tauOverTime);
        console.log("TOT ABOVE, DA BELOW")
        for (let b = 0; b < tauOverTime.length; b++) {
            let tau1 = 0;
            let tau2 = 0;
            let tau3 = 0;
            let tau4 = 0;
            let tau5 = 0;

            for (let i = 0; i < tauOverTime[b].length; i++) {
                for (let j = 0; j < tauOverTime[b][i].length; j++) {
                    for (let k = 0; k < tauOverTime[b][i][j].length; k++) {
                        tau1 += tauOverTime[b][i][j][k][0];
                        tau2 += tauOverTime[b][i][j][k][1];
                        tau3 += tauOverTime[b][i][j][k][2];
                        tau4 += tauOverTime[b][i][j][k][3];
                        tau5 += tauOverTime[b][i][j][k][4];
                    }
                }
            }

            dataArrays[0].push(tau1);
            dataArrays[1].push(tau2);
            dataArrays[2].push(tau3);
            dataArrays[3].push(tau4);
            dataArrays[4].push(tau5);
        }
        console.log(dataArrays);

        // Update chart labels
        chart.data.labels = dataArrays[0].map((_, index) => `${index + 1}`);

        updateSelectedData();
    });

    // Event listener to close the graph modal
    closeGraphButton.addEventListener('click', () => {
        graphContainer.style.display = 'none';
    });

    // Event listeners for the data checkboxes
    dataCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateSelectedData);
    });
});
