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

const STYLE_OVERRIDES = {
  classic: (pc, sc, bg, tc, hf, bf) => "",
  minimal: (pc, sc, bg, tc, hf, bf) => `
    body{font-family:${bf}}
    h1,h2,h3,h4{font-family:${bf};font-weight:300;letter-spacing:-0.01em}
    .section{padding:140px 0;background:#fff}
    .section-title{text-align:left;font-size:clamp(1.5rem,2.4vw,2.2rem);font-weight:300;margin-bottom:8px;letter-spacing:-0.02em;border-bottom:1px solid #e5e5e5;padding-bottom:18px}
    .section-subtitle{text-align:left;font-size:0.95rem;letter-spacing:0.04em;text-transform:uppercase;opacity:0.5;margin-bottom:50px}
    .btn{background:transparent;color:${pc};border:1px solid ${pc};border-radius:0;padding:12px 32px;text-transform:uppercase;letter-spacing:0.15em;font-size:0.78rem;font-weight:500}
    .btn:hover{background:${pc};color:#fff;transform:none}
    .room-card,.service-card,.testimonial-card{box-shadow:none;border:1px solid #ececec;border-radius:0;background:#fff}
    .room-card:hover,.service-card:hover{transform:none;border-color:${pc}}
    .room-card img{height:280px}
    .site-header{padding:18px 0;background:#fff !important;border-bottom:1px solid #ececec}
    .site-header .logo{color:${sc};font-size:1.2rem;letter-spacing:0.2em;text-transform:uppercase;font-family:${bf};font-weight:400}
    .site-header nav a{color:${tc};text-transform:uppercase;letter-spacing:0.1em;font-size:0.8rem;font-weight:400}
    .hero{min-height:90vh}
    .hero-overlay{background:rgba(0,0,0,0.25)}
    .hero h1{font-weight:300;letter-spacing:-0.03em}
    .room-card-body{padding:30px 25px}
    .room-features span{background:transparent;border:1px solid ${pc}40;border-radius:0;font-size:0.7rem;text-transform:uppercase;letter-spacing:0.08em}
  `,
  "luxury-dark": (pc, sc, bg, tc, hf, bf) => `
    body{background:#0E0E10;color:#D4D4D8}
    h1,h2,h3,h4{color:#FAFAF5}
    .section{padding:130px 0;background:#0E0E10}
    .section:nth-of-type(even){background:#15151A}
    .section-title{color:#FAFAF5;font-size:clamp(2rem,4vw,3.6rem);font-weight:400;letter-spacing:0.02em}
    .section-title::after{content:"";display:block;width:60px;height:1px;background:${pc};margin:24px auto 0}
    .section-subtitle{color:#A1A1AA;letter-spacing:0.06em;font-size:0.95rem;text-transform:uppercase}
    .btn{background:transparent;color:${pc};border:1px solid ${pc};border-radius:0;padding:14px 44px;text-transform:uppercase;letter-spacing:0.2em;font-size:0.8rem;font-weight:500}
    .btn:hover{background:${pc};color:#0E0E10;transform:none}
    .site-header.solid,.site-header{background:rgba(14,14,16,0.85);backdrop-filter:blur(8px);border-bottom:1px solid rgba(255,255,255,0.08)}
    .site-header .logo{color:${pc};font-family:${hf};font-weight:400;letter-spacing:0.15em;font-size:1.4rem;text-transform:uppercase}
    .room-card,.service-card,.testimonial-card{background:#15151A;border:1px solid rgba(255,255,255,0.06);box-shadow:none;border-radius:0;color:#D4D4D8}
    .room-card:hover{transform:translateY(-3px);border-color:${pc}}
    .room-card h3,.service-card h3{color:#FAFAF5}
    .room-card p,.service-card p,.testimonial-card p{color:#A1A1AA}
    .room-price{color:${pc}}
    .room-features span{background:rgba(197,165,114,0.1);color:${pc};border-radius:0}
    .hero-overlay{background:linear-gradient(180deg,rgba(0,0,0,0.6),rgba(0,0,0,0.85))}
    .hero h1{font-weight:400;letter-spacing:0.04em}
    .hero h1::after{content:"";display:block;width:80px;height:1px;background:${pc};margin:30px auto}
    .gallery-grid{background:transparent}
    .contact-form input,.contact-form textarea{background:#15151A;border:1px solid rgba(255,255,255,0.1);color:#FAFAF5}
    .contact-form input::placeholder,.contact-form textarea::placeholder{color:#71717A}
  `,
  rustic: (pc, sc, bg, tc, hf, bf) => `
    body{background:${bg}}
    .section{padding:90px 0}
    .section:nth-of-type(even){background:rgba(0,0,0,0.02)}
    .section-title{font-style:italic;font-weight:400;color:${sc}}
    .section-title::before{content:"~ ";color:${pc};font-style:normal}
    .section-title::after{content:" ~";color:${pc};font-style:normal}
    .btn{border-radius:50px;padding:14px 38px;background:${pc};box-shadow:0 4px 12px ${pc}40;font-weight:600}
    .btn:hover{box-shadow:0 6px 18px ${pc}60;transform:translateY(-2px)}
    .room-card,.service-card,.testimonial-card{border-radius:20px;background:#FFFCF7;border:2px dashed ${pc}30;box-shadow:none}
    .room-card:hover{border-style:solid;border-color:${pc};transform:translateY(-3px)}
    .room-card img{border-radius:18px 18px 0 0}
    .room-features span{border-radius:50px;padding:5px 14px}
    .site-header.solid{background:${sc}}
    .site-header .logo{font-style:italic}
    .hero h1{font-style:italic;font-weight:400}
    .gallery-item{border-radius:16px}
    .service-card{padding:50px 30px}
    .contact-form input,.contact-form textarea{border-radius:50px;padding:14px 22px}
    .contact-form textarea{border-radius:20px}
  `,
  "bold-modern": (pc, sc, bg, tc, hf, bf) => `
    h1,h2,h3,h4{font-weight:800;letter-spacing:-0.03em;text-transform:none}
    .section{padding:100px 0}
    .section:nth-of-type(odd){background:${bg}}
    .section:nth-of-type(even){background:${pc}08}
    .section-title{font-size:clamp(2.2rem,5vw,4rem);text-align:left;font-weight:900;line-height:1;margin-bottom:20px;letter-spacing:-0.04em}
    .section-subtitle{text-align:left;font-size:1.1rem;font-weight:500;max-width:600px;margin-left:0;margin-bottom:60px}
    .btn{border-radius:0;padding:18px 48px;text-transform:uppercase;letter-spacing:0.06em;font-weight:800;font-size:0.95rem}
    .btn:hover{transform:translate(-2px,-2px);box-shadow:6px 6px 0 ${sc}}
    .room-card,.service-card{background:${sc};color:#fff;border-radius:0;box-shadow:none;border:none}
    .room-card h3,.service-card h3{color:#fff;font-weight:800}
    .room-card p,.service-card p{color:rgba(255,255,255,0.75)}
    .room-card:hover,.service-card:hover{transform:translate(-4px,-4px);box-shadow:8px 8px 0 ${pc}}
    .room-card img{border-radius:0}
    .room-price{color:${pc};font-size:1.8rem;font-weight:900}
    .room-features span{background:rgba(255,255,255,0.1);color:#fff;border-radius:0;border:1px solid rgba(255,255,255,0.2)}
    .testimonial-card{border-radius:0;border-left:6px solid ${pc};box-shadow:none;background:#fff}
    .gallery-item{border-radius:0}
    .site-header.solid{background:${sc}}
    .site-header .logo{font-weight:900;letter-spacing:-0.02em;text-transform:uppercase}
    .site-header nav a{font-weight:700;text-transform:uppercase;font-size:0.85rem;letter-spacing:0.08em}
    .hero h1{font-weight:900;letter-spacing:-0.04em;text-align:left}
    .hero p{text-align:left;font-weight:500}
    .hero-content{text-align:left;max-width:900px;margin:0;padding:40px 60px}
    .hero{justify-content:flex-start}
    .hero-overlay{background:rgba(0,0,0,0.35)}
    .contact-form input,.contact-form textarea{border-radius:0;border-width:2px;border-color:${sc}}
    .contact-form input:focus,.contact-form textarea:focus{border-color:${pc}}
  `,
  magazine: (pc, sc, bg, tc, hf, bf) => `
    body{font-family:${bf};font-size:1.05rem}
    .section{padding:110px 0}
    .section-title{text-align:left;font-style:italic;font-weight:400;font-size:clamp(2rem,3.2vw,3rem);position:relative;padding-top:30px;margin-bottom:10px}
    .section-title::before{content:"";position:absolute;top:0;left:0;width:50px;height:3px;background:${pc}}
    .section-subtitle{text-align:left;font-size:1.05rem;color:${tc};opacity:0.8;font-style:italic;margin-bottom:55px;max-width:680px;margin-left:0}
    .btn{background:transparent;color:${sc};border:none;border-bottom:2px solid ${sc};border-radius:0;padding:8px 0;font-weight:600;font-size:1rem;letter-spacing:0.04em}
    .btn::after{content:" →";transition:margin 0.2s}
    .btn:hover{transform:none;color:${pc};border-color:${pc}}
    .btn:hover::after{margin-left:6px}
    .room-card,.service-card,.testimonial-card{background:#fff;border:none;border-top:3px solid ${pc};border-radius:0;box-shadow:none;padding-top:0}
    .room-card{padding-top:0}
    .room-card:hover{transform:none;border-top-width:6px;margin-top:-3px}
    .room-card img{border-radius:0;height:230px}
    .room-card-body{padding:25px 0}
    .room-card h3{font-style:italic;font-weight:400}
    .testimonial-card{padding:30px 0;border-top:1px solid #e5e5e5}
    .testimonial-card p{font-style:italic;font-size:1.2rem;line-height:1.6;color:${sc}}
    .testimonial-card p::before{content:"\u201C";font-size:3rem;color:${pc};line-height:0;vertical-align:-0.5em;margin-right:6px}
    .site-header.solid{background:${sc}}
    .site-header .logo{font-style:italic;font-weight:400;letter-spacing:0;font-size:2rem}
    .hero h1{font-style:italic;font-weight:400}
    .hero h1::first-letter{color:${pc}}
    .hero-overlay{background:rgba(0,0,0,0.45)}
    .gallery-item{border-radius:0}
    .service-card{text-align:left;padding:30px 0}
    .service-icon{display:block;text-align:left}
    .room-features span{border-radius:0;background:transparent;border-bottom:1px solid ${pc};padding:2px 0;margin-right:12px}
  `,
};

