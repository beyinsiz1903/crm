import { useState, useEffect, useCallback, useRef } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import {
  ArrowLeft, Save, Download, Monitor, Tablet, Smartphone, Eye,
  EyeOff, ChevronUp, ChevronDown, GripVertical, Plus, Trash2, Check,
  Globe, History, Copy, Search as SearchIcon, FileText, Settings2
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Separator } from "@/components/ui/separator";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import ImageUpload from "@/components/ImageUpload";
import {
  getProject, updateProject, exportProject,
  cloneTemplateFromProject, getVersions, createVersion, restoreVersion
} from "@/lib/api";
import { generatePreviewHTML } from "@/lib/previewRenderer";

const SECTION_LABELS = {
  header: "Baslik", hero: "Hero Banner", about: "Hakkimizda", rooms: "Odalar",
  gallery: "Galeri", services: "Hizmetler", testimonials: "Yorumlar",
  contact: "Iletisim", banner: "CTA Banner", footer: "Alt Bilgi",
};

const FONT_OPTIONS = [
  "'Playfair Display', serif", "'Cormorant Garamond', serif", "'Libre Baskerville', serif",
  "'Merriweather', serif", "'Crimson Text', serif", "'Noto Serif', serif",
  "'Poppins', sans-serif", "'Inter', sans-serif", "'Montserrat', sans-serif",
  "'Lato', sans-serif", "'Open Sans', sans-serif", "'Raleway', sans-serif",
  "'Space Grotesk', sans-serif", "'DM Sans', sans-serif", "'Roboto', sans-serif",
  "'Josefin Sans', sans-serif", "'Comfortaa', sans-serif", "'Bebas Neue', sans-serif",
];

