import { useState, useEffect, useCallback, useRef } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import {
  ArrowLeft, Save, Download, Monitor, Tablet, Smartphone, Eye,
  EyeOff, ChevronUp, ChevronDown, GripVertical, Plus, Trash2, Check
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Separator } from "@/components/ui/separator";
import { getProject, updateProject, exportProject } from "@/lib/api";
import { generatePreviewHTML } from "@/lib/previewRenderer";

const SECTION_LABELS = {
  header: "Baslik",
  hero: "Hero Banner",
  about: "Hakkimizda",
  rooms: "Odalar",
  gallery: "Galeri",
  services: "Hizmetler",
  testimonials: "Yorumlar",
  contact: "Iletisim",
  banner: "CTA Banner",
  footer: "Alt Bilgi",
};

const FONT_OPTIONS = [
  "'Playfair Display', serif",
  "'Cormorant Garamond', serif",
  "'Libre Baskerville', serif",
  "'Merriweather', serif",
  "'Crimson Text', serif",
  "'Noto Serif', serif",
  "'Poppins', sans-serif",
  "'Inter', sans-serif",
  "'Montserrat', sans-serif",
  "'Lato', sans-serif",
  "'Open Sans', sans-serif",
  "'Raleway', sans-serif",
  "'Space Grotesk', sans-serif",
  "'DM Sans', sans-serif",
  "'Roboto', sans-serif",
  "'Josefin Sans', sans-serif",
  "'Comfortaa', sans-serif",
  "'Bebas Neue', sans-serif",
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
  const saveTimeout = useRef(null);

  useEffect(() => {
    getProject(projectId)
      .then((p) => {
        setProject(p);
        setPreviewHtml(generatePreviewHTML(p.sections, p.theme));
      })
      .catch((err) => {
        console.error(err);
        navigate("/projects");
      })
      .finally(() => setLoading(false));
  }, [projectId, navigate]);

  const updatePreview = useCallback((sections, theme) => {
    setPreviewHtml(generatePreviewHTML(sections, theme));
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
      updatePreview(updated.sections, updated.theme);
      autoSave(updated);
      return updated;
    });
  };

  const updateTheme = (key, value) => {
    setProject((prev) => {
      const updated = { ...prev, theme: { ...prev.theme, [key]: value } };
      updatePreview(updated.sections, updated.theme);
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
      updatePreview(updated.sections, updated.theme);
      autoSave(updated);
      return updated;
    });
  };

  const moveSection = (idx, dir) => {
    setProject((prev) => {
      const updated = { ...prev };
      const sections = [...prev.sections];
      const newIdx = idx + dir;
      if (newIdx < 0 || newIdx >= sections.length) return prev;
      [sections[idx], sections[newIdx]] = [sections[newIdx], sections[idx]];
      updated.sections = sections;
      updatePreview(updated.sections, updated.theme);
      autoSave(updated);
      return updated;
    });
  };

  const addBannerSection = () => {
    setProject((prev) => {
      const updated = { ...prev };
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
      // Insert before footer
      const footerIdx = updated.sections.findIndex((s) => s.type === "footer");
      if (footerIdx >= 0) {
        updated.sections = [...updated.sections.slice(0, footerIdx), newSection, ...updated.sections.slice(footerIdx)];
      } else {
        updated.sections = [...updated.sections, newSection];
      }
      updatePreview(updated.sections, updated.theme);
      autoSave(updated);
      setActiveSection(newSection.id);
      return updated;
    });
  };

  const removeSection = (sectionId) => {
    setProject((prev) => {
      const section = prev.sections.find((s) => s.id === sectionId);
      if (section?.type === "footer" || section?.type === "header") return prev;
      const updated = { ...prev };
      updated.sections = prev.sections.filter((s) => s.id !== sectionId);
      updatePreview(updated.sections, updated.theme);
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
      alert("Disa aktarma basarisiz oldu");
    }
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      await updateProject(projectId, {
        theme: project.theme,
        sections: project.sections,
        name: project.name,
      });
      setSaved(true);
      setTimeout(() => setSaved(false), 2000);
    } catch (err) {
      console.error(err);
    } finally {
      setSaving(false);
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

  const activeData = project.sections.find((s) => s.id === activeSection);

  return (
    <div className="h-screen flex flex-col bg-background">
      {/* Top Bar */}
      <div className="h-14 border-b border-border flex items-center px-4 gap-3 flex-shrink-0" style={{ height: "var(--editor-top)" }}>
        <Button variant="ghost" size="icon" onClick={() => navigate("/projects")} data-testid="editor-back-button">
          <ArrowLeft size={18} />
        </Button>
        <Separator orientation="vertical" className="h-6" />
        <Input
          value={project.name}
          onChange={(e) => setProject((p) => ({ ...p, name: e.target.value }))}
          onBlur={() => autoSave(project)}
          className="max-w-xs h-8 text-sm bg-transparent border-none focus-visible:ring-0 font-medium"
          data-testid="editor-project-name"
        />
        <div className="flex-1" />
        {/* Device toggles */}
        <div className="flex items-center gap-1 bg-muted rounded-lg p-0.5">
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
        <Button variant="outline" size="sm" onClick={handleSave} disabled={saving} data-testid="template-editor-save-button">
          <Save size={14} className="mr-1" /> {saving ? "Kaydediliyor..." : "Kaydet"}
        </Button>
        <Button size="sm" onClick={handleExport} data-testid="template-editor-export-zip-button">
          <Download size={14} className="mr-1" /> Disa Aktar
        </Button>
      </div>

      {/* Editor Body */}
      <div className="editor-layout">
        {/* Left Panel */}
        <div className="editor-left">
          <Tabs defaultValue="sections" className="h-full flex flex-col">
            <TabsList className="w-full rounded-none border-b border-border h-10 bg-transparent">
              <TabsTrigger value="sections" className="flex-1 text-xs" data-testid="editor-tab-sections">
                Bolumler
              </TabsTrigger>
              <TabsTrigger value="theme" className="flex-1 text-xs" data-testid="editor-tab-theme">
                Tema
              </TabsTrigger>
            </TabsList>

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
                        <div className="flex items-center gap-1">
                          <button
                            onClick={(e) => { e.stopPropagation(); moveSection(idx, -1); }}
                            className="p-1 hover:bg-muted rounded" title="Yukari"
                          >
                            <ChevronUp size={12} />
                          </button>
                          <button
                            onClick={(e) => { e.stopPropagation(); moveSection(idx, 1); }}
                            className="p-1 hover:bg-muted rounded" title="Asagi"
                          >
                            <ChevronDown size={12} />
                          </button>
                          <button
                            onClick={(e) => { e.stopPropagation(); toggleSectionVisibility(section.id); }}
                            className="p-1 hover:bg-muted rounded"
                            title={section.visible ? "Gizle" : "Goster"}
                          >
                            {section.visible !== false ? <Eye size={12} /> : <EyeOff size={12} />}
                          </button>
                          {section.type === "banner" && (
                            <button
                              onClick={(e) => { e.stopPropagation(); removeSection(section.id); }}
                              className="p-1 hover:bg-destructive/20 rounded text-destructive"
                              title="Sil"
                            >
                              <Trash2 size={12} />
                            </button>
                          )}
                        </div>
                      </div>

                      {/* Section Form */}
                      {activeSection === section.id && (
                        <motion.div
                          initial={{ height: 0, opacity: 0 }}
                          animate={{ height: "auto", opacity: 1 }}
                          className="px-3 py-4 space-y-3 bg-muted/20 rounded-lg mt-1 mb-2"
                        >
                          <SectionForm
                            section={section}
                            onUpdate={(prop, val) => updateSectionProp(section.id, prop, val)}
                          />
                        </motion.div>
                      )}
                    </div>
                  ))}
                </div>
              </ScrollArea>
            </TabsContent>

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
                      <input
                        type="color"
                        value={project.theme[key] || "#000000"}
                        onChange={(e) => updateTheme(key, e.target.value)}
                        data-testid={`editor-theme-${key}`}
                      />
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
                      <SelectTrigger className="h-9" data-testid="editor-theme-headerFont">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {FONT_OPTIONS.map((f) => (
                          <SelectItem key={f} value={f}>
                            <span style={{ fontFamily: f }}>{f.split("'")[1] || f.split(",")[0]}</span>
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <label className="text-xs text-muted-foreground mb-1 block">Govde Fontu</label>
                    <Select value={project.theme.bodyFont} onValueChange={(v) => updateTheme("bodyFont", v)}>
                      <SelectTrigger className="h-9" data-testid="editor-theme-bodyFont">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {FONT_OPTIONS.map((f) => (
                          <SelectItem key={f} value={f}>
                            <span style={{ fontFamily: f }}>{f.split("'")[1] || f.split(",")[0]}</span>
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              </ScrollArea>
            </TabsContent>
          </Tabs>
        </div>

        {/* Right Panel - Preview */}
        <div className="editor-right">
          <div className={`preview-frame ${deviceMode}`}>
            <iframe
              srcDoc={previewHtml}
              title="Preview"
              data-testid="editor-preview-iframe"
              sandbox="allow-same-origin"
            />
          </div>
        </div>
      </div>
    </div>
  );
}

// Section Form Component
function SectionForm({ section, onUpdate }) {
  const props = section.props || {};

  const Field = ({ label, prop, multiline, type = "text" }) => (
    <div>
      <label className="text-xs text-muted-foreground mb-1 block">{label}</label>
      {multiline ? (
        <Textarea
          value={props[prop] || ""}
          onChange={(e) => onUpdate(prop, e.target.value)}
          className="text-sm min-h-[80px]"
          data-testid={`editor-field-${section.type}-${prop}`}
        />
      ) : (
        <Input
          type={type}
          value={typeof props[prop] === "string" ? props[prop] : (props[prop] || "")}
          onChange={(e) => onUpdate(prop, e.target.value)}
          className="h-8 text-sm"
          data-testid={`editor-field-${section.type}-${prop}`}
        />
      )}
    </div>
  );

  const LayoutSelect = ({ prop, options }) => (
    <div>
      <label className="text-xs text-muted-foreground mb-1 block">Yerlesim</label>
      <Select value={props[prop] || options[0]?.value} onValueChange={(v) => onUpdate(prop, v)}>
        <SelectTrigger className="h-8" data-testid={`editor-field-${section.type}-${prop}`}>
          <SelectValue />
        </SelectTrigger>
        <SelectContent>
          {options.map((o) => (
            <SelectItem key={o.value} value={o.value}>{o.label}</SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  );

  switch (section.type) {
    case "header":
      return (
        <div className="space-y-3">
          <Field label="Otel Adi" prop="hotelName" />
          <Field label="Logo URL" prop="logo" />
          <LayoutSelect prop="style" options={[
            { value: "transparent", label: "Seffaf" },
            { value: "solid", label: "Dolu" },
          ]} />
        </div>
      );
    case "hero":
      return (
        <div className="space-y-3">
          <Field label="Baslik" prop="title" />
          <Field label="Alt Baslik" prop="subtitle" />
          <Field label="Arka Plan Gorseli (URL)" prop="backgroundImage" />
          <Field label="Buton Metni" prop="ctaText" />
          <Field label="Buton Linki" prop="ctaLink" />
          <Field label="Overlay Opakligi (0-1)" prop="overlayOpacity" />
          <LayoutSelect prop="layout" options={[
            { value: "fullscreen", label: "Tam Ekran" },
            { value: "centered", label: "Ortalanmis" },
            { value: "split", label: "Bolumlenmis" },
          ]} />
        </div>
      );
    case "about":
      return (
        <div className="space-y-3">
          <Field label="Baslik" prop="title" />
          <Field label="Aciklama" prop="description" multiline />
          <Field label="Gorsel URL" prop="image" />
          <LayoutSelect prop="layout" options={[
            { value: "left-image", label: "Sol Gorsel" },
            { value: "right-image", label: "Sag Gorsel" },
          ]} />
        </div>
      );
    case "rooms":
      return (
        <div className="space-y-3">
          <Field label="Baslik" prop="title" />
          <Field label="Alt Baslik" prop="subtitle" />
          {(props.rooms || []).map((room, i) => (
            <div key={i} className="p-3 bg-muted/30 rounded-lg space-y-2">
              <p className="text-xs font-medium text-muted-foreground">Oda {i + 1}</p>
              <Input
                value={room.name || ""}
                onChange={(e) => {
                  const rooms = [...(props.rooms || [])];
                  rooms[i] = { ...rooms[i], name: e.target.value };
                  onUpdate("rooms", rooms);
                }}
                placeholder="Oda Adi" className="h-8 text-sm"
                data-testid={`editor-room-${i}-name`}
              />
              <Textarea
                value={room.description || ""}
                onChange={(e) => {
                  const rooms = [...(props.rooms || [])];
                  rooms[i] = { ...rooms[i], description: e.target.value };
                  onUpdate("rooms", rooms);
                }}
                placeholder="Aciklama" className="text-sm min-h-[60px]"
              />
              <Input
                value={room.image || ""}
                onChange={(e) => {
                  const rooms = [...(props.rooms || [])];
                  rooms[i] = { ...rooms[i], image: e.target.value };
                  onUpdate("rooms", rooms);
                }}
                placeholder="Gorsel URL" className="h-8 text-sm"
              />
              <Input
                value={room.price || ""}
                onChange={(e) => {
                  const rooms = [...(props.rooms || [])];
                  rooms[i] = { ...rooms[i], price: e.target.value };
                  onUpdate("rooms", rooms);
                }}
                placeholder="Fiyat" className="h-8 text-sm"
              />
            </div>
          ))}
        </div>
      );
    case "gallery":
      return (
        <div className="space-y-3">
          <Field label="Baslik" prop="title" />
          <LayoutSelect prop="layout" options={[
            { value: "grid", label: "Grid" },
            { value: "masonry", label: "Masonry" },
          ]} />
          {(props.images || []).map((img, i) => (
            <div key={i} className="flex gap-2">
              <Input
                value={img.url || ""}
                onChange={(e) => {
                  const images = [...(props.images || [])];
                  images[i] = { ...images[i], url: e.target.value };
                  onUpdate("images", images);
                }}
                placeholder={`Gorsel ${i + 1} URL`} className="h-8 text-sm flex-1"
                data-testid={`editor-gallery-${i}-url`}
              />
            </div>
          ))}
        </div>
      );
    case "services":
      return (
        <div className="space-y-3">
          <Field label="Baslik" prop="title" />
          {(props.services || []).map((svc, i) => (
            <div key={i} className="p-3 bg-muted/30 rounded-lg space-y-2">
              <Input
                value={svc.name || ""}
                onChange={(e) => {
                  const services = [...(props.services || [])];
                  services[i] = { ...services[i], name: e.target.value };
                  onUpdate("services", services);
                }}
                placeholder="Hizmet Adi" className="h-8 text-sm"
                data-testid={`editor-service-${i}-name`}
              />
              <Textarea
                value={svc.description || ""}
                onChange={(e) => {
                  const services = [...(props.services || [])];
                  services[i] = { ...services[i], description: e.target.value };
                  onUpdate("services", services);
                }}
                placeholder="Aciklama" className="text-sm min-h-[50px]"
              />
            </div>
          ))}
        </div>
      );
    case "testimonials":
      return (
        <div className="space-y-3">
          <Field label="Baslik" prop="title" />
          {(props.testimonials || []).map((t, i) => (
            <div key={i} className="p-3 bg-muted/30 rounded-lg space-y-2">
              <Input
                value={t.name || ""}
                onChange={(e) => {
                  const testimonials = [...(props.testimonials || [])];
                  testimonials[i] = { ...testimonials[i], name: e.target.value };
                  onUpdate("testimonials", testimonials);
                }}
                placeholder="Isim" className="h-8 text-sm"
                data-testid={`editor-testimonial-${i}-name`}
              />
              <Textarea
                value={t.text || ""}
                onChange={(e) => {
                  const testimonials = [...(props.testimonials || [])];
                  testimonials[i] = { ...testimonials[i], text: e.target.value };
                  onUpdate("testimonials", testimonials);
                }}
                placeholder="Yorum" className="text-sm min-h-[60px]"
              />
            </div>
          ))}
        </div>
      );
    case "contact":
      return (
        <div className="space-y-3">
          <Field label="Baslik" prop="title" />
          <Field label="Adres" prop="address" />
          <Field label="Telefon" prop="phone" />
          <Field label="E-posta" prop="email" />
          <LayoutSelect prop="layout" options={[
            { value: "split", label: "Ikiye Bolunmus" },
            { value: "centered", label: "Ortalanmis" },
          ]} />
        </div>
      );
    case "banner":
      return (
        <div className="space-y-3">
          <Field label="Baslik" prop="title" />
          <Field label="Alt Baslik" prop="subtitle" />
          <Field label="Arka Plan Gorseli (URL)" prop="backgroundImage" />
          <Field label="Buton Metni" prop="ctaText" />
          <Field label="Buton Linki" prop="ctaLink" />
        </div>
      );
    case "footer":
      return (
        <div className="space-y-3">
          <Field label="Otel Adi" prop="hotelName" />
          <Field label="Adres" prop="address" />
          <Field label="Telefon" prop="phone" />
          <Field label="E-posta" prop="email" />
          <p className="text-[10px] text-muted-foreground italic">* "Powered by Syroce" ibaresi her zaman gorunur.</p>
        </div>
      );
    default:
      return <p className="text-xs text-muted-foreground">Bu bolum icin duzenleme secenegi yok.</p>;
  }
}
