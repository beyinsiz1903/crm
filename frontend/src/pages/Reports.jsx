import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { TrendingUp, Users, Target, Mail, Activity, BarChart3 } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import PageHeader from "@/components/PageHeader";
import { getReportsOverview, getReportsPipeline, getReportsLeads, getReportsActivity } from "@/lib/api";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line, CartesianGrid, Legend } from "recharts";

const COLORS = ["#3B82F6", "#F59E0B", "#F97316", "#8B5CF6", "#6366F1", "#10B981", "#EF4444", "#EC4899"];

export default function Reports() {
  const [overview, setOverview] = useState(null);
  const [pipeline, setPipeline] = useState([]);
  const [leadData, setLeadData] = useState(null);
  const [activityData, setActivityData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    Promise.all([
      getReportsOverview(),
      getReportsPipeline(),
      getReportsLeads(),
      getReportsActivity(30),
    ]).then(([o, p, l, a]) => {
      setOverview(o); setPipeline(p); setLeadData(l); setActivityData(a);
    }).catch(console.error).finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="page-content"><div className="animate-pulse space-y-6"><div className="h-8 w-48 bg-muted rounded" /><div className="grid grid-cols-4 gap-4">{[1,2,3,4].map(i => <div key={i} className="h-24 bg-muted rounded-xl" />)}</div><div className="grid grid-cols-2 gap-4">{[1,2].map(i => <div key={i} className="h-64 bg-muted rounded-xl" />)}</div></div></div>;

  const statCards = [
    { label: "Toplam Lead", value: overview?.total_leads || 0, icon: Users, color: "text-blue-500" },
    { label: "Donusum Orani", value: `${overview?.conversion_rate || 0}%`, icon: Target, color: "text-green-500" },
    { label: "Ort. Lead Skoru", value: overview?.avg_lead_score || 0, icon: TrendingUp, color: "text-purple-500" },
    { label: "Aktif Kampanya", value: overview?.active_campaigns || 0, icon: Mail, color: "text-orange-500" },
    { label: "Kazanilan", value: overview?.won_leads || 0, icon: Target, color: "text-emerald-500" },
    { label: "Kaybedilen", value: overview?.lost_leads || 0, icon: Target, color: "text-red-500" },
    { label: "Haftalik Aktivite", value: overview?.recent_activities || 0, icon: Activity, color: "text-indigo-500" },
    { label: "Toplam Iletisim", value: overview?.total_communications || 0, icon: BarChart3, color: "text-cyan-500" },
  ];

  const sourcePieData = overview?.source_distribution ? Object.entries(overview.source_distribution).map(([k, v]) => ({
    name: {website:"Website",referral:"Referans",social:"Sosyal",direct:"Direkt",ad:"Reklam",event:"Etkinlik",other:"Diger"}[k] || k, value: v
  })) : [];

  const stagePieData = overview?.stage_distribution ? Object.entries(overview.stage_distribution).filter(([,v]) => v > 0).map(([k, v]) => ({
    name: {new:"Yeni",contacted:"Iletisim",qualified:"Nitelikli",proposal:"Teklif",negotiation:"Muzakere",won:"Kazanildi",lost:"Kaybedildi"}[k] || k, value: v
  })) : [];

  return (
    <div className="page-content">
      <PageHeader title="Raporlar" subtitle="CRM performans metrikleri ve analizler" />

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        {statCards.map((stat, i) => {
          const Icon = stat.icon;
          return (
            <motion.div key={i} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.05 }}>
              <Card><CardContent className="p-4">
                <div className="flex items-center gap-2 mb-2"><Icon size={16} className={stat.color} /><span className="text-xs text-muted-foreground">{stat.label}</span></div>
                <div className="text-2xl font-bold">{stat.value}</div>
              </CardContent></Card>
            </motion.div>
          );
        })}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* Pipeline Funnel */}
        <Card>
          <CardContent className="p-5">
            <h3 className="font-semibold text-sm mb-4">Pipeline Dagilimi</h3>
            {pipeline.length > 0 ? (
              <ResponsiveContainer width="100%" height={250}>
                <BarChart data={pipeline}>
                  <XAxis dataKey="name" tick={{ fontSize: 10 }} />
                  <YAxis tick={{ fontSize: 10 }} />
                  <Tooltip />
                  <Bar dataKey="count" fill="#3B82F6" radius={[4, 4, 0, 0]}>
                    {pipeline.map((entry, idx) => <Cell key={idx} fill={entry.color || COLORS[idx % COLORS.length]} />)}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            ) : <div className="text-center py-12 text-muted-foreground text-sm">Veri yok</div>}
          </CardContent>
        </Card>

        {/* Source Distribution */}
        <Card>
          <CardContent className="p-5">
            <h3 className="font-semibold text-sm mb-4">Lead Kaynak Dagilimi</h3>
            {sourcePieData.length > 0 ? (
              <ResponsiveContainer width="100%" height={250}>
                <PieChart>
                  <Pie data={sourcePieData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80} label={({ name, value }) => `${name} (${value})`}>
                    {sourcePieData.map((_, idx) => <Cell key={idx} fill={COLORS[idx % COLORS.length]} />)}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            ) : <div className="text-center py-12 text-muted-foreground text-sm">Veri yok</div>}
          </CardContent>
        </Card>

        {/* Monthly Lead Trend */}
        <Card>
          <CardContent className="p-5">
            <h3 className="font-semibold text-sm mb-4">Aylik Lead Trendi</h3>
            {leadData?.monthly_trend?.length > 0 ? (
              <ResponsiveContainer width="100%" height={250}>
                <LineChart data={leadData.monthly_trend}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="label" tick={{ fontSize: 10 }} />
                  <YAxis tick={{ fontSize: 10 }} />
                  <Tooltip />
                  <Line type="monotone" dataKey="count" stroke="#8B5CF6" strokeWidth={2} dot={{ r: 4 }} />
                </LineChart>
              </ResponsiveContainer>
            ) : <div className="text-center py-12 text-muted-foreground text-sm">Veri yok</div>}
          </CardContent>
        </Card>

        {/* Score Distribution */}
        <Card>
          <CardContent className="p-5">
            <h3 className="font-semibold text-sm mb-4">Lead Skor Dagilimi</h3>
            {leadData?.score_distribution?.length > 0 ? (
              <ResponsiveContainer width="100%" height={250}>
                <BarChart data={leadData.score_distribution}>
                  <XAxis dataKey="range" tick={{ fontSize: 10 }} />
                  <YAxis tick={{ fontSize: 10 }} />
                  <Tooltip />
                  <Bar dataKey="count" fill="#10B981" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            ) : <div className="text-center py-12 text-muted-foreground text-sm">Veri yok</div>}
          </CardContent>
        </Card>
      </div>

      {/* Activity Timeline */}
      {activityData?.daily?.length > 0 && (
        <Card>
          <CardContent className="p-5">
            <h3 className="font-semibold text-sm mb-4">Gunluk Aktivite ({activityData.total} toplam)</h3>
            <ResponsiveContainer width="100%" height={200}>
              <BarChart data={activityData.daily}>
                <XAxis dataKey="date" tick={{ fontSize: 9 }} />
                <YAxis tick={{ fontSize: 10 }} />
                <Tooltip />
                <Bar dataKey="count" fill="#6366F1" radius={[2, 2, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
