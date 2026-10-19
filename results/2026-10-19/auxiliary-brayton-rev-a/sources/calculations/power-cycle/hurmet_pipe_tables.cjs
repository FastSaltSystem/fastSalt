// Keep simple Hurmet-exported grid tables readable in standard Markdown viewers.
// This worksheet uses plain text cells, without merged cells or nested blocks.
function pipeTables(markdown) {
  return markdown.replace(/^\+(?:[-=]+\+)+\n(?:[|+][^\n]*\n)+\{\.grid[^\n]*\}/gm, block => {
    const rows = [];
    let row = null;
    for (const line of block.split('\n')) {
      if (line.startsWith('|')) {
        const cells = line.slice(1, -1).split('|').map(cell => cell.trim());
        if (row === null) row = cells;
        else {
          if (cells.length !== row.length) throw Error('Inconsistent grid table width');
          row = row.map((cell, i) => [cell, cells[i]].filter(Boolean).join(' '));
        }
      } else if (line.startsWith('+') && row !== null) {
        rows.push(row); row = null;
      }
    }
    if (rows.length < 2) throw Error('Expected a header and table rows');
    const format = cells => '| ' + cells.join(' | ') + ' |';
    return [format(rows[0]), format(rows[0].map(() => '---')), ...rows.slice(1).map(format)].join('\n');
  });
}
// Hurmet's save serializer needs explicit widths; add them only in memory.
// Leaving these attributes in the .md file makes them visible in VS Code.
function withHurmetWidths(markdown) {
  return markdown.replace(/^\|[^\n]+\|\n\|[ :|\-]+\|\n(?:\|[^\n]*\|(?:\n|$))+/gm, table => {
    const columns = table.split('\n')[0].split('|').length - 2;
    return table.trimEnd() + '\n{.grid colWidths="' + [250, ...Array(columns - 1).fill(120)].join(' ') + '"}\n';
  });
}
module.exports = {pipeTables, withHurmetWidths};
