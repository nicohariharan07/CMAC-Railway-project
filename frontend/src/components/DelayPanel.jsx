import React from "react";

export default function DelayPanel({ predictions }) {
  return (
    <div className="card col-4">
      <h2>Delay Predictions</h2>
      <table>
        <thead>
          <tr>
            <th>Train</th>
            <th>Predicted Delay</th>
            <th>Weather</th>
            <th>Congestion</th>
          </tr>
        </thead>
        <tbody>
          {predictions.length === 0 && (
            <tr><td colSpan={4} className="empty-state">No predictions yet.</td></tr>
          )}
          {predictions.slice(0, 8).map((p) => (
            <tr key={p.id}>
              <td>{p.train_number}</td>
              <td>
                <span className={`badge ${p.predicted_delay_min >= 15 ? "MEDIUM" : "LOW"}`}>
                  {p.predicted_delay_min} min
                </span>
              </td>
              <td>{Math.round(p.weather_factor * 100)}%</td>
              <td>{Math.round(p.congestion_factor * 100)}%</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
