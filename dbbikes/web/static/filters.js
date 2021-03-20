function getStations() {
    return fetch('/stations').then(async response => {
        return await response.json()
    })
}

function filter(data) {
    const stations = getStations();
    station === stations.available_bikes
      ? stations.filter(stations.available_bike_stands)
      : stations.filter(stations.available_bikes)
}