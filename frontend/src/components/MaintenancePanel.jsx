import React from "react";

export default function MaintenancePanel({ readings }) {
  return (
    <div className="card col-4">
      <h2>Predictive Maintenance</h2>
      <table>
        <thead>
          <tr>
            <th>Asset</th>
            <th>Vib.</th>
            <th>Temp</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {readings.length === 0 && (
            <tr><td colSpan={4} className="empty-state">No sensor data yet — start the simulator.</td></tr>
          )}
          {readings.slice(0, 8).map((r) => (
            <tr key={r.id}>
              <td>{r.asset_id}</td>
              <td>{r.vibration_mm_s} mm/s</td>
              <td>{r.temperature_c}°C</td>
              <td>
                <span className={`badge ${r.is_anomalous ? "CRITICAL" : "LOW"}`}>
                  {r.is_anomalous ? "AT RISK" : "NORMAL"}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
