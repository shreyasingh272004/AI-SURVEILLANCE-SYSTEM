import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  Tooltip,
} from "recharts";
import { useEffect, useState } from "react";
import "../styles/threatChart.css";


function ThreatChart() {
  const [data, setData] = useState([]);
  useEffect(() => {

    const fetchChart = async () => {

        try {

            const response = await fetch(
                "http://127.0.0.1:5000/analytics"
            );

            const chart = await response.json();

            setData(chart);

        } catch (error) {

            console.log("Backend not connected.");

        }

    };

    fetchChart();

    const interval = setInterval(fetchChart, 1000);

    return () => clearInterval(interval);

}, []);
  return (
    <div className="threat-chart">
      <ResponsiveContainer width="100%" height={280}>
        <LineChart data={data}>
          <XAxis
            dataKey="time"
            axisLine={false}
            tickLine={false}
          />

          <Tooltip />

          <Line
            type="monotone"
            dataKey="threat"
            stroke="#D4AF37"
            strokeWidth={4}
            dot={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default ThreatChart;