import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const api = axios.create({
  baseURL: API,
  headers: { "Content-Type": "application/json" },
});

// Auth interceptor
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("syroce_token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// Auth
export const checkAuth = () => api.get("/auth/check").then((r) => r.data);
export const login = (data) => api.post("/auth/login", data).then((r) => r.data);
export const register = (data) => api.post("/auth/register", data).then((r) => r.data);
export const getMe = () => api.get("/auth/me").then((r) => r.data);

// Templates
export const getTemplates = (category) =>
  api.get("/templates", { params: category ? { category } : {} }).then((r) => r.data);
export const getTemplate = (id) => api.get(`/templates/${id}`).then((r) => r.data);
export const createTemplate = (data) => api.post("/templates", data).then((r) => r.data);
export const updateTemplate = (id, data) => api.put(`/templates/${id}`, data).then((r) => r.data);
export const deleteTemplate = (id) => api.delete(`/templates/${id}`).then((r) => r.data);
export const cloneTemplateFromProject = (projectId, name, category) =>
  api.post(`/templates/clone-from-project/${projectId}?name=${encodeURIComponent(name)}&category=${category}`).then((r) => r.data);

// Projects
export const getProjects = (status) =>
  api.get("/projects", { params: status ? { status } : {} }).then((r) => r.data);
export const getProject = (id) => api.get(`/projects/${id}`).then((r) => r.data);
export const createProject = (data) => api.post("/projects", data).then((r) => r.data);
export const updateProject = (id, data) => api.put(`/projects/${id}`, data).then((r) => r.data);
export const deleteProject = (id) => api.delete(`/projects/${id}`).then((r) => r.data);
export const exportProject = (id) =>
  api.post(`/projects/${id}/export`, {}, { responseType: "blob" }).then((r) => r.data);

// Versioning
export const getVersions = (projectId) => api.get(`/projects/${projectId}/versions`).then((r) => r.data);
export const createVersion = (projectId) => api.post(`/projects/${projectId}/versions`).then((r) => r.data);
export const restoreVersion = (projectId, versionId) =>
  api.post(`/projects/${projectId}/restore/${versionId}`).then((r) => r.data);

// Publish / Live Hosting
export const publishProject = (projectId) => api.post(`/projects/${projectId}/publish`).then((r) => r.data);
export const unpublishProject = (projectId) => api.post(`/projects/${projectId}/unpublish`).then((r) => r.data);

// Languages
export const getLanguages = () => api.get("/languages").then((r) => r.data);

// Section Presets (Block Library)
export const getSectionPresets = (category, sectionType) =>
  api.get("/section-presets", { params: { ...(category ? { category } : {}), ...(sectionType ? { section_type: sectionType } : {}) } }).then((r) => r.data);
export const createSectionPreset = (data) => api.post("/section-presets", data).then((r) => r.data);
export const deleteSectionPreset = (id) => api.delete(`/section-presets/${id}`).then((r) => r.data);

// Upload
export const uploadFile = (file) => {
  const formData = new FormData();
  formData.append("file", file);
  return api.post("/upload", formData, { headers: { "Content-Type": "multipart/form-data" } }).then((r) => r.data);
};

// Clients
export const getClients = (search) =>
  api.get("/clients", { params: search ? { search } : {} }).then((r) => r.data);
export const getClient = (id) => api.get(`/clients/${id}`).then((r) => r.data);
export const createClient = (data) => api.post("/clients", data).then((r) => r.data);
export const updateClient = (id, data) => api.put(`/clients/${id}`, data).then((r) => r.data);
export const deleteClient = (id) => api.delete(`/clients/${id}`).then((r) => r.data);

// Leads
export const getLeads = (params) => api.get("/leads", { params }).then((r) => r.data);
export const getLead = (id) => api.get(`/leads/${id}`).then((r) => r.data);
export const createLead = (data) => api.post("/leads", data).then((r) => r.data);
export const updateLead = (id, data) => api.put(`/leads/${id}`, data).then((r) => r.data);
export const deleteLead = (id) => api.delete(`/leads/${id}`).then((r) => r.data);
export const updateLeadStage = (id, stage) => api.put(`/leads/${id}/stage`, { stage }).then((r) => r.data);
export const updateLeadScore = (id, score) => api.put(`/leads/${id}/score`, { score }).then((r) => r.data);
export const assignLead = (id, assigned_to) => api.put(`/leads/${id}/assign`, { assigned_to }).then((r) => r.data);

// Pipeline
export const getPipelineStages = () => api.get("/pipeline/stages").then((r) => r.data);
export const getPipelineBoard = () => api.get("/pipeline/board").then((r) => r.data);
export const createPipelineStage = (data) => api.post("/pipeline/stages", data).then((r) => r.data);

// Communications
export const getCommunications = (entity_type, entity_id) =>
  api.get("/communications", { params: { entity_type, entity_id } }).then((r) => r.data);
export const createCommunication = (data) => api.post("/communications", data).then((r) => r.data);
export const deleteCommunication = (id) => api.delete(`/communications/${id}`).then((r) => r.data);

// Campaigns (MOCK)
export const getCampaigns = (status) =>
  api.get("/campaigns", { params: status ? { status } : {} }).then((r) => r.data);
export const getCampaign = (id) => api.get(`/campaigns/${id}`).then((r) => r.data);
export const createCampaign = (data) => api.post("/campaigns", data).then((r) => r.data);
export const updateCampaign = (id, data) => api.put(`/campaigns/${id}`, data).then((r) => r.data);
export const deleteCampaign = (id) => api.delete(`/campaigns/${id}`).then((r) => r.data);
export const activateCampaign = (id) => api.post(`/campaigns/${id}/activate`).then((r) => r.data);
export const pauseCampaign = (id) => api.post(`/campaigns/${id}/pause`).then((r) => r.data);

// Reports
export const getReportsOverview = () => api.get("/reports/overview").then((r) => r.data);
export const getReportsPipeline = () => api.get("/reports/pipeline").then((r) => r.data);
export const getReportsLeads = () => api.get("/reports/leads").then((r) => r.data);
export const getReportsActivity = (days) =>
  api.get("/reports/activity", { params: { days } }).then((r) => r.data);

// Forms
export const getForms = (project_id) =>
  api.get("/forms", { params: project_id ? { project_id } : {} }).then((r) => r.data);
export const getForm = (id) => api.get(`/forms/${id}`).then((r) => r.data);
export const createForm = (data) => api.post("/forms", data).then((r) => r.data);
export const updateForm = (id, data) => api.put(`/forms/${id}`, data).then((r) => r.data);
export const deleteForm = (id) => api.delete(`/forms/${id}`).then((r) => r.data);
export const getFormSubmissions = (id) => api.get(`/forms/${id}/submissions`).then((r) => r.data);

// Blog
export const getBlogPosts = (params) => api.get("/blog/posts", { params }).then((r) => r.data);
export const getBlogPost = (id) => api.get(`/blog/posts/${id}`).then((r) => r.data);
export const createBlogPost = (data) => api.post("/blog/posts", data).then((r) => r.data);
export const updateBlogPost = (id, data) => api.put(`/blog/posts/${id}`, data).then((r) => r.data);
export const deleteBlogPost = (id) => api.delete(`/blog/posts/${id}`).then((r) => r.data);

// Domains (MOCK)
export const getDomains = (project_id) =>
  api.get("/domains", { params: project_id ? { project_id } : {} }).then((r) => r.data);
export const createDomain = (data) => api.post("/domains", data).then((r) => r.data);
export const deleteDomain = (id) => api.delete(`/domains/${id}`).then((r) => r.data);
export const verifyDomain = (id) => api.post(`/domains/${id}/verify`).then((r) => r.data);

// Team
export const getTeam = () => api.get("/team").then((r) => r.data);
export const inviteTeamMember = (data) => api.post("/team/invite", data).then((r) => r.data);
export const updateTeamRole = (userId, role) => api.put(`/team/${userId}/role`, { role }).then((r) => r.data);
export const removeTeamMember = (userId) => api.delete(`/team/${userId}`).then((r) => r.data);

// Activity Log
export const getActivityLog = (params) => api.get("/activity-log", { params }).then((r) => r.data);

// Segments
export const getSegmentTags = () => api.get("/segments/tags").then((r) => r.data);
export const getSegmentCategories = () => api.get("/segments/categories").then((r) => r.data);

// Dashboard
export const getDashboardStats = () => api.get("/dashboard/stats").then((r) => r.data);
export const getActivity = (limit = 20) =>
  api.get("/dashboard/activity", { params: { limit } }).then((r) => r.data);

// Seed
export const seedTemplates = () => api.post("/seed").then((r) => r.data);

export default api;
