import React, { useEffect, useRef, useState } from 'react';
import { generatePattern } from '../api';

const PatternPreview = ({ design }) => {
  const canvasRef = useRef(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    const { width, height } = canvas;

    // Clear the canvas
    ctx.clearRect(0, 0, width, height);

    // Reset error state
    setError(null);
    setLoading(true);

    // Fetch the pattern data from the backend
    generatePattern(design)
      .then(data => {
        // Draw the pattern
        ctx.beginPath();
        data.points.forEach((point, index) => {
          if (index === 0) {
            ctx.moveTo(point[0] + width / 2, point[1] + height / 2);
          } else {
            ctx.lineTo(point[0] + width / 2, point[1] + height / 2);
          }
        });
        ctx.strokeStyle = 'blue';
        ctx.stroke();
        setLoading(false);
      })
      .catch(error => {
        console.error('Error generating pattern:', error);
        setError('Failed to generate pattern. Please try again.');
        setLoading(false);
      });
  }, [design]);

  return (
    <div className="pattern-preview">
      <canvas ref={canvasRef} width={500} height={500} />
      {loading && <div className="loading-message">Generating pattern...</div>}
      {error && <div className="error-message">{error}</div>}
    </div>
  );
};

export default PatternPreview;