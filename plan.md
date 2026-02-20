# plan.md

## 1) Objectives
- Syroce altında **tek kullanıcı** için CRM + otel web sitesi üretim aracı (FastAPI + React + MongoDB, shadcn/ui).
- **30+ otel templatesi** (kategori bazlı) ve **template → yeni template** türetme.
- **Section-based** düzenleme: tüm metin/görsel/renk/typography, section görünürlük & sıralama, **banner ekleme**.
- **Canlı önizleme** ile form tabanlı editör.
- Proje bazlı **statik HTML/CSS export (zip)** + hosting yönlendirme/teslim bilgisi.
- Her sitede zorunlu **“Powered by Syroce”** footer branding.
- Basit müşteri/proje takibi (hangi otel hangi siteye sahip).

## 2) Implementation Steps

### Phase 1 — Core Flow POC (Isolation)
Amaç: “Template seç → section verilerini değiştir → canlı önizleme → statik export zip” akışını kanıtlamak.

**User stories (POC)**
1. Bir template seçip proje oluşturmak istiyorum ki otel için hızlı başlayabileyim.
2. Hero/banner metni ve görselini değiştirip anında önizlemede görmek istiyorum.
3. Section’ları gizleyip/sıralayıp sayfa yapısını hızlıca şekillendirmek istiyorum.
4. Renk/typography değiştirince tüm sitede tutarlı uygulansın istiyorum.
5. Export alıp zip içinden index.html ve asset’lerin doğru çıktığını doğrulamak istiyorum.

**POC scope**
- Backend: 1 template JSON şeması + 1 proje dokümanı + export endpointi.
- Frontend: Template gallery (min), editor (min), live preview iframe.
- Export: server-side render (Jinja2) + CSS + assets kopyalama + zip.
- Branding: footer partial’ı export’ta her zaman eklenir (kapatılamaz).

**Tasks**
- Template şeması (sections[]; each section type + props; theme tokens).
- React editor: sol panel form, sağ panel preview (iframe + postMessage ile state güncelleme).
- FastAPI: 
  - `GET /templates`, `POST /projects`, `GET/PUT /projects/{id}`
  - `POST /projects/{id}/export` → zip stream
- Websearch (best practice): “static site export from templates”, “React iframe live preview postMessage pattern”, “FastAPI streaming zip”.
- POC test: 1 projeyi uçtan uca export edip zip’i açarak render doğrulama.
- Fix-until-works: export bozuksa Phase 2’ye geçme.

---

### Phase 2 — V1 App Development (MVP)
Amaç: POC core’u sağlamlaştırıp CRM sayfaları + 30+ template + üretim akışını tamamlamak.

**User stories (V1)**
1. Dashboard’da toplam müşteri/proje ve son aktiviteleri görmek istiyorum.
2. Template galerisinde kategori filtreleyip önizleme alarak doğru şablonu seçmek istiyorum.
3. Editörde tüm section alanlarını (metin/görsel/link) düzenleyip geri al/ileri al ile güvenle çalışmak istiyorum.
4. Yeni banner section ekleyip CTA linki tanımlamak istiyorum.
5. Projeyi bir otele bağlayıp teslim durumunu (taslak/yayında/teslim) takip etmek istiyorum.

**Backend (FastAPI + MongoDB)**
- Collections: `templates`, `projects`, `clients`, `activity_log`.
- Models:
  - Template: category, pages (initially 1 page: Home), sections schema, default theme.
  - Project: templateId, clientId, overrides (sections/theme), status, domain/hosting notes.
  - Client: hotel name, contacts, notes.
- Endpoints:
  - Templates: CRUD (clone-from-template, publish/unpublish template).
  - Projects: CRUD, duplicate project, export.
  - Clients: CRUD.
- Export v1:
  - Home page only (index.html) + assets folder + styles.css.
  - Image handling: URL references first; optional upload later.
  - Add `delivery.md` in zip: hosting yönlendirme / kurulum notları.

