import "../styles/recentEvents.css";
import { useEffect, useState } from "react";

function RecentEvents() {

  const [events, setEvents] = useState([]);

  useEffect(() => {

    const fetchEvents = async () => {

      try {

        const response = await fetch("http://127.0.0.1:5000/events");

        const data = await response.json();

        setEvents(data);

      } catch (error) {

        console.log("Couldn't load events");

      }

    };

    fetchEvents();

    const interval = setInterval(fetchEvents, 1000);

    return () => clearInterval(interval);

  }, []);

  return (

    <table className="events-table">

      <thead>

        <tr>

          <th>Time</th>
          <th>Event</th>
          <th>Threat</th>
          <th>ID</th>

        </tr>

      </thead>

      <tbody>
        {events.map((event, index) => (
           <tr key={index}>
            <td>{event.Timestamp.split(" ")[1]}</td>
            <td>
                {event.Event === "Intrusion" ? "🚨 Intrusion" :
                event.Event === "Crowd" ? "👥 Crowd" :
                "⏱ Loitering"}
            </td>
            <td>
                <span className={`threat ${event.Threat.toLowerCase()}`}>
                    {event.Threat}
                </span>
            </td>
            <td>{event["Track ID"]}</td>
        </tr>
  ))}
</tbody>
    </table>

  );

}

export default RecentEvents;