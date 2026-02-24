import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { Users, FolderOpen, Palette, ArrowRight, FileDown, UserPlus, Plus, Target, TrendingUp, Mail, Activity, BarChart3, Kanban } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import PageHeader from "@/components/PageHeader";
import { getDashboardStats, getActivity } from "@/lib/api";

const activityIcons = {
  project_created: <Plus size={14} />,
  project_exported: <FileDown size={14} />,
  client_added: <UserPlus size={14} />,
  template_created: <Palette size={14} />,
  lead_created: <Target size={14} />,
  lead_converted: <TrendingUp size={14} />,
  lead_stage_changed: <Kanban size={14} />,
  campaign_created: <Mail size={14} />,
  campaign_activated: <Mail size={14} />,
  communication_added: <Activity size={14} />,
  lead_from_form: <Target size={14} />,
  bulk_stage_update: <Kanban size={14} />,
};

const activityColors = {
  project_created: "bg-primary/20 text-primary",
  project_exported: "bg-accent/20 text-accent",
  client_added: "bg-chart-3/20 text-chart-3",
  template_created: "bg-chart-4/20 text-chart-4",
  lead_created: "bg-blue-500/20 text-blue-400",
  lead_converted: "bg-green-500/20 text-green-400",
  lead_stage_changed: "bg-purple-500/20 text-purple-400",
  campaign_created: "bg-orange-500/20 text-orange-400",
  campaign_activated: "bg-emerald-500/20 text-emerald-400",
  communication_added: "bg-cyan-500/20 text-cyan-400",
  lead_from_form: "bg-indigo-500/20 text-indigo-400",
};

