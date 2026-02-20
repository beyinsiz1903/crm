import io
import zipfile
from typing import Dict, Any, List

# ==================== TRANSLATIONS ====================
TRANSLATIONS = {
    "tr": {
        "home": "Anasayfa", "about": "Hakkimizda", "rooms": "Odalar",
        "gallery": "Galeri", "services": "Hizmetler", "contact": "Iletisim",
        "testimonials": "Yorumlar", "book_now": "Rezervasyon Yap",
        "send": "Gonder", "your_name": "Adiniz Soyadiniz",
        "your_email": "E-posta Adresiniz", "subject": "Konu",
        "message": "Mesajiniz", "quick_links": "Hizli Erisim",
        "contact_info": "Iletisim Bilgileri", "all_rights": "Tum haklari saklidir",
        "powered_by": "Powered by", "view_all_rooms": "Tum Odalari Gor",
        "view_gallery": "Galeriyi Gor", "our_services": "Hizmetlerimiz",
        "guest_reviews": "Misafir Yorumlari",
    },
    "en": {
        "home": "Home", "about": "About", "rooms": "Rooms",
        "gallery": "Gallery", "services": "Services", "contact": "Contact",
        "testimonials": "Testimonials", "book_now": "Book Now",
        "send": "Send", "your_name": "Your Name",
        "your_email": "Your Email", "subject": "Subject",
        "message": "Your Message", "quick_links": "Quick Links",
        "contact_info": "Contact Information", "all_rights": "All rights reserved",
        "powered_by": "Powered by", "view_all_rooms": "View All Rooms",
        "view_gallery": "View Gallery", "our_services": "Our Services",
        "guest_reviews": "Guest Reviews",
    },
}


def get_t(lang: str = "tr"):
    return TRANSLATIONS.get(lang, TRANSLATIONS["tr"])


def get_service_icon_svg(icon_name: str) -> str:
    icons = {
        "spa": '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 22c-4-3-8-6-8-10a8 8 0 0 1 16 0c0 4-4 7-8 10z"/></svg>',
        "restaurant": '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2"/><path d="M7 2v20"/><path d="M21 15V2v0a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3zm0 0v7"/></svg>',
        "pool": '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M2 20c2-1 4-1 6 0s4 1 6 0 4-1 6 0"/><path d="M2 17c2-1 4-1 6 0s4 1 6 0 4-1 6 0"/><circle cx="9" cy="6" r="2"/><path d="M9 8v4"/><path d="M6 12h6"/></svg>',
        "fitness": '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M6.5 6.5h11"/><path d="M6.5 17.5h11"/><path d="M4.5 9v6"/><path d="M2.5 10v4"/><path d="M19.5 9v6"/><path d="M21.5 10v4"/><path d="M12 6.5v11"/></svg>',
        "parking": '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="3" width="18" height="18" rx="3"/><path d="M9 17V7h4a3 3 0 0 1 0 6H9"/></svg>',
        "transfer": '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M5 17h14v-5H5z"/><path d="M2 12l3-5h14l3 5"/><circle cx="7.5" cy="17" r="2"/><circle cx="16.5" cy="17" r="2"/></svg>',
    }
    return icons.get(icon_name, icons["spa"])


def render_star_svg() -> str:
    return '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>'


