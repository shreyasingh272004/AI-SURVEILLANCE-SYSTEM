import { useEffect, useRef, useState } from "react";
import "../styles/dashboard.css";
import Header from "../components/Header";
import MetricCard from "../components/MetricCard";
import AnalyticsGrid from "../components/AnalyticsGrid";

function Dashboard() {
  const [stats, setStats] = useState({
    intrusions: 0,
    crowdEvents: 0,
    threatLevel: "LOW",
    totalThreats: 0,
  });

  const alarm = useRef(new Audio("/alarm.mp3"));
  const previousThreat = useRef("LOW");

  // Fetch stats every second
  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/stats");
        const data = await response.json();
        setStats(data);
      } catch (error) {
        console.log("Backend not connected.");
      }
    };

    fetchStats();

    const interval = setInterval(fetchStats, 1000);

    return () => clearInterval(interval);
  }, []);

  // Play alarm when threat changes to HIGH
  useEffect(() => {
    if (
      stats.threatLevel === "HIGH" &&
      previousThreat.current !== "HIGH"
    ) {
      alarm.current.currentTime = 0;
      alarm.current.play().catch(() => {});
    }

    previousThreat.current = stats.threatLevel;
  }, [stats.threatLevel]);

  return (
    <div className="dashboard">
      <div className="dashboard-container">
        <Header />

        <div className="metrics">
          <MetricCard
            title="Intrusions"
            value={stats.intrusions}
            icon="🚨"
            color="#D4AF37"
          />

          <MetricCard
            title="Loitering"
            value="5"
            icon="⏱"
            color="#D4AF37"
          />

          <MetricCard
            title="Crowd"
            value={stats.crowdEvents}
            icon="👥"
            color="#D4AF37"
          />

          <MetricCard
            title="Threat"
            value={stats.threatLevel}
            icon="🛡"
            color="#D4AF37"
          />
        </div>

        <AnalyticsGrid />
      </div>
    </div>
  );
}

export default Dashboard;