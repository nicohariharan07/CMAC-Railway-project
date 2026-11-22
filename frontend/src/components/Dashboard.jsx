import React, { useEffect, useState, useCallback } from "react";
import {
  getTrains,
  getCrowdReadings,
  getSensorReadings,
  getDelayPredictions,
  getAlerts,
} from "../api";
import TrainMap from "./TrainMap";
import CrowdChart from "./CrowdChart";
import MaintenancePanel from "./MaintenancePanel";
import AlertFeed from "./AlertFeed";
import DelayPanel from "./DelayPanel";

const POLL_INTERVAL_MS = 4000;

export default function Dashboard() {
  const [trains, setTrains] = useState([]);
  const [crowd, setCrowd] = useState([]);
  const [sensors, setSensors] = useState([]);
  const [delays, setDelays] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [error, setError] = useState(null);

  const refresh = useCallback(async () => {
    try {
      const [t, c, s, d, a] = await Promise.all([
        getTrains(),
        getCrowdReadings(),
        getSensorReadings(),
        getDelayPredictions(),
        getAlerts(),
      ]);
      setTrains(t);
      setCrowd(c);
      setSensors(s);
      setDelays(d);
      setAlerts(a);
      setError(null);
    } catch (e) {
      setError("Could not reach the CMAC backend. Is it running on http://localhost:8000?");
    }
  }, []);

  useEffect(() => {
    refresh();
    const id = setInterval(refresh, POLL_INTERVAL_MS);
    return () => clearInterval(id);
  }, [refresh]);

  return (
    <div className="grid">
      {error && (
        <div className="card col-12" style={{ borderColor: "#e35d5d" }}>
          {error}
        </div>
      )}
      <TrainMap trains={trains} />
      <CrowdChart readings={crowd} />
      <MaintenancePanel readings={sensors} />
      <DelayPanel predictions={delays} />
      <AlertFeed alerts={alerts} onAcknowledged={refresh} />
    </div>
  );
}
