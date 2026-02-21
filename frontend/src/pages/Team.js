import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Plus, Trash2, Shield, ShieldCheck, ShieldAlert, Eye, Edit as EditIcon, UserPlus, Crown, Clock, Copy } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import PageHeader from "@/components/PageHeader";
import { getTeam, inviteTeamMember, updateTeamRole, removeTeamMember, getActivityLog } from "@/lib/api";

const ROLES = [
  { value: "admin", label: "Admin", icon: Crown, color: "text-yellow-500", desc: "Tam yetki" },
  { value: "editor", label: "Editor", icon: EditIcon, color: "text-blue-500", desc: "Icerik duzenleme" },
  { value: "viewer", label: "Viewer", icon: Eye, color: "text-gray-500", desc: "Sadece goruntuleme" },
];

const ACTIVITY_ICONS = {
  lead_created: "🟢", lead_updated: "🟡", lead_deleted: "🔴", lead_stage_changed: "🔄", lead_assigned: "👤",
  campaign_created: "📧", campaign_activated: "▶️", campaign_paused: "⏸️",
  form_created: "📋", blog_created: "📝", domain_added: "🌐", domain_verified: "✅",
  team_invite: "👥", team_removed: "🚫", role_changed: "🛡️",
  project_created: "📁", project_exported: "📤", project_published: "🚀", project_unpublished: "⏹️",
  client_added: "🏨", template_created: "🎨", communication_added: "💬",
};