def generate_css(theme: Dict[str, Any]) -> str:
    pc = theme.get("primaryColor", "#C5A572")
    sc = theme.get("secondaryColor", "#1A1A2E")
    bg = theme.get("backgroundColor", "#FFFFFF")
    tc = theme.get("textColor", "#333333")
    hf = theme.get("headerFont", "'Playfair Display', serif")
    bf = theme.get("bodyFont", "'Lato', sans-serif")
    return f"""
    *{{margin:0;padding:0;box-sizing:border-box}}
    html{{scroll-behavior:smooth}}
    body{{font-family:{bf};color:{tc};background:{bg};line-height:1.7}}
    h1,h2,h3,h4{{font-family:{hf};line-height:1.3}}
    img{{max-width:100%;height:auto}}
    a{{color:{pc};text-decoration:none}}
    .container{{max-width:1200px;margin:0 auto;padding:0 20px}}
    .site-header{{position:fixed;top:0;left:0;right:0;z-index:100;padding:20px 0;transition:background 0.3s}}
    .site-header.solid{{background:{sc}}}
    .site-header.transparent{{background:transparent}}
    .site-header .nav-inner{{display:flex;justify-content:space-between;align-items:center;max-width:1200px;margin:0 auto;padding:0 20px}}
    .site-header .logo{{font-family:{hf};font-size:1.8rem;color:#fff;font-weight:700}}
    .site-header nav a{{color:#fff;margin-left:25px;font-size:0.95rem;font-weight:500;transition:opacity 0.2s}}
    .site-header nav a:hover{{opacity:0.8}}
    .hero{{position:relative;min-height:100vh;display:flex;align-items:center;justify-content:center;text-align:center;color:#fff;overflow:hidden}}
    .hero-bg{{position:absolute;inset:0;background-size:cover;background-position:center}}
    .hero-overlay{{position:absolute;inset:0;background:rgba(0,0,0,0.5)}}
    .hero-content{{position:relative;z-index:2;max-width:800px;padding:40px 20px}}
    .hero h1{{font-size:clamp(2.5rem,5vw,4.5rem);margin-bottom:20px;font-weight:700}}
    .hero p{{font-size:clamp(1rem,2vw,1.4rem);margin-bottom:30px;opacity:0.9}}
    .btn{{display:inline-block;padding:14px 40px;background:{pc};color:#fff;border-radius:4px;font-weight:600;font-size:1rem;transition:all 0.3s;border:none;cursor:pointer}}
    .btn:hover{{opacity:0.9;transform:translateY(-2px)}}
    .section{{padding:100px 0}}
    .section-title{{font-size:clamp(1.8rem,3vw,2.8rem);text-align:center;margin-bottom:15px;color:{sc}}}
    .section-subtitle{{text-align:center;color:{tc};opacity:0.7;margin-bottom:60px;font-size:1.1rem}}
    .about-grid{{display:grid;grid-template-columns:1fr 1fr;gap:60px;align-items:center}}
    .about-grid img{{border-radius:12px;width:100%;height:400px;object-fit:cover}}
    .about-text h2{{font-size:2.2rem;margin-bottom:20px;color:{sc}}}
    .about-text p{{font-size:1.05rem;line-height:1.8}}
    .rooms-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:30px}}
    .room-card{{border-radius:12px;overflow:hidden;box-shadow:0 4px 20px rgba(0,0,0,0.08);transition:transform 0.3s;background:#fff}}
    .room-card:hover{{transform:translateY(-5px)}}
    .room-card img{{width:100%;height:250px;object-fit:cover}}
    .room-card-body{{padding:25px}}
    .room-card h3{{font-size:1.4rem;margin-bottom:10px;color:{sc}}}
    .room-card p{{font-size:0.95rem;opacity:0.8;margin-bottom:15px}}
    .room-price{{font-size:1.5rem;font-weight:700;color:{pc}}}
    .room-features{{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}}
    .room-features span{{background:{pc}15;color:{pc};padding:4px 12px;border-radius:20px;font-size:0.8rem}}
    .gallery-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:15px}}
    .gallery-grid.masonry{{grid-auto-rows:200px}}
    .gallery-grid.masonry .gallery-item:nth-child(1){{grid-row:span 2}}
    .gallery-grid.masonry .gallery-item:nth-child(4){{grid-row:span 2}}
    .gallery-item{{border-radius:8px;overflow:hidden}}
    .gallery-item img{{width:100%;height:100%;object-fit:cover;transition:transform 0.5s}}
    .gallery-item:hover img{{transform:scale(1.05)}}
    .services-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:30px}}
    .service-card{{text-align:center;padding:40px 25px;border-radius:12px;background:#fff;box-shadow:0 2px 15px rgba(0,0,0,0.05);transition:transform 0.3s}}
    .service-card:hover{{transform:translateY(-5px)}}
    .service-icon{{color:{pc};margin-bottom:20px;display:inline-block}}
    .service-card h3{{font-size:1.2rem;margin-bottom:10px;color:{sc}}}
    .service-card p{{font-size:0.95rem;opacity:0.7}}
    .testimonials-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:30px}}
    .testimonial-card{{padding:35px;border-radius:12px;background:#fff;box-shadow:0 2px 15px rgba(0,0,0,0.05)}}
    .testimonial-stars{{color:{pc};display:flex;gap:4px;margin-bottom:15px}}
    .testimonial-card p{{font-style:italic;font-size:1.05rem;line-height:1.7;margin-bottom:20px}}
    .testimonial-author{{font-weight:600;color:{sc}}}
    .contact-grid{{display:grid;grid-template-columns:1fr 1fr;gap:60px;align-items:start}}
    .contact-info h3{{font-size:1.3rem;margin-bottom:15px;color:{sc}}}
    .contact-item{{display:flex;align-items:center;gap:12px;margin-bottom:18px;font-size:1rem}}
    .contact-form input,.contact-form textarea{{width:100%;padding:14px 18px;border:1px solid #ddd;border-radius:8px;font-family:{bf};font-size:1rem;margin-bottom:15px;transition:border 0.2s}}
    .contact-form input:focus,.contact-form textarea:focus{{border-color:{pc};outline:none}}
    .contact-form textarea{{min-height:140px;resize:vertical}}
    .cta-banner{{position:relative;padding:80px 0;text-align:center;color:#fff;overflow:hidden}}
    .cta-banner .hero-bg{{position:absolute;inset:0;background-size:cover;background-position:center}}
    .cta-banner .hero-overlay{{position:absolute;inset:0;background:rgba(0,0,0,0.6)}}
    .cta-banner .hero-content{{position:relative;z-index:2}}
    .cta-banner h2{{font-size:2.5rem;margin-bottom:15px}}
    .cta-banner p{{font-size:1.2rem;margin-bottom:30px;opacity:0.9}}
    .site-footer{{background:{sc};color:#fff;padding:60px 0 30px}}
    .footer-grid{{display:grid;grid-template-columns:2fr 1fr 1fr;gap:40px;margin-bottom:40px}}
    .footer-grid h3{{font-size:1.3rem;margin-bottom:20px;font-family:{hf}}}
    .footer-grid p,.footer-grid a{{font-size:0.95rem;color:rgba(255,255,255,0.8)}}
    .footer-grid a:hover{{color:#fff}}
    .footer-social{{display:flex;gap:15px;margin-top:15px}}
    .footer-social a{{width:40px;height:40px;border-radius:50%;border:1px solid rgba(255,255,255,0.3);display:flex;align-items:center;justify-content:center;transition:all 0.3s}}
    .footer-social a:hover{{background:{pc};border-color:{pc}}}
    .footer-bottom{{border-top:1px solid rgba(255,255,255,0.15);padding-top:25px;display:flex;justify-content:space-between;align-items:center}}
    .footer-bottom p{{font-size:0.85rem;opacity:0.7}}
    .syroce-brand{{display:flex;align-items:center;gap:6px;font-size:0.85rem;opacity:0.7;color:#fff}}
    .syroce-brand:hover{{opacity:1}}
    .syroce-brand span{{font-weight:700;color:{pc}}}
    @media(max-width:768px){{
      .about-grid,.contact-grid{{grid-template-columns:1fr;gap:30px}}
      .footer-grid{{grid-template-columns:1fr}}
      .gallery-grid{{grid-template-columns:repeat(2,1fr)}}
      .site-header nav{{display:none}}
      .hero h1{{font-size:2.2rem}}
      .section{{padding:60px 0}}
    }}
    """


