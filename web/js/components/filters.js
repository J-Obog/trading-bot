export function Filters({ onChange }) {
  const wrapper = document.createElement('div');

  wrapper.innerHTML = `
    <input placeholder="Ticker..." id="ticker" />
    <select id="status">
      <option value="">All</option>
      <option value="hit">Hit</option>
      <option value="miss">Miss</option>
    </select>
  `;

  wrapper.addEventListener('input', () => {
    onChange({
      ticker: wrapper.querySelector('#ticker').value,
      status: wrapper.querySelector('#status').value
    });
  });

  return wrapper;
}
