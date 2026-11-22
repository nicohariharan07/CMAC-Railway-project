import React from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";

export default function CrowdChart({ readings }) {
  // Take the most recent reading per zone for a clean bar chart
  const latestByZone = {};
  readings.forEach((r) => {
    if (!latestByZone[r.zone_id] || new Date(r.recorded_at) > new Date(latestByZone[r.zone_id].recorded_at)) {
      latestByZone[r.zone_id] = r;
    }
  });
  const data = Object.values(latestByZone).map((r) => ({
    zone: r.zone_id,
    capacity_pct: r.capacity_pct,
    person_count: r.person_count,
  }));

  return (
    <div className="card col-4">
      <h2>Crowd Density (% Capacity)</h2>
      {data.length === 0 ? (
        <div className="empty-state">No crowd data yet — start the simulator.</div>
      ) : (
        <ResponsiveContainer width="100%" height={220}>
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#24365c" />
            <XAxis dataKey="zone" tick={{ fill: "#9aa7bd", fontSize: 10 }} />
            <YAxis tick={{ fill: "#9aa7bd", fontSize: 10 }} />
            <Tooltip
              contentStyle={{ background: "#0b1f3a", border: "1px solid #24365c", color: "#e8ecf4" }}
            />
            <Bar dataKey="capacity_pct" fill="#c9a44c" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      )}
    </div>
  );
}