def render_header(props, theme, lang="tr", nav_links=None):
    hotel_name = props.get("hotelName", "Hotel")
    t = get_t(lang)
    if nav_links:
        menu_html = "".join([f'<a href="{link}">{label}</a>' for label, link in nav_links])
    else:
        menu_items = props.get("menuItems", [])
        menu_html = "".join([f'<a href="#{item.lower().replace(\" \", \"-\")}">{item}</a>' for item in menu_items])
    style = props.get("style", "transparent")
    return f'<header class="site-header {style}"><div class="nav-inner"><div class="logo">{hotel_name}</div><nav>{menu_html}</nav></div></header>'


def render_hero(props, theme, lang="tr"):
    title = props.get("title", "")
    subtitle = props.get("subtitle", "")
    bg = props.get("backgroundImage", "")
    cta_text = props.get("ctaText", "")
    cta_link = props.get("ctaLink", "#")
    opacity = props.get("overlayOpacity", "0.5")
    cta_html = f'<a href="{cta_link}" class="btn">{cta_text}</a>' if cta_text else ""
    return f'<section class="hero" id="anasayfa"><div class="hero-bg" style="background-image:url(\'{bg}\')"></div><div class="hero-overlay" style="opacity:{opacity}"></div><div class="hero-content"><h1>{title}</h1><p>{subtitle}</p>{cta_html}</div></section>'


