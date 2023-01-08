for (sheetName in ORIGINAL_DATA.sheets) {
    let sheetData = ORIGINAL_DATA.sheets[sheetName];

    let xs = sheetData.map(point => point.x);
    let minX = Math.min(...xs);
    let maxX = Math.max(...xs);
    let N = xs.length;

    console.log(minX, maxX, N);
}
