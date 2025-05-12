import React, { useState, useRef } from "react";
import axios from "axios";
import RealTimeGraph from "./RealTimeGraph";
import html2canvas from "html2canvas";
import { jsPDF } from "jspdf";
import "./AnalyzePanel.css";

const AnalyzePanel = () => {
  const [selectedStreams, setSelectedStreams] = useState([]);
  const [startTime, setStartTime] = useState("");
  const [endTime, setEndTime] = useState("");
  const [expectedCorrelation, setExpectedCorrelation] = useState("");
  const [exportType, setExportType] = useState("CSV");
  const graphRef = useRef(null);

  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const sampleData = [
    {
      Time: "08:00",
      "Sensor 1": 21.5,
      "Sensor 2": 45.2,
      "Sensor 3": 10.7,
      "Sensor 4": 33.1,
      "Sensor 5": 67.8,
    },
    {
      Time: "09:00",
      "Sensor 1": 22.1,
      "Sensor 2": 44.8,
      "Sensor 3": 11.2,
      "Sensor 4": 34.5,
      "Sensor 5": 66.3,
    },
    {
      Time: "10:00",
      "Sensor 1": 23.4,
      "Sensor 2": 46.1,
      "Sensor 3": 12.5,
      "Sensor 4": 35.2,
      "Sensor 5": 65.9,
    },
    {
      Time: "11:00",
      "Sensor 1": 24.2,
      "Sensor 2": 45.7,
      "Sensor 3": 11.9,
      "Sensor 4": 36.7,
      "Sensor 5": 68.2,
    },
    {
      Time: "12:00",
      "Sensor 1": 25.0,
      "Sensor 2": 47.3,
      "Sensor 3": 12.1,
      "Sensor 4": 35.9,
      "Sensor 5": 70.1,
    },
  ];

  const [timeRange, setTimeRange] = useState("");
  const [sensorFilter, setSensorFilter] = useState("");
  const [valueThreshold, setValueThreshold] = useState("");
  const [showFilters, setShowFilters] = useState(false);

  const availableStreams = [
    "Sensor 1",
    "Sensor 2",
    "Sensor 3",
    "Sensor 4",
    "Sensor 5",
  ];

  const handleStreamChange = (stream) => {
    setSelectedStreams((prev) =>
      prev.includes(stream)
        ? prev.filter((s) => s !== stream)
        : [...prev, stream]
    );
  };

  const handleAnalyze = async () => {
    if (
      selectedStreams.length < 3 ||
      !startTime ||
      !endTime ||
      !expectedCorrelation
    ) {
      setError("Please select 3 streams and fill all fields.");
      return;
    }

    setError("");

    try {
      const response = await axios.post("http://localhost:5000/api/analyze", {
        streams: selectedStreams,
        start: startTime,
        end: endTime,
        expectedCorrelation: parseFloat(expectedCorrelation),
      });
      setResult(response.data);
    } catch (err) {
      console.error("Error during analysis:", err);
      setError("Analysis failed. Check backend or network.");
    }
  };

  const getFilteredData = () => {
    if (selectedStreams.length === 0) return sampleData;

    return sampleData.map((row) => {
      const filteredRow = { Time: row.Time };
      selectedStreams.forEach((stream) => {
        filteredRow[stream] = row[stream];
      });
      return filteredRow;
    });
  };

  const exportToCSV = () => {
    const filteredData = getFilteredData();

    const headers = Object.keys(filteredData[0]);

    let csvContent = headers.join(",") + "\n";

    filteredData.forEach((row) => {
      const rowValues = headers.map((header) => {
        const value = row[header];
        // Handle values that might need quotes (like strings with commas)
        const cellValue =
          value !== null && value !== undefined ? String(value) : "";
        return cellValue.includes(",") ? `"${cellValue}"` : cellValue;
      });
      csvContent += rowValues.join(",") + "\n";
    });

    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const link = document.createElement("a");
    const url = URL.createObjectURL(blob);

    link.setAttribute("href", url);
    link.setAttribute("download", "sensor-data.csv");
    link.style.visibility = "hidden";

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handleExport = () => {
    switch (exportType) {
      case "CSV":
        exportToCSV();
        break;
      case "PDF":
        exportToPDF();
        break;
      case "PNG":
        exportToPNG();
        break;
      default:
        break;
    }
  };

  const exportToPDF = () => {
    if (!graphRef.current) return;

    const doc = new jsPDF("landscape", "mm", "a4");
    const pageWidth = doc.internal.pageSize.getWidth();

    doc.setFontSize(16);
    doc.text("Sensor Correlation Analysis", pageWidth / 2, 20, {
      align: "center",
    });

    html2canvas(graphRef.current).then((canvas) => {
      const imgData = canvas.toDataURL("image/png");
      const imgWidth = pageWidth - 40;
      const imgHeight = (canvas.height * imgWidth) / canvas.width;

      doc.addImage(imgData, "PNG", 20, 30, imgWidth, imgHeight);

      const filteredData = getFilteredData();
      const startY = imgHeight + 40;

      doc.setFontSize(12);
      let yPos = startY;
      let xPos = 20;

      const headers = Object.keys(filteredData[0]);
      headers.forEach((header) => {
        doc.text(header, xPos, yPos);
        xPos += 40;
      });
      filteredData.slice(0, 5).forEach((row, rowIndex) => {
        yPos += 10;
        xPos = 20;

        headers.forEach((header) => {
          doc.text(String(row[header]), xPos, yPos);
          xPos += 40;
        });
      });
      doc.save("sensor-analysis.pdf");
    });
  };

  const exportToPNG = () => {
    if (!graphRef.current) return;

    html2canvas(graphRef.current).then((canvas) => {
      const link = document.createElement("a");
      link.download = "sensor-graph.png";
      link.href = canvas.toDataURL("image/png");
      link.click();
    });
  };

  return (
    <div className="analyze-container">
      <h2>📊 Analyze Sensor Correlation</h2>

      <div className="form-group">
        <label>Select 3 Streams:</label>
        <div className="checkbox-group">
          {availableStreams.map((stream) => (
            <label key={stream} className="checkbox-label">
              <input
                type="checkbox"
                checked={selectedStreams.includes(stream)}
                onChange={() => handleStreamChange(stream)}
              />
              {stream}
            </label>
          ))}
        </div>
      </div>

      <div className="form-group">
        <label>Start Time:</label>
        <input
          type="time"
          value={startTime}
          onChange={(e) => setStartTime(e.target.value)}
          className="input-field"
        />
      </div>

      <div className="form-group">
        <label>End Time:</label>
        <input
          type="time"
          value={endTime}
          onChange={(e) => setEndTime(e.target.value)}
          className="input-field"
        />
      </div>

      <div className="form-group">
        <label>Expected Correlation (0.0 - 1.0):</label>
        <input
          type="number"
          step="0.1"
          min="0"
          max="1"
          value={expectedCorrelation}
          onChange={(e) => setExpectedCorrelation(e.target.value)}
          className="input-field"
        />
      </div>

      <button onClick={handleAnalyze} className="analyze-btn">
        🔍 Analyze
      </button>
      <select
        value={exportType}
        onChange={(e) => setExportType(e.target.value)}
        className="select"
      >
        <option value="CSV">CSV</option>
        <option value="PDF">PDF</option>
        <option value="PNG">PNG</option>
      </select>

      <button
        onClick={handleExport}
        className="analyze_button analyze_secondaryButton"
      >
        <span className="analyze_icon">📥</span>
        Export
      </button>

      {error && <div className="error-msg">{error}</div>}

      {result && (
        <div className="result-section">
          <strong>Result:</strong>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}

      <div className="graph-section">
        <div className="graph-header">
          <h3>📈 Real-Time Data Graph</h3>
          <span className="live-badge">🟢 Live Stream</span>
        </div>
        <RealTimeGraph selectedStreams={selectedStreams} />

        <div className="action-row">
          <button onClick={handleAnalyze} className="analyze-btn">
            🔍 Analyze
          </button>
          <button
            onClick={() => setShowFilters(!showFilters)}
            className="analyze-btn"
          >
            ⏳ Filter Data
          </button>
        </div>

        {showFilters && (
          <div className="filter-menu">
            <select
              value={timeRange}
              onChange={(e) => setTimeRange(e.target.value)}
              className="input-field"
            >
              <option value="">Time Range</option>
              <option value="1h">Last Hour</option>
              <option value="24h">Last Day</option>
            </select>

            <select
              value={sensorFilter}
              onChange={(e) => setSensorFilter(e.target.value)}
              className="input-field"
            >
              <option value="">Sensor Type</option>
              {availableStreams.map((s) => (
                <option key={s} value={s}>
                  {s}
                </option>
              ))}
            </select>

            <select
              value={valueThreshold}
              onChange={(e) => setValueThreshold(e.target.value)}
              className="input-field"
            >
              <option value="">Value Range</option>
              <option value="10">Above 10</option>
              <option value="20">Above 20</option>
              <option value="30">Above 30</option>
              <option value="40">Above 40</option>
              <option value="50">Above 50</option>
            </select>
          </div>
        )}

        {error && <div className="error-msg">{error}</div>}

        <div className="graph-section">
          <div className="graph-header">
            <h3>📈 Real-Time Data Graph</h3>
            <span className="live-badge">
              🟢 Live Stream {sensorFilter ? `for ${sensorFilter}` : ""}
            </span>
          </div>
          <div ref={graphRef}>
            <RealTimeGraph
              selectedStreams={selectedStreams}
              timeRange={timeRange}
              sensorFilter={sensorFilter}
              valueThreshold={valueThreshold}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalyzePanel;
