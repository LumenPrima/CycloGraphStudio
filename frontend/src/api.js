const API_BASE_URL = 'http://localhost:5001/api';

export const generatePattern = async (design) => {
  const response = await fetch(`${API_BASE_URL}/generate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(design),
  });

  if (!response.ok) {
    throw new Error('Failed to generate pattern');
  }

  return response.json();
};

export const createGear = async (gearData) => {
  const response = await fetch(`${API_BASE_URL}/gear/create`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(gearData),
  });

  if (!response.ok) {
    throw new Error('Failed to create gear');
  }

  return response.json();
};

export const modifyDesign = async (designId, designData) => {
  const response = await fetch(`${API_BASE_URL}/design/modify`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ id: designId, ...designData }),
  });

  if (!response.ok) {
    throw new Error('Failed to modify design');
  }

  return response.json();
};

export const exportSVG = async (design) => {
  const response = await fetch(`${API_BASE_URL}/export/svg`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(design),
  });

  if (!response.ok) {
    throw new Error('Failed to export SVG');
  }

  return response.blob();
};

export const exportPNG = async (design) => {
  const response = await fetch(`${API_BASE_URL}/export/png`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(design),
  });

  if (!response.ok) {
    throw new Error('Failed to export PNG');
  }

  return response.blob();
};

export const exportGCode = async (design) => {
  const response = await fetch(`${API_BASE_URL}/export/gcode`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(design),
  });

  if (!response.ok) {
    throw new Error('Failed to export G-code');
  }

  return response.text();
};