function generateCSS(theme) {
  const pc = theme.primaryColor || "#C5A572";
  const sc = theme.secondaryColor || "#1A1A2E";
  const bg = theme.backgroundColor || "#FFFFFF";
  const tc = theme.textColor || "#333333";
  const hf = theme.headerFont || "'Playfair Display', serif";
  const bf = theme.bodyFont || "'Lato', sans-serif";
  const style = theme.style || "classic";
  const styleCSS = (STYLE_OVERRIDES[style] || STYLE_OVERRIDES.classic)(pc, sc, bg, tc, hf, bf);

  return `
    *{margin:0;padding:0;box-sizing:border-box}
    html{scroll-behavior:smooth;scroll-padding-top:90px}
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
    .booking-section{background:linear-gradient(135deg,${sc}05,${pc}08);padding:80px 0}
    .booking-form-container{max-width:900px;margin:0 auto;background:#fff;border-radius:16px;padding:40px;box-shadow:0 8px 40px rgba(0,0,0,0.1)}
    .booking-form{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:20px;margin-top:30px}
    .booking-field label{display:block;font-size:0.85rem;font-weight:600;margin-bottom:8px;color:${sc}}
    .booking-field input,.booking-field select{width:100%;padding:12px 16px;border:2px solid #eee;border-radius:8px;font-size:1rem;font-family:${bf};transition:border 0.2s}
    .booking-field input:focus,.booking-field select:focus{border-color:${pc};outline:none}
    .booking-submit{grid-column:1/-1;text-align:center;margin-top:10px}
    .booking-submit .btn{padding:16px 60px;font-size:1.1rem}
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
      .booking-form{grid-template-columns:1fr}
    }
    ${styleCSS}
  `;
}

