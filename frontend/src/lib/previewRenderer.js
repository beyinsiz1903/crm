// Generates complete hotel website HTML from section data and theme
// Used for live preview in editor and matches backend export output

const SERVICE_ICONS = {
  spa: `<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 22c-4-3-8-6-8-10a8 8 0 0 1 16 0c0 4-4 7-8 10z"/></svg>`,
  restaurant: `<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2"/><path d="M7 2v20"/><path d="M21 15V2v0a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3zm0 0v7"/></svg>`,
  pool: `<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M2 20c2-1 4-1 6 0s4 1 6 0 4-1 6 0"/><path d="M2 17c2-1 4-1 6 0s4 1 6 0 4-1 6 0"/></svg>`,
  fitness: `<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M6.5 6.5h11"/><path d="M6.5 17.5h11"/><path d="M4.5 9v6"/><path d="M19.5 9v6"/><path d="M12 6.5v11"/></svg>`,
  parking: `<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="3" width="18" height="18" rx="3"/><path d="M9 17V7h4a3 3 0 0 1 0 6H9"/></svg>`,
  transfer: `<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M5 17h14v-5H5z"/><path d="M2 12l3-5h14l3 5"/><circle cx="7.5" cy="17" r="2"/><circle cx="16.5" cy="17" r="2"/></svg>`,
};

const STAR_SVG = `<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>`;

