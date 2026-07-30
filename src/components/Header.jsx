import "../styles/header.css";

function Header() {
  return (
    <>
      <div className="header">

        <div className="header-left">

          <h1>SENTINEL AI</h1>

          <p>Smart Surveillance Command Center</p>

        </div>

        <div className="header-right">

          <input
            type="text"
            placeholder="Search events, IDs, locations..."
          />

          <button>🔔</button>

          <span className="time">
            10:46 PM
          </span>

          <button className="profile">
            Admin
          </button>

        </div>

      </div>

      <div className="divider"></div>
    </>
  );
}

export default Header;