import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Plus, Trash2, Edit, GripVertical, Eye, FileText, X, CheckCircle, ClipboardList } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Switch } from "@/components/ui/switch";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import PageHeader from "@/components/PageHeader";
import { getForms, createForm, updateForm, deleteForm, getFormSubmissions, getProjects } from "@/lib/api";

const FIELD_TYPES = [
  { value: "text", label: "Metin" },
  { value: "email", label: "Email" },
  { value: "phone", label: "Telefon" },
  { value: "textarea", label: "Uzun Metin" },
  { value: "select", label: "Secim Listesi" },
  { value: "date", label: "Tarih" },
  { value: "number", label: "Sayi" },
  { value: "checkbox", label: "Onay Kutusu" },
];

const FORM_TYPES = [
  { value: "contact", label: "Iletisim" },
  { value: "reservation", label: "Rezervasyon" },
  { value: "feedback", label: "Geri Bildirim" },
  { value: "custom", label: "Ozel" },
];

const emptyField = { type: "text", label: "", required: false, placeholder: "", options: "" };

export default function FormBuilder() {
  const [forms, setForms] = useState([]);
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [subsOpen, setSubsOpen] = useState(false);
  const [editingForm, setEditingForm] = useState(null);
  const [submissions, setSubmissions] = useState([]);
  const [selectedForm, setSelectedForm] = useState(null);
  const [form, setForm] = useState({ name: "", project_id: "", form_type: "contact", fields: [] });
  const [submitting, setSubmitting] = useState(false);

  const load = () => { setLoading(true); Promise.all([getForms(), getProjects()]).then(([f, p]) => { setForms(f); setProjects(p); }).catch(console.error).finally(() => setLoading(false)); };
  useEffect(() => { load(); }, []);

  const openCreate = () => {
    setEditingForm(null);
    setForm({ name: "", project_id: "", form_type: "contact", fields: [{ type: "text", label: "Ad Soyad", required: true, placeholder: "Adinizi girin", options: "" }, { type: "email", label: "Email", required: true, placeholder: "Email adresiniz", options: "" }, { type: "textarea", label: "Mesaj", required: false, placeholder: "Mesajiniz...", options: "" }] });
    setDialogOpen(true);
  };

  const openEdit = (f) => {
    setEditingForm(f);
    setForm({ name: f.name, project_id: f.project_id || "", form_type: f.form_type || "contact", fields: f.fields || [] });
    setDialogOpen(true);
  };

  const openSubs = async (f) => {
    setSelectedForm(f);
    const subs = await getFormSubmissions(f.id).catch(() => []);
    setSubmissions(subs);
    setSubsOpen(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!form.name.trim()) return;
    setSubmitting(true);
    try {
      if (editingForm) { await updateForm(editingForm.id, form); }
      else { await createForm(form); }
      setDialogOpen(false); load();
    } catch (err) { console.error(err); }
    setSubmitting(false);
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Bu formu silmek istediginize emin misiniz?")) return;
    await deleteForm(id).catch(console.error); load();
  };

  const addField = () => setForm({ ...form, fields: [...form.fields, { ...emptyField }] });
  const updateField = (idx, key, value) => {
    const fields = [...form.fields];
    fields[idx] = { ...fields[idx], [key]: value };
    setForm({ ...form, fields });
  };
  const removeField = (idx) => setForm({ ...form, fields: form.fields.filter((_, i) => i !== idx) });

  return (
    <div className="page-content">
      <PageHeader title="Form Builder" subtitle="Dinamik formlar olusturun ve veri toplayin" />

      <div className="flex justify-end mb-6">
        <Button onClick={openCreate}><Plus size={16} className="mr-1" /> Yeni Form</Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {loading ? [1,2,3].map(i => <Card key={i}><CardContent className="p-6"><div className="animate-pulse space-y-3"><div className="h-5 bg-muted rounded w-3/4" /><div className="h-4 bg-muted rounded w-1/2" /></div></CardContent></Card>) :
        forms.length === 0 ? <div className="col-span-3 text-center py-12 text-muted-foreground">Henuz form olusturulmadi</div> :
        forms.map((f) => (
          <motion.div key={f.id} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
            <Card className="card-hover">
              <CardContent className="p-5">
                <div className="flex justify-between items-start mb-3">
                  <div>
                    <h3 className="font-semibold text-sm">{f.name}</h3>
                    <p className="text-xs text-muted-foreground mt-0.5">{FORM_TYPES.find(t => t.value === f.form_type)?.label || f.form_type}</p>
                  </div>
                  <Badge variant={f.status === "active" ? "default" : "secondary"}>{f.status === "active" ? "Aktif" : "Pasif"}</Badge>
                </div>
                <div className="flex items-center gap-3 text-xs text-muted-foreground mb-3">
                  <span>{(f.fields || []).length} alan</span>
                  <span>{f.submissions_count || 0} gonderim</span>
                  {f.project_id && <span>Proje baglantiili</span>}
                </div>
                <div className="flex gap-1.5">
                  <Button size="sm" variant="outline" className="flex-1" onClick={() => openSubs(f)}><ClipboardList size={12} className="mr-1" />Gonderimler</Button>
                  <Button size="sm" variant="ghost" onClick={() => openEdit(f)}><Edit size={12} /></Button>
                  <Button size="sm" variant="ghost" className="text-destructive" onClick={() => handleDelete(f.id)}><Trash2 size={12} /></Button>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>

      {/* Form Builder Dialog */}
      <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
        <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
          <DialogHeader><DialogTitle>{editingForm ? "Form Duzenle" : "Yeni Form"}</DialogTitle></DialogHeader>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-3 gap-3">
              <div><label className="text-xs font-medium mb-1 block">Form Adi *</label><Input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required /></div>
              <div><label className="text-xs font-medium mb-1 block">Tur</label>
                <Select value={form.form_type} onValueChange={(v) => setForm({ ...form, form_type: v })}><SelectTrigger><SelectValue /></SelectTrigger><SelectContent>{FORM_TYPES.map(t => <SelectItem key={t.value} value={t.value}>{t.label}</SelectItem>)}</SelectContent></Select>
              </div>
              <div><label className="text-xs font-medium mb-1 block">Proje</label>
                <Select value={form.project_id || "none"} onValueChange={(v) => setForm({ ...form, project_id: v === "none" ? "" : v })}>
                  <SelectTrigger><SelectValue placeholder="Sec..." /></SelectTrigger>
                  <SelectContent><SelectItem value="none">Bagimsiz</SelectItem>{projects.map(p => <SelectItem key={p.id} value={p.id}>{p.name}</SelectItem>)}</SelectContent>
                </Select>
              </div>
            </div>

            <div>
              <div className="flex justify-between items-center mb-2">
                <label className="text-xs font-semibold">Form Alanlari</label>
                <Button type="button" variant="outline" size="sm" onClick={addField}><Plus size={12} className="mr-1" />Alan Ekle</Button>
              </div>
              {form.fields.map((field, idx) => (
                <div key={idx} className="border rounded-lg p-3 mb-2">
                  <div className="flex gap-2 items-start">
                    <div className="flex-1 grid grid-cols-2 gap-2">
                      <Input placeholder="Alan adi" value={field.label} onChange={(e) => updateField(idx, "label", e.target.value)} />
                      <Select value={field.type} onValueChange={(v) => updateField(idx, "type", v)}>
                        <SelectTrigger><SelectValue /></SelectTrigger>
                        <SelectContent>{FIELD_TYPES.map(ft => <SelectItem key={ft.value} value={ft.value}>{ft.label}</SelectItem>)}</SelectContent>
                      </Select>
                      <Input placeholder="Placeholder" value={field.placeholder || ""} onChange={(e) => updateField(idx, "placeholder", e.target.value)} />
                      {field.type === "select" && <Input placeholder="Secenekler (virgul ile)" value={field.options || ""} onChange={(e) => updateField(idx, "options", e.target.value)} />}
                    </div>
                    <div className="flex items-center gap-2">
                      <label className="text-[10px] flex items-center gap-1"><Switch checked={field.required} onCheckedChange={(v) => updateField(idx, "required", v)} />Zorunlu</label>
                      <Button type="button" variant="ghost" size="icon" className="h-7 w-7" onClick={() => removeField(idx)}><Trash2 size={12} /></Button>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            <div className="flex justify-end gap-2">
              <Button type="button" variant="outline" onClick={() => setDialogOpen(false)}>Iptal</Button>
              <Button type="submit" disabled={submitting}>{submitting ? "Kaydediliyor..." : editingForm ? "Guncelle" : "Olustur"}</Button>
            </div>
          </form>
        </DialogContent>
      </Dialog>

      {/* Submissions Dialog */}
      <Dialog open={subsOpen} onOpenChange={setSubsOpen}>
        <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
          <DialogHeader><DialogTitle>{selectedForm?.name} - Gonderimler</DialogTitle></DialogHeader>
          {submissions.length === 0 ? <p className="text-sm text-muted-foreground text-center py-8">Henuz gonderim yok</p> : (
            <Table>
              <TableHeader><TableRow><TableHead>#</TableHead><TableHead>Veri</TableHead><TableHead>Tarih</TableHead></TableRow></TableHeader>
              <TableBody>
                {submissions.map((s, i) => (
                  <TableRow key={s.id}>
                    <TableCell>{i + 1}</TableCell>
                    <TableCell><pre className="text-xs whitespace-pre-wrap">{JSON.stringify(s.data, null, 2)}</pre></TableCell>
                    <TableCell className="text-xs">{new Date(s.created_at).toLocaleString("tr-TR")}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
}
