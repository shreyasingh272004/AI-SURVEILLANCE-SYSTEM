import "../styles/panel.css";

function Panel({ title, children }) {
  return (
    <div className="panel">

      <div className="panel-header">
        <div className="panel-title">
            <h3>{title}</h3>
        </div>

<div className="panel-status">
    LIVE
</div>
      </div>

      <div className="panel-body">
        {children}
      </div>

    </div>
  );
}

export default Panel;