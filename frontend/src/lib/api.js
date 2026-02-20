import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const api = axios.create({
  baseURL: API,
  headers: { "Content-Type": "application/json" },
});

// Templates
export const getTemplates = (category) =>
  api.get("/templates", { params: category ? { category } : {} }).then((r) => r.data);
export const getTemplate = (id) => api.get(`/templates/${id}`).then((r) => r.data);
export const createTemplate = (data) => api.post("/templates", data).then((r) => r.data);
export const updateTemplate = (id, data) => api.put(`/templates/${id}`, data).then((r) => r.data);
export const deleteTemplate = (id) => api.delete(`/templates/${id}`).then((r) => r.data);

// Projects
export const getProjects = (status) =>
  api.get("/projects", { params: status ? { status } : {} }).then((r) => r.data);
export const getProject = (id) => api.get(`/projects/${id}`).then((r) => r.data);
export const createProject = (data) => api.post("/projects", data).then((r) => r.data);
export const updateProject = (id, data) => api.put(`/projects/${id}`, data).then((r) => r.data);
export const deleteProject = (id) => api.delete(`/projects/${id}`).then((r) => r.data);
export const exportProject = (id) =>
  api.post(`/projects/${id}/export`, {}, { responseType: "blob" }).then((r) => r.data);

// Clients
export const getClients = (search) =>
  api.get("/clients", { params: search ? { search } : {} }).then((r) => r.data);
export const getClient = (id) => api.get(`/clients/${id}`).then((r) => r.data);
export const createClient = (data) => api.post("/clients", data).then((r) => r.data);
export const updateClient = (id, data) => api.put(`/clients/${id}`, data).then((r) => r.data);
export const deleteClient = (id) => api.delete(`/clients/${id}`).then((r) => r.data);

// Dashboard
export const getDashboardStats = () => api.get("/dashboard/stats").then((r) => r.data);
export const getActivity = (limit = 20) =>
  api.get("/dashboard/activity", { params: { limit } }).then((r) => r.data);

// Seed
export const seedTemplates = () => api.post("/seed").then((r) => r.data);

export default api;
