import { useState, useEffect, useCallback, useRef } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import {
  DndContext, closestCenter, KeyboardSensor, PointerSensor, useSensor, useSensors
} from "@dnd-kit/core";
import {
  arrayMove, SortableContext, sortableKeyboardCoordinates,
  useSortable, verticalListSortingStrategy
} from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";
import {
  ArrowLeft, Save, Download, Monitor, Tablet, Smartphone, Eye,
  EyeOff, Plus, Trash2, Check,
  Globe, History, Copy, Search as SearchIcon, Settings2, Send,
  CalendarDays, BarChart3, ExternalLink, Package, GripVertical,
  Undo2, Redo2, Library, Bookmark
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
  cloneTemplateFromProject, getVersions, createVersion, restoreVersion,
  publishProject, unpublishProject,
  getSectionPresets, createSectionPreset, deleteSectionPreset
} from "@/lib/api";
import { generatePreviewHTML } from "@/lib/previewRenderer";

const SECTION_LABELS = {
  header: "Baslik", hero: "Hero Banner", about: "Hakkimizda", rooms: "Odalar",
  gallery: "Galeri", services: "Hizmetler", testimonials: "Yorumlar",
  contact: "Iletisim", banner: "CTA Banner", footer: "Alt Bilgi",
  booking: "Rezervasyon",
};

const FONT_OPTIONS = [
  "'Playfair Display', serif", "'Cormorant Garamond', serif", "'Libre Baskerville', serif",
  "'Merriweather', serif", "'Crimson Text', serif", "'Noto Serif', serif",
  "'Poppins', sans-serif", "'Inter', sans-serif", "'Montserrat', sans-serif",
  "'Lato', sans-serif", "'Open Sans', sans-serif", "'Raleway', sans-serif",
  "'Space Grotesk', sans-serif", "'DM Sans', sans-serif", "'Roboto', sans-serif",
  "'Josefin Sans', sans-serif", "'Comfortaa', sans-serif", "'Bebas Neue', sans-serif",
];

const LANGUAGE_OPTIONS = [
  { value: "tr", label: "Turkce", flag: "TR" },
  { value: "en", label: "English", flag: "GB" },
  { value: "de", label: "Deutsch", flag: "DE" },
  { value: "fr", label: "Francais", flag: "FR" },
  { value: "es", label: "Espanol", flag: "ES" },
  { value: "it", label: "Italiano", flag: "IT" },
  { value: "ru", label: "Russkiy", flag: "RU" },
  { value: "ar", label: "العربية", flag: "SA" },
  { value: "ja", label: "日本語", flag: "JP" },
  { value: "zh", label: "中文", flag: "CN" },
];

