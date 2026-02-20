import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { Plus, Search, Edit, Trash2, Download, ExternalLink, FolderOpen, Eye } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Textarea } from "@/components/ui/textarea";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import PageHeader from "@/components/PageHeader";
import { getProjects, deleteProject, updateProject, exportProject, getClients } from "@/lib/api";

const STATUS_OPTIONS = [
  { value: "all", label: "Tum Durumlar" },
  { value: "draft", label: "Taslak" },
  { value: "published", label: "Yayinda" },
  { value: "delivered", label: "Teslim Edildi" },
];

const STATUS_CLASS = {
  draft: "status-draft",
  published: "status-published",
  delivered: "status-delivered",
};

const STATUS_LABEL = {
  draft: "Taslak",
  published: "Yayinda",
  delivered: "Teslim Edildi",
};

export default function Projects() {
  const navigate = useNavigate();
  const [projects, setProjects] = useState([]);
  const [clients, setClients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState("all");
  const [search, setSearch] = useState("");
  const [editDialog, setEditDialog] = useState(null);
  const [editForm, setEditForm] = useState({ name: "", status: "draft", client_id: "", domain_notes: "", hosting_notes: "" });
  const [submitting, setSubmitting] = useState(false);

  const load = () => {
    setLoading(true);
    Promise.all([
      getProjects(statusFilter === "all" ? null : statusFilter),
      getClients(),
    ])
      .then(([projs, cls]) => {
        setProjects(projs);
        setClients(cls);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    load();
  }, [statusFilter]);

  const filtered = projects.filter((p) =>
    !search || p.name.toLowerCase().includes(search.toLowerCase())
  );

  const getClientName = (clientId) => {
    const client = clients.find((c) => c.id === clientId);
    return client?.hotel_name || "-";
  };

  const handleExport = async (project) => {
    try {
      const blob = await exportProject(project.id);
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${project.name}.zip`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      console.error(err);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Bu projeyi silmek istediginize emin misiniz?")) return;
    try {
      await deleteProject(id);
      load();
    } catch (err) {
      console.error(err);
    }
  };

  const openEditDialog = (project) => {
    setEditDialog(project);
    setEditForm({
      name: project.name || "",
      status: project.status || "draft",
      client_id: project.client_id || "",
      domain_notes: project.domain_notes || "",
      hosting_notes: project.hosting_notes || "",
    });
  };

  const handleEditSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await updateProject(editDialog.id, editForm);
      setEditDialog(null);
      load();
    } catch (err) {
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  const formatDate = (dateStr) => {
    if (!dateStr) return "-";
    return new Date(dateStr).toLocaleDateString("tr-TR", { day: "numeric", month: "short", year: "numeric" });
  };

  return (
    <div className="page-content">
      <PageHeader title="Projeler" subtitle="Olusturulan web sitesi projeleriniz">
        <Button onClick={() => navigate("/templates")} data-testid="projects-new-button">
          <Plus size={16} className="mr-2" /> Yeni Proje
        </Button>
      </PageHeader>

      {/* Filters */}
      <div className="flex items-center gap-3 mb-6">
        <div className="relative max-w-xs">
          <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" />
          <Input
            placeholder="Proje ara..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="pl-9"
            data-testid="projects-search-input"
          />
        </div>
        <Select value={statusFilter} onValueChange={setStatusFilter}>
          <SelectTrigger className="w-[180px]" data-testid="projects-status-filter">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            {STATUS_OPTIONS.map((o) => (
              <SelectItem key={o.value} value={o.value}>{o.label}</SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      {/* Projects Table */}
      <Card className="border-border/50">
        <CardContent className="p-0">
          {loading ? (
            <div className="p-8 text-center text-muted-foreground">Yukleniyor...</div>
          ) : filtered.length === 0 ? (
            <div className="p-12 text-center">
              <FolderOpen size={48} className="mx-auto mb-4 text-muted-foreground/50" />
              <p className="text-muted-foreground mb-4">Henuz proje yok. Bir sablon secerek baslayin.</p>
              <Button onClick={() => navigate("/templates")} data-testid="projects-empty-start">
                <Plus size={16} className="mr-2" /> Sablonlardan Baslat
              </Button>
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Proje Adi</TableHead>
                  <TableHead>Musteri</TableHead>
                  <TableHead>Durum</TableHead>
                  <TableHead>Olusturma</TableHead>
                  <TableHead>Guncelleme</TableHead>
                  <TableHead className="text-right">Islemler</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filtered.map((project) => (
                  <TableRow key={project.id} className="hover:bg-muted/30">
                    <TableCell className="font-medium">{project.name}</TableCell>
                    <TableCell>{getClientName(project.client_id)}</TableCell>
                    <TableCell>
                      <Badge
                        variant="outline"
                        className={`text-xs px-2 py-0.5 ${STATUS_CLASS[project.status]}`}
                        data-testid="projects-status-badge"
                      >
                        {STATUS_LABEL[project.status] || project.status}
                      </Badge>
                    </TableCell>
                    <TableCell className="text-sm text-muted-foreground">{formatDate(project.created_at)}</TableCell>
                    <TableCell className="text-sm text-muted-foreground">{formatDate(project.updated_at)}</TableCell>
                    <TableCell className="text-right">
                      <div className="flex items-center justify-end gap-1">
                        <Button
                          variant="ghost" size="icon" className="h-8 w-8"
                          onClick={() => navigate(`/editor/${project.id}`)}
                          title="Duzenle"
                          data-testid={`project-edit-${project.id}`}
                        >
                          <Edit size={14} />
                        </Button>
                        <Button
                          variant="ghost" size="icon" className="h-8 w-8"
                          onClick={() => openEditDialog(project)}
                          title="Ayarlar"
                          data-testid={`project-settings-${project.id}`}
                        >
                          <ExternalLink size={14} />
                        </Button>
                        <Button
                          variant="ghost" size="icon" className="h-8 w-8"
                          onClick={() => handleExport(project)}
                          title="Disa Aktar"
                          data-testid={`project-export-${project.id}`}
                        >
                          <Download size={14} />
                        </Button>
                        <Button
                          variant="ghost" size="icon" className="h-8 w-8 text-destructive hover:text-destructive"
                          onClick={() => handleDelete(project.id)}
                          title="Sil"
                          data-testid={`project-delete-${project.id}`}
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

      {/* Edit Project Dialog */}
      <Dialog open={!!editDialog} onOpenChange={() => setEditDialog(null)}>
        <DialogContent className="max-w-lg">
          <DialogHeader>
            <DialogTitle>Proje Ayarlari</DialogTitle>
          </DialogHeader>
          <form onSubmit={handleEditSubmit} className="space-y-4">
            <div>
              <label className="text-xs text-muted-foreground mb-1 block">Proje Adi</label>
              <Input
                value={editForm.name}
                onChange={(e) => setEditForm((f) => ({ ...f, name: e.target.value }))}
                data-testid="project-form-name-input"
              />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-xs text-muted-foreground mb-1 block">Durum</label>
                <Select value={editForm.status} onValueChange={(v) => setEditForm((f) => ({ ...f, status: v }))}>
                  <SelectTrigger data-testid="project-form-status-select">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="draft">Taslak</SelectItem>
                    <SelectItem value="published">Yayinda</SelectItem>
                    <SelectItem value="delivered">Teslim Edildi</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div>
                <label className="text-xs text-muted-foreground mb-1 block">Musteri</label>
                <Select value={editForm.client_id || "none"} onValueChange={(v) => setEditForm((f) => ({ ...f, client_id: v === "none" ? "" : v }))}>
                  <SelectTrigger data-testid="project-form-client-select">
                    <SelectValue placeholder="Musteri sec" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="none">Musteri Yok</SelectItem>
                    {clients.map((c) => (
                      <SelectItem key={c.id} value={c.id}>{c.hotel_name}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>
            <div>
              <label className="text-xs text-muted-foreground mb-1 block">Domain Notlari</label>
              <Textarea
                value={editForm.domain_notes}
                onChange={(e) => setEditForm((f) => ({ ...f, domain_notes: e.target.value }))}
                placeholder="Domain bilgileri..."
                className="min-h-[60px]"
                data-testid="project-form-domain-notes"
              />
            </div>
            <div>
              <label className="text-xs text-muted-foreground mb-1 block">Hosting Notlari</label>
              <Textarea
                value={editForm.hosting_notes}
                onChange={(e) => setEditForm((f) => ({ ...f, hosting_notes: e.target.value }))}
                placeholder="Hosting bilgileri..."
                className="min-h-[60px]"
                data-testid="project-form-hosting-notes"
              />
            </div>
            <div className="flex justify-end gap-3 pt-2">
              <Button type="button" variant="outline" onClick={() => setEditDialog(null)}>Iptal</Button>
              <Button type="submit" disabled={submitting} data-testid="project-form-submit">
                {submitting ? "Kaydediliyor..." : "Guncelle"}
              </Button>
            </div>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  );
}
