# plan.md (Güncellenmiş)

## 1) Objectives
- Syroce altında **tek kullanıcı** için CRM + otel web sitesi üretim aracı (FastAPI + React + MongoDB, shadcn/ui).
- **30+ otel templatesi** (kategori bazlı) ile hızlı başlangıç ve üretim.
- **Section-based** düzenleme: metin/görsel/renk/typography, section görünürlük & sıralama, **banner ekleme/silme**.
- **Canlı önizleme** (iframe) + responsive modlar (desktop/tablet/mobile).
- Proje bazlı **statik website export (ZIP)**:
  - **Tek sayfa (single-page)** export
  - **Çoklu sayfa (multi-page)** export (index.html + rooms.html + gallery.html + contact.html)
- **Görsel upload** (dosya yükleme) ve URL’leri editörden yönetme.
- **SEO paneli**: title/description/keywords + OG meta (og:image, og:title, og:description).
- **TR/EN dil desteği** (üretilen web sitelerinde navigasyon/footer/form metinleri).
- **Template klonlama**:
  - Projeyi **“Şablon olarak kaydet”** ile yeni template’e dönüştürme.
- **Versiyonlama**:
  - Proje snapshot (v1, v2...) oluşturma
  - Versiyondan geri yükleme (restore)
- **JWT Auth**:
  - İlk kurulumda register, sonra login ile erişim
  - Sidebar’da çıkış
- **Performans**:
  - Debounce autosave (editörde hızlı değişikliklerde stabil)

> Durum: Phase 1–4 tamamlandı. Phase 3 ve Phase 4 özellikleri uygulandı, test edildi. Backend testleri %100 başarılı.

---

## 2) Implementation Steps

### Phase 1 — Core Flow POC (Isolation)
Amaç: “Template seç → section verilerini değiştir → canlı önizleme → statik export zip” akışını kanıtlamak.

**Durum:** ✅ Tamamlandı

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

**Durum:** ✅ Tamamlandı

**User stories (V1)**
1. Dashboard’da toplam müşteri/proje/şablon ve son aktiviteleri görmek istiyorum.
2. Template galerisinde kategori filtreleyip önizleme alarak doğru şablonu seçmek istiyorum.
3. Editörde tüm section alanlarını (metin/görsel/link) düzenleyip canlı önizlemede görmek istiyorum.
4. Yeni banner section ekleyip CTA linki tanımlamak istiyorum.
5. Projeyi bir otele bağlayıp teslim durumunu (taslak/yayında/teslim) takip etmek istiyorum.

**Backend (FastAPI + MongoDB)**
- Collections: `templates`, `projects`, `clients`, `activity_log`.
- Endpoints:
  - Templates: `GET/POST/PUT/DELETE /templates` (seed + CRUD)
  - Projects: `GET/POST/PUT/DELETE /projects`, `POST /projects/{id}/export`, `GET /projects/{id}/preview`
  - Clients: `GET/POST/PUT/DELETE /clients`
  - Dashboard: `GET /dashboard/stats`, `GET /dashboard/activity`
- Seed: Startup’ta **30 template otomatik yüklenir**.

**Frontend (React + shadcn/ui)**
- Pages: Dashboard, Template Gallery, Template Editor, Clients, Projects.
- Editor UX:
  - Bölüm listesi, show/hide, yukarı-aşağı sıralama
  - Bölüm formları (header/hero/about/rooms/gallery/services/testimonials/contact/footer)
  - Tema paneli (renkler + fontlar)
  - Live preview iframe + responsive modlar
  - Autosave + manual save
  - Banner ekleme/silme
- UI: Türkçe, dark theme, premium SaaS görünümü.

**Export v1**
- ZIP içinde: `{project-name}/index.html` + `{project-name}/README.md`
- Site içinde: “Powered by Syroce” footer (kapatılamaz)

**V1 testing**
- ✅ Backend testleri: %100 geçti.
- ✅ Frontend testleri: %95 geçti (minor timing uyarısı dışında).

---

### Phase 3 — Feature Expansion (Post-V1)
Amaç: üretim hızını artıran ve teslim kalitesini yükselten özellikler.

**Durum:** ✅ Tamamlandı