def render_about(props, theme, lang="tr"):
    title = props.get("title", "")
    desc = props.get("description", "")
    image = props.get("image", "")
    layout = props.get("layout", "left-image")
    img_html = f'<img src="{image}" alt="{title}">' if image else ""
    text_html = f'<div class="about-text"><h2>{title}</h2><p>{desc}</p></div>'
    if layout == "right-image":
        inner = f'{text_html}<div>{img_html}</div>'
    else:
        inner = f'<div>{img_html}</div>{text_html}'
    return f'<section class="section" id="hakkimizda"><div class="container"><div class="about-grid">{inner}</div></div></section>'


def render_rooms(props, theme, lang="tr"):
    title = props.get("title", "")
    subtitle = props.get("subtitle", "")
    rooms = props.get("rooms", [])
    rooms_html = ""
    for room in rooms:
        features = room.get("features", [])
        features_html = "".join([f'<span>{f}</span>' for f in features])
        rooms_html += f'<div class="room-card"><img src="{room.get("image", "")}" alt="{room.get("name", "")}"><div class="room-card-body"><h3>{room.get("name", "")}</h3><p>{room.get("description", "")}</p><div class="room-price">{room.get("price", "")}</div><div class="room-features">{features_html}</div></div></div>'
    return f'<section class="section" id="odalar"><div class="container"><h2 class="section-title">{title}</h2><p class="section-subtitle">{subtitle}</p><div class="rooms-grid">{rooms_html}</div></div></section>'


def render_gallery(props, theme, lang="tr"):
    title = props.get("title", "")
    images = props.get("images", [])
    layout = props.get("layout", "grid")
    grid_class = "masonry" if layout == "masonry" else ""
    images_html = "".join([f'<div class="gallery-item"><img src="{img.get("url", "")}" alt="{img.get("alt", "")}"></div>' for img in images])
    return f'<section class="section" style="background:#f8f8f8" id="galeri"><div class="container"><h2 class="section-title">{title}</h2><div class="gallery-grid {grid_class}">{images_html}</div></div></section>'


def render_services(props, theme, lang="tr"):
    title = props.get("title", "")
    services = props.get("services", [])
    svc_html = ""
    for svc in services:
        icon_svg = get_service_icon_svg(svc.get("icon", "spa"))
        svc_html += f'<div class="service-card"><div class="service-icon">{icon_svg}</div><h3>{svc.get("name", "")}</h3><p>{svc.get("description", "")}</p></div>'
    return f'<section class="section" id="hizmetler"><div class="container"><h2 class="section-title">{title}</h2><div class="services-grid">{svc_html}</div></div></section>'


def render_testimonials(props, theme, lang="tr"):
    title = props.get("title", "")
    testimonials = props.get("testimonials", [])
    items_html = ""
    for t in testimonials:
        rating = t.get("rating", 5)
        stars = render_star_svg() * rating
        items_html += f'<div class="testimonial-card"><div class="testimonial-stars">{stars}</div><p>"{t.get("text", "")}"</p><div class="testimonial-author">{t.get("name", "")}</div></div>'
    return f'<section class="section" style="background:#f8f8f8" id="yorumlar"><div class="container"><h2 class="section-title">{title}</h2><div class="testimonials-grid">{items_html}</div></div></section>'


def render_contact(props, theme, lang="tr"):
    title = props.get("title", "")
    address = props.get("address", "")
    phone = props.get("phone", "")
    email = props.get("email", "")
    pc = theme.get("primaryColor", "#C5A572")
    t = get_t(lang)
    return f'<section class="section" id="iletisim"><div class="container"><h2 class="section-title">{title}</h2><div class="contact-grid"><div class="contact-info"><h3>{t["contact_info"]}</h3><div class="contact-item"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="{pc}" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg><span>{address}</span></div><div class="contact-item"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="{pc}" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg><span>{phone}</span></div><div class="contact-item"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="{pc}" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg><span>{email}</span></div></div><div class="contact-form"><input type="text" placeholder="{t["your_name"]}"><input type="email" placeholder="{t["your_email"]}"><input type="text" placeholder="{t["subject"]}"><textarea placeholder="{t["message"]}"></textarea><button class="btn">{t["send"]}</button></div></div></div></section>'


def render_banner(props, theme, lang="tr"):
    title = props.get("title", "")
    subtitle = props.get("subtitle", "")
    bg = props.get("backgroundImage", "")
    cta_text = props.get("ctaText", "")
    cta_link = props.get("ctaLink", "#")
    cta_html = f'<a href="{cta_link}" class="btn">{cta_text}</a>' if cta_text else ""
    return f'<section class="cta-banner"><div class="hero-bg" style="background-image:url(\'{bg}\')"></div><div class="hero-overlay"></div><div class="hero-content"><h2>{title}</h2><p>{subtitle}</p>{cta_html}</div></section>'


