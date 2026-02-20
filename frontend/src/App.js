import { useState, useEffect } from "react";
import "@/App.css";
import { BrowserRouter, Routes, Route, Navigate, useNavigate } from "react-router-dom";
import Sidebar from "@/components/Sidebar";
import Dashboard from "@/pages/Dashboard";
import TemplateGallery from "@/pages/TemplateGallery";
import TemplateEditor from "@/pages/TemplateEditor";
import Clients from "@/pages/Clients";
import Projects from "@/pages/Projects";
import Login from "@/pages/Login";
import { checkAuth, getMe } from "@/lib/api";

function AuthWrapper({ children }) {
  const [authState, setAuthState] = useState("loading"); // loading, needs_setup, needs_login, authenticated

  useEffect(() => {
    let mounted = true;
    const init = async () => {
      try {
        const token = localStorage.getItem("syroce_token");
        if (token) {
          try {
            await getMe();
            if (mounted) setAuthState("authenticated");
            return;
          } catch {
            localStorage.removeItem("syroce_token");
          }
        }
        const { has_users } = await checkAuth();
        if (mounted) {
          setAuthState(has_users ? "needs_login" : "needs_setup");
        }
      } catch {
        if (mounted) setAuthState("authenticated"); // If auth check fails, allow access
      }
    };
    init();
    return () => { mounted = false; };
  }, []);

  if (authState === "loading") {
    return (
      <div className="flex items-center justify-center h-screen bg-background">
        <div className="text-center">
          <div className="w-12 h-12 rounded-xl bg-primary flex items-center justify-center mx-auto mb-4">
            <span className="text-primary-foreground font-bold text-xl">S</span>
          </div>
          <p className="text-muted-foreground">Yukleniyor...</p>
        </div>
      </div>
    );
  }

  if (authState === "needs_setup" || authState === "needs_login") {
    return <Login mode={authState === "needs_setup" ? "register" : "login"} onSuccess={() => setAuthState("authenticated")} />;
  }

  return children;
}

function App() {
  return (
    <BrowserRouter>
      <AuthWrapper>
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
      </AuthWrapper>
    </BrowserRouter>
  );
}

export default App;
