import React from "react";
import { acknowledgeAlert } from "../api";

export default function AlertFeed({ alerts, onAcknowledged }) {
  const handleAck = async (id) => {
    await acknowledgeAlert(id);
    onAcknowledged();
  };

  return (
    <div className="card col-4">
      <h2>Live Alert Feed</h2>
      {alerts.length === 0 ? (
        <div className="empty-state">No alerts yet. All systems nominal.</div>
      ) : (
        alerts.map((a) => (
          <div className="alert-item" key={a.id}>
            <div>
              <span className={`badge ${a.severity}`}>{a.severity}</span>{" "}
              <strong style={{ fontSize: 12 }}>{a.category}</strong>
              <div className="alert-meta">{a.message}</div>
              <div className="alert-meta">{new Date(a.created_at).toLocaleTimeString()}</div>
            </div>
            {!a.acknowledged && (
              <button className="ack-btn" onClick={() => handleAck(a.id)}>
                Ack
              </button>
            )}
          </div>
        ))
      )}
    </div>
  );
}
