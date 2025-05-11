
import React, { useState, useEffect } from "react";
import { Line } from "react-chartjs-2";

import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend

} from "chart.js";
import axios from "axios";

} from 'chart.js';


ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);


const RealTimeGraph = () => {
  const [data, setData] = useState({
    labels: [],
    datasets: [
      {
        label: 'Real-Time Data',
        data: [],
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        fill: true,
        tension: 0.4,
      },
    ],
  });

  const fetchData = async () => {
    try {
      const response = await axios.get('https://your-api-endpoint.com/data');
      return response.data;
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  useEffect(() => {
    const interval = setInterval(async () => {
      const newData = await fetchData();
      setData((prev) => {
        const labels = [...prev.labels, new Date().toLocaleTimeString()].slice(-10);
        const dataset = [...prev.datasets[0].data, newData].slice(-10);
        return {
          ...prev,
          labels,
          datasets: [{ ...prev.datasets[0], data: dataset }],
        };
      });
    }, 2000);

const RealTimeGraph = ({ selectedStreams, timeRange, sensorFilter, valueThreshold }) => {
  const [chartData, setChartData] = useState({
    labels: [],
    datasets: [
      {
        label: 'Sensor Value',
        data: [],
        borderColor: 'rgb(0, 123, 255)',
        backgroundColor: 'rgba(0, 123, 255, 0.1)',
        fill: true,
        tension: 0.4,
        pointRadius: 4,
        borderWidth: 2,
      },
    ],
  });

  useEffect(() => {
    const interval = setInterval(() => {
      const now = new Date();
      const timeLabel = now.toISOString().split('T')[1].split('.')[0]; // HH:MM:SS

      const newValue = Math.floor(Math.random() * 30) + 20; // random value for example
      setChartData((prev) => {
        const updatedLabels = [...prev.labels, timeLabel].slice(-10);
        const updatedData = [...prev.datasets[0].data, newValue].slice(-10);

        return {
          labels: updatedLabels,
          datasets: [
            {
              ...prev.datasets[0],
              data: updatedData,
            },
          ],
        };
      });
    }, 2000);


    return () => clearInterval(interval);
  }, []);

  const options = {
    responsive: true,
    plugins: {
      legend: {

        display: false,
      },
    },
  };

  return <Line data={data} options={options} />;

        display: false, // Hide default legend
      },
    },
  };

  return (
    <div>
      {/* Custom Legend Styled Like Live Stream */}
      <div className="custom-legend">
        📡 Sensor Stream {sensorFilter ? `(${sensorFilter})` : ''}
      </div>
      <Line data={chartData} options={options} />
    </div>
  );

};

export default RealTimeGraph;
