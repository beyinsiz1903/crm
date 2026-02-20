import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { Search, Eye, ArrowRight, X } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import PageHeader from "@/components/PageHeader";
import { getTemplates, createProject } from "@/lib/api";
import { generatePreviewHTML } from "@/lib/previewRenderer";

const CATEGORIES = [
  { value: "all", label: "Tumu" },
  { value: "luxury", label: "Luks" },
  { value: "boutique", label: "Butik" },
  { value: "resort", label: "Resort & Spa" },
  { value: "business", label: "Is Oteli" },
  { value: "beach", label: "Sahil" },
  { value: "mountain", label: "Dag" },
  { value: "city", label: "Sehir" },
];

export default function TemplateGallery() {
  const navigate = useNavigate();
  const [templates, setTemplates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [category, setCategory] = useState("all");
  const [search, setSearch] = useState("");
  const [previewTemplate, setPreviewTemplate] = useState(null);
  const [creating, setCreating] = useState(false);

  useEffect(() => {
    setLoading(true);
    getTemplates(category === "all" ? null : category)
      .then(setTemplates)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [category]);

  const filtered = templates.filter((t) =>
    !search || t.name.toLowerCase().includes(search.toLowerCase()) || t.description.toLowerCase().includes(search.toLowerCase())
  );

  const handleUseTemplate = async (template) => {
    setCreating(true);
    try {
      const project = await createProject({
        name: `${template.name} - Yeni Proje`,
        template_id: template.id,
      });
      navigate(`/editor/${project.id}`);
    } catch (err) {
      console.error(err);
      alert("Proje olusturulamadi");
    } finally {
      setCreating(false);
    }
  };

  return (
    <div className="page-content">
      <PageHeader title="Sablon Galerisi" subtitle={`${templates.length} adet otel web sitesi sablonu`} />

      {/* Filter Bar */}
      <div className="sticky top-0 z-10 bg-background/80 backdrop-blur-sm pb-4 mb-6 -mt-2">
        <div className="flex flex-wrap items-center gap-3">
          <div className="relative flex-1 max-w-xs">
            <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" />
            <Input
              placeholder="Sablon ara..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="pl-9"
              data-testid="template-gallery-search"
            />
          </div>
          <div className="flex flex-wrap gap-2" data-testid="template-gallery-category-filter">
            {CATEGORIES.map((cat) => (
              <Button
                key={cat.value}
                variant={category === cat.value ? "default" : "outline"}
                size="sm"
                onClick={() => setCategory(cat.value)}
                data-testid={`template-filter-${cat.value}`}
                className="text-xs"
              >
                {cat.label}
              </Button>
            ))}
          </div>
        </div>
      </div>

      {/* Templates Grid */}
      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <div key={i} className="h-72 bg-muted rounded-xl animate-pulse" />
          ))}
        </div>
      ) : filtered.length === 0 ? (
        <div className="text-center py-16">
          <p className="text-muted-foreground text-lg">Bu kategoride sablon bulunamadi.</p>
          <Button variant="outline" className="mt-4" onClick={() => { setCategory("all"); setSearch(""); }}>
            Filtreyi Temizle
          </Button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filtered.map((template, i) => (
            <motion.div
              key={template.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.03 }}
            >
              <Card className="template-card card-hover border-border/50 overflow-hidden">
                <div className="relative h-48 overflow-hidden">
                  <img
                    src={template.thumbnail}
                    alt={template.name}
                    className="w-full h-full object-cover"
                    loading="lazy"
                  />
                  <div className="template-overlay">
                    <Button
                      size="sm"
                      variant="secondary"
                      onClick={() => setPreviewTemplate(template)}
                      data-testid={`template-card-preview-${template.id}`}
                    >
                      <Eye size={14} className="mr-1" /> Onizle
                    </Button>
                    <Button
                      size="sm"
                      onClick={() => handleUseTemplate(template)}
                      disabled={creating}
                      data-testid={`template-card-use-${template.id}`}
                    >
                      <ArrowRight size={14} className="mr-1" /> Kullan
                    </Button>
                  </div>
                  <Badge className="absolute top-3 left-3 text-[10px] bg-background/80 backdrop-blur-sm">
                    {CATEGORIES.find((c) => c.value === template.category)?.label || template.category}
                  </Badge>
                </div>
                <CardContent className="p-4">
                  <h3 className="font-semibold text-sm mb-1">{template.name}</h3>
                  <p className="text-xs text-muted-foreground line-clamp-2">{template.description}</p>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>
      )}

      {/* Preview Dialog */}
      <Dialog open={!!previewTemplate} onOpenChange={() => setPreviewTemplate(null)}>
        <DialogContent className="max-w-5xl h-[85vh] flex flex-col p-0">
          <DialogHeader className="px-6 py-4 border-b border-border flex-shrink-0">
            <div className="flex items-center justify-between">
              <div>
                <DialogTitle className="text-lg">{previewTemplate?.name}</DialogTitle>
                <p className="text-xs text-muted-foreground mt-1">{previewTemplate?.description}</p>
              </div>
              <div className="flex items-center gap-2">
                <Button
                  onClick={() => previewTemplate && handleUseTemplate(previewTemplate)}
                  disabled={creating}
                  data-testid="template-preview-use-button"
                >
                  {creating ? "Olusturuluyor..." : "Bu Sablonu Kullan"}
                </Button>
              </div>
            </div>
          </DialogHeader>
          <div className="flex-1 overflow-hidden bg-muted">
            {previewTemplate && (
              <iframe
                srcDoc={generatePreviewHTML(previewTemplate.sections, previewTemplate.theme)}
                className="w-full h-full border-0"
                title="Template Preview"
                sandbox="allow-same-origin"
              />
            )}
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}
