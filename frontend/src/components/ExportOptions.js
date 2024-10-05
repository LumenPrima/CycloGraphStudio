import React, { useState } from 'react';
import { exportSVG, exportPNG, exportGCode } from '../api';

const ExportOptions = ({ design }) => {
  const [exportStatus, setExportStatus] = useState({ loading: false, message: '', error: false });

  const handleExport = async (exportFunction, fileType, fileName) => {
    setExportStatus({ loading: true, message: `Exporting ${fileType}...`, error: false });
    try {
      const data = await exportFunction(design);
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
  };

  const handleExportSVG = () => handleExport(exportSVG, 'image/svg+xml', 'cyclograph.svg');
  const handleExportPNG = () => handleExport(exportPNG, 'image/png', 'cyclograph.png');
  const handleExportGCode = () => handleExport(exportGCode, 'text/plain', 'cyclograph.gcode');

  return (
    <div className="export-options">
      <h3>Export / Save Options</h3>
      <button onClick={handleExportSVG} disabled={exportStatus.loading}>Export SVG</button>
      <button onClick={handleExportPNG} disabled={exportStatus.loading}>Export PNG</button>
      <button onClick={handleExportGCode} disabled={exportStatus.loading}>Export G-code</button>
      {exportStatus.loading && <div className="loading-message">{exportStatus.message}</div>}
      {!exportStatus.loading && exportStatus.message && (
        <div className={`export-status ${exportStatus.error ? 'error' : 'success'}`}>
          {exportStatus.message}
        </div>
      )}
    </div>
  );
};

export default ExportOptions;