import { Table } from '../../table.js';
import { Filters } from '../../filters.js';
import { fetchPredictions } from '../../api.js';

export async function renderHome(root) {
  root.innerHTML = '';

  let state = {};

  const container = document.createElement('div');
  const filters = Filters({
    onChange: (s) => {
      state = s;
      render();
    }
  });

  const tableContainer = document.createElement('div');

  async function render() {
    const data = await fetchPredictions(state);

    tableContainer.innerHTML = '';
    tableContainer.appendChild(Table({
      columns: [
        { key: 'ticker', label: 'Ticker' },
        { key: 'analyst', label: 'Analyst' },
        { key: 'target', label: 'Target' },
        {
          label: '% Upside',
          render: r => `${(((r.target - r.price) / r.price) * 100).toFixed(1)}%`
        },
        {
          label: 'Status',
          render: r => `<span class="status ${r.status}">${r.status}</span>`
        }
      ],
      data
    }));
  }

  container.append(filters, tableContainer);
  root.appendChild(container);

  render();
}
