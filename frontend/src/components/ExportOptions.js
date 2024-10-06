import React, { useState } from 'react';
import { exportSVG, exportPNG, exportGCode } from '../api';

const ExportOptions = ({ design }) => {
  const [exportStatus, setExportStatus] = useState({ loading: false, message: '', error: false });
  const [showGCodeDialog, setShowGCodeDialog] = useState(false);
  const [gcodeOptions, setGcodeOptions] = useState({
    startGcode: `G90 ; use absolute positioning\nG21 ; use mm as unit\nG0 Z3 ; raise pen`,
    endGcode: `G0 Z3 ; raise pen\nM2 ; end program`,
    penDownCommand: 'G1 Z-1 F300 ; lower a bit slower',
    penUpCommand: 'G0 Z3',
    targetWidth: 200,
    targetHeight: 200,
    moveSpeed: 1500,
    drawSpeed: 1000,
    startingCorner: '0,0',   // Default starting corner
    machineRule: 'right-hand' // Default machine rule (right-hand)
  });

  const handleExport = async (exportFunction, fileType, fileName) => {
    setExportStatus({ loading: true, message: `Exporting ${fileType}...`, error: false });
    try {
      const data = await exportFunction(design, gcodeOptions);
      const blob = new Blob([data], { type: fileType });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = fileName;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      setExportStatus({ loading: false, message: `${fileType} exported successfully!`, error: false });
    } catch (err) {
      console.error(`Error exporting ${fileType}:`, err);
      setExportStatus({ loading: false, message: `Failed to export ${fileType}. Please try again.`, error: true });
    }
    setShowGCodeDialog(false); // Close the dialog after export
  };

  const handleExportSVG = () => handleExport(exportSVG, 'image/svg+xml', 'cyclograph.svg');
  const handleExportPNG = () => handleExport(exportPNG, 'image/png', 'cyclograph.png');
  
  const handleExportGCode = async () => {
    setExportStatus({ loading: true, message: `Exporting G-code...`, error: false });
    await handleExport(exportGCode, 'text/plain', 'cyclograph.gcode');
  };

  const openGCodeDialog = () => setShowGCodeDialog(true);
  
  const updateGcodeOptions = (field, value) => setGcodeOptions(prev => ({ ...prev, [field]: value }));

  return (
    <div className="export-options">
      <h3>Export / Save Options</h3>
      <button onClick={handleExportSVG} disabled={exportStatus.loading}>Export SVG</button>
      <button onClick={handleExportPNG} disabled={exportStatus.loading}>Export PNG</button>
      <button onClick={openGCodeDialog} disabled={exportStatus.loading}>Export G-code</button>

      {exportStatus.loading && <div className="loading-message">{exportStatus.message}</div>}
      {!exportStatus.loading && exportStatus.message && (
        <div className={`export-status ${exportStatus.error ? 'error' : 'success'}`}>
          {exportStatus.message}
        </div>
      )}

      {/* G-code export dialog */}
      {showGCodeDialog && (
        <div className="gcode-dialog">
          <h4>Customize G-code Export</h4>
          <label>Start G-code:</label>
          <textarea value={gcodeOptions.startGcode} onChange={(e) => updateGcodeOptions('startGcode', e.target.value)} />

          <label>End G-code:</label>
          <textarea value={gcodeOptions.endGcode} onChange={(e) => updateGcodeOptions('endGcode', e.target.value)} />

          <label>Pen Down Command:</label>
          <input type="text" value={gcodeOptions.penDownCommand} onChange={(e) => updateGcodeOptions('penDownCommand', e.target.value)} />

          <label>Pen Up Command:</label>
          <input type="text" value={gcodeOptions.penUpCommand} onChange={(e) => updateGcodeOptions('penUpCommand', e.target.value)} />

          <label>Target Width (mm):</label>
          <input type="number" value={gcodeOptions.targetWidth} onChange={(e) => updateGcodeOptions('targetWidth', e.target.value)} />

          <label>Target Height (mm):</label>
          <input type="number" value={gcodeOptions.targetHeight} onChange={(e) => updateGcodeOptions('targetHeight', e.target.value)} />

          <label>Move Speed (mm/min):</label>
          <input type="number" value={gcodeOptions.moveSpeed} onChange={(e) => updateGcodeOptions('moveSpeed', e.target.value)} />

          <label>Draw Speed (mm/min):</label>
          <input type="number" value={gcodeOptions.drawSpeed} onChange={(e) => updateGcodeOptions('drawSpeed', e.target.value)} />

          <label>Starting Corner (0,0):</label>
          <select value={gcodeOptions.startingCorner} onChange={(e) => updateGcodeOptions('startingCorner', e.target.value)}>
            <option value="0,0">Bottom-left (0,0)</option>
            <option value="top-right">Top-right</option>
          </select>

          <label>Machine Rule:</label>
          <select value={gcodeOptions.machineRule} onChange={(e) => updateGcodeOptions('machineRule', e.target.value)}>
            <option value="right-hand">Right-hand rule</option>
            <option value="left-hand">Left-hand rule</option>
          </select>

          <button onClick={handleExportGCode}>Generate G-code</button>
          <button onClick={() => setShowGCodeDialog(false)}>Cancel</button>
        </div>
      )}
    </div>
  );
};

export default ExportOptions;