// ============ Sortable Section Item ============
function SortableSectionItem({ section, idx, activeSection, setActiveSection, toggleSectionVisibility, removeSection, children }) {
  const { attributes, listeners, setNodeRef, transform, transition, isDragging } = useSortable({ id: section.id });
  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.5 : 1,
    zIndex: isDragging ? 100 : "auto",
  };

  return (
    <div ref={setNodeRef} style={style}>
      <div
        className={`section-item ${activeSection === section.id ? "active" : ""}`}
        onClick={() => setActiveSection(activeSection === section.id ? null : section.id)}
        data-testid={`editor-section-${section.type}-${idx}`}
      >
        <button {...attributes} {...listeners} className="p-1 hover:bg-muted rounded cursor-grab active:cursor-grabbing" onClick={(e) => e.stopPropagation()}>
          <GripVertical size={14} className="text-muted-foreground flex-shrink-0" />
        </button>
        <span className={`text-sm flex-1 ${!section.visible ? "line-through opacity-50" : ""}`}>
          {SECTION_LABELS[section.type] || section.title}
        </span>
        <div className="flex items-center gap-0.5">
          <button onClick={(e) => { e.stopPropagation(); toggleSectionVisibility(section.id); }} className="p-1 hover:bg-muted rounded">
            {section.visible !== false ? <Eye size={12} /> : <EyeOff size={12} />}
          </button>
          {(section.type === "banner" || section.type === "booking") && (
            <button onClick={(e) => { e.stopPropagation(); removeSection(section.id); }} className="p-1 hover:bg-destructive/20 rounded text-destructive"><Trash2 size={12} /></button>
          )}
        </div>
      </div>
      {activeSection === section.id && (
        <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: "auto", opacity: 1 }} className="px-3 py-4 space-y-3 bg-muted/20 rounded-lg mt-1 mb-2">
          {children}
          {section.type !== "header" && section.type !== "footer" && (
            <button
              onClick={() => {
                // Find the handleSaveAsPreset from parent - it's passed via children's context
                const event = new CustomEvent('saveAsPreset', { detail: { sectionId: section.id } });
                window.dispatchEvent(event);
              }}
              className="flex items-center gap-1 text-[10px] text-muted-foreground hover:text-primary transition-colors mt-2 pt-2 border-t border-border/50"
            >
              <Bookmark size={10} /> Blok olarak kaydet
            </button>
          )}
        </motion.div>
      )}
    </div>
  );
}

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
  const [publishing, setPublishing] = useState(false);
  const saveTimeout = useRef(null);
  // Undo/Redo state
  const [undoStack, setUndoStack] = useState([]);
  const [redoStack, setRedoStack] = useState([]);
  const isUndoRedo = useRef(false);
  // Block Library state
  const [showBlockLibrary, setShowBlockLibrary] = useState(false);
  const [presets, setPresets] = useState([]);
  const [showSavePreset, setShowSavePreset] = useState(false);
  const [presetSectionId, setPresetSectionId] = useState(null);
  const [presetName, setPresetName] = useState("");
  const [presetCategory, setPresetCategory] = useState("genel");

  // DnD sensors
  const sensors = useSensors(
    useSensor(PointerSensor, { activationConstraint: { distance: 5 } }),
    useSensor(KeyboardSensor, { coordinateGetter: sortableKeyboardCoordinates })
  );

  useEffect(() => {
    getProject(projectId)
      .then((p) => {
        if (!p.seo) p.seo = { title: "", description: "", keywords: "", og_image: "" };
        if (!p.language) p.language = "tr";
        if (!p.export_mode) p.export_mode = "single";
        if (!p.analytics) p.analytics = { ga_id: "", custom_head_code: "" };
        if (p.published === undefined) p.published = false;
        if (p.bundle_assets === undefined) p.bundle_assets = false;
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
          analytics: updatedProject.analytics,
          bundle_assets: updatedProject.bundle_assets,
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

  // ==================== UNDO/REDO ====================
  const pushUndoState = useCallback((proj) => {
    if (isUndoRedo.current) return;
    setUndoStack((prev) => {
      const snapshot = JSON.stringify({ sections: proj.sections, theme: proj.theme });
      const newStack = [...prev, snapshot];
      if (newStack.length > 30) newStack.shift();
      return newStack;
    });
    setRedoStack([]);
  }, []);

  const handleUndo = useCallback(() => {
    if (undoStack.length === 0 || !project) return;
    isUndoRedo.current = true;
    const currentSnapshot = JSON.stringify({ sections: project.sections, theme: project.theme });
    setRedoStack((prev) => [...prev, currentSnapshot]);
    const prevSnapshot = JSON.parse(undoStack[undoStack.length - 1]);
    setUndoStack((prev) => prev.slice(0, -1));
    setProject((p) => {
      const updated = { ...p, sections: prevSnapshot.sections, theme: prevSnapshot.theme };
      updatePreview(updated.sections, updated.theme, updated.language);
      autoSave(updated);
      return updated;
    });
    setTimeout(() => { isUndoRedo.current = false; }, 100);
  }, [undoStack, project, updatePreview, autoSave]);

  const handleRedo = useCallback(() => {
    if (redoStack.length === 0 || !project) return;
    isUndoRedo.current = true;
    const currentSnapshot = JSON.stringify({ sections: project.sections, theme: project.theme });
    setUndoStack((prev) => [...prev, currentSnapshot]);
    const nextSnapshot = JSON.parse(redoStack[redoStack.length - 1]);
    setRedoStack((prev) => prev.slice(0, -1));
    setProject((p) => {
      const updated = { ...p, sections: nextSnapshot.sections, theme: nextSnapshot.theme };
      updatePreview(updated.sections, updated.theme, updated.language);
      autoSave(updated);
      return updated;
    });
    setTimeout(() => { isUndoRedo.current = false; }, 100);
  }, [redoStack, project, updatePreview, autoSave]);

  // Keyboard shortcuts for undo/redo
  useEffect(() => {
    const handler = (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key === "z" && !e.shiftKey) {
        e.preventDefault();
        handleUndo();
      }
      if ((e.ctrlKey || e.metaKey) && (e.key === "y" || (e.key === "z" && e.shiftKey))) {
        e.preventDefault();
        handleRedo();
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [handleUndo, handleRedo]);

  // Listen for save-as-preset events from section items
  useEffect(() => {
    const handler = (e) => {
      if (e.detail && e.detail.sectionId) {
        handleSaveAsPreset(e.detail.sectionId);
      }
    };
    window.addEventListener("saveAsPreset", handler);
    return () => window.removeEventListener("saveAsPreset", handler);
  });

  const updateSectionProp = (sectionId, propPath, value) => {
    setProject((prev) => {
      pushUndoState(prev);
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
      pushUndoState(prev);
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

  const updateAnalytics = (key, value) => {
    setProject((prev) => {
      const updated = { ...prev, analytics: { ...prev.analytics, [key]: value } };
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

  const updateBundleAssets = (val) => {
    setProject((prev) => {
      const updated = { ...prev, bundle_assets: val };
      autoSave(updated);
      return updated;
    });
  };

  const toggleSectionVisibility = (sectionId) => {
    setProject((prev) => {
      pushUndoState(prev);
      const updated = { ...prev };
      updated.sections = prev.sections.map((s) =>
        s.id === sectionId ? { ...s, visible: !s.visible } : s
      );
      updatePreview(updated.sections, updated.theme, updated.language);
      autoSave(updated);
      return updated;
    });
  };

  // Drag-and-drop section reorder
  const handleDragEnd = (event) => {
    const { active, over } = event;
    if (!over || active.id === over.id) return;

    setProject((prev) => {
      pushUndoState(prev);
      const oldIndex = prev.sections.findIndex((s) => s.id === active.id);
      const newIndex = prev.sections.findIndex((s) => s.id === over.id);
      const newSections = arrayMove(prev.sections, oldIndex, newIndex);
      const updated = { ...prev, sections: newSections };
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

  const addBookingSection = () => {
    setProject((prev) => {
      const newSection = {
        id: crypto.randomUUID(),
        type: "booking",
        title: "Rezervasyon",
        visible: true,
        props: {
          title: "",
          subtitle: "",
          bookingUrl: "",
          phone: "",
          email: "",
          roomTypes: [],
          widgetCode: "",
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
        analytics: project.analytics,
        bundle_assets: project.bundle_assets,
      });
      setSaved(true);
      setTimeout(() => setSaved(false), 2000);
    } catch (err) {
      console.error(err);
    } finally {
      setSaving(false);
    }
  };

  const handlePublish = async () => {
    setPublishing(true);
    try {
      await handleSave();
      if (project.published) {
        await unpublishProject(projectId);
        setProject((p) => ({ ...p, published: false, status: "draft" }));
      } else {
        const result = await publishProject(projectId);
        setProject((p) => ({ ...p, published: true, status: "published" }));
        // Open hosted URL in new tab
        if (result.live_url) {
          const backendUrl = process.env.REACT_APP_BACKEND_URL;
          window.open(`${backendUrl}${result.live_url}`, "_blank");
        }
      }
    } catch (err) {
      console.error(err);
    } finally {
      setPublishing(false);
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
      if (!restored.analytics) restored.analytics = { ga_id: "", custom_head_code: "" };
      if (restored.published === undefined) restored.published = false;
      if (restored.bundle_assets === undefined) restored.bundle_assets = false;
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

  const openHostedUrl = () => {
    const backendUrl = process.env.REACT_APP_BACKEND_URL;
    window.open(`${backendUrl}/api/hosted/${projectId}`, "_blank");
  };

  // ==================== BLOCK LIBRARY ====================
  const loadPresets = async () => {
    try {
      const data = await getSectionPresets();
      setPresets(data);
    } catch (err) {
      console.error("Failed to load presets:", err);
    }
  };

  const handleOpenBlockLibrary = async () => {
    await loadPresets();
    setShowBlockLibrary(true);
  };

  const handleSaveAsPreset = (sectionId) => {
    const section = project.sections.find((s) => s.id === sectionId);
    if (!section) return;
    setPresetSectionId(sectionId);
    setPresetName(SECTION_LABELS[section.type] || section.title || "Blok");
    setPresetCategory("genel");
    setShowSavePreset(true);
  };

  const handleConfirmSavePreset = async () => {
    if (!presetName.trim() || !presetSectionId) return;
    const section = project.sections.find((s) => s.id === presetSectionId);
    if (!section) return;
    try {
      await createSectionPreset({
        name: presetName,
        category: presetCategory,
        section_type: section.type,
        props: section.props,
      });
      setShowSavePreset(false);
      setPresetSectionId(null);
      setPresetName("");
    } catch (err) {
      console.error("Failed to save preset:", err);
    }
  };

  const handleAddPresetToProject = (preset) => {
    setProject((prev) => {
      pushUndoState(prev);
      const newSection = {
        id: crypto.randomUUID(),
        type: preset.section_type,
        title: preset.name,
        visible: true,
        props: JSON.parse(JSON.stringify(preset.props)),
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
    setShowBlockLibrary(false);
  };

  const handleDeletePreset = async (presetId) => {
    try {
      await deleteSectionPreset(presetId);
      setPresets((prev) => prev.filter((p) => p.id !== presetId));
    } catch (err) {
      console.error("Failed to delete preset:", err);
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
        {/* Language select */}
        <Select value={project.language || "tr"} onValueChange={updateLanguage}>
          <SelectTrigger className="h-7 w-[90px] text-[11px]" data-testid="editor-language-toggle">
            <Globe size={12} className="mr-1" />
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            {LANGUAGE_OPTIONS.map((l) => (
              <SelectItem key={l.value} value={l.value}>{l.flag} {l.label}</SelectItem>
            ))}
          </SelectContent>
        </Select>
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
        {/* Undo/Redo */}
        <div className="flex items-center gap-0.5">
          <Button variant="ghost" size="icon" className="h-7 w-7 relative" onClick={handleUndo} disabled={undoStack.length === 0} title={`Geri Al (Ctrl+Z) — ${undoStack.length} adim`} data-testid="editor-undo">
            <Undo2 size={14} />
            {undoStack.length > 0 && (
              <span className="absolute -top-1 -right-1 min-w-[14px] h-[14px] rounded-full bg-primary text-[9px] text-primary-foreground flex items-center justify-center font-bold leading-none">{undoStack.length}</span>
            )}
          </Button>
          <Button variant="ghost" size="icon" className="h-7 w-7 relative" onClick={handleRedo} disabled={redoStack.length === 0} title={`Yinele (Ctrl+Y) — ${redoStack.length} adim`} data-testid="editor-redo">
            <Redo2 size={14} />
            {redoStack.length > 0 && (
              <span className="absolute -top-1 -right-1 min-w-[14px] h-[14px] rounded-full bg-accent text-[9px] text-accent-foreground flex items-center justify-center font-bold leading-none">{redoStack.length}</span>
            )}
          </Button>
        </div>
        {/* Publish button */}
        <Button
          variant={project.published ? "default" : "outline"}
          size="sm"
          className={`h-7 text-xs ${project.published ? "bg-green-600 hover:bg-green-700" : ""}`}
          onClick={handlePublish}
          disabled={publishing}
          data-testid="editor-publish-button"
        >
          <Send size={12} className="mr-1" /> {publishing ? "..." : project.published ? "Yayinda" : "Yayinla"}
        </Button>
        {project.published && (
          <Button variant="ghost" size="icon" className="h-7 w-7" onClick={openHostedUrl} title="Canli siteyi ac" data-testid="editor-open-hosted">
            <ExternalLink size={14} />
          </Button>
        )}
        <Button variant="outline" size="sm" className="h-7 text-xs" onClick={handleOpenVersions} data-testid="editor-versions-button">
          <History size={12} className="mr-1" /> Versiyon
        </Button>
        <Button variant="outline" size="sm" className="h-7 text-xs" onClick={() => { setTemplateName(project.name); setShowSaveAsTemplate(true); }} data-testid="editor-save-as-template">
          <Copy size={12} className="mr-1" /> Sablon
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
                  <div className="flex gap-2 mb-3">
                    <Button variant="outline" size="sm" className="flex-1" onClick={addBannerSection} data-testid="editor-add-banner">
                      <Plus size={14} className="mr-1" /> Banner
                    </Button>
                    <Button variant="outline" size="sm" className="flex-1" onClick={addBookingSection} data-testid="editor-add-booking">
                      <CalendarDays size={14} className="mr-1" /> Rezervasyon
                    </Button>
                  </div>
                  <Button variant="outline" size="sm" className="w-full mb-3" onClick={handleOpenBlockLibrary} data-testid="editor-block-library">
                    <Library size={14} className="mr-1" /> Blok Kutuphanesi
                  </Button>
                  <DndContext sensors={sensors} collisionDetection={closestCenter} onDragEnd={handleDragEnd}>
                    <SortableContext items={project.sections.map((s) => s.id)} strategy={verticalListSortingStrategy}>
                      {project.sections.map((section, idx) => (
                        <SortableSectionItem
                          key={section.id}
                          section={section}
                          idx={idx}
                          activeSection={activeSection}
                          setActiveSection={setActiveSection}
                          toggleSectionVisibility={toggleSectionVisibility}
                          removeSection={removeSection}
                        >
                          <SectionForm section={section} onUpdate={(prop, val) => updateSectionProp(section.id, prop, val)} deviceMode={deviceMode} />
                        </SortableSectionItem>
                      ))}
                    </SortableContext>
                  </DndContext>
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
                  {/* Responsive hint */}
                  {deviceMode !== "desktop" && (
                    <div className="p-3 bg-primary/10 rounded-lg border border-primary/20">
                      <p className="text-[11px] text-primary font-medium">
                        {deviceMode === "tablet" ? "Tablet" : "Mobil"} Modu Aktif
                      </p>
                      <p className="text-[10px] text-muted-foreground mt-1">
                        Tema degisiklikleri tum cihazlara uygulanir. Onizlemede {deviceMode === "tablet" ? "tablet" : "mobil"} gorunum aktif.
                      </p>
                    </div>
                  )}
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

                  <Separator />

                  {/* Analytics */}
                  <h3 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider flex items-center gap-2">
                    <BarChart3 size={12} /> Analytics & Izleme
                  </h3>
                  <div>
                    <label className="text-xs text-muted-foreground mb-1 block">Google Analytics ID</label>
                    <Input value={project.analytics?.ga_id || ""} onChange={(e) => updateAnalytics("ga_id", e.target.value)} className="h-8 text-sm font-mono" data-testid="editor-analytics-ga-id" placeholder="G-XXXXXXXXXX" />
                    <p className="text-[10px] text-muted-foreground mt-1">Google Analytics 4 olcum kimligini girin.</p>
                  </div>
                  <div>
                    <label className="text-xs text-muted-foreground mb-1 block">Ozel Izleme Kodu (Head)</label>
                    <Textarea value={project.analytics?.custom_head_code || ""} onChange={(e) => updateAnalytics("custom_head_code", e.target.value)} className="text-sm min-h-[80px] font-mono" data-testid="editor-analytics-custom-code" placeholder="<!-- Facebook Pixel, Hotjar, vb. -->" />
                    <p className="text-[10px] text-muted-foreground mt-1">Export ve canli sitede head bolumune eklenir.</p>
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
                        {LANGUAGE_OPTIONS.map((l) => (
                          <SelectItem key={l.value} value={l.value}>{l.flag} {l.label}</SelectItem>
                        ))}
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
                  {/* Asset Bundling */}
                  <div>
                    <label className="text-xs text-muted-foreground mb-1 block flex items-center gap-2">
                      <Package size={12} /> Asset Bundling
                    </label>
                    <div
                      className={`flex items-center gap-3 p-3 rounded-lg border cursor-pointer transition-colors ${project.bundle_assets ? "border-primary bg-primary/5" : "border-border bg-muted/20"}`}
                      onClick={() => updateBundleAssets(!project.bundle_assets)}
                      data-testid="editor-settings-bundle-assets"
                    >
                      <div className={`w-10 h-5 rounded-full transition-colors flex items-center px-0.5 ${project.bundle_assets ? "bg-primary" : "bg-muted"}`}>
                        <div className={`w-4 h-4 rounded-full bg-white shadow transition-transform ${project.bundle_assets ? "translate-x-5" : "translate-x-0"}`} />
                      </div>
                      <div>
                        <p className="text-xs font-medium">{project.bundle_assets ? "Aktif" : "Kapali"}</p>
                        <p className="text-[10px] text-muted-foreground">Harici gorseller ZIP icine dahil edilir (offline calisan paket).</p>
                      </div>
                    </div>
                  </div>
                  <Separator />
                  {/* Publish Status */}
                  <div>
                    <label className="text-xs text-muted-foreground mb-1 block flex items-center gap-2">
                      <Send size={12} /> Yayinlama Durumu
                    </label>
                    <div className={`p-3 rounded-lg border ${project.published ? "border-green-500/30 bg-green-500/5" : "border-border bg-muted/20"}`}>
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="text-xs font-medium">{project.published ? "Canli Yayinda" : "Yayinda Degil"}</p>
                          <p className="text-[10px] text-muted-foreground mt-0.5">
                            {project.published ? "Proje canli URL uzerinden erisime acik." : "Yayinlamak icin ustteki 'Yayinla' butonunu kullanin."}
                          </p>
                        </div>
                        {project.published && (
                          <Button variant="outline" size="sm" className="h-7 text-[10px]" onClick={openHostedUrl}>
                            <ExternalLink size={10} className="mr-1" /> Ac
                          </Button>
                        )}
                      </div>
                    </div>
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

      {/* Block Library Dialog */}
      <Dialog open={showBlockLibrary} onOpenChange={setShowBlockLibrary}>
        <DialogContent className="max-w-lg">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2"><Library size={18} /> Blok Kutuphanesi</DialogTitle>
          </DialogHeader>
          {presets.length > 0 && (
            <div className="flex flex-wrap gap-1 pb-2 border-b border-border">
              <Badge variant="outline" className="text-[10px] cursor-pointer hover:bg-primary/10" onClick={() => loadPresets()}>Tumu ({presets.length})</Badge>
              {[...new Set(presets.map(p => p.category))].map(cat => (
                <Badge key={cat} variant="outline" className="text-[10px] cursor-pointer hover:bg-primary/10" onClick={async () => { const data = await getSectionPresets(cat); setPresets(data); }}>{cat.charAt(0).toUpperCase() + cat.slice(1)}</Badge>
              ))}
            </div>
          )}
          <div className="space-y-2 max-h-[400px] overflow-auto">
            {presets.length === 0 ? (
              <div className="text-center py-8">
                <Library size={32} className="mx-auto mb-3 text-muted-foreground/40" />
                <p className="text-sm text-muted-foreground">Henuz kaydedilmis blok yok.</p>
                <p className="text-xs text-muted-foreground mt-1">Herhangi bir section'da "Blok olarak kaydet" secenegini kullanin.</p>
              </div>
            ) : (
              presets.map((preset) => (
                <div key={preset.id} className="flex items-center justify-between p-3 rounded-lg bg-muted/30 hover:bg-muted/50 transition-colors">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <Badge variant="outline" className="text-[10px]">{SECTION_LABELS[preset.section_type] || preset.section_type}</Badge>
                      <p className="text-sm font-medium truncate">{preset.name}</p>
                    </div>
                    <p className="text-xs text-muted-foreground mt-0.5">{preset.category} &middot; {new Date(preset.created_at).toLocaleDateString("tr-TR")}</p>
                  </div>
                  <div className="flex items-center gap-1 ml-3">
                    <Button variant="default" size="sm" className="h-7 text-xs" onClick={() => handleAddPresetToProject(preset)} data-testid={`preset-add-${preset.id}`}>
                      <Plus size={12} className="mr-1" /> Ekle
                    </Button>
                    <Button variant="ghost" size="icon" className="h-7 w-7 text-destructive" onClick={() => handleDeletePreset(preset.id)}>
                      <Trash2 size={12} />
                    </Button>
                  </div>
                </div>
              ))
            )}
          </div>
        </DialogContent>
      </Dialog>

      {/* Save Section as Preset Dialog */}
      <Dialog open={showSavePreset} onOpenChange={setShowSavePreset}>
        <DialogContent className="max-w-sm">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2"><Bookmark size={18} /> Blok Olarak Kaydet</DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <div>
              <label className="text-xs text-muted-foreground mb-1 block">Blok Adi</label>
              <Input value={presetName} onChange={(e) => setPresetName(e.target.value)} data-testid="save-preset-name" placeholder="Orn: Luks Hero Banner" />
            </div>
            <div>
              <label className="text-xs text-muted-foreground mb-1 block">Kategori</label>
              <Select value={presetCategory} onValueChange={setPresetCategory}>
                <SelectTrigger data-testid="save-preset-category"><SelectValue /></SelectTrigger>
                <SelectContent>
                  {["genel", "hero", "odalar", "galeri", "hizmetler", "iletisim", "banner", "rezervasyon", "luks", "modern", "klasik", "minimal", "butik", "sahil", "dag", "sehir", "spa", "restoran"].map((c) => (
                    <SelectItem key={c} value={c}>{c.charAt(0).toUpperCase() + c.slice(1)}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="flex justify-end gap-2">
              <Button variant="outline" onClick={() => setShowSavePreset(false)}>Iptal</Button>
              <Button onClick={handleConfirmSavePreset} data-testid="save-preset-confirm">Kaydet</Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}

// ============ Section Form Component ============
function SectionForm({ section, onUpdate, deviceMode }) {
  const props = section.props || {};

  const Field = ({ label, prop, multiline, placeholder }) => (
    <div>
      <label className="text-xs text-muted-foreground mb-1 block">{label}</label>
      {multiline ? (
        <Textarea value={props[prop] || ""} onChange={(e) => onUpdate(prop, e.target.value)} className="text-sm min-h-[80px]" data-testid={`editor-field-${section.type}-${prop}`} placeholder={placeholder} />
      ) : (
        <Input value={typeof props[prop] === "string" ? props[prop] : (props[prop] || "")} onChange={(e) => onUpdate(prop, e.target.value)} className="h-8 text-sm" data-testid={`editor-field-${section.type}-${prop}`} placeholder={placeholder} />
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

  // Responsive hint for certain sections
  const responsiveHint = deviceMode !== "desktop" ? (
    <div className="p-2 bg-primary/10 rounded text-[10px] text-primary">
      {deviceMode === "mobile" ? "Mobil goruntuleme: Bazi ogeler tek sutuna dusecek" : "Tablet goruntuleme: Grid 2 sutuna dusecek"}
    </div>
  ) : null;

  switch (section.type) {
    case "header":
      return (<div className="space-y-3"><Field label="Otel Adi" prop="hotelName" /><ImageField label="Logo URL" prop="logo" /><LayoutSelect prop="style" options={[{ value: "transparent", label: "Seffaf" }, { value: "solid", label: "Dolu" }]} /></div>);
    case "hero":
      return (<div className="space-y-3"><Field label="Baslik" prop="title" /><Field label="Alt Baslik" prop="subtitle" /><ImageField label="Arka Plan Gorseli" prop="backgroundImage" /><Field label="Buton Metni" prop="ctaText" /><Field label="Buton Linki" prop="ctaLink" /><Field label="Overlay Opakligi (0-1)" prop="overlayOpacity" /><LayoutSelect prop="layout" options={[{ value: "fullscreen", label: "Tam Ekran" }, { value: "centered", label: "Ortalanmis" }, { value: "split", label: "Bolumlenmis" }]} />{responsiveHint}</div>);
    case "about":
      return (<div className="space-y-3"><Field label="Baslik" prop="title" /><Field label="Aciklama" prop="description" multiline /><ImageField label="Gorsel" prop="image" /><LayoutSelect prop="layout" options={[{ value: "left-image", label: "Sol Gorsel" }, { value: "right-image", label: "Sag Gorsel" }]} />{responsiveHint}</div>);
    case "rooms":
      return (<div className="space-y-3"><Field label="Baslik" prop="title" /><Field label="Alt Baslik" prop="subtitle" />{(props.rooms || []).map((room, i) => (<div key={i} className="p-3 bg-muted/30 rounded-lg space-y-2"><p className="text-xs font-medium text-muted-foreground">Oda {i + 1}</p><Input value={room.name || ""} onChange={(e) => { const rooms = [...(props.rooms || [])]; rooms[i] = { ...rooms[i], name: e.target.value }; onUpdate("rooms", rooms); }} placeholder="Oda Adi" className="h-8 text-sm" /><Textarea value={room.description || ""} onChange={(e) => { const rooms = [...(props.rooms || [])]; rooms[i] = { ...rooms[i], description: e.target.value }; onUpdate("rooms", rooms); }} placeholder="Aciklama" className="text-sm min-h-[50px]" /><ImageUpload value={room.image || ""} onChange={(v) => { const rooms = [...(props.rooms || [])]; rooms[i] = { ...rooms[i], image: v }; onUpdate("rooms", rooms); }} label="Gorsel" /><Input value={room.price || ""} onChange={(e) => { const rooms = [...(props.rooms || [])]; rooms[i] = { ...rooms[i], price: e.target.value }; onUpdate("rooms", rooms); }} placeholder="Fiyat" className="h-8 text-sm" /></div>))}{responsiveHint}</div>);
    case "menu":
      return (<div className="space-y-3"><Field label="Baslik" prop="title" /><Field label="Alt Baslik" prop="subtitle" />{(props.items || []).map((item, i) => (<div key={i} className="p-3 bg-muted/30 rounded-lg space-y-2"><p className="text-xs font-medium text-muted-foreground">Menu {i + 1}</p><Input value={item.name || ""} onChange={(e) => { const items = [...(props.items || [])]; items[i] = { ...items[i], name: e.target.value }; onUpdate("items", items); }} placeholder="Yemek Adi" className="h-8 text-sm" /><Textarea value={item.description || ""} onChange={(e) => { const items = [...(props.items || [])]; items[i] = { ...items[i], description: e.target.value }; onUpdate("items", items); }} placeholder="Aciklama" className="text-sm min-h-[50px]" /><ImageUpload value={item.image || ""} onChange={(v) => { const items = [...(props.items || [])]; items[i] = { ...items[i], image: v }; onUpdate("items", items); }} label="Gorsel" /><Input value={item.price || ""} onChange={(e) => { const items = [...(props.items || [])]; items[i] = { ...items[i], price: e.target.value }; onUpdate("items", items); }} placeholder="Fiyat" className="h-8 text-sm" /></div>))}<Button variant="outline" size="sm" onClick={() => { const items = [...(props.items || []), { name: "", description: "", image: "", price: "" }]; onUpdate("items", items); }}><Plus className="w-3 h-3 mr-1" />Yeni Urun Ekle</Button>{responsiveHint}</div>);
    case "tours":
      return (<div className="space-y-3"><Field label="Baslik" prop="title" /><Field label="Alt Baslik" prop="subtitle" />{(props.tours || []).map((tour, i) => (<div key={i} className="p-3 bg-muted/30 rounded-lg space-y-2"><p className="text-xs font-medium text-muted-foreground">Tur {i + 1}</p><Input value={tour.name || ""} onChange={(e) => { const tours = [...(props.tours || [])]; tours[i] = { ...tours[i], name: e.target.value }; onUpdate("tours", tours); }} placeholder="Tur Adi" className="h-8 text-sm" /><Textarea value={tour.description || ""} onChange={(e) => { const tours = [...(props.tours || [])]; tours[i] = { ...tours[i], description: e.target.value }; onUpdate("tours", tours); }} placeholder="Aciklama" className="text-sm min-h-[50px]" /><ImageUpload value={tour.image || ""} onChange={(v) => { const tours = [...(props.tours || [])]; tours[i] = { ...tours[i], image: v }; onUpdate("tours", tours); }} label="Gorsel" /><div className="grid grid-cols-2 gap-2"><Input value={tour.price || ""} onChange={(e) => { const tours = [...(props.tours || [])]; tours[i] = { ...tours[i], price: e.target.value }; onUpdate("tours", tours); }} placeholder="Fiyat" className="h-8 text-sm" /><Input value={tour.duration || ""} onChange={(e) => { const tours = [...(props.tours || [])]; tours[i] = { ...tours[i], duration: e.target.value }; onUpdate("tours", tours); }} placeholder="Sure" className="h-8 text-sm" /></div></div>))}<Button variant="outline" size="sm" onClick={() => { const tours = [...(props.tours || []), { name: "", description: "", image: "", price: "", duration: "" }]; onUpdate("tours", tours); }}><Plus className="w-3 h-3 mr-1" />Yeni Tur Ekle</Button>{responsiveHint}</div>);
    case "gallery":
      return (<div className="space-y-3"><Field label="Baslik" prop="title" /><LayoutSelect prop="layout" options={[{ value: "grid", label: "Grid" }, { value: "masonry", label: "Masonry" }]} />{(props.images || []).map((img, i) => (<ImageUpload key={i} value={img.url || ""} onChange={(v) => { const images = [...(props.images || [])]; images[i] = { ...images[i], url: v }; onUpdate("images", images); }} label={`Gorsel ${i + 1}`} testId={`editor-gallery-${i}-url`} />))}{responsiveHint}</div>);
    case "services":
      return (<div className="space-y-3"><Field label="Baslik" prop="title" />{(props.services || []).map((svc, i) => (<div key={i} className="p-3 bg-muted/30 rounded-lg space-y-2"><Input value={svc.name || ""} onChange={(e) => { const services = [...(props.services || [])]; services[i] = { ...services[i], name: e.target.value }; onUpdate("services", services); }} placeholder="Hizmet Adi" className="h-8 text-sm" /><Textarea value={svc.description || ""} onChange={(e) => { const services = [...(props.services || [])]; services[i] = { ...services[i], description: e.target.value }; onUpdate("services", services); }} placeholder="Aciklama" className="text-sm min-h-[50px]" /></div>))}</div>);
    case "testimonials":
      return (<div className="space-y-3"><Field label="Baslik" prop="title" />{(props.testimonials || []).map((t, i) => (<div key={i} className="p-3 bg-muted/30 rounded-lg space-y-2"><Input value={t.name || ""} onChange={(e) => { const testimonials = [...(props.testimonials || [])]; testimonials[i] = { ...testimonials[i], name: e.target.value }; onUpdate("testimonials", testimonials); }} placeholder="Isim" className="h-8 text-sm" /><Textarea value={t.text || ""} onChange={(e) => { const testimonials = [...(props.testimonials || [])]; testimonials[i] = { ...testimonials[i], text: e.target.value }; onUpdate("testimonials", testimonials); }} placeholder="Yorum" className="text-sm min-h-[60px]" /></div>))}</div>);
    case "contact":
      return (<div className="space-y-3"><Field label="Baslik" prop="title" /><Field label="Adres" prop="address" /><Field label="Telefon" prop="phone" /><Field label="E-posta" prop="email" /><LayoutSelect prop="layout" options={[{ value: "split", label: "Ikiye Bolunmus" }, { value: "centered", label: "Ortalanmis" }]} />{responsiveHint}</div>);
    case "banner":
      return (<div className="space-y-3"><Field label="Baslik" prop="title" /><Field label="Alt Baslik" prop="subtitle" /><ImageField label="Arka Plan Gorseli" prop="backgroundImage" /><Field label="Buton Metni" prop="ctaText" /><Field label="Buton Linki" prop="ctaLink" /></div>);
    case "booking":
      return (
        <div className="space-y-3">
          <div className="p-2 bg-primary/10 rounded-lg">
            <p className="text-[10px] text-primary font-medium">Rezervasyon Widget</p>
            <p className="text-[10px] text-muted-foreground">Harici bir booking engine embed kodu veya yerlesik formu kullanabilirsiniz.</p>
          </div>
          <Field label="Baslik" prop="title" placeholder="Rezervasyon" />
          <Field label="Alt Baslik" prop="subtitle" placeholder="Tatilinizi simdi planlayin" />
          <Field label="Telefon" prop="phone" placeholder="+90 555 123 4567" />
          <Field label="E-posta" prop="email" placeholder="info@otel.com" />
          <Field label="Booking URL (Form action)" prop="bookingUrl" placeholder="https://booking.com/hotel/..." />
          <div>
            <label className="text-xs text-muted-foreground mb-1 block">Oda Tipleri (virgul ile ayirin)</label>
            <Input
              value={(props.roomTypes || []).join(", ")}
              onChange={(e) => onUpdate("roomTypes", e.target.value.split(",").map((s) => s.trim()).filter(Boolean))}
              className="h-8 text-sm"
              placeholder="Standart, Deluxe, Suite"
              data-testid="editor-field-booking-roomTypes"
            />
          </div>
          <div>
            <label className="text-xs text-muted-foreground mb-1 block">Harici Widget Kodu (Opsiyonel)</label>
            <Textarea
              value={props.widgetCode || ""}
              onChange={(e) => onUpdate("widgetCode", e.target.value)}
              className="text-sm min-h-[80px] font-mono"
              data-testid="editor-field-booking-widgetCode"
              placeholder="<script>...</script> veya <iframe>...</iframe>"
            />
            <p className="text-[10px] text-muted-foreground mt-1">Booking.com, HotelRunner vb. embed kodu yapistirin. Bos birakirsaniz yerlesik form kullanilir.</p>
          </div>
        </div>
      );
    case "footer":
      return (<div className="space-y-3"><Field label="Otel Adi" prop="hotelName" /><Field label="Adres" prop="address" /><Field label="Telefon" prop="phone" /><Field label="E-posta" prop="email" /><p className="text-[10px] text-muted-foreground italic">* "Powered by Syroce" ibaresi her zaman gorunur.</p></div>);
    default:
      return <p className="text-xs text-muted-foreground">Bu bolum icin duzenleme secenegi yok.</p>;
  }
}
