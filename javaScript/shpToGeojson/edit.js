const fs = require('fs');

const jsonObject = JSON.parse(fs.readFileSync('./out3.geojson', 'utf8'));

console.log('{\n\t"type": "FeatureCollection",\n\t "features": [');

var count = 0;

jsonObject.features.forEach((obj) => {
    count++;
    if (count > 4) return;
    console.log(JSON.stringify(obj, null, "  "));
    console.log(',')
});

console.log(']\n}');
