import React from 'react';

const GearControl = ({ gear, onChange, label }) => (
  <div className="gear-control">
    <h3>{label}</h3>
    <div>
      <label>Shape:</label>
      <select value={gear.shape} onChange={(e) => onChange({ ...gear, shape: e.target.value })}>
        <option value="polygon">Polygon</option>
        <option value="line">Line</option>
      </select>
    </div>
    <div>
      <label>Sides:</label>
      <input 
        type="number" 
        value={gear.sides} 
        onChange={(e) => onChange({ ...gear, sides: parseInt(e.target.value) })}
        min={gear.shape === 'line' ? 2 : 3}
        max={100}
      />
    </div>
    <div>
      <label>Size:</label>
      <input 
        type="range" 
        value={gear.radius} 
        onChange={(e) => onChange({ ...gear, radius: parseInt(e.target.value) })}
        min={10}
        max={200}
      />
      <input 
        type="number" 
        value={gear.radius} 
        onChange={(e) => onChange({ ...gear, radius: parseInt(e.target.value) })}
      /> px
    </div>
    <div>
      <label>Start At:</label>
      <input 
        type="number" 
        value={gear.startAngle} 
        onChange={(e) => onChange({ ...gear, startAngle: parseFloat(e.target.value) })}
        step={0.1}
      /> degrees
    </div>
  </div>
);

const PathConfig = ({ pathType, lineMovement, onChange }) => (
  <div className="path-config">
    <h3>Path Configuration</h3>
    <div>
      <label>Type:</label>
      <label>
        <input 
          type="radio" 
          value="outside" 
          checked={pathType === 'outside'} 
          onChange={() => onChange('pathType', 'outside')} 
        /> Outside
      </label>
      <label>
        <input 
          type="radio" 
          value="inside" 
          checked={pathType === 'inside'} 
          onChange={() => onChange('pathType', 'inside')} 
        /> Inside
      </label>
    </div>
    <div>
      <label>Line Movement:</label>
      <select value={lineMovement} onChange={(e) => onChange('lineMovement', e.target.value)}>
        <option value="along">Along</option>
        <option value="around">Around</option>
      </select>
    </div>
  </div>
);

const PenConfig = ({ penDistance, penAngle, onChange }) => (
  <div className="pen-config">
    <h3>Pen Configuration</h3>
    <div>
      <label>Distance:</label>
      <input 
        type="range" 
        value={penDistance} 
        onChange={(e) => onChange('penDistance', parseInt(e.target.value))}
        min={0}
        max={100}
      />
      <input 
        type="number" 
        value={penDistance} 
        onChange={(e) => onChange('penDistance', parseInt(e.target.value))}
      /> px
    </div>
    <div>
      <label>Angle:</label>
      <input 
        type="range" 
        value={penAngle} 
        onChange={(e) => onChange('penAngle', parseFloat(e.target.value))}
        min={0}
        max={360}
        step={0.1}
      />
      <input 
        type="number" 
        value={penAngle} 
        onChange={(e) => onChange('penAngle', parseFloat(e.target.value))}
        step={0.1}
      /> degrees
    </div>
  </div>
);

const AnimationControls = ({ steps, onChange }) => (
  <div className="animation-controls">
    <h3>Animation</h3>
    <div>
      <button>Play</button>
      <button>Pause</button>
      <button>Reset</button>
    </div>
    <div>
      <label>Steps:</label>
      <input 
        type="range" 
        value={steps} 
        onChange={(e) => onChange('steps', parseInt(e.target.value))}
        min={100}
        max={10000}
        step={100}
      />
      <input 
        type="number" 
        value={steps} 
        onChange={(e) => onChange('steps', parseInt(e.target.value))}
        step={100}
      />
    </div>
  </div>
);

const ControlsPanel = ({ design, onDesignChange }) => {
  const handleChange = (key, value) => {
    onDesignChange({ ...design, [key]: value });
  };

  return (
    <div className="controls-panel">
      <GearControl gear={design.fixedGear} onChange={(gear) => handleChange('fixedGear', gear)} label="Fixed Gear" />
      <GearControl gear={design.movingGear} onChange={(gear) => handleChange('movingGear', gear)} label="Moving Gear" />
      <PathConfig pathType={design.pathType} lineMovement={design.lineMovement} onChange={handleChange} />
      <PenConfig penDistance={design.penDistance} penAngle={design.penAngle} onChange={handleChange} />
      <AnimationControls steps={design.steps} onChange={handleChange} />
    </div>
  );
};

export default ControlsPanel;