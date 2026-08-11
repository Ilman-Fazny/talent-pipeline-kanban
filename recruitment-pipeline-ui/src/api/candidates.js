const API_BASE = "http://localhost:8000/candidates";

export async function fetchCandidates(params = {}) {
  const query = new URLSearchParams(params).toString();
  const url = query ? `${API_BASE}?${query}` : API_BASE;
  const response = await fetch(url);
  return response.json();
}

export async function fetchCandidate(id) {
  const response = await fetch(`${API_BASE}/${id}`);
  if (!response.ok) return null;
  return response.json();
}

export async function createCandidate(candidateData) {
  const response = await fetch(API_BASE, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(candidateData),
  });
  return response.json();
}

export async function updateCandidate(id, candidateData) {
  const response = await fetch(`${API_BASE}/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(candidateData),
  });
  return response.json();
}

export async function updateCandidateStage(id, stage) {
  const response = await fetch(`${API_BASE}/${id}/stage`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ stage }),
  });
  return response.json();
}

export async function deleteCandidate(id) {
  const response = await fetch(`${API_BASE}/${id}`, {
    method: "DELETE",
  });
  return response.json();
}