export default function Team() {
  const [members, setMembers] = useState([]);
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [inviteOpen, setInviteOpen] = useState(false);
  const [inviteForm, setInviteForm] = useState({ email: "", name: "", role: "editor" });
  const [inviteResult, setInviteResult] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [tab, setTab] = useState("team");

  const load = () => {
    setLoading(true);
    Promise.all([getTeam(), getActivityLog({ limit: 100 })])
      .then(([t, a]) => { setMembers(t); setActivities(a); })
      .catch(console.error).finally(() => setLoading(false));
  };
  useEffect(() => { load(); }, []);

  const handleInvite = async (e) => {
    e.preventDefault();
    if (!inviteForm.email.trim()) return;
    setSubmitting(true);
    try {
      const result = await inviteTeamMember(inviteForm);
      setInviteResult(result);
      load();
    } catch (err) {
      console.error(err);
      alert(err.response?.data?.detail || "Davet gonderilemedi");
    }
    setSubmitting(false);
  };

  const handleRoleChange = async (userId, newRole) => {
    await updateTeamRole(userId, newRole).catch((err) => alert(err.response?.data?.detail || "Hata"));
    load();
  };

  const handleRemove = async (userId, name) => {
    if (!window.confirm(`${name} takimdan cikarilacak. Emin misiniz?`)) return;
    await removeTeamMember(userId).catch((err) => alert(err.response?.data?.detail || "Hata"));
    load();
  };

  const formatDate = (d) => {
    if (!d) return "";
    const dt = new Date(d);
    const diff = Math.floor((Date.now() - dt) / 60000);
    if (diff < 60) return `${diff} dk once`;
    if (diff < 1440) return `${Math.floor(diff / 60)} saat once`;
    return dt.toLocaleDateString("tr-TR") + " " + dt.toLocaleTimeString("tr-TR", { hour: "2-digit", minute: "2-digit" });
  };

  const currentUser = JSON.parse(localStorage.getItem("syroce_user") || "{}");

  return (
    <div className="page-content">
      <PageHeader title="Takim & Aktivite" subtitle="Kullanici yonetimi ve aktivite kayitlari" />

      {/* Tabs */}
      <div className="flex gap-2 mb-6 border-b border-border pb-2">
        <Button variant={tab === "team" ? "default" : "ghost"} size="sm" onClick={() => setTab("team")}>
          <Shield size={14} className="mr-1" /> Takim ({members.length})
        </Button>
        <Button variant={tab === "activity" ? "default" : "ghost"} size="sm" onClick={() => setTab("activity")}>
          <Clock size={14} className="mr-1" /> Aktivite Log ({activities.length})
        </Button>
      </div>

      {tab === "team" && (
        <>
          <div className="flex justify-end mb-4">
            <Button onClick={() => { setInviteOpen(true); setInviteResult(null); setInviteForm({ email: "", name: "", role: "editor" }); }}>
              <UserPlus size={16} className="mr-1" /> Uye Davet Et
            </Button>
          </div>

          <Card>
            <CardContent className="p-0">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Kullanici</TableHead>
                    <TableHead>Rol</TableHead>
                    <TableHead>Durum</TableHead>
                    <TableHead>Kayit Tarihi</TableHead>
                    <TableHead className="w-[100px]">Islemler</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {loading ? <TableRow><TableCell colSpan={5} className="text-center py-8">Yukleniyor...</TableCell></TableRow> :
                  members.map((m) => {
                    const role = ROLES.find(r => r.value === (m.role || "admin"));
                    const RoleIcon = role?.icon || Shield;
                    return (
                      <TableRow key={m.id}>
                        <TableCell>
                          <div className="font-medium text-sm">{m.name || m.email}</div>
                          <div className="text-xs text-muted-foreground">{m.email}</div>
                        </TableCell>
                        <TableCell>
                          <Select value={m.role || "admin"} onValueChange={(v) => handleRoleChange(m.id, v)}>
                            <SelectTrigger className="w-[120px] h-8">
                              <div className="flex items-center gap-1"><RoleIcon size={12} className={role?.color} /><span className="text-xs">{role?.label}</span></div>
                            </SelectTrigger>
                            <SelectContent>
                              {ROLES.map(r => {
                                const Icon = r.icon;
                                return <SelectItem key={r.value} value={r.value}><div className="flex items-center gap-1.5"><Icon size={12} className={r.color} />{r.label} <span className="text-[10px] text-muted-foreground">({r.desc})</span></div></SelectItem>;
                              })}
                            </SelectContent>
                          </Select>
                        </TableCell>
                        <TableCell>
                          <Badge variant={m.status === "active" ? "default" : m.status === "invited" ? "outline" : "secondary"}>
                            {m.status === "active" ? "Aktif" : m.status === "invited" ? "Davetli" : m.status || "Aktif"}
                          </Badge>
                        </TableCell>
                        <TableCell className="text-xs text-muted-foreground">{formatDate(m.created_at)}</TableCell>
                        <TableCell>
                          <Button variant="ghost" size="icon" className="h-7 w-7 text-destructive" onClick={() => handleRemove(m.id, m.name)}><Trash2 size={14} /></Button>
                        </TableCell>
                      </TableRow>
                    );
                  })}
                </TableBody>
              </Table>
            </CardContent>
          </Card>

          {/* Invite Dialog */}
          <Dialog open={inviteOpen} onOpenChange={setInviteOpen}>
            <DialogContent className="max-w-md">
              <DialogHeader><DialogTitle>Takim Uyesi Davet Et</DialogTitle></DialogHeader>
              {inviteResult ? (
                <div className="space-y-4">
                  <div className="bg-green-500/10 border border-green-500/30 rounded-lg p-4 text-center">
                    <ShieldCheck className="mx-auto mb-2 text-green-500" size={32} />
                    <p className="font-semibold text-sm">Davet Basarili!</p>
                    <p className="text-xs text-muted-foreground mt-1">{inviteResult.email} ({inviteResult.role})</p>
                  </div>
                  <div className="bg-muted/50 rounded-lg p-3">
                    <p className="text-xs font-medium mb-1">Gecici Sifre:</p>
                    <div className="flex items-center gap-2">
                      <code className="flex-1 bg-card p-2 rounded text-sm font-mono">{inviteResult.temp_password}</code>
                      <Button size="sm" variant="outline" onClick={() => navigator.clipboard.writeText(inviteResult.temp_password)}><Copy size={12} /></Button>
                    </div>
                    <p className="text-[10px] text-muted-foreground mt-2">Bu sifreyi kullaniciya iletin. Giris yaptiktan sonra sifresini degistirebilir.</p>
                  </div>
                  <Button className="w-full" onClick={() => setInviteOpen(false)}>Tamam</Button>
                </div>
              ) : (
                <form onSubmit={handleInvite} className="space-y-4">
                  <div><label className="text-xs font-medium mb-1 block">Email *</label><Input type="email" value={inviteForm.email} onChange={(e) => setInviteForm({ ...inviteForm, email: e.target.value })} required /></div>
                  <div><label className="text-xs font-medium mb-1 block">Ad</label><Input value={inviteForm.name} onChange={(e) => setInviteForm({ ...inviteForm, name: e.target.value })} /></div>
                  <div><label className="text-xs font-medium mb-1 block">Rol</label>
                    <Select value={inviteForm.role} onValueChange={(v) => setInviteForm({ ...inviteForm, role: v })}>
                      <SelectTrigger><SelectValue /></SelectTrigger>
                      <SelectContent>{ROLES.map(r => <SelectItem key={r.value} value={r.value}>{r.label} - {r.desc}</SelectItem>)}</SelectContent>
                    </Select>
                  </div>
                  <div className="flex justify-end gap-2">
                    <Button type="button" variant="outline" onClick={() => setInviteOpen(false)}>Iptal</Button>
                    <Button type="submit" disabled={submitting}>{submitting ? "Gonderiliyor..." : "Davet Et"}</Button>
                  </div>
                </form>
              )}
            </DialogContent>
          </Dialog>
        </>
      )}

      {tab === "activity" && (
        <Card>
          <CardContent className="p-0">
            <div className="max-h-[600px] overflow-y-auto">
              {activities.length === 0 ? <p className="text-sm text-muted-foreground text-center py-8">Henuz aktivite yok</p> :
              activities.map((a) => (
                <div key={a.id} className="flex items-start gap-3 px-4 py-3 border-b border-border last:border-0 hover:bg-muted/30">
                  <span className="text-lg mt-0.5">{ACTIVITY_ICONS[a.type] || "📌"}</span>
                  <div className="flex-1">
                    <p className="text-sm">{a.message}</p>
                    <div className="flex items-center gap-2 mt-1">
                      <span className="text-[10px] text-muted-foreground">{formatDate(a.created_at)}</span>
                      {a.entity_type && <Badge variant="outline" className="text-[9px]">{a.entity_type}</Badge>}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
