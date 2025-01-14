function fetchTelemetryData() {
    fetch('http://127.0.0.1:5000/telemetry')
        .then(response => response.json())
        .then(data => {
            const gpsElement = document.getElementById('gps');
            const altitudeElement = document.getElementById('altitude');
            const batteryElement = document.getElementById('battery');

            gpsElement.textContent = `Lat: ${data.gps.lat}, Lon: ${data.gps.lon}`;
            altitudeElement.textContent = `${data.altitude} meters`;
            batteryElement.textContent = `${data.battery}%`;

            [gpsElement, altitudeElement, batteryElement].forEach(el => {
                el.style.transition = 'transform 0.3s ease, opacity 0.3s ease';
                el.style.transform = 'scale(1.1)';
                el.style.opacity = '0.8';
                setTimeout(() => {
                    el.style.transform = 'scale(1)';
                    el.style.opacity = '1';
                }, 300);
            });
        })
        .catch(err => console.error('Error fetching telemetry data:', err));
}
// Update the altitude value from the input
function updateAltitude() {
    const altitudeInput = document.getElementById('altitudeInput').value;
    const altitudeElement = document.getElementById('altitude');
    if (altitudeInput) {
        altitudeElement.textContent = `${altitudeInput} meters`;
    }
}