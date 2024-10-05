import React, { useState } from 'react';
import './App.css';
import ControlsPanel from './components/ControlsPanel';
import PatternPreview from './components/PatternPreview';
import ExportOptions from './components/ExportOptions';

function App() {
  const [design, setDesign] = useState({
    fixedGear: { shape: 'polygon', sides: 5, radius: 100, startAngle: 0 },
    movingGear: { shape: 'polygon', sides: 3, radius: 50, startAngle: 0 },
    penDistance: 30,
    penAngle: 0,
    pathType: 'outside',
    lineMovement: 'around',
    steps: 1000
  });

  const handleDesignChange = (newDesign) => {
    setDesign(newDesign);
  };

  return (
    <div className="App">
      <header>
        <h1>Cyclograph Studio</h1>
      </header>
      <main>
        <ControlsPanel design={design} onDesignChange={handleDesignChange} />
        <PatternPreview design={design} />
      </main>
      <ExportOptions design={design} />
    </div>
  );
}

export default App;