**Frontend (React + shadcn/ui)**
- Pages: Dashboard, Template Gallery, Template Editor, Clients, Projects, Settings.
- Editor UX:
  - Section list (reorder via drag handle), show/hide toggle.
  - Section forms by type (hero, rooms, gallery, services, testimonials, contact, footer).
  - Theme panel (primary/secondary, font, radius).
  - Live preview (iframe) + responsive breakpoints.
  - Autosave + manual save.
- Branding:
  - Footer’da “Powered by Syroce” sabit; template editörde kapatılamaz.

**Templates (30+)**
- 30 template seed: 7 kategoriye dağıtılmış, aynı section types ama farklı layout variants + theme tokens.
- Data-driven yaklaşım: layout variant’ları (e.g., heroSplit, heroCentered, galleryMasonry) Jinja/React preview renderer’da desteklenir.

**V1 testing**
- 1 tur E2E: template seç → proje → edit → müşteri bağla → export zip → içerik doğrula.
- Regression: 3 farklı template ile export doğrulama.

---

### Phase 3 — Feature Expansion (Post-V1)
Amaç: üretim hızını artıran ve teslim kalitesini yükselten özellikler.

**User stories (Expansion)**
1. Proje exportlarında birden fazla sayfa (Rooms, Contact) çıkarmak istiyorum.
2. Görselleri sisteme upload edip export’ta otomatik asset’e dönüştürmek istiyorum.
3. SEO alanlarını (title/description/og tags) proje bazında düzenlemek istiyorum.
4. Projeler için checklist/teslim adımları ekleyip süreci standartlaştırmak istiyorum.
5. Sık kullandığım section bloklarını “blok kütüphanesi” olarak kaydetmek istiyorum.

**Scope**
- Multi-page export + navigation.
- Image upload (S3 yoksa local + export bundle), basit resize opsiyonu.
- SEO panel + sitemap.xml/robots.txt.
- Project workflow checklist + activity timeline.
- Template/block library.

**Testing**
- Multi-page export E2E + asset bundling doğrulama.

---

### Phase 4 — Hardening & Optional Auth
Not: Tek kullanıcı olduğu için auth opsiyonel; istenirse basit admin login eklenir.

**User stories (Hardening)**
1. Büyük projelerde editörün hızlı kalmasını istiyorum.
2. Export sırasında hata olursa anlaşılır log ve tekrar dene seçeneği istiyorum.
3. Template/Project versiyonlarını geri alabilmek istiyorum.
4. Uygulama ayarlarını (default theme, branding metni) yönetmek istiyorum.
5. (Opsiyonel) Admin login ile uygulamayı güvenceye almak istiyorum.

**Scope**
- Caching, export job queue (gerekirse), audit logs.
- Versioning (snapshots) + restore.
- Opsiyonel JWT auth.
- Son kapsamlı regression.

## 3) Next Actions
1. POC için 1 adet “Luxury” template şemasını ve renderer yaklaşımını netleştir (Jinja2 + theme tokens).
2. Live preview için iframe + postMessage protokolünü belirle.
3. Export zip endpointini (stream) prototiple ve yerelde zip doğrula.
4. POC başarı sonrası: data model final + seed 30 template üretimi.
5. V1 sayfalarını (Dashboard/Gallery/Editor/Clients/Projects) minimum akışla ayağa kaldır.

## 4) Success Criteria
- Template → proje → düzenleme → canlı önizleme → export zip akışı %100 çalışır.
- Export zip açıldığında site offline çalışır (index.html + css + assets).
- Footer’da “Powered by Syroce” her export’ta görünür ve devre dışı bırakılamaz.
- 30+ template galeride kategorilerle seçilebilir ve her biri export edilebilir.
- Müşteri–proje bağlama ve temel durum takibi sorunsuzdur.
- V1 E2E testlerinde en az 3 farklı template ile export/regression geçer.
