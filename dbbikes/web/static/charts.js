google.charts.load('current', {packages: ['corechart', 'line']});

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
            console.log('response data?', data)
            drawChart(data);
        } catch (error) {
            console.log('Error happened here!')
            console.error(error)
        }
    });
}


function drawChart(stats) {
    var data = google.visualization.arrayToDataTable([['Timestamp', 'Bikes', 'Stands']].concat(stats));

    var options = {
        hAxis: {
            title: 'Days',
            format: "yyyy/MM/dd",
        },
        vAxis: {
            title: 'Count'
        },
        colors: ['#a52714', '#097138'],
        width: '100%',
        height: 300,

    };

    var chart = new google.visualization.LineChart(document.getElementById('stationModalChart'));
    chart.draw(data, options);
}