import axios from "axios";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export const api = axios.create({ baseURL: API_BASE });

export const getTrains = () => api.get("/api/trains/").then((r) => r.data);
export const getCrowdReadings = () => api.get("/api/crowd/latest").then((r) => r.data);
export const getSensorReadings = () => api.get("/api/maintenance/readings").then((r) => r.data);
export const getDelayPredictions = () => api.get("/api/delays/recent").then((r) => r.data);
export const getAlerts = (unacknowledgedOnly = false) =>
  api.get("/api/alerts/", { params: { unacknowledged_only: unacknowledgedOnly } }).then((r) => r.data);
export const acknowledgeAlert = (id) => api.post(`/api/alerts/${id}/acknowledge`).then((r) => r.data);
