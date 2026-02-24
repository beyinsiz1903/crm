import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Plus, Search, Star, Phone, Mail, Building2, Tag, Trash2, Edit, ChevronDown, User, Filter, ArrowUpDown, Download, UserCheck, ChevronLeft, ChevronRight, CheckSquare } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Checkbox } from "@/components/ui/checkbox";
import PageHeader from "@/components/PageHeader";
import { getLeads, createLead, updateLead, deleteLead, getTeam, getCommunications, createCommunication, deleteCommunication, convertLead, exportLeadsCsv, bulkUpdateStage, bulkDeleteLeads } from "@/lib/api";

const SOURCES = [
  { value: "website", label: "Website" },
  { value: "referral", label: "Referans" },
  { value: "social", label: "Sosyal Medya" },
  { value: "direct", label: "Direkt" },
  { value: "ad", label: "Reklam" },
  { value: "event", label: "Etkinlik" },
  { value: "other", label: "Diger" },
];

const STAGES = [
  { value: "new", label: "Yeni", color: "bg-blue-500" },
  { value: "contacted", label: "Iletisime Gecildi", color: "bg-yellow-500" },
  { value: "qualified", label: "Nitelikli", color: "bg-orange-500" },
  { value: "proposal", label: "Teklif", color: "bg-purple-500" },
  { value: "negotiation", label: "Muzakere", color: "bg-indigo-500" },
  { value: "won", label: "Kazanildi", color: "bg-green-500" },
  { value: "lost", label: "Kaybedildi", color: "bg-red-500" },
];

const COMM_TYPES = [
  { value: "email", label: "Email", icon: "📧" },
  { value: "phone", label: "Telefon", icon: "📞" },
  { value: "meeting", label: "Toplanti", icon: "🤝" },
  { value: "note", label: "Not", icon: "📝" },
];

const emptyForm = { name: "", email: "", phone: "", company: "", source: "direct", score: 0, stage: "new", tags: [], notes: "" };

