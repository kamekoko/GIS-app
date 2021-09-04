const fs = require('fs');

const testObject = JSON.parse(fs.readFileSync('./test.json', 'utf-8'));

console.log('{\n\t"test": [\n\t\t[');

var count = 0;

testObject.test.forEach((obj) => {
  obj.forEach((elem) => {
    if (count != 0) console.log('\t\t\t,');
    count++;
    var lon = elem[0] + 1;
    var lat = elem[1] + 1;
    console.log('\t\t\t[\n\t\t\t\t' + lon + ',\n\t\t\t\t' + lat + '\n\t\t\t]');
  });
});

console.log('\t\t]\n\t]\n}');
