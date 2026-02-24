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
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <>
      {/* Mobile hamburger */}
      <button
        className="md:hidden fixed top-3 left-3 z-50 p-2 rounded-lg bg-card border border-border"
        onClick={() => setMobileOpen(!mobileOpen)}
      >
        <div className="w-5 h-0.5 bg-foreground mb-1" />
        <div className="w-5 h-0.5 bg-foreground mb-1" />
        <div className="w-5 h-0.5 bg-foreground" />
      </button>

      {/* Mobile overlay */}
      {mobileOpen && (
        <div className="md:hidden fixed inset-0 bg-black/50 z-40" onClick={() => setMobileOpen(false)} />
      )}

      <aside
        data-testid="app-sidebar"
        className={`fixed left-0 top-0 bottom-0 bg-card border-r border-border flex flex-col z-40 transition-transform duration-200 ${
          mobileOpen ? "translate-x-0" : "-translate-x-full md:translate-x-0"
        }`}
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
      <div className="px-3 py-3 border-t border-border space-y-1">
        {/* Notifications */}
        <button
          onClick={() => navigate("/notifications")}
          className={`w-full flex items-center gap-3 px-4 py-2 rounded-lg text-sm font-medium transition-colors duration-150 ${
            location.pathname === "/notifications"
              ? "bg-primary/10 text-primary border-l-2 border-primary"
              : "text-muted-foreground hover:text-foreground hover:bg-muted/50"
          }`}
        >
          <Bell size={16} />
          <span>Bildirimler</span>
          {unreadCount > 0 && (
            <span className="ml-auto bg-red-500 text-white text-[10px] rounded-full w-5 h-5 flex items-center justify-center font-bold">
              {unreadCount > 9 ? "9+" : unreadCount}
            </span>
          )}
        </button>
        {/* Profile */}
        <button
          onClick={() => navigate("/profile")}
          className={`w-full flex items-center gap-3 px-4 py-2 rounded-lg text-sm font-medium transition-colors duration-150 ${
            location.pathname === "/profile"
              ? "bg-primary/10 text-primary border-l-2 border-primary"
              : "text-muted-foreground hover:text-foreground hover:bg-muted/50"
          }`}
        >
          <User size={16} />
          <span>Profil</span>
        </button>
        {/* Theme Toggle */}
        <button
          onClick={toggleTheme}
          className="w-full flex items-center gap-3 px-4 py-2 rounded-lg text-sm font-medium text-muted-foreground hover:text-foreground hover:bg-muted/50 transition-colors duration-150"
        >
          {theme === "dark" ? <Sun size={16} /> : <Moon size={16} />}
          <span>{theme === "dark" ? "Acik Tema" : "Koyu Tema"}</span>
        </button>
        <p className="text-[10px] text-muted-foreground font-mono text-center mt-2">
          Syroce CRM v3.0
        </p>
      </div>
    </aside>
    </>
  );
}
