import { useLocation, useNavigate } from "react-router-dom";
import { LayoutDashboard, Palette, Users, FolderOpen, Target, Kanban, Mail, BarChart3, FileText, BookOpen, Shield, ChevronDown, ChevronRight, User, Bell, Sun, Moon } from "lucide-react";
import { motion } from "framer-motion";
import { useState, useEffect } from "react";
import { getUnreadCount } from "@/lib/api";

const navSections = [
  {
    title: "CRM",
    items: [
      { path: "/", label: "Genel Bakis", icon: LayoutDashboard },
      { path: "/leads", label: "Leadler", icon: Target },
      { path: "/pipeline", label: "Satis Hunisi", icon: Kanban },
      { path: "/clients", label: "Musteriler", icon: Users },
    ],
  },
  {
    title: "Projeler",
    items: [
      { path: "/projects", label: "Projeler", icon: FolderOpen },
      { path: "/templates", label: "Sablonlar", icon: Palette },
      { path: "/forms", label: "Formlar", icon: FileText },
      { path: "/blog", label: "Blog", icon: BookOpen },
    ],
  },
  {
    title: "Pazarlama",
    items: [
      { path: "/campaigns", label: "Kampanyalar", icon: Mail },
      { path: "/reports", label: "Raporlar", icon: BarChart3 },
    ],
  },
  {
    title: "Yonetim",
    items: [
      { path: "/team", label: "Takim & Log", icon: Shield },
    ],
  },
];

export default function Sidebar() {
  const location = useLocation();
  const navigate = useNavigate();
  const [collapsed, setCollapsed] = useState({});
  const [unreadCount, setUnreadCount] = useState(0);
  const [theme, setTheme] = useState(localStorage.getItem("syroce_theme") || "dark");

  useEffect(() => {
    getUnreadCount().then((r) => setUnreadCount(r.count)).catch(() => {});
    const interval = setInterval(() => {
      getUnreadCount().then((r) => setUnreadCount(r.count)).catch(() => {});
    }, 30000);
    return () => clearInterval(interval);
  }, []);

  const toggleTheme = () => {
    const newTheme = theme === "dark" ? "light" : "dark";
    setTheme(newTheme);
    localStorage.setItem("syroce_theme", newTheme);
    document.documentElement.classList.toggle("light-theme", newTheme === "light");
    document.documentElement.setAttribute("data-theme", newTheme);
  };

  const toggleSection = (title) => setCollapsed((p) => ({ ...p, [title]: !p[title] }));

  return (
    <aside
      data-testid="app-sidebar"
      className="fixed left-0 top-0 bottom-0 bg-card border-r border-border flex flex-col z-40"
      style={{ width: "var(--sidebar-w)" }}
    >
      {/* Logo */}
      <div className="px-6 py-5 border-b border-border">
        <div
          className="flex items-center gap-3 cursor-pointer"
          onClick={() => navigate("/")}
          data-testid="sidebar-logo"
        >
          <div className="w-9 h-9 rounded-lg bg-primary flex items-center justify-center">
            <span className="text-primary-foreground font-bold text-lg">S</span>
          </div>
          <div>
            <h1 className="text-lg font-bold tracking-tight text-foreground">Syroce</h1>
            <p className="text-[10px] text-muted-foreground font-mono uppercase tracking-widest">CRM</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-3 space-y-1 overflow-y-auto">
        {navSections.map((section) => (
          <div key={section.title} className="mb-2">
            <button
              onClick={() => toggleSection(section.title)}
              className="w-full flex items-center justify-between px-3 py-1.5 text-[10px] font-semibold uppercase tracking-wider text-muted-foreground hover:text-foreground transition-colors"
            >
              {section.title}
              {collapsed[section.title] ? <ChevronRight size={12} /> : <ChevronDown size={12} />}
            </button>
            {!collapsed[section.title] && section.items.map((item) => {
              const isActive = location.pathname === item.path;
              const Icon = item.icon;
              return (
                <motion.button
                  key={item.path}
                  whileHover={{ x: 2 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={() => navigate(item.path)}
                  data-testid={`sidebar-nav-${item.path.replace("/", "") || "dashboard"}`}
                  className={`w-full flex items-center gap-3 px-4 py-2 rounded-lg text-sm font-medium transition-colors duration-150 ${
                    isActive
                      ? "bg-primary/10 text-primary border-l-2 border-primary"
                      : "text-muted-foreground hover:text-foreground hover:bg-muted/50"
                  }`}
                >
                  <Icon size={16} />
                  <span>{item.label}</span>
                </motion.button>
              );
            })}
          </div>
        ))}
      </nav>

      {/* Footer */}
      <div className="px-4 py-4 border-t border-border">
        <button
          onClick={() => {
            localStorage.removeItem("syroce_token");
            window.location.reload();
          }}
          className="w-full text-[10px] text-muted-foreground font-mono text-center hover:text-foreground transition-colors cursor-pointer"
          data-testid="sidebar-logout"
        >
          Cikis Yap
        </button>
        <p className="text-[10px] text-muted-foreground font-mono text-center mt-1">
          Syroce CRM v3.0
        </p>
      </div>
    </aside>
  );
}
