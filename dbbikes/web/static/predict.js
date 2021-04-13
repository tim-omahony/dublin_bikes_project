function predict(event, station) {
    event.preventDefault();
    const datetime = new Date($('#predictTime').val());
    const weekday = datetime.getDay();
    const hour = datetime.getHours();
    fetch('/predict?station=' + station + '&weekday=' + weekday + '&hour=' + hour).then(async response => {
        const data = await response.json();
        $('#stationModalPrediction').html(`<p class="mt-4">Prediction: On ${datetime.toLocaleDateString()} at ${datetime.toLocaleTimeString()} there will be ${Number(data.available_bikes).toFixed(0)} available bikes and the temperature will be ${Number(data.temperature).toFixed(2)}°.</p>`);
    });
}