def render_footer(props, theme, lang="tr"):
    hotel_name = props.get("hotelName", "Hotel")
    address = props.get("address", "")
    phone = props.get("phone", "")
    email = props.get("email", "")
    social = props.get("socialLinks", {})
    t = get_t(lang)
    social_html = "".join([f'<a href="{link}" title="{p.capitalize()}">{p[0].upper()}</a>' for p, link in social.items()])
    return f'<footer class="site-footer"><div class="container"><div class="footer-grid"><div><h3>{hotel_name}</h3><p>{address}</p><div class="footer-social">{social_html}</div></div><div><h3>{t["quick_links"]}</h3><p><a href="#anasayfa">{t["home"]}</a></p><p><a href="#odalar">{t["rooms"]}</a></p><p><a href="#galeri">{t["gallery"]}</a></p><p><a href="#iletisim">{t["contact"]}</a></p></div><div><h3>{t["contact"]}</h3><p>{phone}</p><p>{email}</p></div></div><div class="footer-bottom"><p>&copy; 2025 {hotel_name}. {t["all_rights"]}.</p><a href="https://syroce.com" class="syroce-brand" target="_blank">{t["powered_by"]} <span>Syroce</span></a></div></div></footer>'


SECTION_RENDERERS = {
    "header": render_header,
    "hero": render_hero,
    "about": render_about,
    "rooms": render_rooms,
    "gallery": render_gallery,
    "services": render_services,
    "testimonials": render_testimonials,
    "contact": render_contact,
    "banner": render_banner,
    "footer": render_footer,
}


def _get_fonts_url(theme):
    hf = theme.get("headerFont", "Playfair Display")
    bf = theme.get("bodyFont", "Lato")
    font_families = set()
    for font in [hf, bf]:
        name = font.split("'")[1] if "'" in font else font.split(",")[0].strip()
        font_families.add(name)
    return "https://fonts.googleapis.com/css2?" + "&".join(
        [f"family={f.replace(' ', '+')}:wght@400;500;600;700" for f in font_families]
    ) + "&display=swap"


def _get_seo_meta(project_data):
    seo = project_data.get("seo", {})
    meta = ""
    if seo.get("description"):
        meta += f'<meta name="description" content="{seo["description"]}">\n'
    if seo.get("keywords"):
        meta += f'<meta name="keywords" content="{seo["keywords"]}">\n'
    if seo.get("og_image"):
        meta += f'<meta property="og:image" content="{seo["og_image"]}">\n'
    if seo.get("title"):
        meta += f'<meta property="og:title" content="{seo["title"]}">\n'
    if seo.get("description"):
        meta += f'<meta property="og:description" content="{seo["description"]}">\n'
    return meta


def generate_full_html(project_data: Dict[str, Any]) -> str:
    theme = project_data.get("theme", {})
    sections = project_data.get("sections", [])
    project_name = project_data.get("name", "Hotel Website")
    lang = project_data.get("language", "tr")
    seo = project_data.get("seo", {})
    page_title = seo.get("title") or project_name
    fonts_url = _get_fonts_url(theme)
    seo_meta = _get_seo_meta(project_data)

    sections_html = ""
    for section in sections:
        if section.get("visible", True):
            renderer = SECTION_RENDERERS.get(section.get("type"))
            if renderer:
                sections_html += renderer(section.get("props", {}), theme, lang)

    css = generate_css(theme)

    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title}</title>
    {seo_meta}
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="{fonts_url}" rel="stylesheet">
    <style>{css}</style>
</head>
<body>
{sections_html}
</body>
</html>"""


def _build_page_html(title, css, fonts_url, seo_meta, lang, header_html, body_sections, footer_html):
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    {seo_meta}
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="{fonts_url}" rel="stylesheet">
    <style>{css}</style>
</head>
<body>
{header_html}
{body_sections}
{footer_html}
</body>
</html>"""


