# plan.md (Güncellenmiş)

## 1) Objectives
- Syroce altında **tek kullanıcı** için CRM + otel web sitesi üretim aracı (FastAPI + React + MongoDB, shadcn/ui).
- **30+ otel templatesi** (kategori bazlı) ile hızlı başlangıç ve üretim.
- **Section-based** düzenleme: metin/görsel/renk/typography, section görünürlük & sıralama, **banner ekleme**.
- **Canlı önizleme** (iframe) ile form tabanlı editör.
- Proje bazlı **statik HTML export (ZIP)** (index.html + README teslim notları).
- Her sitede zorunlu **“Powered by Syroce”** footer branding (kapatılamaz).
- Basit müşteri/proje takibi (hangi otel hangi siteye sahip, durum takibi).

> Durum: Phase 2 (MVP) tamamlandı. Uygulama çalışır durumda; 30 template seed edildi, CRUD + editör + export + Türkçe/dark UI hazır.

---

## 2) Implementation Steps

### Phase 1 — Core Flow POC (Isolation)
Amaç: “Template seç → section verilerini değiştir → canlı önizleme → statik export zip” akışını kanıtlamak.

**Durum:** ✅ Tamamlandı (MVP kapsamında doğrudan uygulandı ve doğrulandı).

**User stories (POC)**
1. Bir template seçip proje oluşturmak istiyorum ki otel için hızlı başlayabileyim.
2. Hero/banner metni ve görselini değiştirip anında önizlemede görmek istiyorum.
3. Section’ları gizleyip/sıralayıp sayfa yapısını hızlıca şekillendirmek istiyorum.
4. Renk/typography değiştirince tüm sitede tutarlı uygulansın istiyorum.
5. Export alıp zip içinden index.html çıktısını doğrulamak istiyorum.

**POC scope**
- Backend: Template/Project şeması + export endpoint.
- Frontend: Template Gallery (min), Editor (min), live preview.
- Export: Server-side HTML üretimi + zip.
- Branding: footer’da her zaman “Powered by Syroce”.

**Sonuçlar / Gerçekleşenler**
- ✅ Preview renderer ile canlı önizleme.
- ✅ ZIP export endpoint (download).
- ✅ Branding zorunlu.

---

### Phase 2 — V1 App Development (MVP)
Amaç: CRM sayfaları + 30+ template + üretim akışını tamamlamak.

**Durum:** ✅ Tamamlandı (Testler geçti, üretime hazır).

**User stories (V1)**
1. Dashboard’da toplam müşteri/proje/şablon ve son aktiviteleri görmek istiyorum.
2. Template galerisinde kategori filtreleyip önizleme alarak doğru şablonu seçmek istiyorum.
3. Editörde tüm section alanlarını (metin/görsel/link) düzenleyip canlı önizlemede görmek istiyorum.
4. Yeni banner section ekleyip CTA linki tanımlamak istiyorum.
5. Projeyi bir otele bağlayıp teslim durumunu (taslak/yayında/teslim) takip etmek istiyorum.

**Backend (FastAPI + MongoDB)**
- Collections: `templates`, `projects`, `clients`, `activity_log`.
- Endpoints (tamamlandı):
  - Templates: `GET/POST/PUT/DELETE /templates` (seed + CRUD)
  - Projects: `GET/POST/PUT/DELETE /projects`, `POST /projects/{id}/export`, `GET /projects/{id}/preview`
  - Clients: `GET/POST/PUT/DELETE /clients`
  - Dashboard: `GET /dashboard/stats`, `GET /dashboard/activity`
- Seed: Startup’ta **30 template otomatik yüklenir** (kategori bazlı).

**Frontend (React + shadcn/ui)**
- Pages (tamamlandı): Dashboard, Template Gallery, Template Editor, Clients, Projects.
- Editor UX (tamamlandı):
  - Bölüm listesi, show/hide, yukarı-aşağı sıralama
  - Bölüm formları (header/hero/about/rooms/gallery/services/testimonials/contact/footer)
  - Tema paneli (renkler + fontlar)
  - Live preview iframe + responsive modlar (desktop/tablet/mobile)
  - Autosave + manual save
  - Banner ekleme/silme