function escapeHtml(text) {
  if (!text) return "";
  return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function generateCSS(theme) {
  const pc = theme.primaryColor || "#C5A572";
  const sc = theme.secondaryColor || "#1A1A2E";
  const bg = theme.backgroundColor || "#FFFFFF";
  const tc = theme.textColor || "#333333";
  const hf = theme.headerFont || "'Playfair Display', serif";
  const bf = theme.bodyFont || "'Lato', sans-serif";

  return `
    *{margin:0;padding:0;box-sizing:border-box}
    html{scroll-behavior:smooth}
    body{font-family:${bf};color:${tc};background:${bg};line-height:1.7}
    h1,h2,h3,h4{font-family:${hf};line-height:1.3}
    img{max-width:100%;height:auto}
    a{color:${pc};text-decoration:none}
    .container{max-width:1200px;margin:0 auto;padding:0 20px}
    .site-header{position:fixed;top:0;left:0;right:0;z-index:100;padding:20px 0;transition:background 0.3s}
    .site-header.solid{background:${sc}}
    .site-header.transparent{background:transparent}
    .site-header .nav-inner{display:flex;justify-content:space-between;align-items:center;max-width:1200px;margin:0 auto;padding:0 20px}
    .site-header .logo{font-family:${hf};font-size:1.8rem;color:#fff;font-weight:700}
    .site-header nav a{color:#fff;margin-left:25px;font-size:0.95rem;font-weight:500;transition:opacity 0.2s}
    .site-header nav a:hover{opacity:0.8}
    .hero{position:relative;min-height:100vh;display:flex;align-items:center;justify-content:center;text-align:center;color:#fff;overflow:hidden}
    .hero-bg{position:absolute;inset:0;background-size:cover;background-position:center}
    .hero-overlay{position:absolute;inset:0;background:rgba(0,0,0,0.5)}
    .hero-content{position:relative;z-index:2;max-width:800px;padding:40px 20px}
    .hero h1{font-size:clamp(2.5rem,5vw,4.5rem);margin-bottom:20px;font-weight:700}
    .hero p{font-size:clamp(1rem,2vw,1.4rem);margin-bottom:30px;opacity:0.9}
    .btn{display:inline-block;padding:14px 40px;background:${pc};color:#fff;border-radius:4px;font-weight:600;font-size:1rem;transition:all 0.3s;border:none;cursor:pointer}
    .btn:hover{opacity:0.9;transform:translateY(-2px)}
    .section{padding:100px 0}
    .section-title{font-size:clamp(1.8rem,3vw,2.8rem);text-align:center;margin-bottom:15px;color:${sc}}
    .section-subtitle{text-align:center;color:${tc};opacity:0.7;margin-bottom:60px;font-size:1.1rem}
    .about-grid{display:grid;grid-template-columns:1fr 1fr;gap:60px;align-items:center}
    .about-grid img{border-radius:12px;width:100%;height:400px;object-fit:cover}
    .about-text h2{font-size:2.2rem;margin-bottom:20px;color:${sc}}
    .about-text p{font-size:1.05rem;line-height:1.8}
    .rooms-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:30px}
    .room-card{border-radius:12px;overflow:hidden;box-shadow:0 4px 20px rgba(0,0,0,0.08);transition:transform 0.3s;background:#fff}
    .room-card:hover{transform:translateY(-5px)}
    .room-card img{width:100%;height:250px;object-fit:cover}
    .room-card-body{padding:25px}
    .room-card h3{font-size:1.4rem;margin-bottom:10px;color:${sc}}
    .room-card p{font-size:0.95rem;opacity:0.8;margin-bottom:15px}
    .room-price{font-size:1.5rem;font-weight:700;color:${pc}}
    .room-features{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}
    .room-features span{background:${pc}15;color:${pc};padding:4px 12px;border-radius:20px;font-size:0.8rem}
    .gallery-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:15px}
    .gallery-grid.masonry{grid-auto-rows:200px}
    .gallery-grid.masonry .gallery-item:nth-child(1){grid-row:span 2}
    .gallery-grid.masonry .gallery-item:nth-child(4){grid-row:span 2}
    .gallery-item{border-radius:8px;overflow:hidden}
    .gallery-item img{width:100%;height:100%;object-fit:cover;transition:transform 0.5s}
    .gallery-item:hover img{transform:scale(1.05)}
    .services-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:30px}
    .service-card{text-align:center;padding:40px 25px;border-radius:12px;background:#fff;box-shadow:0 2px 15px rgba(0,0,0,0.05);transition:transform 0.3s}
    .service-card:hover{transform:translateY(-5px)}
    .service-icon{color:${pc};margin-bottom:20px;display:inline-block}
    .service-card h3{font-size:1.2rem;margin-bottom:10px;color:${sc}}
    .service-card p{font-size:0.95rem;opacity:0.7}
    .testimonials-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:30px}
    .testimonial-card{padding:35px;border-radius:12px;background:#fff;box-shadow:0 2px 15px rgba(0,0,0,0.05)}
    .testimonial-stars{color:${pc};display:flex;gap:4px;margin-bottom:15px}
    .testimonial-card p{font-style:italic;font-size:1.05rem;line-height:1.7;margin-bottom:20px}
    .testimonial-author{font-weight:600;color:${sc}}
    .contact-grid{display:grid;grid-template-columns:1fr 1fr;gap:60px;align-items:start}
    .contact-info h3{font-size:1.3rem;margin-bottom:15px;color:${sc}}
    .contact-item{display:flex;align-items:center;gap:12px;margin-bottom:18px;font-size:1rem}
    .contact-form input,.contact-form textarea{width:100%;padding:14px 18px;border:1px solid #ddd;border-radius:8px;font-family:${bf};font-size:1rem;margin-bottom:15px;transition:border 0.2s}
    .contact-form input:focus,.contact-form textarea:focus{border-color:${pc};outline:none}
    .contact-form textarea{min-height:140px;resize:vertical}
    .cta-banner{position:relative;padding:80px 0;text-align:center;color:#fff;overflow:hidden}
    .cta-banner .hero-bg{position:absolute;inset:0;background-size:cover;background-position:center}
    .cta-banner .hero-overlay{position:absolute;inset:0;background:rgba(0,0,0,0.6)}
    .cta-banner .hero-content{position:relative;z-index:2}
    .cta-banner h2{font-size:2.5rem;margin-bottom:15px}
    .cta-banner p{font-size:1.2rem;margin-bottom:30px;opacity:0.9}
    .site-footer{background:${sc};color:#fff;padding:60px 0 30px}
    .footer-grid{display:grid;grid-template-columns:2fr 1fr 1fr;gap:40px;margin-bottom:40px}
    .footer-grid h3{font-size:1.3rem;margin-bottom:20px;font-family:${hf}}
    .footer-grid p,.footer-grid a{font-size:0.95rem;color:rgba(255,255,255,0.8)}
    .footer-grid a:hover{color:#fff}
    .footer-social{display:flex;gap:15px;margin-top:15px}
    .footer-social a{width:40px;height:40px;border-radius:50%;border:1px solid rgba(255,255,255,0.3);display:flex;align-items:center;justify-content:center;transition:all 0.3s}
    .footer-social a:hover{background:${pc};border-color:${pc}}
    .footer-bottom{border-top:1px solid rgba(255,255,255,0.15);padding-top:25px;display:flex;justify-content:space-between;align-items:center}
    .footer-bottom p{font-size:0.85rem;opacity:0.7}
    .syroce-brand{display:flex;align-items:center;gap:6px;font-size:0.85rem;opacity:0.7;color:#fff}
    .syroce-brand:hover{opacity:1}
    .syroce-brand span{font-weight:700;color:${pc}}
    @media(max-width:768px){
      .about-grid,.contact-grid{grid-template-columns:1fr;gap:30px}
      .footer-grid{grid-template-columns:1fr}
      .gallery-grid{grid-template-columns:repeat(2,1fr)}
      .site-header nav{display:none}
      .hero h1{font-size:2.2rem}
      .section{padding:60px 0}
    }
  `;
}

function renderSection(section, theme, t) {
  const props = section.props || {};
  const type = section.type;
  const pc = theme.primaryColor || "#C5A572";
  const sc = theme.secondaryColor || "#1A1A2E";

  switch (type) {
    case "header": {
      const menuItems = props.menuItems || [];
      const menuHtml = menuItems.map((item) => `<a href="#${item.toLowerCase().replace(/ /g, "-")}">${item}</a>`).join("");
      return `<header class="site-header ${props.style || "transparent"}"><div class="nav-inner"><div class="logo">${props.hotelName || "Hotel"}</div><nav>${menuHtml}</nav></div></header>`;
    }
    case "hero": {
      const ctaHtml = props.ctaText ? `<a href="${props.ctaLink || "#"}" class="btn">${props.ctaText}</a>` : "";
      return `<section class="hero ${props.layout || "fullscreen"}" id="anasayfa"><div class="hero-bg" style="background-image:url('${props.backgroundImage || ""}')"></div><div class="hero-overlay" style="opacity:${props.overlayOpacity || "0.5"}"></div><div class="hero-content"><h1>${props.title || ""}</h1><p>${props.subtitle || ""}</p>${ctaHtml}</div></section>`;
    }
    case "about": {
      const imgHtml = props.image ? `<img src="${props.image}" alt="${props.title || ""}">` : "";
      const textHtml = `<div class="about-text"><h2>${props.title || ""}</h2><p>${props.description || ""}</p></div>`;
      const isRightImage = props.layout === "right-image";
      return `<section class="section" id="hakkimizda"><div class="container"><div class="about-grid">${isRightImage ? textHtml + "<div>" + imgHtml + "</div>" : "<div>" + imgHtml + "</div>" + textHtml}</div></div></section>`;
    }
    case "rooms": {
      const rooms = props.rooms || [];
      const roomsHtml = rooms.map((room) => {
        const features = (room.features || []).map((f) => `<span>${f}</span>`).join("");
        return `<div class="room-card"><img src="${room.image || ""}" alt="${room.name || ""}"><div class="room-card-body"><h3>${room.name || ""}</h3><p>${room.description || ""}</p><div class="room-price">${room.price || ""}</div><div class="room-features">${features}</div></div></div>`;
      }).join("");
      return `<section class="section" id="odalar"><div class="container"><h2 class="section-title">${props.title || ""}</h2><p class="section-subtitle">${props.subtitle || ""}</p><div class="rooms-grid">${roomsHtml}</div></div></section>`;
    }
    case "gallery": {
      const images = props.images || [];
      const layoutClass = props.layout === "masonry" ? "masonry" : "";
      const imgsHtml = images.map((img) => `<div class="gallery-item"><img src="${img.url || ""}" alt="${img.alt || ""}"></div>`).join("");
      return `<section class="section" style="background:#f8f8f8" id="galeri"><div class="container"><h2 class="section-title">${props.title || ""}</h2><div class="gallery-grid ${layoutClass}">${imgsHtml}</div></div></section>`;
    }
    case "services": {
      const services = props.services || [];
      const svcHtml = services.map((svc) => {
        const icon = SERVICE_ICONS[svc.icon] || SERVICE_ICONS.spa;
        return `<div class="service-card"><div class="service-icon">${icon}</div><h3>${svc.name || ""}</h3><p>${svc.description || ""}</p></div>`;
      }).join("");
      return `<section class="section" id="hizmetler"><div class="container"><h2 class="section-title">${props.title || ""}</h2><div class="services-grid">${svcHtml}</div></div></section>`;
    }
    case "testimonials": {
      const testimonials = props.testimonials || [];
      const itemsHtml = testimonials.map((t) => {
        const stars = STAR_SVG.repeat(t.rating || 5);
        return `<div class="testimonial-card"><div class="testimonial-stars">${stars}</div><p>"${t.text || ""}"</p><div class="testimonial-author">${t.name || ""}</div></div>`;
      }).join("");
      return `<section class="section" style="background:#f8f8f8" id="yorumlar"><div class="container"><h2 class="section-title">${props.title || ""}</h2><div class="testimonials-grid">${itemsHtml}</div></div></section>`;
    }
    case "contact": {
      return `<section class="section" id="iletisim"><div class="container"><h2 class="section-title">${props.title || ""}</h2><div class="contact-grid"><div class="contact-info"><h3>Iletisim Bilgileri</h3><div class="contact-item"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="${pc}" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg><span>${props.address || ""}</span></div><div class="contact-item"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="${pc}" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg><span>${props.phone || ""}</span></div><div class="contact-item"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="${pc}" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg><span>${props.email || ""}</span></div></div><div class="contact-form"><input type="text" placeholder="Adiniz Soyadiniz"><input type="email" placeholder="E-posta Adresiniz"><input type="text" placeholder="Konu"><textarea placeholder="Mesajiniz"></textarea><button class="btn">Gonder</button></div></div></div></section>`;
    }
    case "banner": {
      const ctaHtml = props.ctaText ? `<a href="${props.ctaLink || "#"}" class="btn">${props.ctaText}</a>` : "";
      return `<section class="cta-banner"><div class="hero-bg" style="background-image:url('${props.backgroundImage || ""}')"></div><div class="hero-overlay"></div><div class="hero-content"><h2>${props.title || ""}</h2><p>${props.subtitle || ""}</p>${ctaHtml}</div></section>`;
    }
    case "footer": {
      const social = props.socialLinks || {};
      const socialHtml = Object.entries(social).map(([platform, link]) => `<a href="${link}" title="${platform}">${platform[0].toUpperCase()}</a>`).join("");
      return `<footer class="site-footer"><div class="container"><div class="footer-grid"><div><h3>${props.hotelName || "Hotel"}</h3><p>${props.address || ""}</p><div class="footer-social">${socialHtml}</div></div><div><h3>Hizli Erisim</h3><p><a href="#anasayfa">Anasayfa</a></p><p><a href="#odalar">Odalar</a></p><p><a href="#galeri">Galeri</a></p><p><a href="#iletisim">Iletisim</a></p></div><div><h3>Iletisim</h3><p>${props.phone || ""}</p><p>${props.email || ""}</p></div></div><div class="footer-bottom"><p>&copy; 2025 ${props.hotelName || "Hotel"}. Tum haklari saklidir.</p><a href="https://syroce.com" class="syroce-brand" target="_blank">Powered by <span>Syroce</span></a></div></div></footer>`;
    }
    default:
      return "";
  }
}

const TRANSLATIONS = {
  tr: {
    home: "Anasayfa", about: "Hakkimizda", rooms: "Odalar", gallery: "Galeri",
    services: "Hizmetler", contact: "Iletisim", testimonials: "Yorumlar",
    your_name: "Adiniz Soyadiniz", your_email: "E-posta Adresiniz",
    subject: "Konu", message: "Mesajiniz", send: "Gonder",
    quick_links: "Hizli Erisim", contact_info: "Iletisim Bilgileri",
    all_rights: "Tum haklari saklidir", powered_by: "Powered by",
  },
  en: {
    home: "Home", about: "About", rooms: "Rooms", gallery: "Gallery",
    services: "Services", contact: "Contact", testimonials: "Testimonials",
    your_name: "Your Name", your_email: "Your Email",
    subject: "Subject", message: "Your Message", send: "Send",
    quick_links: "Quick Links", contact_info: "Contact Information",
    all_rights: "All rights reserved", powered_by: "Powered by",
  },
};

export function generatePreviewHTML(sections, theme, lang = "tr") {
  const t = TRANSLATIONS[lang] || TRANSLATIONS.tr;
  const hf = theme.headerFont || "Playfair Display";
  const bf = theme.bodyFont || "Lato";
  const fontFamilies = new Set();
  [hf, bf].forEach((font) => {
    const name = font.includes("'") ? font.split("'")[1] : font.split(",")[0].trim();
    if (name) fontFamilies.add(name);
  });
  const fontsUrl = `https://fonts.googleapis.com/css2?${[...fontFamilies].map((f) => `family=${f.replace(/ /g, "+")}:wght@400;500;600;700`).join("&")}&display=swap`;

  const visibleSections = (sections || []).filter((s) => s.visible !== false);
  const sectionsHtml = visibleSections.map((s) => renderSection(s, theme, t)).join("\n");
  const css = generateCSS(theme);

  return `<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="${fontsUrl}" rel="stylesheet">
  <style>${css}</style>
</head>
<body>
${sectionsHtml}
</body>
</html>`;
}