def create_multipage_export_zip(project_data: Dict[str, Any]) -> bytes:
    theme = project_data.get("theme", {})
    sections = project_data.get("sections", [])
    project_name = project_data.get("name", "Hotel Website")
    lang = project_data.get("language", "tr")
    t = get_t(lang)
    seo = project_data.get("seo", {})
    page_title = seo.get("title") or project_name
    fonts_url = _get_fonts_url(theme)
    seo_meta = _get_seo_meta(project_data)
    css = generate_css(theme)
    folder = project_name.lower().replace(" ", "-")

    # Collect section data
    header_props = {}
    hero_props = {}
    about_props = {}
    rooms_props = {}
    gallery_props = {}
    services_props = {}
    testimonials_props = {}
    contact_props = {}
    footer_props = {}
    banners = []

    for s in sections:
        if not s.get("visible", True):
            continue
        st = s.get("type")
        p = s.get("props", {})
        if st == "header": header_props = p
        elif st == "hero": hero_props = p
        elif st == "about": about_props = p
        elif st == "rooms": rooms_props = p
        elif st == "gallery": gallery_props = p
        elif st == "services": services_props = p
        elif st == "testimonials": testimonials_props = p
        elif st == "contact": contact_props = p
        elif st == "footer": footer_props = p
        elif st == "banner": banners.append(p)

    # Multi-page navigation
    nav_links = [
        (t["home"], "index.html"),
        (t["about"], "index.html#hakkimizda"),
        (t["rooms"], "rooms.html"),
        (t["gallery"], "gallery.html"),
        (t["contact"], "contact.html"),
    ]
    header_html = render_header(header_props, theme, lang, nav_links=nav_links)
    footer_html = render_footer(footer_props, theme, lang)

    # Home page: hero + about + services + testimonials + banners
    home_body = render_hero(hero_props, theme, lang)
    home_body += render_about(about_props, theme, lang)
    home_body += render_services(services_props, theme, lang)
    home_body += render_testimonials(testimonials_props, theme, lang)
    for bp in banners:
        home_body += render_banner(bp, theme, lang)
    home_html = _build_page_html(page_title, css, fonts_url, seo_meta, lang, header_html, home_body, footer_html)

    # Rooms page
    rooms_body = f'<div style="padding-top:80px"></div>'
    rooms_body += render_rooms(rooms_props, theme, lang)
    rooms_html = _build_page_html(f"{t['rooms']} - {page_title}", css, fonts_url, seo_meta, lang, header_html, rooms_body, footer_html)

    # Gallery page
    gallery_body = f'<div style="padding-top:80px"></div>'
    gallery_body += render_gallery(gallery_props, theme, lang)
    gallery_html = _build_page_html(f"{t['gallery']} - {page_title}", css, fonts_url, seo_meta, lang, header_html, gallery_body, footer_html)

    # Contact page
    contact_body = f'<div style="padding-top:80px"></div>'
    contact_body += render_contact(contact_props, theme, lang)
    contact_html = _build_page_html(f"{t['contact']} - {page_title}", css, fonts_url, seo_meta, lang, header_html, contact_body, footer_html)

    # Create ZIP
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(f"{folder}/index.html", home_html)
        zf.writestr(f"{folder}/rooms.html", rooms_html)
        zf.writestr(f"{folder}/gallery.html", gallery_html)
        zf.writestr(f"{folder}/contact.html", contact_html)
        readme = f"""# {project_name}

## Pages
- index.html (Home)
- rooms.html (Rooms)
- gallery.html (Gallery)
- contact.html (Contact)

## Setup
1. Upload all files to your web server
2. Open index.html in your browser
3. Configure DNS settings for your domain

## Hosting Notes
{project_data.get('hosting_notes', 'No hosting info added yet.')}

## Domain Info
{project_data.get('domain_notes', 'No domain info added yet.')}

---
Powered by Syroce - https://syroce.com
"""
        zf.writestr(f"{folder}/README.md", readme)
    buffer.seek(0)
    return buffer.getvalue()


def create_export_zip(project_data: Dict[str, Any]) -> bytes:
    html_content = generate_full_html(project_data)
    project_name = project_data.get("name", "hotel-website").lower().replace(" ", "-")
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(f"{project_name}/index.html", html_content)
        readme = f"""# {project_data.get('name', 'Hotel Website')}

## Setup
1. Upload this folder to your web server
2. Open index.html in your browser
3. Configure DNS settings for your domain

## Hosting Notes
{project_data.get('hosting_notes', 'No hosting info added yet.')}

## Domain Info
{project_data.get('domain_notes', 'No domain info added yet.')}

---
Powered by Syroce - https://syroce.com
"""
        zf.writestr(f"{project_name}/README.md", readme)
    buffer.seek(0)
    return buffer.getvalue()
