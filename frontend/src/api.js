import axios from "axios";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  "https://deepdocqa.onrender.com";

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 120000
});

export const getStatus = () => api.get("/status");

export const uploadDocument = (file) => {
  const formData = new FormData();
  formData.append("file", file);
  return api.post("/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" }
  });
};

export const askQuestion = (question) => api.post("/ask", { question });

export default api;