export default function TemplateEditor() {
  const { projectId } = useParams();
  const navigate = useNavigate();
  const [project, setProject] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [activeSection, setActiveSection] = useState(null);
  const [deviceMode, setDeviceMode] = useState("desktop");
  const [previewHtml, setPreviewHtml] = useState("");
  const [versions, setVersions] = useState([]);
  const [showVersions, setShowVersions] = useState(false);
  const [showSaveAsTemplate, setShowSaveAsTemplate] = useState(false);
  const [templateName, setTemplateName] = useState("");
  const [templateCategory, setTemplateCategory] = useState("custom");
  const saveTimeout = useRef(null);

  useEffect(() => {
    getProject(projectId)
      .then((p) => {
        // Ensure seo and new fields exist
        if (!p.seo) p.seo = { title: "", description: "", keywords: "", og_image: "" };
        if (!p.language) p.language = "tr";
        if (!p.export_mode) p.export_mode = "single";
        setProject(p);
        setPreviewHtml(generatePreviewHTML(p.sections, p.theme, p.language));
      })
      .catch(() => navigate("/projects"))
      .finally(() => setLoading(false));
  }, [projectId, navigate]);

  const updatePreview = useCallback((sections, theme, lang) => {
    setPreviewHtml(generatePreviewHTML(sections, theme, lang || "tr"));
  }, []);

  const autoSave = useCallback((updatedProject) => {
    if (saveTimeout.current) clearTimeout(saveTimeout.current);
    saveTimeout.current = setTimeout(async () => {
      setSaving(true);
      try {
        await updateProject(updatedProject.id, {
          theme: updatedProject.theme,
          sections: updatedProject.sections,
          name: updatedProject.name,
          seo: updatedProject.seo,
          language: updatedProject.language,
          export_mode: updatedProject.export_mode,
        });
        setSaved(true);
        setTimeout(() => setSaved(false), 2000);
      } catch (err) {
        console.error("Auto-save failed:", err);
      } finally {
        setSaving(false);
      }
    }, 800);
  }, []);

  const updateSectionProp = (sectionId, propPath, value) => {
    setProject((prev) => {
      const updated = { ...prev };
      updated.sections = prev.sections.map((s) => {
        if (s.id !== sectionId) return s;
        const newSection = { ...s, props: { ...s.props } };
        const parts = propPath.split(".");
        if (parts.length === 1) {
          newSection.props[parts[0]] = value;
        } else {
          let obj = newSection.props;
          for (let i = 0; i < parts.length - 1; i++) {
            if (typeof obj[parts[i]] === "object" && obj[parts[i]] !== null) {
              obj[parts[i]] = Array.isArray(obj[parts[i]]) ? [...obj[parts[i]]] : { ...obj[parts[i]] };
            } else {
              obj[parts[i]] = {};
            }
            obj = obj[parts[i]];
          }
          obj[parts[parts.length - 1]] = value;
        }
        return newSection;
      });
      updatePreview(updated.sections, updated.theme, updated.language);
      autoSave(updated);
      return updated;
    });
  };

  const updateTheme = (key, value) => {
    setProject((prev) => {
      const updated = { ...prev, theme: { ...prev.theme, [key]: value } };
      updatePreview(updated.sections, updated.theme, updated.language);
      autoSave(updated);
      return updated;
    });
  };

  const updateSeo = (key, value) => {
    setProject((prev) => {
      const updated = { ...prev, seo: { ...prev.seo, [key]: value } };
      autoSave(updated);
      return updated;
    });
  };

  const updateLanguage = (lang) => {
    setProject((prev) => {
      const updated = { ...prev, language: lang };
      updatePreview(updated.sections, updated.theme, lang);
      autoSave(updated);
      return updated;
    });
  };

  const updateExportMode = (mode) => {
    setProject((prev) => {
      const updated = { ...prev, export_mode: mode };
      autoSave(updated);
      return updated;
    });
  };

  const toggleSectionVisibility = (sectionId) => {
    setProject((prev) => {
      const updated = { ...prev };
      updated.sections = prev.sections.map((s) =>
        s.id === sectionId ? { ...s, visible: !s.visible } : s
      );
      updatePreview(updated.sections, updated.theme, updated.language);
      autoSave(updated);
      return updated;
    });
  };

  const moveSection = (idx, dir) => {
    setProject((prev) => {
      const sections = [...prev.sections];
      const newIdx = idx + dir;
      if (newIdx < 0 || newIdx >= sections.length) return prev;
      [sections[idx], sections[newIdx]] = [sections[newIdx], sections[idx]];
      const updated = { ...prev, sections };
      updatePreview(updated.sections, updated.theme, updated.language);
      autoSave(updated);
      return updated;
    });
  };

  const addBannerSection = () => {
    setProject((prev) => {
      const newSection = {
        id: crypto.randomUUID(),
        type: "banner",
        title: "Yeni Banner",
        visible: true,
        props: {
          title: "Ozel Teklif",
          subtitle: "Bu firsati kacirmayin!",
          backgroundImage: "",
          ctaText: "Simdi Rezervasyon Yapin",
          ctaLink: "#iletisim",
        },
      };
      const footerIdx = prev.sections.findIndex((s) => s.type === "footer");
      const sections = footerIdx >= 0
        ? [...prev.sections.slice(0, footerIdx), newSection, ...prev.sections.slice(footerIdx)]
        : [...prev.sections, newSection];
      const updated = { ...prev, sections };
      updatePreview(updated.sections, updated.theme, updated.language);
      autoSave(updated);
      setActiveSection(newSection.id);
      return updated;
    });
  };

  const removeSection = (sectionId) => {
    setProject((prev) => {
      const section = prev.sections.find((s) => s.id === sectionId);
      if (section?.type === "footer" || section?.type === "header") return prev;
      const updated = { ...prev, sections: prev.sections.filter((s) => s.id !== sectionId) };
      updatePreview(updated.sections, updated.theme, updated.language);
      autoSave(updated);
      if (activeSection === sectionId) setActiveSection(null);
      return updated;
    });
  };

  const handleExport = async () => {
    try {
      const blob = await exportProject(projectId);
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${project?.name || "website"}.zip`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      console.error("Export failed:", err);
    }
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      await updateProject(projectId, {
        theme: project.theme,
        sections: project.sections,
        name: project.name,
        seo: project.seo,
        language: project.language,
        export_mode: project.export_mode,
      });
      setSaved(true);
      setTimeout(() => setSaved(false), 2000);
    } catch (err) {
      console.error(err);
    } finally {
      setSaving(false);
    }
  };

  const handleCreateVersion = async () => {
    try {
      await handleSave();
      await createVersion(projectId);
      const v = await getVersions(projectId);
      setVersions(v);
    } catch (err) {
      console.error(err);
    }
  };

  const handleRestoreVersion = async (versionId) => {
    if (!window.confirm("Bu versiyona geri donmek istediginize emin misiniz?")) return;
    try {
      const restored = await restoreVersion(projectId, versionId);
      if (!restored.seo) restored.seo = { title: "", description: "", keywords: "", og_image: "" };
      if (!restored.language) restored.language = "tr";
      if (!restored.export_mode) restored.export_mode = "single";
      setProject(restored);
      updatePreview(restored.sections, restored.theme, restored.language);
    } catch (err) {
      console.error(err);
    }
  };

  const handleOpenVersions = async () => {
    try {
      const v = await getVersions(projectId);
      setVersions(v);
      setShowVersions(true);
    } catch (err) {
      console.error(err);
    }
  };

  const handleSaveAsTemplate = async () => {
    if (!templateName.trim()) return;
    try {
      await cloneTemplateFromProject(projectId, templateName, templateCategory);
      setShowSaveAsTemplate(false);
      setTemplateName("");
      alert("Sablon olarak kaydedildi!");
    } catch (err) {
      console.error(err);
      alert("Sablon olusturulamadi");
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen bg-background">
        <div className="animate-pulse text-muted-foreground">Yukleniyor...</div>
      </div>
    );
  }
  if (!project) return null;

  return (
    <div className="h-screen flex flex-col bg-background">
      {/* Top Bar */}
      <div className="h-14 border-b border-border flex items-center px-4 gap-2 flex-shrink-0" style={{ height: "var(--editor-top)" }}>
        <Button variant="ghost" size="icon" onClick={() => navigate("/projects")} data-testid="editor-back-button">
          <ArrowLeft size={18} />
        </Button>
        <Separator orientation="vertical" className="h-6" />
        <Input
          value={project.name}
          onChange={(e) => setProject((p) => ({ ...p, name: e.target.value }))}
          onBlur={() => autoSave(project)}
          className="max-w-[200px] h-8 text-sm bg-transparent border-none focus-visible:ring-0 font-medium"
          data-testid="editor-project-name"
        />
        <div className="flex-1" />
        {/* Language toggle */}
        <Button
          variant={project.language === "en" ? "default" : "outline"}
          size="sm"
          className="h-7 text-xs gap-1"
          onClick={() => updateLanguage(project.language === "en" ? "tr" : "en")}
          data-testid="editor-language-toggle"
        >
          <Globe size={12} /> {project.language === "en" ? "EN" : "TR"}
        </Button>
        {/* Device toggles */}
        <div className="flex items-center gap-0.5 bg-muted rounded-lg p-0.5">
          {[
            { mode: "desktop", icon: Monitor },
            { mode: "tablet", icon: Tablet },
            { mode: "mobile", icon: Smartphone },
          ].map(({ mode, icon: Icon }) => (
            <Button
              key={mode}
              variant={deviceMode === mode ? "secondary" : "ghost"}
              size="icon"
              className="h-7 w-7"
              onClick={() => setDeviceMode(mode)}
              data-testid={`editor-device-${mode}`}
            >
              <Icon size={14} />
            </Button>
          ))}
        </div>
        <Separator orientation="vertical" className="h-6" />
        {saved && (
          <Badge variant="outline" className="text-xs text-primary border-primary/30">
            <Check size={12} className="mr-1" /> Kaydedildi
          </Badge>
        )}
        <Button variant="outline" size="sm" className="h-7 text-xs" onClick={handleOpenVersions} data-testid="editor-versions-button">
          <History size={12} className="mr-1" /> Versiyon
        </Button>
        <Button variant="outline" size="sm" className="h-7 text-xs" onClick={() => { setTemplateName(project.name); setShowSaveAsTemplate(true); }} data-testid="editor-save-as-template">
          <Copy size={12} className="mr-1" /> Sablon Kaydet
        </Button>
        <Button variant="outline" size="sm" className="h-7 text-xs" onClick={handleSave} disabled={saving} data-testid="template-editor-save-button">
          <Save size={12} className="mr-1" /> {saving ? "..." : "Kaydet"}
        </Button>
        <Button size="sm" className="h-7 text-xs" onClick={handleExport} data-testid="template-editor-export-zip-button">
          <Download size={12} className="mr-1" /> Disa Aktar
        </Button>
      </div>

      {/* Editor Body */}
      <div className="editor-layout">
        {/* Left Panel */}
        <div className="editor-left">
          <Tabs defaultValue="sections" className="h-full flex flex-col">
            <TabsList className="w-full rounded-none border-b border-border h-10 bg-transparent px-1">
              <TabsTrigger value="sections" className="flex-1 text-[11px]" data-testid="editor-tab-sections">Bolumler</TabsTrigger>
              <TabsTrigger value="theme" className="flex-1 text-[11px]" data-testid="editor-tab-theme">Tema</TabsTrigger>
              <TabsTrigger value="seo" className="flex-1 text-[11px]" data-testid="editor-tab-seo">SEO</TabsTrigger>
              <TabsTrigger value="settings" className="flex-1 text-[11px]" data-testid="editor-tab-settings">Ayarlar</TabsTrigger>
            </TabsList>

            {/* ===== SECTIONS TAB ===== */}
            <TabsContent value="sections" className="flex-1 overflow-hidden mt-0">
              <ScrollArea className="h-full">
                <div className="p-3 space-y-1">
                  <Button variant="outline" size="sm" className="w-full mb-3" onClick={addBannerSection} data-testid="editor-add-banner">
                    <Plus size={14} className="mr-1" /> Banner Ekle
                  </Button>
                  {project.sections.map((section, idx) => (
                    <div key={section.id}>
                      <div
                        className={`section-item ${activeSection === section.id ? "active" : ""}`}
                        onClick={() => setActiveSection(activeSection === section.id ? null : section.id)}
                        data-testid={`editor-section-${section.type}-${idx}`}
                      >
                        <GripVertical size={14} className="text-muted-foreground flex-shrink-0" />
                        <span className={`text-sm flex-1 ${!section.visible ? "line-through opacity-50" : ""}`}>
                          {SECTION_LABELS[section.type] || section.title}
                        </span>
                        <div className="flex items-center gap-0.5">
                          <button onClick={(e) => { e.stopPropagation(); moveSection(idx, -1); }} className="p-1 hover:bg-muted rounded"><ChevronUp size={12} /></button>
                          <button onClick={(e) => { e.stopPropagation(); moveSection(idx, 1); }} className="p-1 hover:bg-muted rounded"><ChevronDown size={12} /></button>
                          <button onClick={(e) => { e.stopPropagation(); toggleSectionVisibility(section.id); }} className="p-1 hover:bg-muted rounded">
                            {section.visible !== false ? <Eye size={12} /> : <EyeOff size={12} />}
                          </button>
                          {section.type === "banner" && (
                            <button onClick={(e) => { e.stopPropagation(); removeSection(section.id); }} className="p-1 hover:bg-destructive/20 rounded text-destructive"><Trash2 size={12} /></button>
                          )}
                        </div>
                      </div>
                      {activeSection === section.id && (
                        <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: "auto", opacity: 1 }} className="px-3 py-4 space-y-3 bg-muted/20 rounded-lg mt-1 mb-2">
                          <SectionForm section={section} onUpdate={(prop, val) => updateSectionProp(section.id, prop, val)} />
                        </motion.div>
                      )}
                    </div>
                  ))}
                </div>
              </ScrollArea>
            </TabsContent>

            {/* ===== THEME TAB ===== */}
            <TabsContent value="theme" className="flex-1 overflow-hidden mt-0">
              <ScrollArea className="h-full">
                <div className="p-4 space-y-5">
                  <h3 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Renkler</h3>
                  {[
                    { key: "primaryColor", label: "Ana Renk" },
                    { key: "secondaryColor", label: "Ikincil Renk" },
                    { key: "backgroundColor", label: "Arka Plan" },
                    { key: "textColor", label: "Metin Rengi" },
                    { key: "accentColor", label: "Vurgu Rengi" },
                  ].map(({ key, label }) => (
                    <div key={key} className="color-input-wrapper">
                      <input type="color" value={project.theme[key] || "#000000"} onChange={(e) => updateTheme(key, e.target.value)} data-testid={`editor-theme-${key}`} />
                      <div>
                        <p className="text-xs text-muted-foreground">{label}</p>
                        <p className="text-xs font-mono">{project.theme[key]}</p>
                      </div>
                    </div>
                  ))}
                  <Separator />
                  <h3 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Yazitipi</h3>
                  <div>
                    <label className="text-xs text-muted-foreground mb-1 block">Baslik Fontu</label>
                    <Select value={project.theme.headerFont} onValueChange={(v) => updateTheme("headerFont", v)}>
                      <SelectTrigger className="h-9" data-testid="editor-theme-headerFont"><SelectValue /></SelectTrigger>
                      <SelectContent>{FONT_OPTIONS.map((f) => (<SelectItem key={f} value={f}><span style={{ fontFamily: f }}>{f.split("'")[1] || f.split(",")[0]}</span></SelectItem>))}</SelectContent>
                    </Select>
                  </div>
                  <div>
                    <label className="text-xs text-muted-foreground mb-1 block">Govde Fontu</label>
                    <Select value={project.theme.bodyFont} onValueChange={(v) => updateTheme("bodyFont", v)}>
                      <SelectTrigger className="h-9" data-testid="editor-theme-bodyFont"><SelectValue /></SelectTrigger>
                      <SelectContent>{FONT_OPTIONS.map((f) => (<SelectItem key={f} value={f}><span style={{ fontFamily: f }}>{f.split("'")[1] || f.split(",")[0]}</span></SelectItem>))}</SelectContent>
                    </Select>
                  </div>
                </div>
              </ScrollArea>
            </TabsContent>

            {/* ===== SEO TAB ===== */}
            <TabsContent value="seo" className="flex-1 overflow-hidden mt-0">
              <ScrollArea className="h-full">
                <div className="p-4 space-y-4">
                  <h3 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider flex items-center gap-2">
                    <SearchIcon size={12} /> SEO Ayarlari
                  </h3>
                  <div>
                    <label className="text-xs text-muted-foreground mb-1 block">Sayfa Basligi (Title)</label>
                    <Input value={project.seo?.title || ""} onChange={(e) => updateSeo("title", e.target.value)} className="h-8 text-sm" data-testid="editor-seo-title" placeholder="Otel Adi - Luks Konaklama" />
                  </div>
                  <div>
                    <label className="text-xs text-muted-foreground mb-1 block">Aciklama (Meta Description)</label>
                    <Textarea value={project.seo?.description || ""} onChange={(e) => updateSeo("description", e.target.value)} className="text-sm min-h-[80px]" data-testid="editor-seo-description" placeholder="Otelimiz hakkinda kisa aciklama..." />
                    <p className="text-[10px] text-muted-foreground mt-1">{(project.seo?.description || "").length}/160 karakter</p>
                  </div>
                  <div>
                    <label className="text-xs text-muted-foreground mb-1 block">Anahtar Kelimeler</label>
                    <Input value={project.seo?.keywords || ""} onChange={(e) => updateSeo("keywords", e.target.value)} className="h-8 text-sm" data-testid="editor-seo-keywords" placeholder="otel, konaklama, tatil" />
                  </div>
                  <div>
                    <label className="text-xs text-muted-foreground mb-1 block">OG Image URL</label>
                    <ImageUpload value={project.seo?.og_image || ""} onChange={(v) => updateSeo("og_image", v)} testId="editor-seo-og-image" />
                  </div>
                  <div className="p-3 bg-muted/30 rounded-lg">
                    <p className="text-[10px] text-muted-foreground mb-2">Onizleme (Google Arama)</p>
                    <p className="text-sm text-blue-400 font-medium">{project.seo?.title || project.name || "Sayfa Basligi"}</p>
                    <p className="text-[11px] text-green-400 font-mono">www.otel.com</p>
                    <p className="text-xs text-muted-foreground mt-1 line-clamp-2">{project.seo?.description || "Sayfa aciklamasi burada gorunecek..."}</p>
                  </div>
                </div>
              </ScrollArea>
            </TabsContent>

            {/* ===== SETTINGS TAB ===== */}
            <TabsContent value="settings" className="flex-1 overflow-hidden mt-0">
              <ScrollArea className="h-full">
                <div className="p-4 space-y-5">
                  <h3 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider flex items-center gap-2">
                    <Settings2 size={12} /> Proje Ayarlari
                  </h3>
                  <div>
                    <label className="text-xs text-muted-foreground mb-1 block">Web Sitesi Dili</label>
                    <Select value={project.language || "tr"} onValueChange={updateLanguage}>
                      <SelectTrigger className="h-9" data-testid="editor-settings-language"><SelectValue /></SelectTrigger>
                      <SelectContent>
                        <SelectItem value="tr">Turkce (TR)</SelectItem>
                        <SelectItem value="en">English (EN)</SelectItem>
                      </SelectContent>
                    </Select>
                    <p className="text-[10px] text-muted-foreground mt-1">Iletisim formu, footer ve navigasyon metinleri bu dilde gorunur.</p>
                  </div>
                  <Separator />
                  <div>
                    <label className="text-xs text-muted-foreground mb-1 block">Export Modu</label>
                    <Select value={project.export_mode || "single"} onValueChange={updateExportMode}>
                      <SelectTrigger className="h-9" data-testid="editor-settings-export-mode"><SelectValue /></SelectTrigger>
                      <SelectContent>
                        <SelectItem value="single">Tek Sayfa (Single Page)</SelectItem>
                        <SelectItem value="multi">Coklu Sayfa (Multi Page)</SelectItem>
                      </SelectContent>
                    </Select>
                    <p className="text-[10px] text-muted-foreground mt-1">
                      {project.export_mode === "multi"
                        ? "Export: index.html, rooms.html, gallery.html, contact.html"
                        : "Export: tek index.html dosyasi"}
                    </p>
                  </div>
                  <Separator />
                  <div>
                    <h3 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-3">Islemler</h3>
                    <div className="space-y-2">
                      <Button variant="outline" size="sm" className="w-full justify-start" onClick={handleCreateVersion} data-testid="editor-create-version">
                        <History size={14} className="mr-2" /> Versiyon Olustur
                      </Button>
                      <Button variant="outline" size="sm" className="w-full justify-start" onClick={() => { setTemplateName(project.name); setShowSaveAsTemplate(true); }}>
                        <Copy size={14} className="mr-2" /> Sablon Olarak Kaydet
                      </Button>
                      <Button variant="outline" size="sm" className="w-full justify-start" onClick={handleOpenVersions}>
                        <FileText size={14} className="mr-2" /> Versiyon Gecmisi
                      </Button>
                    </div>
                  </div>
                </div>
              </ScrollArea>
            </TabsContent>
          </Tabs>
        </div>

        {/* Right Panel - Preview */}
        <div className="editor-right">
          <div className={`preview-frame ${deviceMode}`}>
            <iframe srcDoc={previewHtml} title="Preview" data-testid="editor-preview-iframe" sandbox="allow-same-origin" />
          </div>
        </div>
      </div>

      {/* Version History Dialog */}
      <Dialog open={showVersions} onOpenChange={setShowVersions}>
        <DialogContent className="max-w-md">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2"><History size={18} /> Versiyon Gecmisi</DialogTitle>
          </DialogHeader>
          <div className="space-y-2 max-h-96 overflow-auto">
            {versions.length === 0 ? (
              <div className="text-center py-8">
                <p className="text-sm text-muted-foreground">Henuz versiyon yok.</p>
                <Button variant="outline" size="sm" className="mt-3" onClick={handleCreateVersion}>Ilk Versiyonu Olustur</Button>
              </div>
            ) : (
              versions.map((v) => (
                <div key={v.id} className="flex items-center justify-between p-3 rounded-lg bg-muted/30 hover:bg-muted/50">
                  <div>
                    <p className="text-sm font-medium">{v.label}</p>
                    <p className="text-xs text-muted-foreground font-mono">{new Date(v.created_at).toLocaleString("tr-TR")}</p>
                  </div>
                  <Button variant="outline" size="sm" onClick={() => handleRestoreVersion(v.id)} data-testid={`version-restore-${v.id}`}>Geri Yukle</Button>
                </div>
              ))
            )}
          </div>
        </DialogContent>
      </Dialog>

      {/* Save As Template Dialog */}
      <Dialog open={showSaveAsTemplate} onOpenChange={setShowSaveAsTemplate}>
        <DialogContent className="max-w-sm">
          <DialogHeader>
            <DialogTitle>Sablon Olarak Kaydet</DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <div>
              <label className="text-xs text-muted-foreground mb-1 block">Sablon Adi</label>
              <Input value={templateName} onChange={(e) => setTemplateName(e.target.value)} data-testid="save-template-name" />
            </div>
            <div>
              <label className="text-xs text-muted-foreground mb-1 block">Kategori</label>
              <Select value={templateCategory} onValueChange={setTemplateCategory}>
                <SelectTrigger data-testid="save-template-category"><SelectValue /></SelectTrigger>
                <SelectContent>
                  {["custom", "luxury", "boutique", "resort", "business", "beach", "mountain", "city"].map((c) => (
                    <SelectItem key={c} value={c}>{c.charAt(0).toUpperCase() + c.slice(1)}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="flex justify-end gap-2">
              <Button variant="outline" onClick={() => setShowSaveAsTemplate(false)}>Iptal</Button>
              <Button onClick={handleSaveAsTemplate} data-testid="save-template-confirm">Kaydet</Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}

// ============ Section Form Component ============
function SectionForm({ section, onUpdate }) {
  const props = section.props || {};

  const Field = ({ label, prop, multiline }) => (
    <div>
      <label className="text-xs text-muted-foreground mb-1 block">{label}</label>
      {multiline ? (
        <Textarea value={props[prop] || ""} onChange={(e) => onUpdate(prop, e.target.value)} className="text-sm min-h-[80px]" data-testid={`editor-field-${section.type}-${prop}`} />
      ) : (
        <Input value={typeof props[prop] === "string" ? props[prop] : (props[prop] || "")} onChange={(e) => onUpdate(prop, e.target.value)} className="h-8 text-sm" data-testid={`editor-field-${section.type}-${prop}`} />
      )}
    </div>
  );

  const LayoutSelect = ({ prop, options }) => (
    <div>
      <label className="text-xs text-muted-foreground mb-1 block">Yerlesim</label>
      <Select value={props[prop] || options[0]?.value} onValueChange={(v) => onUpdate(prop, v)}>
        <SelectTrigger className="h-8" data-testid={`editor-field-${section.type}-${prop}`}><SelectValue /></SelectTrigger>
        <SelectContent>{options.map((o) => (<SelectItem key={o.value} value={o.value}>{o.label}</SelectItem>))}</SelectContent>
      </Select>
    </div>
  );

  const ImageField = ({ label, prop }) => (
    <ImageUpload value={props[prop] || ""} onChange={(v) => onUpdate(prop, v)} label={label} testId={`editor-field-${section.type}-${prop}`} />
  );

  switch (section.type) {
    case "header":
      return (<div className="space-y-3"><Field label="Otel Adi" prop="hotelName" /><ImageField label="Logo URL" prop="logo" /><LayoutSelect prop="style" options={[{ value: "transparent", label: "Seffaf" }, { value: "solid", label: "Dolu" }]} /></div>);
    case "hero":
      return (<div className="space-y-3"><Field label="Baslik" prop="title" /><Field label="Alt Baslik" prop="subtitle" /><ImageField label="Arka Plan Gorseli" prop="backgroundImage" /><Field label="Buton Metni" prop="ctaText" /><Field label="Buton Linki" prop="ctaLink" /><Field label="Overlay Opakligi (0-1)" prop="overlayOpacity" /><LayoutSelect prop="layout" options={[{ value: "fullscreen", label: "Tam Ekran" }, { value: "centered", label: "Ortalanmis" }, { value: "split", label: "Bolumlenmis" }]} /></div>);
    case "about":
      return (<div className="space-y-3"><Field label="Baslik" prop="title" /><Field label="Aciklama" prop="description" multiline /><ImageField label="Gorsel" prop="image" /><LayoutSelect prop="layout" options={[{ value: "left-image", label: "Sol Gorsel" }, { value: "right-image", label: "Sag Gorsel" }]} /></div>);
    case "rooms":
      return (<div className="space-y-3"><Field label="Baslik" prop="title" /><Field label="Alt Baslik" prop="subtitle" />{(props.rooms || []).map((room, i) => (<div key={i} className="p-3 bg-muted/30 rounded-lg space-y-2"><p className="text-xs font-medium text-muted-foreground">Oda {i + 1}</p><Input value={room.name || ""} onChange={(e) => { const rooms = [...(props.rooms || [])]; rooms[i] = { ...rooms[i], name: e.target.value }; onUpdate("rooms", rooms); }} placeholder="Oda Adi" className="h-8 text-sm" /><Textarea value={room.description || ""} onChange={(e) => { const rooms = [...(props.rooms || [])]; rooms[i] = { ...rooms[i], description: e.target.value }; onUpdate("rooms", rooms); }} placeholder="Aciklama" className="text-sm min-h-[50px]" /><ImageUpload value={room.image || ""} onChange={(v) => { const rooms = [...(props.rooms || [])]; rooms[i] = { ...rooms[i], image: v }; onUpdate("rooms", rooms); }} label="Gorsel" /><Input value={room.price || ""} onChange={(e) => { const rooms = [...(props.rooms || [])]; rooms[i] = { ...rooms[i], price: e.target.value }; onUpdate("rooms", rooms); }} placeholder="Fiyat" className="h-8 text-sm" /></div>))}</div>);
    case "gallery":
      return (<div className="space-y-3"><Field label="Baslik" prop="title" /><LayoutSelect prop="layout" options={[{ value: "grid", label: "Grid" }, { value: "masonry", label: "Masonry" }]} />{(props.images || []).map((img, i) => (<ImageUpload key={i} value={img.url || ""} onChange={(v) => { const images = [...(props.images || [])]; images[i] = { ...images[i], url: v }; onUpdate("images", images); }} label={`Gorsel ${i + 1}`} testId={`editor-gallery-${i}-url`} />))}</div>);
    case "services":
      return (<div className="space-y-3"><Field label="Baslik" prop="title" />{(props.services || []).map((svc, i) => (<div key={i} className="p-3 bg-muted/30 rounded-lg space-y-2"><Input value={svc.name || ""} onChange={(e) => { const services = [...(props.services || [])]; services[i] = { ...services[i], name: e.target.value }; onUpdate("services", services); }} placeholder="Hizmet Adi" className="h-8 text-sm" /><Textarea value={svc.description || ""} onChange={(e) => { const services = [...(props.services || [])]; services[i] = { ...services[i], description: e.target.value }; onUpdate("services", services); }} placeholder="Aciklama" className="text-sm min-h-[50px]" /></div>))}</div>);
    case "testimonials":
      return (<div className="space-y-3"><Field label="Baslik" prop="title" />{(props.testimonials || []).map((t, i) => (<div key={i} className="p-3 bg-muted/30 rounded-lg space-y-2"><Input value={t.name || ""} onChange={(e) => { const testimonials = [...(props.testimonials || [])]; testimonials[i] = { ...testimonials[i], name: e.target.value }; onUpdate("testimonials", testimonials); }} placeholder="Isim" className="h-8 text-sm" /><Textarea value={t.text || ""} onChange={(e) => { const testimonials = [...(props.testimonials || [])]; testimonials[i] = { ...testimonials[i], text: e.target.value }; onUpdate("testimonials", testimonials); }} placeholder="Yorum" className="text-sm min-h-[60px]" /></div>))}</div>);
    case "contact":
      return (<div className="space-y-3"><Field label="Baslik" prop="title" /><Field label="Adres" prop="address" /><Field label="Telefon" prop="phone" /><Field label="E-posta" prop="email" /><LayoutSelect prop="layout" options={[{ value: "split", label: "Ikiye Bolunmus" }, { value: "centered", label: "Ortalanmis" }]} /></div>);
    case "banner":
      return (<div className="space-y-3"><Field label="Baslik" prop="title" /><Field label="Alt Baslik" prop="subtitle" /><ImageField label="Arka Plan Gorseli" prop="backgroundImage" /><Field label="Buton Metni" prop="ctaText" /><Field label="Buton Linki" prop="ctaLink" /></div>);
    case "footer":
      return (<div className="space-y-3"><Field label="Otel Adi" prop="hotelName" /><Field label="Adres" prop="address" /><Field label="Telefon" prop="phone" /><Field label="E-posta" prop="email" /><p className="text-[10px] text-muted-foreground italic">* "Powered by Syroce" ibaresi her zaman gorunur.</p></div>);
    default:
      return <p className="text-xs text-muted-foreground">Bu bolum icin duzenleme secenegi yok.</p>;
  }
}
