{
  "product": {
    "name": "Syroce",
    "type": "hotel website templates CRM / website builder",
    "primary_users": ["Ajans sahibi / tek kullanıcı"],
    "language": "tr-TR",
    "north_star_actions": [
      "Template seç → düzenle → canlı önizle → dışa aktar (HTML/CSS zip)",
      "Müşteri ekle → projeye bağla → yayın/durum takibi"
    ]
  },
  "brand_attributes": {
    "keywords": ["premium", "profesyonel", "hızlı", "kontrollü", "editör-odaklı"],
    "visual_personality": "Graphite dark-mode + ocean-teal accent; editorial typography for headings; soft-glow micro-interactions; grid-first layout (bento + split editor).",
    "anti_goals": [
      "Aşırı gradient kullanımı (özellikle koyu/satüre)",
      "Her şeyi ortalama/merkez hizalama",
      "Aşırı skeuomorphism / gereksiz parlaklık",
      "Yoğun gölge ve düşük kontrast"
    ]
  },
  "inspiration_refs": {
    "search_notes": {
      "direction": [
        "SaaS dashboard örnekleri + split editor (sol kontrol paneli / sağ preview)",
        "Template gallery için görsel ağırlıklı kartlar + hızlı filtreleme",
        "Dark mode: nötr graphite + teal/ocean accent (okunabilirlik odaklı)"
      ]
    },
    "urls": [
      "https://dribbble.com/tags/saas-dashboard",
      "https://www.behance.net/search/projects?search=saas%20dashboard%20template",
      "https://www.saasframe.io/categories/dashboard"
    ]
  },
  "design_tokens": {
    "css_custom_properties": {
      "notes": "Mevcut shadcn token yapısını (HSL) koruyun; ancak Syroce için dark varsayılan deneyim tanımlayın. Uygulama ilk açılışta .dark class ile render edilecek şekilde hedefleyin.",
      "recommended_root_dark": {
        "--background": "220 18% 6%",
        "--foreground": "210 20% 96%",
        "--card": "220 18% 8%",
        "--card-foreground": "210 20% 96%",
        "--popover": "220 18% 8%",
        "--popover-foreground": "210 20% 96%",
        "--primary": "174 70% 45%",
        "--primary-foreground": "220 18% 8%",
        "--secondary": "220 14% 14%",
        "--secondary-foreground": "210 20% 96%",
        "--muted": "220 14% 12%",
        "--muted-foreground": "215 12% 70%",
        "--accent": "202 68% 46%",
        "--accent-foreground": "220 18% 8%",
        "--destructive": "0 74% 52%",
        "--destructive-foreground": "210 20% 96%",
        "--border": "220 10% 18%",
        "--input": "220 10% 18%",
        "--ring": "174 70% 45%",
        "--radius": "0.75rem",
        "--chart-1": "174 70% 45%",
        "--chart-2": "202 68% 46%",
        "--chart-3": "36 85% 58%",
        "--chart-4": "152 48% 44%",
        "--chart-5": "0 74% 52%"
      },
      "additional_tokens": {
        "--shadow-elev-1": "0 1px 0 hsl(0 0% 100% / 0.04), 0 10px 30px hsl(220 60% 2% / 0.35)",
        "--shadow-elev-2": "0 1px 0 hsl(0 0% 100% / 0.06), 0 18px 60px hsl(220 60% 2% / 0.5)",
        "--grid-max": "1200px",
        "--sidebar-w": "280px",
        "--editor-left": "360px",
        "--editor-top": "56px"
      }
    },
    "tailwind_semantic_usage": {
      "bg": {
        "app": "bg-background",
        "surface": "bg-card",
        "muted": "bg-muted"
      },
      "text": {
        "primary": "text-foreground",
        "muted": "text-muted-foreground"
      },
      "border": {
        "default": "border-border"
      },
      "ring_focus": "focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background"
    },
    "gradients": {
      "allowed": [
        {
          "name": "Subtle ocean wash (background only)",
          "css": "radial-gradient(900px circle at 20% 10%, hsl(174 70% 45% / 0.12), transparent 60%), radial-gradient(900px circle at 80% 0%, hsl(202 68% 46% / 0.10), transparent 55%)",
          "usage": "Dashboard üst bölümü / empty state arka planı; viewport’un %20’sini geçmesin."
        }
      ],
      "forbidden": "Koyu/satüre mor-pembe, mavi-mor vb. gradient kombinasyonları yasak (kural aşağıda ayrıca eklenecek)."
    },
    "texture": {
      "noise_overlay": {
        "css": "background-image: url('https://images.pexels.com/photos/8337527/pexels-photo-8337527.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940'); background-size: 600px auto; mix-blend-mode: overlay; opacity: 0.06;",
        "usage": "Sadece app shell arka planında çok düşük opaklıkla (okunabilirliği bozmayacak)."
      }
    }
  },
  "typography": {
    "fonts": {
      "heading": {
        "family": "Space Grotesk",
        "fallback": "ui-sans-serif, system-ui",
        "usage": "Sayfa başlıkları, KPI sayıları, editor üst bar"
      },
      "body": {
        "family": "Figtree",
        "fallback": "ui-sans-serif, system-ui",
        "usage": "Tablo, form, açıklamalar"
      },
      "mono": {
        "family": "IBM Plex Mono",
        "usage": "Export bilgileri, dosya isimleri, küçük teknik etiketler"
      }
    },
    "google_fonts_import": {
      "instructions": "index.css içine @import eklemek yerine public/index.html <link> ile eklenmesi önerilir (performans).",
      "links": [
        "https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Figtree:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap"
      ]
    },
    "scale": {
      "h1": "text-4xl sm:text-5xl lg:text-6xl",
      "h2": "text-base md:text-lg",
      "body": "text-sm md:text-base",
      "small": "text-xs"
    },
    "text_rules": [
      "Dashboard ve listelerde: satır aralığı relaxed (leading-relaxed) + yeterli spacing.",
      "Tablo başlıkları uppercase değil; readability için normal-case + tracking-tight.",
      "Türkçe karakterlerde font rendering için antialiased (zaten mevcut)."
    ]
  },
  "layout": {
    "global_shell": {
      "pattern": "Sol sidebar (ikon + label) + üstte page header (breadcrumb + actions) + içerik alanı",
      "sidebar": {
        "width": "var(--sidebar-w)",
        "sections": ["Genel", "Şablonlar", "Editör", "Müşteriler", "Projeler", "Ayarlar"],
        "micro_interaction": "Aktif route: sol border accent + hafif bg-muted; hover: text + icon color shift",
        "data_testid": "app-sidebar"
      },
      "content_grid": {
        "max_width": "var(--grid-max)",
        "padding": "px-4 sm:px-6 lg:px-8",
        "vertical_rhythm": "section arası gap-6/8; kart içi p-5"
      }
    },
    "dashboard": {
      "top": "KPI bento grid (4 kart) + sparkline alanları",
      "bottom": "Sol: son aktiviteler feed; Sağ: projeler durum dağılımı (mini chart)",
      "responsive": "Mobilde tek sütun; md’de 2 sütun; lg’de 12 kolon grid"
    },
    "template_gallery": {
      "structure": "Sticky filtre bar + 3-4 kolon kart grid; kartta hover ile ‘Önizle’ overlay",
      "filtering": "Kategori pills (ToggleGroup) + arama (Command/Input)",
      "preview": "Dialog modal içinde büyük görsel + template meta + ‘Bu şablonu kullan’ CTA"
    },
    "template_editor": {
      "structure": "Topbar (save/export/device toggles) + Split layout: Sol panel formlar, Sağ panel canlı preview",
      "implementation_hint": "shadcn Resizable (resizable.jsx) ile sol panel genişliği ayarlanabilir.",
      "panels": {
        "left": "var(--editor-left) başlangıç; ScrollArea ile içerik; Tabs: Bölümler / Tema",
        "right": "iframe/preview area; AspectRatio + skeleton; responsive device frame toggles"
      },
      "interaction": [
        "Form alanı değişince 250–400ms debounce ile preview update (performans).",
        "Kaydedildi durumu: topbar’da küçük ‘Kaydedildi’ badge.",
        "Export: progress + toast (sonner)."
      ]
    },
    "clients": {
      "structure": "Tablo + sağ üst ‘Yeni Müşteri’ butonu; satır tıklanınca Drawer/Sheet detay",
      "search": "Input + keyboard shortcut (Cmd/Ctrl+K) ile Command palette opsiyonel"
    },
    "projects": {
      "structure": "Tablo veya card-list toggle; status badge; row actions dropdown",
      "statuses": ["Taslak", "Yayınlandı", "Teslim Edildi"]
    }
  },
  "components": {
    "component_path": {
      "primary": [
        "/app/frontend/src/components/ui/button.jsx",
        "/app/frontend/src/components/ui/card.jsx",
        "/app/frontend/src/components/ui/badge.jsx",
        "/app/frontend/src/components/ui/table.jsx",
        "/app/frontend/src/components/ui/dialog.jsx",
        "/app/frontend/src/components/ui/sheet.jsx",
        "/app/frontend/src/components/ui/tabs.jsx",
        "/app/frontend/src/components/ui/resizable.jsx",
        "/app/frontend/src/components/ui/scroll-area.jsx",
        "/app/frontend/src/components/ui/dropdown-menu.jsx",
        "/app/frontend/src/components/ui/select.jsx",
        "/app/frontend/src/components/ui/textarea.jsx",
        "/app/frontend/src/components/ui/input.jsx",
        "/app/frontend/src/components/ui/separator.jsx",
        "/app/frontend/src/components/ui/tooltip.jsx",
        "/app/frontend/src/components/ui/sonner.jsx"
      ],
      "optional": [
        "/app/frontend/src/components/ui/carousel.jsx (template preview gallery için)",
        "/app/frontend/src/components/ui/skeleton.jsx (loading states)",
        "/app/frontend/src/components/ui/breadcrumb.jsx (sayfa başlığı içinde)"
      ]
    },
    "key_patterns": {
      "buttons": {
        "style": "Professional / Corporate + slight premium elevation",
        "variants": {
          "primary": "Button (default) + bg-primary text-primary-foreground; hover: brightness-110",
          "secondary": "outline/secondary; hover: bg-muted",
          "ghost": "ghost; hover: bg-muted/60"
        },
        "radius": "--radius = 0.75rem (12px feel)",
        "motion": "hover: translateY(-1px) + shadow-elev-1; active: scale(0.98)",
        "testid_examples": [
          "data-testid=\"template-editor-save-button\"",
          "data-testid=\"template-editor-export-zip-button\"",
          "data-testid=\"clients-add-button\""
        ]
      },
      "badges_status": {
        "mapping": {
          "Taslak": "bg-muted text-foreground border-border",
          "Yayınlandı": "bg-primary/15 text-foreground border-primary/30",
          "Teslim Edildi": "bg-accent/15 text-foreground border-accent/30"
        },
        "component": "badge.jsx"
      },
      "tables": {
        "behavior": "Row hover bg-muted/50; row actions dropdown right aligned",
        "empty_state": "Card içinde ikon + açıklama + CTA (button)"
      },
      "forms": {
        "component": "form.jsx + input.jsx + textarea.jsx + select.jsx",
        "rules": [
          "Label her input üstünde; helper text muted.",
          "Error state: text-destructive + ring-destructive/40.",
          "Input height: h-10; textarea: min-h-[120px]"
        ],
        "testid_rule": "Tüm input/select/textarea için data-testid zorunlu: örn data-testid=\"client-form-hotel-name-input\""
      },
      "dialogs_drawers": {
        "usage": [
          "Template preview: Dialog",
          "Müşteri ekle/düzenle: Dialog",
          "Müşteri detay: Sheet (sağdan)"
        ]
      },
      "editor_split": {
        "component": "resizable.jsx",
        "left_panel": "Tabs + Accordion (section forms)",
        "right_panel": "Card içinde preview; loading skeleton"
      }
    }
  },
  "motion_microinteractions": {
    "library": {
      "recommended": "framer-motion",
      "why": "Template gallery kart hover, page transitions, editor panel reveal için kontrollü animasyon",
      "install": "npm i framer-motion",
      "usage_snippets_js": {
        "card_hover": "import { motion } from 'framer-motion';\n\n<motion.div whileHover={{ y: -2 }} transition={{ duration: 0.18 }} />",
        "fade_in": "<motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.22 }} />"
      }
    },
    "principles": [
      "Hover: 150–220ms, easing: cubic-bezier(0.2,0.8,0.2,1)",
      "No transition: all (sadece color, background-color, box-shadow, opacity)",
      "Scroll: sticky filter bar + subtle shadow on scroll",
      "Editor: Save feedback (badge) fades in/out"
    ]
  },
  "charts_and_data_viz": {
    "library": {
      "recommended": "recharts",
      "install": "npm i recharts",
      "use_cases": ["Dashboard mini charts", "Projeler durum dağılımı"],
      "styling": {
        "grid": "stroke: hsl(var(--border))",
        "primary": "hsl(var(--primary))",
        "accent": "hsl(var(--accent))",
        "tooltip": "bg-card border-border text-foreground"
      },
      "empty_state": "Veri yoksa Skeleton yerine ‘Henüz veri yok’ + CTA gösterin (özellikle ilk kullanım)."
    }
  },
  "copy_and_ia_tr": {
    "nav_labels": {
      "Dashboard": "Genel Bakış",
      "Templates": "Şablon Galerisi",
      "Editor": "Şablon Editörü",
      "Clients": "Müşteriler",
      "Projects": "Projeler",
      "Settings": "Ayarlar"
    },
    "common_actions": {
      "create": "Yeni Oluştur",
      "save": "Kaydet",
      "saving": "Kaydediliyor…",
      "saved": "Kaydedildi",
      "preview": "Önizle",
      "use_template": "Bu Şablonu Kullan",
      "export_zip": "HTML/CSS Dışa Aktar (ZIP)",
      "publish": "Yayınla",
      "search": "Ara"
    },
    "empty_states": [
      "Henüz müşteri eklemediniz.",
      "Henüz proje yok. Bir şablon seçerek başlayın.",
      "Bu kategoride şablon bulunamadı. Filtreyi temizleyin."
    ]
  },
  "image_urls": {
    "crm_template_thumbs": [
      {
        "category": "Template Gallery thumbnails",
        "description": "Luxury/modern hotel lobby vibe; placeholder thumbnail",
        "url": "https://images.pexels.com/photos/34077115/pexels-photo-34077115.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940"
      },
      {
        "category": "Template Gallery thumbnails",
        "description": "Gold desk / premium reception; placeholder thumbnail",
        "url": "https://images.pexels.com/photos/32978233/pexels-photo-32978233.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940"
      }
    ],
    "template_preview_hero": [
      {
        "category": "Template Preview modal hero",
        "description": "Hotel exterior / night lights (blue-toned)",
        "url": "https://images.pexels.com/photos/34389381/pexels-photo-34389381.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940"
      }
    ],
    "app_background_texture": [
      {
        "category": "App shell noise/texture",
        "description": "Dark wood grain texture for subtle overlay (low opacity)",
        "url": "https://images.pexels.com/photos/8337527/pexels-photo-8337527.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940"
      }
    ]
  },
  "accessibility": {
    "requirements": [
      "WCAG AA kontrast: text-muted-foreground arka plan üzerinde okunur olmalı.",
      "Focus state: tüm interaktiflerde visible ring (ring token).",
      "Keyboard: Template gallery filtreleri Tab ile gezilebilir; Dialog/Sheet focus trap shadcn ile.",
      "Reduced motion: prefers-reduced-motion için framer-motion animasyonları minimalize edilebilir."
    ]
  },
  "testing_attributes": {
    "rule": "Tüm butonlar, linkler, inputlar, selectler, menüler, kritik metinler data-testid içermeli (kebab-case).",
    "examples": [
      "data-testid=\"dashboard-total-clients-stat\"",
      "data-testid=\"template-gallery-category-filter\"",
      "data-testid=\"template-card-preview-button\"",
      "data-testid=\"template-preview-use-button\"",
      "data-testid=\"clients-search-input\"",
      "data-testid=\"projects-status-badge\""
    ]
  },
  "instructions_to_main_agent": [
    "index.css tokenlarını Syroce dark varsayılana göre güncelleyin (dark class aktif).",
    "App.css içindeki merkezlenmiş App-header demo stillerini kaldırın; App container’ı center align etmeyin.",
    "Ana layout: Sidebar + Header + Content. Sidebar nav öğeleri için lucide-react ikonları kullanın.",
    "Template Editor sayfasında shadcn Resizable + ScrollArea + Tabs kullanın; sağ panelde iframe preview (skeleton ile).",
    "Template Gallery’de kart hover overlay + Dialog preview; filtre bar sticky.",
    "Dashboard’da Recharts mini chart ekleyin (sparkline/area).",
    "Her interaktif öğeye data-testid ekleyin (kebab-case).",
    "Toastlar için sonner kullanın (özellikle export)."
  ],
  "general_ui_ux_design_guidelines_appendix": "<General UI UX Design Guidelines>\n    - You must **not** apply universal transition. Eg: `transition: all`. This results in breaking transforms. Always add transitions for specific interactive elements like button, input excluding transforms\n    - You must **not** center align the app container, ie do not add `.App { text-align: center; }` in the css file. This disrupts the human natural reading flow of text\n   - NEVER: use AI assistant Emoji characters like`🤖🧠💭💡🔮🎯📚🎭🎬🎪🎉🎊🎁🎀🎂🍰🎈🎨🎰💰💵💳🏦💎🪙💸🤑📊📈📉💹🔢🏆🥇 etc for icons. Always use **FontAwesome cdn** or **lucid-react** library already installed in the package.json\n\n **GRADIENT RESTRICTION RULE**\nNEVER use dark/saturated gradient combos (e.g., purple/pink) on any UI element.  Prohibited gradients: blue-500 to purple 600, purple 500 to pink-500, green-500 to blue-500, red to pink etc\nNEVER use dark gradients for logo, testimonial, footer etc\nNEVER let gradients cover more than 20% of the viewport.\nNEVER apply gradients to text-heavy content or reading areas.\nNEVER use gradients on small UI elements (<100px width).\nNEVER stack multiple gradient layers in the same viewport.\n\n**ENFORCEMENT RULE:**\n    • Id gradient area exceeds 20% of viewport OR affects readability, **THEN** use solid colors\n\n**How and where to use:**\n   • Section backgrounds (not content backgrounds)\n   • Hero section header content. Eg: dark to light to dark color\n   • Decorative overlays and accent elements only\n   • Hero section with 2-3 mild color\n   • Gradients creation can be done for any angle say horizontal, vertical or diagonal\n\n- For AI chat, voice application, **do not use purple color. Use color like light green, ocean blue, peach orange etc**\n\n</Font Guidelines>\n\n- Every interaction needs micro-animations - hover states, transitions, parallax effects, and entrance animations. Static = dead. \n   \n- Use 2-3x more spacing than feels comfortable. Cramped designs look cheap.\n\n- Subtle grain textures, noise overlays, custom cursors, selection states, and loading animations: separates good from extraordinary.\n   \n- Before generating UI, infer the visual style from the problem statement (palette, contrast, mood, motion) and immediately instantiate it by setting global design tokens (primary, secondary/accent, background, foreground, ring, state colors), rather than relying on any library defaults. Don't make the background dark as a default step, always understand problem first and define colors accordingly\n    Eg: - if it implies playful/energetic, choose a colorful scheme\n           - if it implies monochrome/minimal, choose a black–white/neutral scheme\n\n**Component Reuse:**\n\t- Prioritize using pre-existing components from src/components/ui when applicable\n\t- Create new components that match the style and conventions of existing components when needed\n\t- Examine existing components to understand the project's component patterns before creating new ones\n\n**IMPORTANT**: Do not use HTML based component like dropdown, calendar, toast etc. You **MUST** always use `/app/frontend/src/components/ui/ ` only as a primary components as these are modern and stylish component\n\n**Best Practices:**\n\t- Use Shadcn/UI as the primary component library for consistency and accessibility\n\t- Import path: ./components/[component-name]\n\n**Export Conventions:**\n\t- Components MUST use named exports (export const ComponentName = ...)\n\t- Pages MUST use default exports (export default function PageName() {...})\n\n**Toasts:**\n  - Use `sonner` for toasts\"\n  - Sonner component are located in `/app/src/components/ui/sonner.tsx`\n\nUse 2–4 color gradients, subtle textures/noise overlays, or CSS-based noise to avoid flat visuals.\n</General UI UX Design Guidelines>"
}
