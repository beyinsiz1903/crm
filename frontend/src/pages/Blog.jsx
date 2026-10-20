import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Plus, Trash2, Edit, FileText, Eye, Tag, Calendar, User, Search } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import PageHeader from "@/components/PageHeader";
import { getBlogPosts, createBlogPost, updateBlogPost, deleteBlogPost, getProjects } from "@/lib/api";

export default function Blog() {
  const [posts, setPosts] = useState([]);
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingPost, setEditingPost] = useState(null);
  const [statusFilter, setStatusFilter] = useState("all");
  const [form, setForm] = useState({ project_id: "", title: "", content: "", excerpt: "", cover_image: "", tags: [], status: "draft" });
  const [tagInput, setTagInput] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const load = () => {
    setLoading(true);
    Promise.all([getBlogPosts({ status: statusFilter !== "all" ? statusFilter : undefined }), getProjects()])
      .then(([p, pr]) => { setPosts(p); setProjects(pr); })
      .catch(console.error).finally(() => setLoading(false));
  };
  useEffect(() => { load(); }, [statusFilter]);

  const openCreate = () => {
    setEditingPost(null);
    setForm({ project_id: projects[0]?.id || "", title: "", content: "", excerpt: "", cover_image: "", tags: [], status: "draft" });
    setDialogOpen(true);
  };

  const openEdit = (post) => {
    setEditingPost(post);
    setForm({ project_id: post.project_id || "", title: post.title, content: post.content || "", excerpt: post.excerpt || "", cover_image: post.cover_image || "", tags: post.tags || [], status: post.status || "draft" });
    setDialogOpen(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!form.title.trim() || !form.project_id) return;
    setSubmitting(true);
    try {
      if (editingPost) { await updateBlogPost(editingPost.id, form); }
      else { await createBlogPost(form); }
      setDialogOpen(false); load();
    } catch (err) { console.error(err); }
    setSubmitting(false);
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Bu yaziyi silmek istediginize emin misiniz?")) return;
    await deleteBlogPost(id).catch(console.error); load();
  };

  const toggleStatus = async (post) => {
    const newStatus = post.status === "published" ? "draft" : "published";
    await updateBlogPost(post.id, { status: newStatus }).catch(console.error);
    load();
  };

  const addTag = () => {
    if (tagInput.trim() && !form.tags.includes(tagInput.trim())) {
      setForm({ ...form, tags: [...form.tags, tagInput.trim()] });
      setTagInput("");
    }
  };

  const formatDate = (d) => d ? new Date(d).toLocaleDateString("tr-TR") : "";

  return (
    <div className="page-content">
      <PageHeader title="Blog Yonetimi" subtitle="Otel siteleriniz icin blog yazilari olusturun" />

      <div className="flex justify-between items-center mb-6">
        <div className="flex gap-2">
          <Select value={statusFilter} onValueChange={setStatusFilter}>
            <SelectTrigger className="w-[140px]"><SelectValue /></SelectTrigger>
            <SelectContent>
              <SelectItem value="all">Tumu</SelectItem>
              <SelectItem value="draft">Taslak</SelectItem>
              <SelectItem value="published">Yayinda</SelectItem>
            </SelectContent>
          </Select>
          <Badge variant="secondary">{posts.length} yazi</Badge>
        </div>
        <Button onClick={openCreate}><Plus size={16} className="mr-1" /> Yeni Yazi</Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {loading ? [1,2,3].map(i => <Card key={i}><CardContent className="p-6"><div className="animate-pulse space-y-3"><div className="h-32 bg-muted rounded" /><div className="h-5 bg-muted rounded w-3/4" /></div></CardContent></Card>) :
        posts.length === 0 ? <div className="col-span-3 text-center py-12 text-muted-foreground">Henuz blog yazisi yok</div> :
        posts.map((post) => (
          <motion.div key={post.id} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
            <Card className="card-hover overflow-hidden">
              {post.cover_image && <img src={post.cover_image} alt="" className="w-full h-32 object-cover" />}
              <CardContent className="p-5">
                <div className="flex justify-between items-start mb-2">
                  <h3 className="font-semibold text-sm flex-1">{post.title}</h3>
                  <Badge variant={post.status === "published" ? "default" : "secondary"} className="ml-2">{post.status === "published" ? "Yayinda" : "Taslak"}</Badge>
                </div>
                {post.excerpt && <p className="text-xs text-muted-foreground mb-3 line-clamp-2">{post.excerpt}</p>}
                <div className="flex items-center gap-2 text-xs text-muted-foreground mb-3">
                  <User size={10} /><span>{post.author || "Admin"}</span>
                  <Calendar size={10} className="ml-2" /><span>{formatDate(post.updated_at)}</span>
                </div>
                {post.tags?.length > 0 && <div className="flex gap-1 mb-3 flex-wrap">{post.tags.map(t => <Badge key={t} variant="outline" className="text-[9px]">{t}</Badge>)}</div>}
                <div className="flex gap-1.5">
                  <Button size="sm" variant="outline" className="flex-1" onClick={() => toggleStatus(post)}>{post.status === "published" ? "Taslaga Al" : "Yayinla"}</Button>
                  <Button size="sm" variant="ghost" onClick={() => openEdit(post)}><Edit size={12} /></Button>
                  <Button size="sm" variant="ghost" className="text-destructive" onClick={() => handleDelete(post.id)}><Trash2 size={12} /></Button>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>

      {/* Blog Editor Dialog */}
      <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
        <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
          <DialogHeader><DialogTitle>{editingPost ? "Yazi Duzenle" : "Yeni Blog Yazisi"}</DialogTitle></DialogHeader>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-2 gap-3">
              <div><label className="text-xs font-medium mb-1 block">Baslik *</label><Input value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} required /></div>
              <div><label className="text-xs font-medium mb-1 block">Proje *</label>
                <Select value={form.project_id || "none"} onValueChange={(v) => setForm({ ...form, project_id: v === "none" ? "" : v })}>
                  <SelectTrigger><SelectValue placeholder="Proje sec..." /></SelectTrigger>
                  <SelectContent>{projects.map(p => <SelectItem key={p.id} value={p.id}>{p.name}</SelectItem>)}</SelectContent>
                </Select>
              </div>
            </div>
            <div><label className="text-xs font-medium mb-1 block">Ozet</label><Input value={form.excerpt} onChange={(e) => setForm({ ...form, excerpt: e.target.value })} /></div>
            <div><label className="text-xs font-medium mb-1 block">Kapak Gorseli URL</label><Input value={form.cover_image} onChange={(e) => setForm({ ...form, cover_image: e.target.value })} placeholder="https://..." /></div>
            <div><label className="text-xs font-medium mb-1 block">Icerik</label>
              <Textarea value={form.content} onChange={(e) => setForm({ ...form, content: e.target.value })} rows={10} placeholder="Blog icerigi..." />
            </div>
            <div><label className="text-xs font-medium mb-1 block">Etiketler</label>
              <div className="flex gap-2">
                <Input placeholder="Etiket ekle..." value={tagInput} onChange={(e) => setTagInput(e.target.value)} onKeyDown={(e) => { if (e.key === "Enter") { e.preventDefault(); addTag(); }}} />
                <Button type="button" variant="outline" size="sm" onClick={addTag}>Ekle</Button>
              </div>
              <div className="flex gap-1 mt-2 flex-wrap">{form.tags.map(t => <Badge key={t} variant="secondary" className="cursor-pointer" onClick={() => setForm({ ...form, tags: form.tags.filter(x => x !== t) })}>{t} ×</Badge>)}</div>
            </div>
            <div><label className="text-xs font-medium mb-1 block">Durum</label>
              <Select value={form.status} onValueChange={(v) => setForm({ ...form, status: v })}>
                <SelectTrigger className="w-[140px]"><SelectValue /></SelectTrigger>
                <SelectContent><SelectItem value="draft">Taslak</SelectItem><SelectItem value="published">Yayinla</SelectItem></SelectContent>
              </Select>
            </div>
            <div className="flex justify-end gap-2">
              <Button type="button" variant="outline" onClick={() => setDialogOpen(false)}>Iptal</Button>
              <Button type="submit" disabled={submitting}>{submitting ? "Kaydediliyor..." : editingPost ? "Guncelle" : "Olustur"}</Button>
            </div>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  );
}