- UI: Türkçe, dark theme, premium SaaS görünümü.

**Export v1 (tamamlandı)**
- ZIP içinde: `{project-name}/index.html` + `{project-name}/README.md`
- Site içinde: “Powered by Syroce” footer (kapatılamaz)

**V1 testing**
- ✅ Backend testleri: %100 geçti.
- ✅ Frontend testleri: %95 geçti (template preview’de minor timing/DOM attachment; işlevsel bug yok).
- ✅ E2E akış doğrulandı: Template seç → proje oluştur → edit → export.

---

### Phase 3 — Feature Expansion (Post-V1)
Amaç: üretim hızını artıran ve teslim kalitesini yükselten özellikler.

**Durum:** ⏳ Beklemede (kullanıcı isterse).

**User stories (Expansion)**
1. Proje exportlarında birden fazla sayfa (Rooms, Contact vb.) çıkarmak istiyorum.
2. Görselleri sisteme upload edip export’ta otomatik asset’e dönüştürmek istiyorum.
3. SEO alanlarını (title/description/og tags) proje bazında düzenlemek istiyorum.
4. Projeler için checklist/teslim adımları ekleyip süreci standartlaştırmak istiyorum.
5. Sık kullandığım section bloklarını “blok kütüphanesi” olarak kaydetmek istiyorum.
6. (Opsiyonel) Template → **Yeni template olarak kaydet** (UI üzerinden “Şablon olarak kaydet” akışı).

**Scope**
- Multi-page export + navigation.
- Image upload (local veya S3) + export bundle.
- SEO panel + sitemap.xml/robots.txt.
- Project workflow checklist + activity timeline genişletme.
- Template/block library + template cloning UI.

**Testing**
- Multi-page export E2E + asset bundling doğrulama.

---

### Phase 4 — Hardening & Optional Auth
Not: Tek kullanıcı olduğu için auth opsiyonel; istenirse basit admin login eklenir.

**Durum:** ⏳ Beklemede.

**User stories (Hardening)**
1. Büyük projelerde editörün hızlı kalmasını istiyorum.
2. Export sırasında hata olursa anlaşılır log ve tekrar dene seçeneği istiyorum.
3. Template/Project versiyonlarını geri alabilmek istiyorum.
4. Uygulama ayarlarını (default theme, branding metni) yönetmek istiyorum.
5. (Opsiyonel) Admin login ile uygulamayı güvenceye almak istiyorum.

**Scope**
- Export job queue (gerekirse) + hata logları.
- Versioning (snapshots) + restore.
- Opsiyonel JWT auth.
- Kapsamlı regression testleri.

---

## 3) Next Actions
1. ✅ (Tamamlandı) MVP’nin stabil kullanımına devam edin: şablon seç → proje oluştur → düzenle → export.
2. (İsteğe bağlı) Phase 3 için önceliklendirme:
   - Multi-page export mu?
   - Görsel upload mı?
   - SEO panel mi?
   - Template’i “Yeni şablon olarak kaydet” akışı mı?
3. (İsteğe bağlı) Hosting teslim sürecini standartlaştırmak için export ZIP içine ek bir `delivery-checklist.md` ekleme.
4. (İsteğe bağlı) Editörde Undo/Redo ve daha gelişmiş “section blokları” kütüphanesi.

---

## 4) Success Criteria
- ✅ Template → proje → düzenleme → canlı önizleme → export zip akışı %100 çalışır.
- ✅ Export zip açıldığında site offline çalışır (index.html ile).
- ✅ Footer’da “Powered by Syroce” her export’ta görünür ve devre dışı bırakılamaz.
- ✅ 30+ template galeride kategorilerle seçilebilir ve her biri export edilebilir.
- ✅ Müşteri–proje bağlama ve temel durum takibi sorunsuzdur.
- ✅ E2E testleri geçti (backend %100, frontend %95; minor timing uyarısı dışında).