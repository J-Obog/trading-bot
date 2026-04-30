export async function fetchPredictions(filters = {}) {
  const params = new URLSearchParams(filters);
  const res = await fetch(`/api/predictions?${params}`);
  return res.json();
}