**User stories (Expansion)**
1. Proje exportlarında birden fazla sayfa (Rooms, Gallery, Contact vb.) çıkarmak istiyorum.
2. Görselleri sisteme upload edip editörden yönetmek istiyorum.
3. SEO alanlarını (title/description/og tags) proje bazında düzenlemek istiyorum.
4. Projeyi “Şablon olarak kaydet” ile yeni template’e dönüştürmek istiyorum.
5. Üretilen web sitelerinde **İngilizce dil desteği** (TR/EN) istiyorum.

**Scope (Uygulandı)**
- ✅ **Multi-page export + navigation**
  - `export_mode: single | multi` proje ayarı
  - Multi export: `index.html`, `rooms.html`, `gallery.html`, `contact.html`
- ✅ **Image upload**
  - `POST /api/upload` ile dosya yükleme
  - Editörde image alanlarında URL + upload butonu
  - Upload’lar `GET /api/uploads/{filename}` ile servis edilir
- ✅ **SEO panel**
  - Project SEO: title/description/keywords + OG meta
  - Export ve preview HTML içine meta tag’ler eklenir
- ✅ **Template cloning**
  - `POST /api/templates/clone-from-project/{project_id}`
  - UI: “Şablon Kaydet” dialog’u
- ✅ **TR/EN website language**
  - Proje dili `language: tr | en`
  - Footer, contact placeholders, quick links gibi metinler çeviriyle render edilir

**Testing (Tamamlandı)**
- ✅ Backend: Phase 3 kapsamındaki tüm endpoint’ler %100 geçti.
- ✅ Frontend: Editor’da SEO/Settings/Sections/Theme akışları doğrulandı.

---

### Phase 4 — Hardening & Auth
Amaç: güvenlik, stabilite, geri alma, performans.

**Durum:** ✅ Tamamlandı

**User stories (Hardening)**
1. Proje değişikliklerini snapshot alıp geri dönebilmek istiyorum.
2. Sisteme giriş için basit ama güvenli admin login istiyorum.
3. Editörde hızlı düzenleme yaparken stabil autosave performansı istiyorum.

**Scope (Uygulandı)**
- ✅ **Versioning (snapshots + restore)**
  - `POST /api/projects/{id}/versions` snapshot
  - `GET /api/projects/{id}/versions` liste
  - `POST /api/projects/{id}/restore/{version_id}` restore
  - UI: “Versiyon” dialog + “Versiyon oluştur” aksiyonu
- ✅ **JWT Auth (register/login)**
  - `POST /api/auth/register`, `POST /api/auth/login`, `GET /api/auth/me`, `GET /api/auth/check`
  - Frontend: AuthWrapper + Login ekranı + Sidebar logout
- ✅ **Performance optimization**
  - Debounce autosave
  - Preview güncellemeleri kontrollü

**Testing (Tamamlandı)**
- ✅ Backend: Auth + versioning + multi export + upload %100 geçti.
- ✅ Frontend: Tüm yeni tab ve aksiyonlar doğrulandı.

---

## 3) Next Actions
1. **Stabilizasyon / UX iyileştirme (opsiyonel):**
   - Frontend için ek “loading fallback” ve hata state’leri
   - Export sonrası toast/notification iyileştirmeleri
2. **Undo/Redo (opsiyonel):** editörde kullanıcı deneyimini güçlendirmek için.
3. **Blok kütüphanesi (opsiyonel):** sık kullanılan section konfigürasyonlarını kaydet/yeniden kullan.
4. **Asset bundling (opsiyonel):** export sırasında harici görsel URL’lerini indirip ZIP içine almak (tam offline paket).

---

## 4) Success Criteria
- ✅ Template → proje → düzenleme → canlı önizleme → export zip akışı çalışır.
- ✅ Export zip açıldığında site offline çalışır (tek sayfa) ve multi export’ta sayfalar arası gezilebilir.
- ✅ Footer’da “Powered by Syroce” her export’ta görünür ve devre dışı bırakılamaz.
- ✅ 30+ template galeride kategorilerle seçilebilir ve her biri export edilebilir.
- ✅ Müşteri–proje bağlama ve temel durum takibi sorunsuzdur.
- ✅ SEO alanları export HTML içinde meta tag olarak bulunur.
- ✅ TR/EN dil desteği proje bazında uygulanır.
- ✅ Versioning: snapshot + restore çalışır.
- ✅ JWT auth: register/login + me endpoint + logout çalışır.
- ✅ Testler: Backend %100; Frontend temel akışlar doğrulandı.
