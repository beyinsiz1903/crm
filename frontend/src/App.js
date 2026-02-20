import "@/App.css";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Sidebar from "@/components/Sidebar";
import Dashboard from "@/pages/Dashboard";
import TemplateGallery from "@/pages/TemplateGallery";
import TemplateEditor from "@/pages/TemplateEditor";
import Clients from "@/pages/Clients";
import Projects from "@/pages/Projects";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/editor/:projectId" element={<TemplateEditor />} />
        <Route
          path="/*"
          element={
            <div className="app-layout">
              <Sidebar />
              <main className="app-main">
                <Routes>
                  <Route path="/" element={<Dashboard />} />
                  <Route path="/templates" element={<TemplateGallery />} />
                  <Route path="/clients" element={<Clients />} />
                  <Route path="/projects" element={<Projects />} />
                  <Route path="*" element={<Navigate to="/" replace />} />
                </Routes>
              </main>
            </div>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