function buildQuickLinks(sections, t) {
  const map = {
    hero: { href: "#anasayfa", label: t.home },
    rooms: { href: "#odalar", label: t.rooms },
    menu: { href: "#menu", label: t.menu || "Menu" },
    tours: { href: "#turlar", label: t.tours || "Tours" },
    gallery: { href: "#galeri", label: t.gallery },
    contact: { href: "#iletisim", label: t.contact },
  };
  const seen = new Set();
  const links = [];
  (sections || []).forEach((s) => {
    const entry = map[s.type];
    if (entry && !seen.has(s.type) && s.visible !== false) {
      seen.add(s.type);
      links.push(entry);
    }
  });
  if (links.length === 0) {
    return `<p><a href="#anasayfa">${t.home}</a></p>`;
  }
  return links.map((l) => `<p><a href="${l.href}">${l.label}</a></p>`).join("");
}

function renderSection(section, theme, t, allSections) {
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
    case "menu": {
      const items = props.items || [];
      const itemsHtml = items.map((item) => {
        const priceHtml = item.price ? `<div class="room-price">${item.price}</div>` : "";
        return `<div class="room-card"><img src="${item.image || ""}" alt="${item.name || ""}"><div class="room-card-body"><h3>${item.name || ""}</h3><p>${item.description || ""}</p>${priceHtml}</div></div>`;
      }).join("");
      const sub = props.subtitle ? `<p class="section-subtitle">${props.subtitle}</p>` : "";
      return `<section class="section" id="menu"><div class="container"><h2 class="section-title">${props.title || ""}</h2>${sub}<div class="rooms-grid">${itemsHtml}</div></div></section>`;
    }
    case "tours": {
      const tours = props.tours || [];
      const itemsHtml = tours.map((tour) => {
        const priceHtml = tour.price ? `<div class="room-price">${tour.price}</div>` : "";
        const features = tour.duration ? `<div class="room-features"><span>${tour.duration}</span></div>` : "";
        return `<div class="room-card"><img src="${tour.image || ""}" alt="${tour.name || ""}"><div class="room-card-body"><h3>${tour.name || ""}</h3><p>${tour.description || ""}</p>${priceHtml}${features}</div></div>`;
      }).join("");
      const sub = props.subtitle ? `<p class="section-subtitle">${props.subtitle}</p>` : "";
      return `<section class="section" id="turlar"><div class="container"><h2 class="section-title">${props.title || ""}</h2>${sub}<div class="rooms-grid">${itemsHtml}</div></div></section>`;
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
      const itemsHtml = testimonials.map((testimonial) => {
        const stars = STAR_SVG.repeat(testimonial.rating || 5);
        return `<div class="testimonial-card"><div class="testimonial-stars">${stars}</div><p>"${testimonial.text || ""}"</p><div class="testimonial-author">${testimonial.name || ""}</div></div>`;
      }).join("");
      return `<section class="section" style="background:#f8f8f8" id="yorumlar"><div class="container"><h2 class="section-title">${props.title || ""}</h2><div class="testimonials-grid">${itemsHtml}</div></div></section>`;
    }
    case "contact": {
      return `<section class="section" id="iletisim"><div class="container"><h2 class="section-title">${props.title || ""}</h2><div class="contact-grid"><div class="contact-info"><h3>${t.contact_info}</h3><div class="contact-item"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="${pc}" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg><span>${props.address || ""}</span></div><div class="contact-item"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="${pc}" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg><span>${props.phone || ""}</span></div><div class="contact-item"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="${pc}" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg><span>${props.email || ""}</span></div></div><div class="contact-form"><input type="text" placeholder="${t.your_name}"><input type="email" placeholder="${t.your_email}"><input type="text" placeholder="${t.subject}"><textarea placeholder="${t.message}"></textarea><button class="btn">${t.send}</button></div></div></div></section>`;
    }
    case "banner": {
      const ctaHtml = props.ctaText ? `<a href="${props.ctaLink || "#"}" class="btn">${props.ctaText}</a>` : "";
      return `<section class="cta-banner"><div class="hero-bg" style="background-image:url('${props.backgroundImage || ""}')"></div><div class="hero-overlay"></div><div class="hero-content"><h2>${props.title || ""}</h2><p>${props.subtitle || ""}</p>${ctaHtml}</div></section>`;
    }
    case "booking": {
      const title = props.title || t.booking_title;
      const subtitle = props.subtitle || t.booking_subtitle;
      const widgetCode = props.widgetCode || "";
      const roomTypes = props.roomTypes || [];
      const phone = props.phone || "";
      const email = props.email || "";

      if (widgetCode) {
        return `<section class="booking-section section" id="rezervasyon"><div class="container"><h2 class="section-title">${title}</h2><p class="section-subtitle">${subtitle}</p><div class="booking-form-container">${widgetCode}</div></div></section>`;
      }

      const roomOptions = roomTypes.length > 0
        ? roomTypes.map((r) => `<option value="${r}">${r}</option>`).join("")
        : `<option>${t.select_room}</option>`;

      let contactInfo = "";
      if (phone || email) {
        contactInfo = `<div style="text-align:center;margin-top:25px;padding-top:20px;border-top:1px solid #eee;color:#666;font-size:0.95rem">`;
        if (phone) contactInfo += `<span>${t.phone}: <strong>${phone}</strong></span>`;
        if (phone && email) contactInfo += ` &nbsp;|&nbsp; `;
        if (email) contactInfo += `<span>Email: <strong>${email}</strong></span>`;
        contactInfo += `</div>`;
      }

      return `<section class="booking-section section" id="rezervasyon"><div class="container"><h2 class="section-title">${title}</h2><p class="section-subtitle">${subtitle}</p><div class="booking-form-container"><form onsubmit="return false;"><div class="booking-form"><div class="booking-field"><label>${t.check_in}</label><input type="date" name="checkin"></div><div class="booking-field"><label>${t.check_out}</label><input type="date" name="checkout"></div><div class="booking-field"><label>${t.adults}</label><select name="adults"><option>1</option><option selected>2</option><option>3</option><option>4</option></select></div><div class="booking-field"><label>${t.children}</label><select name="children"><option selected>0</option><option>1</option><option>2</option><option>3</option></select></div><div class="booking-field"><label>${t.room_type}</label><select name="room_type">${roomOptions}</select></div><div class="booking-field"><label>${t.your_name}</label><input type="text" name="name" placeholder="${t.your_name}"></div><div class="booking-field"><label>${t.your_email}</label><input type="email" name="email" placeholder="${t.your_email}"></div><div class="booking-field"><label>${t.phone}</label><input type="tel" name="phone" placeholder="${t.phone}"></div><div class="booking-submit"><button type="submit" class="btn">${t.make_reservation}</button></div></div></form>${contactInfo}</div></div></section>`;
    }
    case "footer": {
      const social = props.socialLinks || {};
      const socialHtml = Object.entries(social).map(([platform, link]) => `<a href="${link}" title="${platform}">${platform[0].toUpperCase()}</a>`).join("");
      const quickLinksHtml = buildQuickLinks(allSections, t);
      return `<footer class="site-footer"><div class="container"><div class="footer-grid"><div><h3>${props.hotelName || "Hotel"}</h3><p>${props.address || ""}</p><div class="footer-social">${socialHtml}</div></div><div><h3>${t.quick_links}</h3>${quickLinksHtml}</div><div><h3>${t.contact}</h3><p>${props.phone || ""}</p><p>${props.email || ""}</p></div></div><div class="footer-bottom"><p>&copy; 2025 ${props.hotelName || "Hotel"}. ${t.all_rights}.</p><a href="https://syroce.com" class="syroce-brand" target="_blank">${t.powered_by} <span>Syroce</span></a></div></div></footer>`;
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
    check_in: "Giris Tarihi", check_out: "Cikis Tarihi",
    guests: "Misafir Sayisi", room_type: "Oda Tipi",
    booking_title: "Rezervasyon", booking_subtitle: "Tatilinizi simdi planlayin",
    select_room: "Oda Secin", adults: "Yetiskin", children: "Cocuk",
    make_reservation: "Rezervasyon Yap", phone: "Telefon",
  },
  en: {
    home: "Home", about: "About", rooms: "Rooms", gallery: "Gallery",
    services: "Services", contact: "Contact", testimonials: "Testimonials",
    your_name: "Your Name", your_email: "Your Email",
    subject: "Subject", message: "Your Message", send: "Send",
    quick_links: "Quick Links", contact_info: "Contact Information",
    all_rights: "All rights reserved", powered_by: "Powered by",
    check_in: "Check-in", check_out: "Check-out",
    guests: "Guests", room_type: "Room Type",
    booking_title: "Reservation", booking_subtitle: "Plan your stay today",
    select_room: "Select Room", adults: "Adults", children: "Children",
    make_reservation: "Make Reservation", phone: "Phone",
  },
  de: {
    home: "Startseite", about: "Uber uns", rooms: "Zimmer", gallery: "Galerie",
    services: "Dienstleistungen", contact: "Kontakt", testimonials: "Bewertungen",
    your_name: "Ihr Name", your_email: "Ihre E-Mail",
    subject: "Betreff", message: "Ihre Nachricht", send: "Senden",
    quick_links: "Schnellzugriff", contact_info: "Kontaktinformationen",
    all_rights: "Alle Rechte vorbehalten", powered_by: "Powered by",
    check_in: "Anreise", check_out: "Abreise",
    guests: "Gaste", room_type: "Zimmertyp",
    booking_title: "Reservierung", booking_subtitle: "Planen Sie Ihren Aufenthalt",
    select_room: "Zimmer wahlen", adults: "Erwachsene", children: "Kinder",
    make_reservation: "Reservierung vornehmen", phone: "Telefon",
  },
  fr: {
    home: "Accueil", about: "A propos", rooms: "Chambres", gallery: "Galerie",
    services: "Services", contact: "Contact", testimonials: "Temoignages",
    your_name: "Votre nom", your_email: "Votre e-mail",
    subject: "Sujet", message: "Votre message", send: "Envoyer",
    quick_links: "Liens rapides", contact_info: "Coordonnees",
    all_rights: "Tous droits reserves", powered_by: "Powered by",
    check_in: "Arrivee", check_out: "Depart",
    guests: "Voyageurs", room_type: "Type de chambre",
    booking_title: "Reservation", booking_subtitle: "Planifiez votre sejour",
    select_room: "Choisir la chambre", adults: "Adultes", children: "Enfants",
    make_reservation: "Reserver", phone: "Telephone",
  },
  es: {
    home: "Inicio", about: "Nosotros", rooms: "Habitaciones", gallery: "Galeria",
    services: "Servicios", contact: "Contacto", testimonials: "Opiniones",
    your_name: "Su nombre", your_email: "Su correo",
    subject: "Asunto", message: "Su mensaje", send: "Enviar",
    quick_links: "Enlaces rapidos", contact_info: "Informacion de contacto",
    all_rights: "Todos los derechos reservados", powered_by: "Powered by",
    check_in: "Llegada", check_out: "Salida",
    guests: "Huespedes", room_type: "Tipo de habitacion",
    booking_title: "Reserva", booking_subtitle: "Planifique su estancia",
    select_room: "Seleccionar habitacion", adults: "Adultos", children: "Ninos",
    make_reservation: "Hacer reserva", phone: "Telefono",
  },
  it: {
    home: "Home", about: "Chi siamo", rooms: "Camere", gallery: "Galleria",
    services: "Servizi", contact: "Contatti", testimonials: "Recensioni",
    your_name: "Nome", your_email: "Email",
    subject: "Oggetto", message: "Messaggio", send: "Invia",
    quick_links: "Link rapidi", contact_info: "Informazioni di contatto",
    all_rights: "Tutti i diritti riservati", powered_by: "Powered by",
    check_in: "Check-in", check_out: "Check-out",
    guests: "Ospiti", room_type: "Tipo di camera",
    booking_title: "Prenotazione", booking_subtitle: "Pianifica il tuo soggiorno",
    select_room: "Seleziona camera", adults: "Adulti", children: "Bambini",
    make_reservation: "Prenota", phone: "Telefono",
  },
  ru: {
    home: "Glavnaya", about: "O nas", rooms: "Nomera", gallery: "Galereya",
    services: "Uslugi", contact: "Kontakty", testimonials: "Otzyvy",
    your_name: "Vashe imya", your_email: "Vash email",
    subject: "Tema", message: "Soobshchenie", send: "Otpravit",
    quick_links: "Bystrye ssylki", contact_info: "Kontaktnaya informatsiya",
    all_rights: "Vse prava zashchishcheny", powered_by: "Powered by",
    check_in: "Zaseleniye", check_out: "Vyseleniye",
    guests: "Gosti", room_type: "Tip nomera",
    booking_title: "Bronirovaniye", booking_subtitle: "Zaplanirujte poezdku",
    select_room: "Vybrat nomer", adults: "Vzroslyye", children: "Deti",
    make_reservation: "Zabronirovat", phone: "Telefon",
  },
  ar: {
    home: "الرئيسية", about: "من نحن", rooms: "الغرف", gallery: "المعرض",
    services: "الخدمات", contact: "اتصل بنا", testimonials: "آراء الضيوف",
    your_name: "الاسم", your_email: "البريد الإلكتروني",
    subject: "الموضوع", message: "الرسالة", send: "إرسال",
    quick_links: "روابط سريعة", contact_info: "معلومات الاتصال",
    all_rights: "جميع الحقوق محفوظة", powered_by: "Powered by",
    check_in: "تسجيل الوصول", check_out: "تسجيل المغادرة",
    guests: "الضيوف", room_type: "نوع الغرفة",
    booking_title: "الحجز", booking_subtitle: "خطط لإقامتك الآن",
    select_room: "اختر الغرفة", adults: "بالغين", children: "أطفال",
    make_reservation: "إجراء الحجز", phone: "الهاتف",
  },
  ja: {
    home: "ホーム", about: "ホテルについて", rooms: "客室", gallery: "ギャラリー",
    services: "サービス", contact: "お問い合わせ", testimonials: "お客様の声",
    your_name: "お名前", your_email: "メールアドレス",
    subject: "件名", message: "メッセージ", send: "送信",
    quick_links: "クイックリンク", contact_info: "連絡先情報",
    all_rights: "全著作権所有", powered_by: "Powered by",
    check_in: "チェックイン", check_out: "チェックアウト",
    guests: "人数", room_type: "客室タイプ",
    booking_title: "ご予約", booking_subtitle: "ご滞在を計画しましょう",
    select_room: "客室を選択", adults: "大人", children: "お子様",
    make_reservation: "予約する", phone: "電話",
  },
  zh: {
    home: "首页", about: "关于我们", rooms: "客房", gallery: "画廊",
    services: "服务", contact: "联系我们", testimonials: "客户评价",
    your_name: "您的姓名", your_email: "您的邮箱",
    subject: "主题", message: "留言", send: "发送",
    quick_links: "快速链接", contact_info: "联系信息",
    all_rights: "版权所有", powered_by: "Powered by",
    check_in: "入住", check_out: "退房",
    guests: "客人", room_type: "房型",
    booking_title: "预订", booking_subtitle: "立即规划您的住宿",
    select_room: "选择客房", adults: "成人", children: "儿童",
    make_reservation: "立即预订", phone: "电话",
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
  const sectionsHtml = visibleSections.map((s) => renderSection(s, theme, t, visibleSections)).join("\n");
  const css = generateCSS(theme);

  return `<!DOCTYPE html>
<html lang="${lang}">
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
<script>
  document.addEventListener('click', function(e){
    var a = e.target.closest('a');
    if(!a) return;
    var href = a.getAttribute('href') || '';
    if(href.charAt(0) !== '#') return;
    e.preventDefault();
    if(href === '#' || href.length < 2){
      window.scrollTo({top:0, behavior:'smooth'});
      return;
    }
    var el = document.getElementById(href.slice(1));
    if(el) el.scrollIntoView({behavior:'smooth', block:'start'});
  });
  document.addEventListener('submit', function(e){
    if(e.target.tagName === 'FORM'){ e.preventDefault(); }
  });
</script>
</body>
</html>`;
}
