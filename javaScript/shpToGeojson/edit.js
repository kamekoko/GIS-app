const fs = require('fs');

const jsonObject = JSON.parse(fs.readFileSync('./out2.geojson', 'utf8'));

console.log('{\n\t"type": "FeatureCollection",\n\t "features": [');

var count = 0;

jsonObject.features.forEach((obj) => {
    count++;
    if (count > 2) return;
    console.log(JSON.stringify(obj, null, "  "));
    console.log(',')
});

console.log()

console.log(']\n"bbox": [\n\t-70469.59017605362,\n\t27964.251346610803,\n\t-52884.54310107909,\n\t49411.407682093384\n]\n}');
