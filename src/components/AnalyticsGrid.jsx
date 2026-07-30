import "../styles/analyticsGrid.css";
import Panel from "./Panel";
import ThreatChart from "./ThreatChart";
import LiveFeed from "./LiveFeed";
import RecentEvents from "./RecentEvents";
import ScreenshotGallery from "./ScreenshotGallery";

function AnalyticsGrid() {
  return (
    <div className="analytics-grid">

      <div className="analytics-card large">
        <Panel title="Threat Analytics">
            <ThreatChart />
        </Panel>
      </div>

      <div className="analytics-card">
        <Panel title="Live Surveillance">
            <LiveFeed />
        </Panel>
      </div>

      <div className="analytics-card events">
        <Panel title="Recent Events">
             <RecentEvents />
        </Panel>
      </div>
      
      <div className="analytics-card gallery">
        <Panel title="Recent Threat Captures">
          <ScreenshotGallery />
        </Panel>
      </div>

    </div>
  );
}

export default AnalyticsGrid;