export default function Leads() {
  const [leads, setLeads] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [stageFilter, setStageFilter] = useState("all");
  const [sourceFilter, setSourceFilter] = useState("all");
  const [dialogOpen, setDialogOpen] = useState(false);
  const [detailOpen, setDetailOpen] = useState(false);
  const [editingLead, setEditingLead] = useState(null);
  const [selectedLead, setSelectedLead] = useState(null);
  const [form, setForm] = useState(emptyForm);
  const [tagInput, setTagInput] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [team, setTeam] = useState([]);
  const [comms, setComms] = useState([]);
  const [commForm, setCommForm] = useState({ comm_type: "note", subject: "", content: "", direction: "outbound" });
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalCount, setTotalCount] = useState(0);
  const [selectedIds, setSelectedIds] = useState([]);

  const load = () => {
    setLoading(true);
    const params = { page, limit: 25 };
    if (search) params.search = search;
    if (stageFilter !== "all") params.stage = stageFilter;
    if (sourceFilter !== "all") params.source = sourceFilter;
    getLeads(params).then((res) => {
      setLeads(res.items || res);
      setTotalPages(res.pages || 1);
      setTotalCount(res.total || (res.items || res).length);
    }).catch(console.error).finally(() => setLoading(false));
  };

  useEffect(() => { load(); }, [search, stageFilter, sourceFilter, page]);
  useEffect(() => { getTeam().then(setTeam).catch(() => {}); }, []);

  const loadComms = (leadId) => {
    getCommunications("lead", leadId).then(setComms).catch(() => setComms([]));
  };

  const openCreate = () => { setEditingLead(null); setForm(emptyForm); setDialogOpen(true); };
  const openEdit = (lead) => {
    setEditingLead(lead);
    setForm({ name: lead.name || "", email: lead.email || "", phone: lead.phone || "", company: lead.company || "", source: lead.source || "direct", score: lead.score || 0, stage: lead.stage || "new", tags: lead.tags || [], notes: lead.notes || "" });
    setDialogOpen(true);
  };
  const openDetail = (lead) => { setSelectedLead(lead); setDetailOpen(true); loadComms(lead.id); };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!form.name.trim()) return;
    setSubmitting(true);
    try {
      if (editingLead) { await updateLead(editingLead.id, form); }
      else { await createLead(form); }
      setDialogOpen(false);
      load();
    } catch (err) { console.error(err); }
    setSubmitting(false);
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Bu lead'i silmek istediginize emin misiniz?")) return;
    await deleteLead(id).catch(console.error);
    load();
  };

  const addTag = () => {
    if (tagInput.trim() && !form.tags.includes(tagInput.trim())) {
      setForm({ ...form, tags: [...form.tags, tagInput.trim()] });
      setTagInput("");
    }
  };

  const removeTag = (t) => setForm({ ...form, tags: form.tags.filter((x) => x !== t) });

  const addComm = async () => {
    if (!commForm.content.trim() || !selectedLead) return;
    await createCommunication({ entity_type: "lead", entity_id: selectedLead.id, ...commForm });
    setCommForm({ comm_type: "note", subject: "", content: "", direction: "outbound" });
    loadComms(selectedLead.id);
  };

  const getScoreColor = (s) => s >= 70 ? "text-green-500" : s >= 40 ? "text-yellow-500" : "text-red-400";
  const getStageBadge = (stage) => {
    const s = STAGES.find((x) => x.value === stage);
    return s ? <span className={`inline-block w-2 h-2 rounded-full ${s.color} mr-1.5`} /> : null;
  };

  const formatDate = (d) => { if (!d) return ""; const dt = new Date(d); const diff = Math.floor((Date.now() - dt) / 60000); if (diff < 60) return `${diff} dk once`; if (diff < 1440) return `${Math.floor(diff / 60)} saat once`; return dt.toLocaleDateString("tr-TR"); };

  const handleConvert = async (lead) => {
    if (!window.confirm(`'${lead.name}' lead'ini musteriye donusturmek istediginize emin misiniz?`)) return;
    try {
      await convertLead(lead.id);
      load();
    } catch (err) {
      alert(err.response?.data?.detail || "Donusturme hatasi");
    }
  };

  const handleExportCsv = async () => {
    try {
      const blob = await exportLeadsCsv();
      const url = window.URL.createObjectURL(new Blob([blob]));
      const a = document.createElement("a");
      a.href = url;
      a.download = "leads_export.csv";
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (err) { console.error(err); }
  };

  const toggleSelectAll = () => {
    if (selectedIds.length === leads.length) {
      setSelectedIds([]);
    } else {
      setSelectedIds(leads.map((l) => l.id));
    }
  };

  const toggleSelect = (id) => {
    setSelectedIds((prev) => prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]);
  };

  const handleBulkStage = async (stage) => {
    if (!selectedIds.length) return;
    await bulkUpdateStage(selectedIds, stage);
    setSelectedIds([]);
    load();
  };

  const handleBulkDelete = async () => {
    if (!selectedIds.length) return;
    if (!window.confirm(`${selectedIds.length} lead silinecek. Emin misiniz?`)) return;
    await bulkDeleteLeads(selectedIds);
    setSelectedIds([]);
    load();
  };

  return (
    <div className="page-content">
      <PageHeader title="Lead Yonetimi" subtitle="Potansiyel musterilerinizi yonetin ve skorlayin" />

      {/* Filters */}
      <div className="flex flex-wrap gap-3 mb-6">
        <div className="relative flex-1 min-w-[200px]">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" size={16} />
          <Input placeholder="Lead ara..." value={search} onChange={(e) => { setSearch(e.target.value); setPage(1); }} className="pl-9" />
        </div>
        <Select value={stageFilter} onValueChange={(v) => { setStageFilter(v); setPage(1); }}>
          <SelectTrigger className="w-[160px]"><SelectValue placeholder="Asama" /></SelectTrigger>
          <SelectContent>
            <SelectItem value="all">Tum Asamalar</SelectItem>
            {STAGES.map((s) => <SelectItem key={s.value} value={s.value}>{s.label}</SelectItem>)}
          </SelectContent>
        </Select>
        <Select value={sourceFilter} onValueChange={(v) => { setSourceFilter(v); setPage(1); }}>
          <SelectTrigger className="w-[160px]"><SelectValue placeholder="Kaynak" /></SelectTrigger>
          <SelectContent>
            <SelectItem value="all">Tum Kaynaklar</SelectItem>
            {SOURCES.map((s) => <SelectItem key={s.value} value={s.value}>{s.label}</SelectItem>)}
          </SelectContent>
        </Select>
        <Button variant="outline" onClick={handleExportCsv} title="CSV Indir"><Download size={16} className="mr-1" /> CSV</Button>
        <Button onClick={openCreate}><Plus size={16} className="mr-1" /> Yeni Lead</Button>
      </div>

      {/* Bulk Actions Bar */}
      {selectedIds.length > 0 && (
        <div className="flex items-center gap-3 mb-4 p-3 bg-primary/10 rounded-lg border border-primary/30">
          <CheckSquare size={16} className="text-primary" />
          <span className="text-sm font-medium">{selectedIds.length} lead secildi</span>
          <div className="flex-1" />
          <Select onValueChange={handleBulkStage}>
            <SelectTrigger className="w-[160px] h-8 text-xs"><SelectValue placeholder="Toplu Asama" /></SelectTrigger>
            <SelectContent>
              {STAGES.map((s) => <SelectItem key={s.value} value={s.value}>{s.label}</SelectItem>)}
            </SelectContent>
          </Select>
          <Button variant="destructive" size="sm" onClick={handleBulkDelete}>
            <Trash2 size={12} className="mr-1" /> Toplu Sil
          </Button>
          <Button variant="ghost" size="sm" onClick={() => setSelectedIds([])}>Iptal</Button>
        </div>
      )}

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        {[{ label: "Toplam", val: totalCount }, { label: "Yeni", val: leads.filter((l) => l.stage === "new").length }, { label: "Kazanildi", val: leads.filter((l) => l.stage === "won").length }, { label: "Ort. Skor", val: leads.length ? Math.round(leads.reduce((a, l) => a + (l.score || 0), 0) / leads.length) : 0 }].map((s, i) => (
          <Card key={i}><CardContent className="p-4 text-center"><div className="text-2xl font-bold">{s.val}</div><div className="text-xs text-muted-foreground">{s.label}</div></CardContent></Card>
        ))}
      </div>

      {/* Table */}
      <Card>
        <CardContent className="p-0">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="w-[40px]">
                  <Checkbox checked={selectedIds.length === leads.length && leads.length > 0} onCheckedChange={toggleSelectAll} />
                </TableHead>
                <TableHead>Ad</TableHead>
                <TableHead>Sirket</TableHead>
                <TableHead>Kaynak</TableHead>
                <TableHead>Asama</TableHead>
                <TableHead>Skor</TableHead>
                <TableHead>Etiketler</TableHead>
                <TableHead>Tarih</TableHead>
                <TableHead className="w-[140px]">Islemler</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {loading ? (
                <TableRow><TableCell colSpan={9} className="text-center py-8 text-muted-foreground">Yukleniyor...</TableCell></TableRow>
              ) : leads.length === 0 ? (
                <TableRow><TableCell colSpan={9} className="text-center py-8 text-muted-foreground">Henuz lead yok</TableCell></TableRow>
              ) : leads.map((lead) => (
                <TableRow key={lead.id} className="cursor-pointer hover:bg-muted/50" onClick={() => openDetail(lead)}>
                  <TableCell>
                    <div className="font-medium">{lead.name}</div>
                    <div className="text-xs text-muted-foreground">{lead.email}</div>
                  </TableCell>
                  <TableCell className="text-sm">{lead.company || "-"}</TableCell>
                  <TableCell><Badge variant="outline" className="text-xs">{SOURCES.find((s) => s.value === lead.source)?.label || lead.source}</Badge></TableCell>
                  <TableCell><div className="flex items-center text-sm">{getStageBadge(lead.stage)}{STAGES.find((s) => s.value === lead.stage)?.label || lead.stage}</div></TableCell>
                  <TableCell><span className={`font-bold ${getScoreColor(lead.score)}`}>{lead.score}</span></TableCell>
                  <TableCell><div className="flex gap-1 flex-wrap">{(lead.tags || []).slice(0, 2).map((t) => <Badge key={t} variant="secondary" className="text-[10px]">{t}</Badge>)}{(lead.tags || []).length > 2 && <Badge variant="secondary" className="text-[10px]">+{lead.tags.length - 2}</Badge>}</div></TableCell>
                  <TableCell className="text-xs text-muted-foreground">{formatDate(lead.created_at)}</TableCell>
                  <TableCell>
                    <div className="flex gap-1" onClick={(e) => e.stopPropagation()}>
                      <Button variant="ghost" size="icon" className="h-7 w-7" onClick={() => openEdit(lead)}><Edit size={14} /></Button>
                      <Button variant="ghost" size="icon" className="h-7 w-7 text-destructive" onClick={() => handleDelete(lead.id)}><Trash2 size={14} /></Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      {/* Create/Edit Dialog */}
      <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
        <DialogContent className="max-w-lg max-h-[90vh] overflow-y-auto">
          <DialogHeader><DialogTitle>{editingLead ? "Lead Duzenle" : "Yeni Lead"}</DialogTitle></DialogHeader>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-2 gap-3">
              <div><label className="text-xs font-medium mb-1 block">Ad Soyad *</label><Input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required /></div>
              <div><label className="text-xs font-medium mb-1 block">Sirket</label><Input value={form.company} onChange={(e) => setForm({ ...form, company: e.target.value })} /></div>
              <div><label className="text-xs font-medium mb-1 block">Email</label><Input type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} /></div>
              <div><label className="text-xs font-medium mb-1 block">Telefon</label><Input value={form.phone} onChange={(e) => setForm({ ...form, phone: e.target.value })} /></div>
              <div><label className="text-xs font-medium mb-1 block">Kaynak</label>
                <Select value={form.source} onValueChange={(v) => setForm({ ...form, source: v })}><SelectTrigger><SelectValue /></SelectTrigger><SelectContent>{SOURCES.map((s) => <SelectItem key={s.value} value={s.value}>{s.label}</SelectItem>)}</SelectContent></Select>
              </div>
              <div><label className="text-xs font-medium mb-1 block">Asama</label>
                <Select value={form.stage} onValueChange={(v) => setForm({ ...form, stage: v })}><SelectTrigger><SelectValue /></SelectTrigger><SelectContent>{STAGES.map((s) => <SelectItem key={s.value} value={s.value}>{s.label}</SelectItem>)}</SelectContent></Select>
              </div>
            </div>
            <div><label className="text-xs font-medium mb-1 block">Skor (0-100)</label>
              <Input type="number" min={0} max={100} value={form.score} onChange={(e) => setForm({ ...form, score: parseInt(e.target.value) || 0 })} />
            </div>
            <div><label className="text-xs font-medium mb-1 block">Etiketler</label>
              <div className="flex gap-2">
                <Input placeholder="Etiket ekle..." value={tagInput} onChange={(e) => setTagInput(e.target.value)} onKeyDown={(e) => { if (e.key === "Enter") { e.preventDefault(); addTag(); }}} />
                <Button type="button" variant="outline" size="sm" onClick={addTag}>Ekle</Button>
              </div>
              <div className="flex gap-1 mt-2 flex-wrap">{form.tags.map((t) => <Badge key={t} variant="secondary" className="cursor-pointer" onClick={() => removeTag(t)}>{t} ×</Badge>)}</div>
            </div>
            <div><label className="text-xs font-medium mb-1 block">Notlar</label><Textarea value={form.notes} onChange={(e) => setForm({ ...form, notes: e.target.value })} rows={2} /></div>
            <div className="flex justify-end gap-2">
              <Button type="button" variant="outline" onClick={() => setDialogOpen(false)}>Iptal</Button>
              <Button type="submit" disabled={submitting}>{submitting ? "Kaydediliyor..." : editingLead ? "Guncelle" : "Olustur"}</Button>
            </div>
          </form>
        </DialogContent>
      </Dialog>

      {/* Detail + Timeline Dialog */}
      <Dialog open={detailOpen} onOpenChange={setDetailOpen}>
        <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
          {selectedLead && (
            <>
              <DialogHeader>
                <DialogTitle className="flex items-center gap-2">
                  {selectedLead.name}
                  <span className={`text-sm font-bold ${getScoreColor(selectedLead.score)}`}>{selectedLead.score} puan</span>
                </DialogTitle>
              </DialogHeader>
              <div className="grid grid-cols-2 gap-4 text-sm mb-4">
                <div><span className="text-muted-foreground">Sirket:</span> {selectedLead.company || "-"}</div>
                <div><span className="text-muted-foreground">Email:</span> {selectedLead.email || "-"}</div>
                <div><span className="text-muted-foreground">Telefon:</span> {selectedLead.phone || "-"}</div>
                <div><span className="text-muted-foreground">Kaynak:</span> {SOURCES.find((s) => s.value === selectedLead.source)?.label}</div>
                <div><span className="text-muted-foreground">Asama:</span> <span className="flex items-center gap-1 inline-flex">{getStageBadge(selectedLead.stage)}{STAGES.find((s) => s.value === selectedLead.stage)?.label}</span></div>
                <div><span className="text-muted-foreground">Etiketler:</span> {(selectedLead.tags || []).map((t) => <Badge key={t} variant="secondary" className="text-[10px] ml-1">{t}</Badge>)}</div>
              </div>
              {selectedLead.notes && <div className="bg-muted/50 p-3 rounded-lg text-sm mb-4">{selectedLead.notes}</div>}

              <h3 className="font-semibold text-sm mb-3 border-t pt-4">Iletisim Gecmisi</h3>
              <div className="flex gap-2 mb-3">
                <Select value={commForm.comm_type} onValueChange={(v) => setCommForm({ ...commForm, comm_type: v })}><SelectTrigger className="w-[120px]"><SelectValue /></SelectTrigger><SelectContent>{COMM_TYPES.map((c) => <SelectItem key={c.value} value={c.value}>{c.icon} {c.label}</SelectItem>)}</SelectContent></Select>
                <Input placeholder="Konu" value={commForm.subject} onChange={(e) => setCommForm({ ...commForm, subject: e.target.value })} className="flex-1" />
              </div>
              <div className="flex gap-2 mb-4">
                <Textarea placeholder="Detay yazin..." value={commForm.content} onChange={(e) => setCommForm({ ...commForm, content: e.target.value })} rows={2} className="flex-1" />
                <Button onClick={addComm} className="self-end">Ekle</Button>
              </div>

              <div className="space-y-3 max-h-[300px] overflow-y-auto">
                {comms.length === 0 ? <p className="text-sm text-muted-foreground text-center py-4">Henuz iletisim kaydı yok</p> : comms.map((c) => (
                  <div key={c.id} className="flex gap-3 p-3 bg-muted/30 rounded-lg">
                    <div className="text-xl">{COMM_TYPES.find((t) => t.value === c.comm_type)?.icon || "📋"}</div>
                    <div className="flex-1">
                      <div className="flex justify-between items-start">
                        <div className="font-medium text-sm">{c.subject || c.comm_type}</div>
                        <span className="text-[10px] text-muted-foreground">{formatDate(c.created_at)}</span>
                      </div>
                      <p className="text-xs text-muted-foreground mt-0.5">{c.content}</p>
                      {c.created_by_name && <p className="text-[10px] text-muted-foreground mt-1">— {c.created_by_name}</p>}
                    </div>
                  </div>
                ))}
              </div>
            </>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
}
