import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Plus, Send, Pause, Play, Trash2, Edit, Mail, BarChart3, AlertTriangle } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import PageHeader from "@/components/PageHeader";
import { getCampaigns, createCampaign, updateCampaign, deleteCampaign, activateCampaign, pauseCampaign } from "@/lib/api";

const STATUS_MAP = {
  draft: { label: "Taslak", color: "bg-gray-500", badge: "secondary" },
  active: { label: "Aktif", color: "bg-green-500", badge: "default" },
  paused: { label: "Duraklatildi", color: "bg-yellow-500", badge: "outline" },
  completed: { label: "Tamamlandi", color: "bg-blue-500", badge: "secondary" },
};

const emptyForm = { name: "", subject: "", content: "", campaign_type: "single", steps: [] };

export default function Campaigns() {
  const [campaigns, setCampaigns] = useState([]);
  const [loading, setLoading] = useState(true);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingCampaign, setEditingCampaign] = useState(null);
  const [form, setForm] = useState(emptyForm);
  const [submitting, setSubmitting] = useState(false);

  const load = () => { setLoading(true); getCampaigns().then(setCampaigns).catch(console.error).finally(() => setLoading(false)); };
  useEffect(() => { load(); }, []);

  const openCreate = () => { setEditingCampaign(null); setForm(emptyForm); setDialogOpen(true); };
  const openEdit = (c) => {
    setEditingCampaign(c);
    setForm({ name: c.name || "", subject: c.subject || "", content: c.content || "", campaign_type: c.campaign_type || "single", steps: c.steps || [] });
    setDialogOpen(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!form.name.trim()) return;
    setSubmitting(true);
    try {
      if (editingCampaign) { await updateCampaign(editingCampaign.id, form); }
      else { await createCampaign(form); }
      setDialogOpen(false); load();
    } catch (err) { console.error(err); }
    setSubmitting(false);
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Bu kampanyayi silmek istediginize emin misiniz?")) return;
    await deleteCampaign(id).catch(console.error); load();
  };

  const handleActivate = async (id) => { await activateCampaign(id).catch(console.error); load(); };
  const handlePause = async (id) => { await pauseCampaign(id).catch(console.error); load(); };

  const addStep = () => {
    setForm({ ...form, steps: [...form.steps, { subject: "", content: "", delay_days: 1 }] });
  };
  const updateStep = (idx, field, value) => {
    const steps = [...form.steps];
    steps[idx] = { ...steps[idx], [field]: value };
    setForm({ ...form, steps });
  };
  const removeStep = (idx) => setForm({ ...form, steps: form.steps.filter((_, i) => i !== idx) });

  const formatDate = (d) => { if (!d) return ""; return new Date(d).toLocaleDateString("tr-TR"); };

  return (
    <div className="page-content">
      <PageHeader title="Email Kampanyalari" subtitle="Drip kampanyalar ve sekans email gonderimi (MOCK)" />
      <div className="mb-4 p-3 bg-yellow-500/10 border border-yellow-500/30 rounded-lg flex items-center gap-2 text-sm">
        <AlertTriangle size={16} className="text-yellow-500" />
        <span className="text-yellow-700">Email gonderimi simule edilmektedir. Gercek email entegrasyonu icin bir email servisi (SendGrid vb.) gereklidir.</span>
      </div>

      <div className="flex justify-between items-center mb-6">
        <div className="flex gap-2">
          {Object.entries(STATUS_MAP).map(([k, v]) => (
            <Badge key={k} variant={v.badge} className="text-xs">{v.label}: {campaigns.filter((c) => c.status === k).length}</Badge>
          ))}
        </div>
        <Button onClick={openCreate}><Plus size={16} className="mr-1" /> Yeni Kampanya</Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {loading ? [1,2,3].map((i) => <Card key={i}><CardContent className="p-6"><div className="animate-pulse space-y-3"><div className="h-5 bg-muted rounded w-3/4" /><div className="h-4 bg-muted rounded w-1/2" /></div></CardContent></Card>) :
        campaigns.length === 0 ? <div className="col-span-3 text-center py-12 text-muted-foreground">Henuz kampanya olusturulmadi</div> :
        campaigns.map((c) => {
          const st = STATUS_MAP[c.status] || STATUS_MAP.draft;
          return (
            <motion.div key={c.id} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
              <Card className="card-hover">
                <CardContent className="p-5">
                  <div className="flex justify-between items-start mb-3">
                    <div className="flex-1">
                      <h3 className="font-semibold text-sm">{c.name}</h3>
                      <p className="text-xs text-muted-foreground mt-0.5">{c.subject || "Konu belirtilmemis"}</p>
                    </div>
                    <Badge variant={st.badge}><span className={`w-1.5 h-1.5 rounded-full ${st.color} mr-1.5 inline-block`} />{st.label}</Badge>
                  </div>
                  <div className="flex items-center gap-3 text-xs text-muted-foreground mb-3">
                    <span>{c.campaign_type === "drip" ? "Drip" : "Tekil"}</span>
                    <span>{formatDate(c.created_at)}</span>
                    {c.steps?.length > 0 && <span>{c.steps.length} adim</span>}
                  </div>
                  {c.stats && c.stats.sent > 0 && (
                    <div className="grid grid-cols-4 gap-2 p-2 bg-muted/50 rounded-lg mb-3">
                      <div className="text-center"><div className="text-sm font-bold">{c.stats.sent}</div><div className="text-[9px] text-muted-foreground">Gonderildi</div></div>
                      <div className="text-center"><div className="text-sm font-bold text-green-500">{c.stats.opened}</div><div className="text-[9px] text-muted-foreground">Acildi</div></div>
                      <div className="text-center"><div className="text-sm font-bold text-blue-500">{c.stats.clicked}</div><div className="text-[9px] text-muted-foreground">Tiklandi</div></div>
                      <div className="text-center"><div className="text-sm font-bold text-red-400">{c.stats.bounced}</div><div className="text-[9px] text-muted-foreground">Bounced</div></div>
                    </div>
                  )}
                  <div className="flex gap-1.5">
                    {c.status === "draft" && <Button size="sm" variant="default" className="flex-1" onClick={() => handleActivate(c.id)}><Play size={12} className="mr-1" />Baslat</Button>}
                    {c.status === "active" && <Button size="sm" variant="outline" className="flex-1" onClick={() => handlePause(c.id)}><Pause size={12} className="mr-1" />Duraklat</Button>}
                    {c.status === "paused" && <Button size="sm" variant="default" className="flex-1" onClick={() => handleActivate(c.id)}><Play size={12} className="mr-1" />Devam</Button>}
                    <Button size="sm" variant="ghost" onClick={() => openEdit(c)}><Edit size={12} /></Button>
                    <Button size="sm" variant="ghost" className="text-destructive" onClick={() => handleDelete(c.id)}><Trash2 size={12} /></Button>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          );
        })}
      </div>

      {/* Create/Edit Dialog */}
      <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
        <DialogContent className="max-w-lg max-h-[90vh] overflow-y-auto">
          <DialogHeader><DialogTitle>{editingCampaign ? "Kampanya Duzenle" : "Yeni Kampanya"}</DialogTitle></DialogHeader>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div><label className="text-xs font-medium mb-1 block">Kampanya Adi *</label><Input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required /></div>
            <div><label className="text-xs font-medium mb-1 block">Email Konusu</label><Input value={form.subject} onChange={(e) => setForm({ ...form, subject: e.target.value })} /></div>
            <div><label className="text-xs font-medium mb-1 block">Tur</label>
              <Select value={form.campaign_type} onValueChange={(v) => setForm({ ...form, campaign_type: v })}>
                <SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent><SelectItem value="single">Tekil Email</SelectItem><SelectItem value="drip">Drip Kampanya</SelectItem></SelectContent>
              </Select>
            </div>
            <div><label className="text-xs font-medium mb-1 block">Email Icerigi</label><Textarea value={form.content} onChange={(e) => setForm({ ...form, content: e.target.value })} rows={4} /></div>
            {form.campaign_type === "drip" && (
              <div>
                <div className="flex justify-between items-center mb-2">
                  <label className="text-xs font-medium">Drip Adimlari</label>
                  <Button type="button" variant="outline" size="sm" onClick={addStep}>+ Adim Ekle</Button>
                </div>
                {form.steps.map((step, idx) => (
                  <div key={idx} className="border rounded-lg p-3 mb-2 space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-xs font-medium">Adim {idx + 1}</span>
                      <Button type="button" variant="ghost" size="sm" onClick={() => removeStep(idx)}><Trash2 size={12} /></Button>
                    </div>
                    <Input placeholder="Konu" value={step.subject} onChange={(e) => updateStep(idx, "subject", e.target.value)} />
                    <Textarea placeholder="Icerik" value={step.content} onChange={(e) => updateStep(idx, "content", e.target.value)} rows={2} />
                    <div className="flex items-center gap-2">
                      <span className="text-xs">Bekleme:</span>
                      <Input type="number" className="w-20" value={step.delay_days} onChange={(e) => updateStep(idx, "delay_days", parseInt(e.target.value) || 1)} min={1} />
                      <span className="text-xs">gun</span>
                    </div>
                  </div>
                ))}
              </div>
            )}
            <div className="flex justify-end gap-2">
              <Button type="button" variant="outline" onClick={() => setDialogOpen(false)}>Iptal</Button>
              <Button type="submit" disabled={submitting}>{submitting ? "Kaydediliyor..." : editingCampaign ? "Guncelle" : "Olustur"}</Button>
            </div>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  );
}
