lat = document.currentScript.getAttribute('lat')
lon = document.currentScript.getAttribute('lon')
server_status = document.currentScript.getAttribute('server_status')

console.log(lat)
console.log(lon)
console.log(server_status)

const mymap = L.map('mapid').setView([lat, lon], 13)

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(mymap);


L.marker([-23.571011, -46.6476696]).addTo(mymap)
    .bindPopup('Local da loja')
    .openPopup();

if(server_status == 1){
    console.log("Nominatim server is cool!")
    L.marker([lat, lon]).addTo(mymap)
    .bindPopup('Seu local.')
    .openPopup();
}

