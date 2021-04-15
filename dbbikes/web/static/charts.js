google.charts.load('current', {packages: ['corechart', 'bar']});

function getChartData(stationId) {
    fetch('/stations/occupancy/' + stationId).then(async response => {
        try {
            let data = await response.json();
            data = data.map(d => {
                const date = new Date(0);
                date.setUTCSeconds(d[0])
                d[0] = date;
                return d;
            });
            drawChart(data);
        } catch (error) {
            console.error(error)
        }
    });
}


function drawChart(stats) {
    var data = google.visualization.arrayToDataTable([['Timestamp', 'Available Bikes']].concat(stats));

    var options = {
        bars: 'vertical',
        axes: {
            x: {
                0: {side: 'top', label: 'Count'}
            },
            y: {
                format: "yyyy/MM/dd"
            }
        },
        width: '100%',
        height: 300,
    };

    var chart = new google.visualization.LineChart(document.getElementById('stationModalChart'));
    chart.draw(data, options);
}