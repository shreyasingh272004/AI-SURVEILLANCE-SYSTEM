import "../styles/metricCard.css";

function MetricCard({ title, value, icon, color }) {
  return (
    <div className="metric-card">

      <div className="metric-header">

        <span>{icon}</span>

        <p>{title}</p>

      </div>

      <h2 style={{ color }}>{value}</h2>

    </div>
  );
}

export default MetricCard;