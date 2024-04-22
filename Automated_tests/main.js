import { simulate } from '@bjornlu/colorblind';
import { readFile } from 'fs';
import {writeFile} from 'fs';
const percorsoFile = '.\\js_input.txt';
readFile(percorsoFile, 'utf8', (err, data) => {
    if (err) {
        console.error("Errore nella lettura del file:", err);
        return;
    }

    const tuples = data.trim().split('\n');
    const results = [];

    tuples.forEach(tuple => {
        const cleanedTuple = tuple.replace(/[() ]/g, '');
        const numbers = cleanedTuple.split(',').map(Number);

        for(let i=0; i<numbers.length; i+=3){
            let r1 = numbers[i];
            let g1 = numbers[i+1];
            let b1 = numbers[i+2];
            let result = simulate({r: r1, g: g1, b: b1},'tritanopia')
            results.push(`(${result.r},${result.g},${result.b})`);
        }
    });
    const resultsJSON = results.map(result => JSON.stringify(result));

    // Scrivi i risultati in un nuovo file 'output.txt'
    let outputPath = '../js_output.txt'
    writeFile(outputPath, results.join('\n'), 'utf8', err => {
        if (err) {
            console.error("Errore nella scrittura del file:", err);
            return;
        }
        let msg = "I risultati sono stati scritti su " + outputPath
        console.log(msg);
    });
});