export default function Dashboard() {
  const navigate = useNavigate();
  const [stats, setStats] = useState(null);
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([getDashboardStats(), getActivity(20)])
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
          <div className="grid grid-cols-4 gap-4">
            {[1, 2, 3, 4].map((i) => (<div key={i} className="h-24 bg-muted rounded-xl" />))}
          </div>
          <div className="grid grid-cols-3 gap-6">
            {[1, 2, 3].map((i) => (<div key={i} className="h-32 bg-muted rounded-xl" />))}
          </div>
        </div>
      </div>
    );
  }

  const crmMetrics = [
    { label: "Toplam Lead", value: stats?.total_leads || 0, icon: Target, color: "text-blue-400", bgColor: "bg-blue-500/10" },
    { label: "Donusum Orani", value: `${stats?.conversion_rate || 0}%`, icon: TrendingUp, color: "text-green-400", bgColor: "bg-green-500/10" },
    { label: "Ort. Skor", value: stats?.avg_lead_score || 0, icon: BarChart3, color: "text-purple-400", bgColor: "bg-purple-500/10" },
    { label: "Aktif Kampanya", value: stats?.active_campaigns || 0, icon: Mail, color: "text-orange-400", bgColor: "bg-orange-500/10" },
  ];

  const projectMetrics = [
    { key: "total_clients", label: "Musteriler", value: stats?.total_clients || 0, icon: Users, color: "text-primary" },
    { key: "total_projects", label: "Projeler", value: stats?.total_projects || 0, icon: FolderOpen, color: "text-accent" },
    { key: "total_templates", label: "Sablonlar", value: stats?.total_templates || 0, icon: Palette, color: "text-chart-3" },
    { key: "total_communications", label: "Iletisim", value: stats?.total_communications || 0, icon: Activity, color: "text-cyan-400" },
  ];

  return (
    <div className="page-content dashboard-gradient">
      <PageHeader title="Genel Bakis" subtitle="Syroce CRM'e hos geldiniz" />

      {/* CRM Metrics */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        {crmMetrics.map((metric, i) => {
          const Icon = metric.icon;
          return (
            <motion.div key={i} initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.05 }}>
              <Card className="card-hover border-border/50">
                <CardContent className="p-4">
                  <div className="flex items-center gap-2 mb-2">
                    <div className={`p-1.5 rounded-md ${metric.bgColor}`}>
                      <Icon size={14} className={metric.color} />
                    </div>
                    <span className="text-[11px] text-muted-foreground">{metric.label}</span>
                  </div>
                  <span className="text-2xl font-bold">{metric.value}</span>
                </CardContent>
              </Card>
            </motion.div>
          );
        })}
      </div>

      {/* Project Metrics */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        {projectMetrics.map((stat, i) => {
          const Icon = stat.icon;
          return (
            <motion.div key={stat.key} initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 + i * 0.05 }}>
              <Card className="card-hover border-border/50">
                <CardContent className="p-4">
                  <div className="flex items-center justify-between mb-2">
                    <div className="p-1.5 rounded-md bg-muted">
                      <Icon size={14} className={stat.color} />
                    </div>
                    <span data-testid={`dashboard-${stat.key}-stat`} className="text-2xl font-bold">{stat.value}</span>
                  </div>
                  <p className="text-[11px] text-muted-foreground">{stat.label}</p>
                </CardContent>
              </Card>
            </motion.div>
          );
        })}
      </div>

      {/* Pipeline + Status + Quick Actions */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
        {/* Pipeline Summary */}
        <Card className="border-border/50">
          <CardContent className="p-5">
            <h3 className="text-xs font-semibold mb-4 text-muted-foreground uppercase tracking-wider">Pipeline Ozeti</h3>
            {stats?.pipeline_summary && stats.pipeline_summary.length > 0 ? (
              <div className="space-y-3">
                {stats.pipeline_summary.map((s) => {
                  const total = stats?.total_leads || 1;
                  const pct = Math.round((s.count / total) * 100);
                  return (
                    <div key={s.stage}>
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-xs">{s.label}</span>
                        <span className="text-xs font-mono text-muted-foreground">{s.count} ({pct}%)</span>
                      </div>
                      <Progress value={pct} className="h-1.5" />
                    </div>
                  );
                })}
              </div>
            ) : (
              <p className="text-sm text-muted-foreground text-center py-4">Henuz lead yok</p>
            )}
            <Button variant="ghost" size="sm" className="w-full mt-3 text-xs" onClick={() => navigate("/pipeline")}>
              Pipeline'i Gor <ArrowRight size={12} className="ml-1" />
            </Button>
          </CardContent>
        </Card>

        {/* Project Status */}
        <Card className="border-border/50">
          <CardContent className="p-5">
            <h3 className="text-xs font-semibold mb-4 text-muted-foreground uppercase tracking-wider">Proje Durumlari</h3>
            {stats?.status_distribution && (
              <div className="space-y-3">
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
            {/* Lead summary mini */}
            <div className="mt-4 pt-3 border-t border-border">
              <div className="flex items-center justify-between text-xs">
                <span className="text-muted-foreground">Kazanilan Lead</span>
                <span className="text-green-400 font-semibold">{stats?.won_leads || 0}</span>
              </div>
              <div className="flex items-center justify-between text-xs mt-1">
                <span className="text-muted-foreground">Kaybedilen Lead</span>
                <span className="text-red-400 font-semibold">{stats?.lost_leads || 0}</span>
              </div>
              <div className="flex items-center justify-between text-xs mt-1">
                <span className="text-muted-foreground">Haftalik Aktivite</span>
                <span className="text-blue-400 font-semibold">{stats?.recent_activities || 0}</span>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Quick Actions */}
        <Card className="border-border/50">
          <CardContent className="p-5">
            <h3 className="text-xs font-semibold mb-4 text-muted-foreground uppercase tracking-wider">Hizli Islemler</h3>
            <div className="space-y-2">
              <Button variant="outline" className="justify-start w-full h-auto py-3 px-3" onClick={() => navigate("/leads")}>
                <Target size={16} className="mr-3 text-blue-400" />
                <div className="text-left">
                  <div className="font-medium text-sm">Yeni Lead</div>
                  <div className="text-[10px] text-muted-foreground">Potansiyel musteri ekle</div>
                </div>
                <ArrowRight size={14} className="ml-auto text-muted-foreground" />
              </Button>
              <Button variant="outline" className="justify-start w-full h-auto py-3 px-3" onClick={() => navigate("/templates")}>
                <Palette size={16} className="mr-3 text-primary" />
                <div className="text-left">
                  <div className="font-medium text-sm">Yeni Web Sitesi</div>
                  <div className="text-[10px] text-muted-foreground">Sablon sec ve baslat</div>
                </div>
                <ArrowRight size={14} className="ml-auto text-muted-foreground" />
              </Button>
              <Button variant="outline" className="justify-start w-full h-auto py-3 px-3" onClick={() => navigate("/clients")}>
                <UserPlus size={16} className="mr-3 text-accent" />
                <div className="text-left">
                  <div className="font-medium text-sm">Musteri Ekle</div>
                  <div className="text-[10px] text-muted-foreground">Yeni otel musterisi</div>
                </div>
                <ArrowRight size={14} className="ml-auto text-muted-foreground" />
              </Button>
              <Button variant="outline" className="justify-start w-full h-auto py-3 px-3" onClick={() => navigate("/reports")}>
                <BarChart3 size={16} className="mr-3 text-purple-400" />
                <div className="text-left">
                  <div className="font-medium text-sm">Raporlar</div>
                  <div className="text-[10px] text-muted-foreground">CRM performansi</div>
                </div>
                <ArrowRight size={14} className="ml-auto text-muted-foreground" />
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Activity Feed */}
      <Card className="border-border/50">
        <CardContent className="p-5">
          <h3 className="text-xs font-semibold mb-4 text-muted-foreground uppercase tracking-wider">Son Aktiviteler</h3>
          {activities.length === 0 ? (
            <div className="text-center py-8">
              <p className="text-muted-foreground">Henuz aktivite yok. Bir sablon secerek baslayin.</p>
              <Button variant="outline" className="mt-4" onClick={() => navigate("/templates")} data-testid="dashboard-empty-start">
                Sablonlara Git
              </Button>
            </div>
          ) : (
            <div className="space-y-2">
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
