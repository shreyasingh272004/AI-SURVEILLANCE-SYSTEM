import "../styles/liveFeed.css";

function LiveFeed() {
  return (
    <img
      src="http://127.0.0.1:5000/video"
      alt="Live Feed"
      style={{
        width: "100%",
        height: "100%",
        objectFit: "contain",
        borderRadius: "12px",
      }}
    />
  );
}

export default LiveFeed;