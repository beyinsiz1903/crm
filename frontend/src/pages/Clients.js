import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Plus, Search, Building2, Phone, Mail, MapPin, Edit, Trash2, X, Tag, MessageSquare } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import PageHeader from "@/components/PageHeader";
import { getClients, createClient, updateClient, deleteClient, getCommunications, createCommunication } from "@/lib/api";

const CATEGORIES = ["", "premium", "standart", "yeni", "vip", "potansiyel"];
const COMM_TYPES = [
  { value: "email", label: "Email", icon: "📧" },
  { value: "phone", label: "Telefon", icon: "📞" },
  { value: "meeting", label: "Toplanti", icon: "🤝" },
  { value: "note", label: "Not", icon: "📝" },
];

const emptyForm = { hotel_name: "", contact_name: "", email: "", phone: "", address: "", city: "", notes: "", tags: [], category: "", custom_fields: {} };

export default function Clients() {
  const [clients, setClients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [dialogOpen, setDialogOpen] = useState(false);
  const [detailOpen, setDetailOpen] = useState(false);
  const [editingClient, setEditingClient] = useState(null);
  const [selectedClient, setSelectedClient] = useState(null);
  const [form, setForm] = useState(emptyForm);
  const [tagInput, setTagInput] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [comms, setComms] = useState([]);
  const [commForm, setCommForm] = useState({ comm_type: "note", subject: "", content: "", direction: "outbound" });
  const [categoryFilter, setCategoryFilter] = useState("all");

  const load = () => {
    setLoading(true);
    getClients(search || null)
      .then((data) => {
        if (categoryFilter !== "all") {
          setClients(data.filter(c => c.category === categoryFilter));
        } else {
          setClients(data);
        }
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    load();
  }, [search, categoryFilter]);

  const openCreate = () => {
    setEditingClient(null);
    setForm(emptyForm);
    setDialogOpen(true);
  };

  const openEdit = (client) => {
    setEditingClient(client);
    setForm({
      hotel_name: client.hotel_name || "",
      contact_name: client.contact_name || "",
      email: client.email || "",
      phone: client.phone || "",
      address: client.address || "",
      city: client.city || "",
      notes: client.notes || "",
      tags: client.tags || [],
      category: client.category || "",
      custom_fields: client.custom_fields || {},
    });
    setDialogOpen(true);
  };

  const openDetail = (client) => {
    setSelectedClient(client);
    setDetailOpen(true);
    getCommunications("client", client.id).then(setComms).catch(() => setComms([]));
  };

  const addTag = () => {
    if (tagInput.trim() && !form.tags.includes(tagInput.trim())) {
      setForm({ ...form, tags: [...form.tags, tagInput.trim()] });
      setTagInput("");
    }
  };

  const addComm = async () => {
    if (!commForm.content.trim() || !selectedClient) return;
    await createCommunication({ entity_type: "client", entity_id: selectedClient.id, ...commForm });
    setCommForm({ comm_type: "note", subject: "", content: "", direction: "outbound" });
    getCommunications("client", selectedClient.id).then(setComms).catch(() => {});
  };

  const formatDate = (d) => { if (!d) return ""; const dt = new Date(d); const diff = Math.floor((Date.now() - dt) / 60000); if (diff < 60) return `${diff} dk once`; if (diff < 1440) return `${Math.floor(diff / 60)} saat once`; return dt.toLocaleDateString("tr-TR"); };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!form.hotel_name.trim()) return;
    setSubmitting(true);
    try {
      if (editingClient) {
        await updateClient(editingClient.id, form);
      } else {
        await createClient(form);
      }
      setDialogOpen(false);
      load();
    } catch (err) {
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Bu musteriyi silmek istediginize emin misiniz?")) return;
    try {
      await deleteClient(id);
      load();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="page-content">
      <PageHeader title="Musteriler" subtitle="Otel musterilerinizi yonetin">
        <Button onClick={openCreate} data-testid="clients-add-button">
          <Plus size={16} className="mr-2" /> Yeni Musteri
        </Button>
      </PageHeader>

      {/* Search + Filter */}
      <div className="flex gap-3 mb-6">
        <div className="relative flex-1 max-w-xs">
          <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" />
          <Input
            placeholder="Musteri ara..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="pl-9"
            data-testid="clients-search-input"
          />
        </div>
        <Select value={categoryFilter} onValueChange={setCategoryFilter}>
          <SelectTrigger className="w-[150px]"><SelectValue placeholder="Kategori" /></SelectTrigger>
          <SelectContent>
            <SelectItem value="all">Tum Kategoriler</SelectItem>
            {CATEGORIES.filter(Boolean).map(c => <SelectItem key={c} value={c}>{c.charAt(0).toUpperCase() + c.slice(1)}</SelectItem>)}
          </SelectContent>
        </Select>
      </div>

      {/* Clients Table */}
      <Card className="border-border/50">
        <CardContent className="p-0">
          {loading ? (
            <div className="p-8 text-center text-muted-foreground">Yukleniyor...</div>
          ) : clients.length === 0 ? (
            <div className="p-12 text-center">
              <Building2 size={48} className="mx-auto mb-4 text-muted-foreground/50" />
              <p className="text-muted-foreground mb-4">Henuz musteri eklemediniz.</p>
              <Button onClick={openCreate} data-testid="clients-empty-add">
                <Plus size={16} className="mr-2" /> Ilk Musteriyi Ekle
              </Button>
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Otel Adi</TableHead>
                  <TableHead>Yetkili</TableHead>
                  <TableHead>Sehir</TableHead>
                  <TableHead>Telefon</TableHead>
                  <TableHead>E-posta</TableHead>
                  <TableHead className="text-right">Islemler</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {clients.map((client) => (
                  <TableRow key={client.id} className="hover:bg-muted/30">
                    <TableCell className="font-medium">{client.hotel_name}</TableCell>
                    <TableCell>{client.contact_name}</TableCell>
                    <TableCell>{client.city}</TableCell>
                    <TableCell className="font-mono text-sm">{client.phone}</TableCell>
                    <TableCell className="text-sm">{client.email}</TableCell>
                    <TableCell className="text-right">
                      <div className="flex items-center justify-end gap-1">
                        <Button
                          variant="ghost" size="icon" className="h-8 w-8"
                          onClick={() => openEdit(client)}
                          data-testid={`client-edit-${client.id}`}
                        >
                          <Edit size={14} />
                        </Button>
                        <Button
                          variant="ghost" size="icon" className="h-8 w-8 text-destructive hover:text-destructive"
                          onClick={() => handleDelete(client.id)}
                          data-testid={`client-delete-${client.id}`}
                        >
                          <Trash2 size={14} />
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>

      {/* Create/Edit Dialog */}
      <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
        <DialogContent className="max-w-lg">
          <DialogHeader>
            <DialogTitle>{editingClient ? "Musteri Duzenle" : "Yeni Musteri"}</DialogTitle>
          </DialogHeader>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="text-xs text-muted-foreground mb-1 block">Otel Adi *</label>
              <Input
                value={form.hotel_name}
                onChange={(e) => setForm((f) => ({ ...f, hotel_name: e.target.value }))}
                placeholder="Ornek: Grand Hotel Istanbul"
                data-testid="client-form-hotel-name-input"
                required
              />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-xs text-muted-foreground mb-1 block">Yetkili Kisi</label>
                <Input
                  value={form.contact_name}
                  onChange={(e) => setForm((f) => ({ ...f, contact_name: e.target.value }))}
                  placeholder="Ad Soyad"
                  data-testid="client-form-contact-name-input"
                />
              </div>
              <div>
                <label className="text-xs text-muted-foreground mb-1 block">Sehir</label>
                <Input
                  value={form.city}
                  onChange={(e) => setForm((f) => ({ ...f, city: e.target.value }))}
                  placeholder="Istanbul"
                  data-testid="client-form-city-input"
                />
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-xs text-muted-foreground mb-1 block">Telefon</label>
                <Input
                  value={form.phone}
                  onChange={(e) => setForm((f) => ({ ...f, phone: e.target.value }))}
                  placeholder="+90 ..."
                  data-testid="client-form-phone-input"
                />
              </div>
              <div>
                <label className="text-xs text-muted-foreground mb-1 block">E-posta</label>
                <Input
                  value={form.email}
                  onChange={(e) => setForm((f) => ({ ...f, email: e.target.value }))}
                  placeholder="info@otel.com"
                  data-testid="client-form-email-input"
                />
              </div>
            </div>
            <div>
              <label className="text-xs text-muted-foreground mb-1 block">Adres</label>
              <Input
                value={form.address}
                onChange={(e) => setForm((f) => ({ ...f, address: e.target.value }))}
                placeholder="Tam adres"
                data-testid="client-form-address-input"
              />
            </div>
            <div>
              <label className="text-xs text-muted-foreground mb-1 block">Notlar</label>
              <Textarea
                value={form.notes}
                onChange={(e) => setForm((f) => ({ ...f, notes: e.target.value }))}
                placeholder="Musteri hakkinda notlar..."
                className="min-h-[80px]"
                data-testid="client-form-notes-input"
              />
            </div>
            <div className="flex justify-end gap-3 pt-2">
              <Button type="button" variant="outline" onClick={() => setDialogOpen(false)}>Iptal</Button>
              <Button type="submit" disabled={submitting} data-testid="client-form-submit">
                {submitting ? "Kaydediliyor..." : (editingClient ? "Guncelle" : "Ekle")}
              </Button>
            </div>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  );
}
