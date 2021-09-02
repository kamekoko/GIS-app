const fs = require('fs');

const jsonObject = JSON.parse(fs.readFileSync('./out2.geojson', 'utf8'));

console.log('{\n\t"type": "FeatureCollection",\n "features": [');

var count = 0;

jsonObject.features.forEach((obj) => {
    count++;
    if (count > 100) return;
    console.log(JSON.stringify(obj, null, "  "));
    console.log(',')
});

console.log()

console.log('],\n}');
