import React from "react";

export default function TrainMap({ trains }) {
  return (
    <div className="card col-8">
      <h2>Live Train Tracking</h2>
      <div className="map-placeholder">
        Map view placeholder — plug in Leaflet/Mapbox here using each train's
        latitude/longitude to render live markers.
      </div>
      <table>
        <thead>
          <tr>
            <th>Train</th>
            <th>Route</th>
            <th>Speed</th>
            <th>Status</th>
            <th>Updated</th>
          </tr>
        </thead>
        <tbody>
          {trains.length === 0 && (
            <tr><td colSpan={5} className="empty-state">No train data yet — start the simulator.</td></tr>
          )}
          {trains.map((t) => (
            <tr key={t.id}>
              <td>{t.train_number} · {t.train_name}</td>
              <td>{t.current_station} → {t.next_station}</td>
              <td>{t.speed_kmph} km/h</td>
              <td><span className={`badge ${t.status}`}>{t.status}</span></td>
              <td>{new Date(t.updated_at).toLocaleTimeString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
