import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { Users, FolderOpen, Palette, ArrowRight, FileDown, UserPlus, Plus } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import PageHeader from "@/components/PageHeader";
import { getDashboardStats, getActivity } from "@/lib/api";

const statCards = [
  { key: "total_clients", label: "Toplam Musteri", icon: Users, color: "text-primary" },
  { key: "total_projects", label: "Toplam Proje", icon: FolderOpen, color: "text-accent" },
  { key: "total_templates", label: "Sablonlar", icon: Palette, color: "text-chart-3" },
];

const activityIcons = {
  project_created: <Plus size={14} />,
  project_exported: <FileDown size={14} />,
  client_added: <UserPlus size={14} />,
  template_created: <Palette size={14} />,
};

const activityColors = {
  project_created: "bg-primary/20 text-primary",
  project_exported: "bg-accent/20 text-accent",
  client_added: "bg-chart-3/20 text-chart-3",
  template_created: "bg-chart-4/20 text-chart-4",
};

export default function Dashboard() {
  const navigate = useNavigate();
  const [stats, setStats] = useState(null);
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([getDashboardStats(), getActivity(15)])
      .then(([statsData, actData]) => {
        setStats(statsData);
        setActivities(actData);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const formatDate = (dateStr) => {
    if (!dateStr) return "";
    const d = new Date(dateStr);
    const now = new Date();
    const diffMs = now - d;
    const diffMin = Math.floor(diffMs / 60000);
    if (diffMin < 1) return "az once";
    if (diffMin < 60) return `${diffMin} dk once`;
    const diffH = Math.floor(diffMin / 60);
    if (diffH < 24) return `${diffH} saat once`;
    const diffD = Math.floor(diffH / 24);
    if (diffD < 7) return `${diffD} gun once`;
    return d.toLocaleDateString("tr-TR");
  };

  if (loading) {
    return (
      <div className="page-content">
        <div className="animate-pulse space-y-6">
          <div className="h-8 w-48 bg-muted rounded" />
          <div className="grid grid-cols-3 gap-6">
            {[1, 2, 3].map((i) => (<div key={i} className="h-32 bg-muted rounded-xl" />))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="page-content dashboard-gradient">
      <PageHeader title="Genel Bakis" subtitle="Syroce CRM'e hos geldiniz" />

      {/* Stat Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        {statCards.map((stat, i) => {
          const Icon = stat.icon;
          const value = stats?.[stat.key] || 0;
          return (
            <motion.div
              key={stat.key}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
            >
              <Card className="card-hover border-border/50">
                <CardContent className="p-6">
                  <div className="flex items-center justify-between mb-4">
                    <div className={`p-2.5 rounded-lg bg-muted`}>
                      <Icon size={20} className={stat.color} />
                    </div>
                    <span data-testid={`dashboard-${stat.key}-stat`} className="text-3xl font-bold tracking-tight">
                      {value}
                    </span>
                  </div>
                  <p className="text-sm text-muted-foreground">{stat.label}</p>
                </CardContent>
              </Card>
            </motion.div>
          );
        })}
      </div>

      {/* Status Distribution + Quick Actions */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <Card className="lg:col-span-1 border-border/50">
          <CardContent className="p-6">
            <h3 className="text-sm font-semibold mb-4 text-muted-foreground uppercase tracking-wider">Proje Durumlari</h3>
            {stats?.status_distribution && (
              <div className="space-y-4">
                {[
                  { key: "draft", label: "Taslak", cls: "status-draft" },
                  { key: "published", label: "Yayinda", cls: "status-published" },
                  { key: "delivered", label: "Teslim Edildi", cls: "status-delivered" },
                ].map((s) => (
                  <div key={s.key} className="flex items-center justify-between">
                    <Badge variant="outline" className={`${s.cls} text-xs px-3 py-1`}>{s.label}</Badge>
                    <span className="text-lg font-semibold" data-testid={`dashboard-status-${s.key}`}>
                      {stats.status_distribution[s.key] || 0}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        <Card className="lg:col-span-2 border-border/50">
          <CardContent className="p-6">
            <h3 className="text-sm font-semibold mb-4 text-muted-foreground uppercase tracking-wider">Hizli Islemler</h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <Button
                variant="outline"
                className="justify-start h-auto py-4 px-4"
                onClick={() => navigate("/templates")}
                data-testid="dashboard-quick-templates"
              >
                <Palette size={18} className="mr-3 text-primary" />
                <div className="text-left">
                  <div className="font-medium">Yeni Web Sitesi</div>
                  <div className="text-xs text-muted-foreground">Sablon sec ve baslat</div>
                </div>
                <ArrowRight size={16} className="ml-auto text-muted-foreground" />
              </Button>
              <Button
                variant="outline"
                className="justify-start h-auto py-4 px-4"
                onClick={() => navigate("/clients")}
                data-testid="dashboard-quick-clients"
              >
                <UserPlus size={18} className="mr-3 text-accent" />
                <div className="text-left">
                  <div className="font-medium">Musteri Ekle</div>
                  <div className="text-xs text-muted-foreground">Yeni otel musterisi</div>
                </div>
                <ArrowRight size={16} className="ml-auto text-muted-foreground" />
              </Button>
              <Button
                variant="outline"
                className="justify-start h-auto py-4 px-4"
                onClick={() => navigate("/projects")}
                data-testid="dashboard-quick-projects"
              >
                <FolderOpen size={18} className="mr-3 text-chart-3" />
                <div className="text-left">
                  <div className="font-medium">Projeler</div>
                  <div className="text-xs text-muted-foreground">Mevcut projeleri gor</div>
                </div>
                <ArrowRight size={16} className="ml-auto text-muted-foreground" />
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Activity Feed */}
      <Card className="border-border/50">
        <CardContent className="p-6">
          <h3 className="text-sm font-semibold mb-4 text-muted-foreground uppercase tracking-wider">Son Aktiviteler</h3>
          {activities.length === 0 ? (
            <div className="text-center py-8">
              <p className="text-muted-foreground">Henuz aktivite yok. Bir sablon secerek baslayin.</p>
              <Button variant="outline" className="mt-4" onClick={() => navigate("/templates")} data-testid="dashboard-empty-start">
                Sablonlara Git
              </Button>
            </div>
          ) : (
            <div className="space-y-3">
              {activities.map((act) => (
                <motion.div
                  key={act.id}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  className="flex items-center gap-3 py-2 px-3 rounded-lg hover:bg-muted/30 transition-colors"
                >
                  <div className={`w-7 h-7 rounded-full flex items-center justify-center flex-shrink-0 ${activityColors[act.type] || "bg-muted text-foreground"}`}>
                    {activityIcons[act.type] || <Plus size={14} />}
                  </div>
                  <span className="text-sm flex-1">{act.message}</span>
                  <span className="text-xs text-muted-foreground font-mono whitespace-nowrap">{formatDate(act.created_at)}</span>
                </motion.div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
