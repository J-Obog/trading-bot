export function Table({ columns, data }) {
  const table = document.createElement('table');
  table.className = 'table';

  const thead = document.createElement('thead');
  thead.innerHTML = `<tr>${columns.map(c => `<th>${c.label}</th>`).join('')}</tr>`;

  const tbody = document.createElement('tbody');

  data.forEach(row => {
    const tr = document.createElement('tr');
    tr.innerHTML = columns.map(c => 
      `<td>${c.render ? c.render(row) : row[c.key]}</td>`
    ).join('');
    tbody.appendChild(tr);
  });

  table.append(thead, tbody);
  return table;
}
