import { useLocation, useNavigate } from "react-router-dom";
import { LayoutDashboard, Palette, Users, FolderOpen, ChevronLeft } from "lucide-react";
import { motion } from "framer-motion";

const navItems = [
  { path: "/", label: "Genel Bakis", icon: LayoutDashboard },
  { path: "/templates", label: "Sablon Galerisi", icon: Palette },
  { path: "/clients", label: "Musteriler", icon: Users },
  { path: "/projects", label: "Projeler", icon: FolderOpen },
];

export default function Sidebar() {
  const location = useLocation();
  const navigate = useNavigate();

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
      <nav className="flex-1 px-3 py-4 space-y-1">
        {navItems.map((item) => {
          const isActive = location.pathname === item.path;
          const Icon = item.icon;
          return (
            <motion.button
              key={item.path}
              whileHover={{ x: 2 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => navigate(item.path)}
              data-testid={`sidebar-nav-${item.path.replace("/", "") || "dashboard"}`}
              className={`w-full flex items-center gap-3 px-4 py-2.5 rounded-lg text-sm font-medium transition-colors duration-150 ${
                isActive
                  ? "bg-primary/10 text-primary border-l-2 border-primary"
                  : "text-muted-foreground hover:text-foreground hover:bg-muted/50"
              }`}
            >
              <Icon size={18} />
              <span>{item.label}</span>
            </motion.button>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="px-4 py-4 border-t border-border">
        <p className="text-[10px] text-muted-foreground font-mono text-center">
          Syroce CRM v1.0
        </p>
      </div>
    </aside>
  );
}
