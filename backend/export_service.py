import io
import os
import re
import zipfile
import httpx
import hashlib
import asyncio
from typing import Dict, Any, List, Tuple
from urllib.parse import urlparse
from html import escape, unescape
from site_safety import prepare_project, safe_url
from site_runtime import SITE_RUNTIME
from form_validation import field_key
from pathlib import Path
from urllib.parse import urljoin, urlsplit
from html.parser import HTMLParser
from asset_transport import image_client
from datetime import datetime, timezone

UPLOADS_DIR = Path(__file__).parent / 'uploads'

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
        "check_in": "Giris Tarihi", "check_out": "Cikis Tarihi",
        "guests": "Misafir Sayisi", "room_type": "Oda Tipi",
        "book_room": "Oda Rezervasyonu", "booking_title": "Rezervasyon",
        "booking_subtitle": "Tatilinizi simdi planlayin",
        "select_room": "Oda Secin", "adults": "Yetiskin", "children": "Cocuk",
        "make_reservation": "Rezervasyon Yap", "phone": "Telefon",
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
        "check_in": "Check-in", "check_out": "Check-out",
        "guests": "Guests", "room_type": "Room Type",
        "book_room": "Book a Room", "booking_title": "Reservation",
        "booking_subtitle": "Plan your stay today",
        "select_room": "Select Room", "adults": "Adults", "children": "Children",
        "make_reservation": "Make Reservation", "phone": "Phone",
    },
    "de": {
        "home": "Startseite", "about": "Uber uns", "rooms": "Zimmer",
        "gallery": "Galerie", "services": "Dienstleistungen", "contact": "Kontakt",
        "testimonials": "Bewertungen", "book_now": "Jetzt buchen",
        "send": "Senden", "your_name": "Ihr Name",
        "your_email": "Ihre E-Mail", "subject": "Betreff",
        "message": "Ihre Nachricht", "quick_links": "Schnellzugriff",
        "contact_info": "Kontaktinformationen", "all_rights": "Alle Rechte vorbehalten",
        "powered_by": "Powered by", "view_all_rooms": "Alle Zimmer ansehen",
        "view_gallery": "Galerie ansehen", "our_services": "Unsere Dienstleistungen",
        "guest_reviews": "Gastebewertungen",
        "check_in": "Anreise", "check_out": "Abreise",
        "guests": "Gaste", "room_type": "Zimmertyp",
        "book_room": "Zimmer buchen", "booking_title": "Reservierung",
        "booking_subtitle": "Planen Sie Ihren Aufenthalt",
        "select_room": "Zimmer wahlen", "adults": "Erwachsene", "children": "Kinder",
        "make_reservation": "Reservierung vornehmen", "phone": "Telefon",
    },
    "fr": {
        "home": "Accueil", "about": "A propos", "rooms": "Chambres",
        "gallery": "Galerie", "services": "Services", "contact": "Contact",
        "testimonials": "Temoignages", "book_now": "Reserver maintenant",
        "send": "Envoyer", "your_name": "Votre nom",
        "your_email": "Votre e-mail", "subject": "Sujet",
        "message": "Votre message", "quick_links": "Liens rapides",
        "contact_info": "Coordonnees", "all_rights": "Tous droits reserves",
        "powered_by": "Powered by", "view_all_rooms": "Voir toutes les chambres",
        "view_gallery": "Voir la galerie", "our_services": "Nos services",
        "guest_reviews": "Avis des clients",
        "check_in": "Arrivee", "check_out": "Depart",
        "guests": "Voyageurs", "room_type": "Type de chambre",
        "book_room": "Reserver une chambre", "booking_title": "Reservation",
        "booking_subtitle": "Planifiez votre sejour",
        "select_room": "Choisir la chambre", "adults": "Adultes", "children": "Enfants",
        "make_reservation": "Reserver", "phone": "Telephone",
    },
    "es": {
        "home": "Inicio", "about": "Nosotros", "rooms": "Habitaciones",
        "gallery": "Galeria", "services": "Servicios", "contact": "Contacto",
        "testimonials": "Opiniones", "book_now": "Reservar ahora",
        "send": "Enviar", "your_name": "Su nombre",
        "your_email": "Su correo", "subject": "Asunto",
        "message": "Su mensaje", "quick_links": "Enlaces rapidos",
        "contact_info": "Informacion de contacto", "all_rights": "Todos los derechos reservados",
        "powered_by": "Powered by", "view_all_rooms": "Ver todas las habitaciones",
        "view_gallery": "Ver galeria", "our_services": "Nuestros servicios",
        "guest_reviews": "Opiniones de huespedes",
        "check_in": "Llegada", "check_out": "Salida",
        "guests": "Huespedes", "room_type": "Tipo de habitacion",
        "book_room": "Reservar habitacion", "booking_title": "Reserva",
        "booking_subtitle": "Planifique su estancia",
        "select_room": "Seleccionar habitacion", "adults": "Adultos", "children": "Ninos",
        "make_reservation": "Hacer reserva", "phone": "Telefono",
    },
    "it": {
        "home": "Home", "about": "Chi siamo", "rooms": "Camere",
        "gallery": "Galleria", "services": "Servizi", "contact": "Contatti",
        "testimonials": "Recensioni", "book_now": "Prenota ora",
        "send": "Invia", "your_name": "Nome",
        "your_email": "Email", "subject": "Oggetto",
        "message": "Messaggio", "quick_links": "Link rapidi",
        "contact_info": "Informazioni di contatto", "all_rights": "Tutti i diritti riservati",
        "powered_by": "Powered by", "view_all_rooms": "Vedi tutte le camere",
        "view_gallery": "Vedi galleria", "our_services": "I nostri servizi",
        "guest_reviews": "Recensioni degli ospiti",
        "check_in": "Check-in", "check_out": "Check-out",
        "guests": "Ospiti", "room_type": "Tipo di camera",
        "book_room": "Prenota camera", "booking_title": "Prenotazione",
        "booking_subtitle": "Pianifica il tuo soggiorno",
        "select_room": "Seleziona camera", "adults": "Adulti", "children": "Bambini",
        "make_reservation": "Prenota", "phone": "Telefono",
    },
    "ru": {
        "home": "Glavnaya", "about": "O nas", "rooms": "Nomera",
        "gallery": "Galereya", "services": "Uslugi", "contact": "Kontakty",
        "testimonials": "Otzyvy", "book_now": "Zabronirovat",
        "send": "Otpravit", "your_name": "Vashe imya",
        "your_email": "Vash email", "subject": "Tema",
        "message": "Soobshchenie", "quick_links": "Bystrye ssylki",
        "contact_info": "Kontaktnaya informatsiya", "all_rights": "Vse prava zashchishcheny",
        "powered_by": "Powered by", "view_all_rooms": "Vse nomera",
        "view_gallery": "Galereya", "our_services": "Nashi uslugi",
        "guest_reviews": "Otzyvy gostey",
        "check_in": "Zaseleniye", "check_out": "Vyseleniye",
        "guests": "Gosti", "room_type": "Tip nomera",
        "book_room": "Zabronirovat nomer", "booking_title": "Bronirovaniye",
        "booking_subtitle": "Zaplanируйте поездку",
        "select_room": "Vybrat nomer", "adults": "Vzroslyye", "children": "Deti",
        "make_reservation": "Zabronirovat", "phone": "Telefon",
    },
    "ar": {
        "home": "الرئيسية", "about": "من نحن", "rooms": "الغرف",
        "gallery": "المعرض", "services": "الخدمات", "contact": "اتصل بنا",
        "testimonials": "آراء الضيوف", "book_now": "احجز الآن",
        "send": "إرسال", "your_name": "الاسم",
        "your_email": "البريد الإلكتروني", "subject": "الموضوع",
        "message": "الرسالة", "quick_links": "روابط سريعة",
        "contact_info": "معلومات الاتصال", "all_rights": "جميع الحقوق محفوظة",
        "powered_by": "Powered by", "view_all_rooms": "جميع الغرف",
        "view_gallery": "عرض المعرض", "our_services": "خدماتنا",
        "guest_reviews": "آراء الضيوف",
        "check_in": "تسجيل الوصول", "check_out": "تسجيل المغادرة",
        "guests": "الضيوف", "room_type": "نوع الغرفة",
        "book_room": "حجز غرفة", "booking_title": "الحجز",
        "booking_subtitle": "خطط لإقامتك الآن",
        "select_room": "اختر الغرفة", "adults": "بالغين", "children": "أطفال",
        "make_reservation": "إجراء الحجز", "phone": "الهاتف",
    },
    "ja": {
        "home": "ホーム", "about": "ホテルについて", "rooms": "客室",
        "gallery": "ギャラリー", "services": "サービス", "contact": "お問い合わせ",
        "testimonials": "お客様の声", "book_now": "予約する",
        "send": "送信", "your_name": "お名前",
        "your_email": "メールアドレス", "subject": "件名",
        "message": "メッセージ", "quick_links": "クイックリンク",
        "contact_info": "連絡先情報", "all_rights": "全著作権所有",
        "powered_by": "Powered by", "view_all_rooms": "全客室を見る",
        "view_gallery": "ギャラリーを見る", "our_services": "サービス一覧",
        "guest_reviews": "お客様の声",
        "check_in": "チェックイン", "check_out": "チェックアウト",
        "guests": "人数", "room_type": "客室タイプ",
        "book_room": "客室予約", "booking_title": "ご予約",
        "booking_subtitle": "ご滞在を計画しましょう",
        "select_room": "客室を選択", "adults": "大人", "children": "お子様",
        "make_reservation": "予約する", "phone": "電話",
    },
    "zh": {
        "home": "首页", "about": "关于我们", "rooms": "客房",
        "gallery": "画廊", "services": "服务", "contact": "联系我们",
        "testimonials": "客户评价", "book_now": "立即预订",
        "send": "发送", "your_name": "您的姓名",
        "your_email": "您的邮箱", "subject": "主题",
        "message": "留言", "quick_links": "快速链接",
        "contact_info": "联系信息", "all_rights": "版权所有",
        "powered_by": "Powered by", "view_all_rooms": "查看所有客房",
        "view_gallery": "查看画廊", "our_services": "我们的服务",
        "guest_reviews": "客户评价",
        "check_in": "入住", "check_out": "退房",
        "guests": "客人", "room_type": "房型",
        "book_room": "预订客房", "booking_title": "预订",
        "booking_subtitle": "立即规划您的住宿",
        "select_room": "选择客房", "adults": "成人", "children": "儿童",
        "make_reservation": "立即预订", "phone": "电话",
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


_STYLE_OVERRIDES_RAW = {
    "depth-3d": """
    body{background:__BG__;font-family:__BF__;perspective:1200px}
    .section{padding:110px 0;overflow:hidden}
    .section:nth-of-type(even){background:__SC__06}
    .section-title{font-weight:900;font-size:clamp(2rem,4.5vw,4rem);letter-spacing:-0.03em;color:__SC__;transform:perspective(600px) rotateX(4deg);transform-origin:left bottom;display:inline-block}
    .section-title::after{content:"";display:block;width:70px;height:5px;background:linear-gradient(90deg,__PC__,__PC__44);margin-top:14px}
    .section-subtitle{font-size:1.05rem;opacity:0.65;margin-bottom:56px}
    .btn{background:__PC__;color:#fff;border-radius:6px;padding:14px 44px;font-weight:700;letter-spacing:0.04em;transform:perspective(400px) translateZ(0);transition:transform 0.2s,box-shadow 0.2s,background 0.2s;border:none}
    .btn:hover{transform:perspective(400px) translateZ(12px) translateY(-3px);box-shadow:0 16px 40px __PC__60;background:__SC__}
    .rooms-grid,.services-grid,.testimonials-grid{perspective:1400px}
    .room-card,.service-card,.testimonial-card{transform:perspective(900px) rotateY(0deg) translateZ(0);transform-style:preserve-3d;transition:transform 0.4s cubic-bezier(0.23,1,0.32,1),box-shadow 0.4s;border-radius:12px;box-shadow:0 4px 16px rgba(0,0,0,0.1);background:#fff;border:none}
    .room-card:hover{transform:perspective(900px) rotateY(-6deg) translateZ(24px);box-shadow:-12px 24px 48px rgba(0,0,0,0.18)}
    .service-card:hover{transform:perspective(900px) rotateX(-6deg) translateZ(20px);box-shadow:0 24px 48px rgba(0,0,0,0.16)}
    .testimonial-card:hover{transform:perspective(900px) rotateY(4deg) translateZ(16px);box-shadow:8px 20px 40px rgba(0,0,0,0.14)}
    .room-card img{border-radius:10px 10px 0 0;transition:transform 0.4s}
    .room-card:hover img{transform:scale(1.04)}
    .room-price{color:__PC__;font-size:1.5rem;font-weight:900}
    .room-features span{background:__PC__15;color:__SC__;border-radius:6px;font-weight:500}
    .gallery-grid{perspective:1200px;display:grid}
    .gallery-item{transition:transform 0.4s,box-shadow 0.4s;border-radius:8px}
    .gallery-item:nth-child(odd){transform:perspective(800px) rotateY(-3deg)}
    .gallery-item:nth-child(even){transform:perspective(800px) rotateY(3deg)}
    .gallery-item:hover{transform:perspective(800px) rotateY(0deg) translateZ(20px) scale(1.06);box-shadow:0 20px 48px rgba(0,0,0,0.22);z-index:2;position:relative}
    .site-header.solid,.site-header{background:rgba(255,255,255,0.94);backdrop-filter:blur(12px);border-bottom:1px solid __PC__20;box-shadow:0 2px 20px rgba(0,0,0,0.08)}
    .site-header .logo{font-weight:900;letter-spacing:-0.01em;color:__SC__}
    .hero{min-height:95vh}
    .hero-content{text-shadow:0 4px 24px rgba(0,0,0,0.3)}
    .hero-overlay{background:linear-gradient(160deg,rgba(0,0,0,0.25),rgba(0,0,0,0.65))}
    .hero h1{font-weight:900;letter-spacing:-0.04em;transform:perspective(600px) rotateX(3deg);display:inline-block;text-shadow:0 8px 32px rgba(0,0,0,0.4)}
    .contact-form input,.contact-form textarea{border-radius:8px;transition:transform 0.2s,box-shadow 0.2s}
    .contact-form input:focus,.contact-form textarea:focus{transform:perspective(600px) translateZ(6px);box-shadow:0 8px 24px __PC__30;border-color:__PC__}
    """,
    "neon-cyber": """
    body{background:#07071a;color:#c8d6e5}
    h1,h2,h3,h4{color:#ffffff;text-shadow:0 0 20px __PC__80}
    .section{padding:120px 0;background:#07071a}
    .section:nth-of-type(even){background:#0d0d26}
    .section-title{color:#fff;font-size:clamp(2rem,4vw,3.5rem);text-shadow:0 0 30px __PC__;letter-spacing:0.05em}
    .section-title::after{content:"";display:block;width:80px;height:2px;background:linear-gradient(90deg,__PC__,transparent);margin:18px auto 0;box-shadow:0 0 10px __PC__}
    .section-subtitle{color:#8899aa;letter-spacing:0.06em;text-transform:uppercase;font-size:0.9rem}
    .btn{background:transparent;color:__PC__;border:1px solid __PC__;border-radius:4px;padding:13px 40px;letter-spacing:0.12em;text-transform:uppercase;font-size:0.85rem;box-shadow:0 0 12px __PC__40,inset 0 0 12px __PC__10}
    .btn:hover{background:__PC__20;box-shadow:0 0 24px __PC__80,inset 0 0 20px __PC__25;transform:none}
    .room-card,.service-card,.testimonial-card{background:#0d0d26;border:1px solid __PC__35;border-radius:8px;box-shadow:0 0 20px __PC__08;color:#c8d6e5}
    .room-card:hover{border-color:__PC__;box-shadow:0 0 32px __PC__45;transform:translateY(-4px)}
    .room-card h3,.service-card h3{color:#fff;text-shadow:0 0 10px __PC__50}
    .room-price{color:__PC__;text-shadow:0 0 10px __PC__;font-size:1.6rem;font-weight:800}
    .room-card p,.service-card p{color:#8899aa}
    .room-features span{background:__PC__15;color:__PC__;border:1px solid __PC__40;border-radius:4px}
    .site-header.solid,.site-header{background:rgba(7,7,26,0.92);backdrop-filter:blur(12px);border-bottom:1px solid __PC__30}
    .site-header .logo{color:__PC__;letter-spacing:0.18em;text-transform:uppercase;text-shadow:0 0 14px __PC__}
    .site-header nav a{color:#c8d6e5;text-transform:uppercase;letter-spacing:0.1em;font-size:0.8rem}
    .hero{min-height:100vh}
    .hero-overlay{background:linear-gradient(135deg,rgba(7,7,26,0.88),rgba(7,7,26,0.5))}
    .hero h1{text-shadow:0 0 40px __PC__60;letter-spacing:0.05em}
    .hero h1::after{content:"";display:block;width:100px;height:2px;background:linear-gradient(90deg,__PC__,transparent);margin:28px auto;box-shadow:0 0 12px __PC__}
    .gallery-item{border-radius:6px;border:1px solid __PC__20}
    .gallery-item:hover{border-color:__PC__;box-shadow:0 0 20px __PC__40}
    .contact-form input,.contact-form textarea{background:#0d0d26;border:1px solid __PC__40;color:#fff;border-radius:4px}
    .contact-form input:focus,.contact-form textarea:focus{border-color:__PC__;box-shadow:0 0 10px __PC__40}
    .contact-form input::placeholder,.contact-form textarea::placeholder{color:#445566}
    """,
    "glassmorphism": """
    body{background:__BG__;min-height:100vh}
    .section{padding:120px 0}
    .section:nth-of-type(even){background:__PC__06}
    .section-title{font-weight:300;letter-spacing:0.02em;color:__SC__}
    .section-subtitle{opacity:0.65;font-size:1rem}
    .btn{background:rgba(255,255,255,0.12);color:__SC__;border:1px solid rgba(255,255,255,0.35);border-radius:50px;padding:13px 38px;backdrop-filter:blur(6px);font-weight:600;letter-spacing:0.04em}
    .btn:hover{background:__PC__;color:#fff;border-color:__PC__;transform:translateY(-2px);box-shadow:0 8px 24px __PC__50}
    .room-card,.service-card,.testimonial-card{background:rgba(255,255,255,0.68);backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px);border:1px solid rgba(255,255,255,0.55);border-radius:22px;box-shadow:0 8px 32px rgba(0,0,0,0.08)}
    .room-card:hover{background:rgba(255,255,255,0.85);transform:translateY(-8px);box-shadow:0 24px 48px rgba(0,0,0,0.14)}
    .room-card img{border-radius:18px 18px 0 0}
    .room-card-body{padding:26px 24px}
    .room-price{color:__PC__;font-weight:800;font-size:1.5rem}
    .room-features span{background:__PC__18;border-radius:50px;border:none;color:__SC__;font-weight:500}
    .service-card{text-align:center;padding:44px 30px}
    .service-icon{color:__PC__}
    .testimonial-card{padding:36px}
    .site-header.solid,.site-header{background:rgba(255,255,255,0.72);backdrop-filter:blur(24px);-webkit-backdrop-filter:blur(24px);border-bottom:1px solid rgba(255,255,255,0.55);box-shadow:0 2px 20px rgba(0,0,0,0.07)}
    .site-header .logo{color:__SC__;font-weight:600}
    .hero{min-height:95vh}
    .hero-overlay{background:linear-gradient(180deg,rgba(0,0,0,0.15),rgba(0,0,0,0.55))}
    .hero-content{background:rgba(255,255,255,0.12);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);border:1px solid rgba(255,255,255,0.28);border-radius:28px;padding:54px 66px;max-width:760px}
    .hero h1{font-weight:300;letter-spacing:-0.02em}
    .gallery-item{border-radius:16px;box-shadow:0 4px 20px rgba(0,0,0,0.1)}
    .gallery-item:hover{transform:scale(1.04);box-shadow:0 12px 32px rgba(0,0,0,0.18)}
    .contact-form input,.contact-form textarea{background:rgba(255,255,255,0.7);backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,0.5);border-radius:14px}
    """,
    "geometric": """
    h1,h2,h3,h4{font-weight:900;letter-spacing:-0.02em}
    .section{padding:120px 0;position:relative;overflow:hidden}
    .section:nth-of-type(even){background:__SC__;color:#fff}
    .section:nth-of-type(even) .section-title,.section:nth-of-type(even) h3{color:#fff}
    .section:nth-of-type(even) .section-subtitle{color:rgba(255,255,255,0.65)}
    .section::before{content:"";position:absolute;top:-70px;right:-70px;width:200px;height:200px;background:__PC__18;transform:rotate(45deg);pointer-events:none}
    .section::after{content:"";position:absolute;bottom:-50px;left:-50px;width:140px;height:140px;background:__PC__10;transform:rotate(20deg);pointer-events:none}
    .section-title{text-align:left;font-size:clamp(2rem,4.5vw,3.8rem);text-transform:uppercase;letter-spacing:-0.02em;line-height:1}
    .section-title::before{content:"";display:block;width:44px;height:6px;background:__PC__;margin-bottom:18px}
    .section-subtitle{text-align:left;font-size:1rem;max-width:560px;margin-left:0;margin-bottom:56px}
    .btn{background:__PC__;color:#fff;clip-path:polygon(0 0,calc(100% - 14px) 0,100% 14px,100% 100%,0 100%);border-radius:0;padding:15px 46px;font-weight:800;text-transform:uppercase;letter-spacing:0.08em}
    .btn:hover{background:__SC__;transform:none;clip-path:polygon(0 0,calc(100% - 14px) 0,100% 14px,100% 100%,14px 100%,0 calc(100% - 14px))}
    .room-card,.service-card{background:#fff;border:none;clip-path:polygon(0 0,calc(100% - 18px) 0,100% 18px,100% 100%,0 100%);border-radius:0;box-shadow:none;border-bottom:4px solid __PC__}
    .room-card:hover,.service-card:hover{transform:none;border-bottom-color:__SC__;box-shadow:6px 6px 0 __PC__40}
    .room-card img{border-radius:0;clip-path:polygon(0 0,calc(100% - 18px) 0,100% 18px,100% 100%,0 100%)}
    .room-price{color:__PC__;font-size:1.7rem;font-weight:900}
    .room-features span{background:__PC__;color:#fff;border-radius:0;font-weight:700;font-size:0.68rem;text-transform:uppercase;letter-spacing:0.06em}
    .testimonial-card{background:__PC__10;border-left:6px solid __PC__;clip-path:none;border-radius:0;box-shadow:none}
    .gallery-item{border-radius:0;clip-path:polygon(0 0,calc(100% - 12px) 0,100% 12px,100% 100%,0 100%)}
    .gallery-item:hover{clip-path:none}
    .site-header.solid{background:__SC__}
    .site-header nav a{font-weight:700;text-transform:uppercase;letter-spacing:0.1em;font-size:0.8rem}
    .hero{clip-path:polygon(0 0,100% 0,100% 90%,0 100%);min-height:95vh}
    .hero-overlay{background:linear-gradient(135deg,__SC__dd,__PC__88)}
    .hero h1{font-weight:900;text-transform:uppercase;letter-spacing:-0.03em;text-align:left}
    .hero p{text-align:left}
    .hero-content{text-align:left;max-width:800px;margin:0;padding:40px 60px}
    .hero{justify-content:flex-start}
    .contact-form input,.contact-form textarea{border-radius:0;border:2px solid __SC__}
    """,
    "full-photo": """
    body{font-family:__BF__;background:__BG__}
    .section{padding:100px 0}
    .section-title{font-size:clamp(2.5rem,5.5vw,5rem);font-weight:200;letter-spacing:-0.04em;line-height:0.95;color:__SC__}
    .section-title::after{content:"";display:block;width:50px;height:3px;background:__PC__;margin:22px 0 0}
    .section-subtitle{font-size:1.15rem;opacity:0.6;font-weight:300;max-width:560px;margin-bottom:52px}
    .btn{background:__PC__;color:#fff;border-radius:50px;padding:16px 52px;font-weight:700;letter-spacing:0.04em;font-size:1.05rem;border:none}
    .btn:hover{background:__SC__;transform:scale(1.04);box-shadow:0 12px 32px __PC__50}
    .room-card,.service-card{background:transparent;border:none;box-shadow:none;border-radius:0;overflow:visible}
    .room-card:hover{transform:none}
    .room-card img{border-radius:14px;height:300px;object-fit:cover;box-shadow:0 16px 48px rgba(0,0,0,0.18);transition:transform 0.4s,box-shadow 0.4s}
    .room-card:hover img{transform:scale(1.03) translateY(-4px);box-shadow:0 28px 60px rgba(0,0,0,0.26)}
    .room-card-body{padding:22px 4px}
    .room-card h3{font-size:1.3rem;font-weight:700;color:__SC__}
    .room-price{color:__PC__;font-size:1.6rem;font-weight:900}
    .room-card p{opacity:0.6;font-size:0.92rem}
    .room-features span{background:transparent;color:__TC__;border:none;padding:0 8px 0 0;font-size:0.78rem;opacity:0.55}
    .room-features span::before{content:"\\2022 ";color:__PC__}
    .room-card-actions{padding:0 4px 18px}
    .service-card{text-align:center;padding:24px 16px}
    .service-icon{color:__PC__;margin-bottom:18px}
    .testimonial-card{background:transparent;border:none;box-shadow:none;border-top:1px solid __PC__30;padding:44px 0;border-radius:0}
    .testimonial-card p{font-size:1.5rem;font-style:italic;line-height:1.55;color:__SC__;font-weight:300}
    .testimonial-card p::before{content:"\\201C";font-size:5rem;color:__PC__;line-height:0;vertical-align:-0.55em;margin-right:6px;font-family:Georgia,serif}
    .site-header{padding:22px 0}
    .site-header.solid{background:rgba(255,255,255,0.94);backdrop-filter:blur(16px)}
    .hero{min-height:100vh}
    .hero-overlay{background:linear-gradient(to bottom,rgba(0,0,0,0.05) 0%,rgba(0,0,0,0.7) 100%)}
    .hero h1{font-size:clamp(3.5rem,9vw,8rem);font-weight:200;letter-spacing:-0.06em;line-height:0.92}
    .hero p{font-size:1.25rem;font-weight:300;opacity:0.9;max-width:680px}
    .gallery-item{border-radius:10px;box-shadow:0 8px 24px rgba(0,0,0,0.14)}
    .gallery-item:hover{transform:scale(1.04);box-shadow:0 20px 48px rgba(0,0,0,0.22)}
    """,
    "mosaic": """
    body{background:__BG__;font-family:__BF__}
    .section{padding:100px 0}
    .section:nth-of-type(even){background:__SC__06}
    .section-title{font-weight:900;font-size:clamp(2rem,4.5vw,3.8rem);text-transform:uppercase;letter-spacing:-0.03em;text-align:left;line-height:1}
    .section-title::after{content:"";display:block;width:90px;height:4px;background:__PC__;margin-top:16px}
    .section-subtitle{text-align:left;margin-left:0;font-size:1rem;opacity:0.65;margin-bottom:56px}
    .btn{background:__PC__;color:#fff;border-radius:4px;padding:14px 42px;font-weight:700;text-transform:uppercase;letter-spacing:0.06em}
    .btn:hover{background:__SC__;transform:none}
    .rooms-grid{display:grid !important;grid-template-columns:repeat(3,1fr) !important;grid-auto-rows:260px !important;gap:5px !important}
    .room-card{border-radius:0;box-shadow:none;border:none;overflow:hidden;position:relative !important;transform:none !important}
    .room-card:nth-child(4n+1){grid-column:span 2 !important}
    .room-card img{width:100% !important;height:100% !important;object-fit:cover;transition:transform 0.5s;border-radius:0}
    .room-card:hover img{transform:scale(1.09)}
    .room-card:hover{transform:none !important}
    .room-card-body{position:absolute !important;bottom:0;left:0;right:0;background:linear-gradient(transparent,rgba(0,0,0,0.88)) !important;color:#fff;padding:14px 18px 18px;border:none !important}
    .room-card h3{color:#fff !important;font-weight:800;font-size:1.05rem}
    .room-price{color:__PC__ !important;font-size:1.2rem;font-weight:900}
    .room-card p{display:none !important}
    .room-features{display:none !important}
    .room-card-actions{padding:0 !important}
    .room-card-actions .btn{padding:6px 14px !important;font-size:0.75rem !important;border-radius:3px !important}
    .gallery-grid{display:grid !important;grid-template-columns:repeat(4,1fr) !important;grid-auto-rows:170px !important;gap:4px !important}
    .gallery-item:nth-child(5n+1){grid-column:span 2 !important;grid-row:span 2 !important}
    .gallery-item{border-radius:0}
    .service-card{background:#fff;border:none;border-radius:0;box-shadow:none;border-bottom:4px solid __PC__;padding:30px 22px}
    .service-card:hover{transform:none;border-bottom-color:__SC__}
    .testimonial-card{background:__PC__09;border:none;box-shadow:none;border-radius:0;border-left:5px solid __PC__;padding:28px 30px}
    .testimonial-card p{font-style:italic;color:__SC__;font-size:1.05rem}
    .site-header.solid{background:__BG__;border-bottom:3px solid __PC__}
    .hero-overlay{background:rgba(0,0,0,0.38)}
    .hero h1{font-weight:900;letter-spacing:-0.04em;text-transform:uppercase}
    """,
    "retro-film": """
    body{background:#f5ede0;font-family:__BF__;color:#3d2b1f}
    h1,h2,h3,h4{color:#3d2b1f;font-family:__HF__}
    .section{padding:100px 0;background:#f5ede0;border-bottom:1px solid #d4b896}
    .section:nth-of-type(even){background:#ede0d0}
    .section-title{text-align:center;color:#3d2b1f;font-size:clamp(1.8rem,3.5vw,3rem);letter-spacing:0.1em;text-transform:uppercase;font-weight:700}
    .section-title::before,.section-title::after{content:"\\2736";margin:0 14px;color:__PC__;font-size:0.65em;vertical-align:middle}
    .section-subtitle{text-align:center;font-style:italic;color:#6b4c36;opacity:0.85;font-size:1rem;margin-bottom:56px}
    .btn{background:transparent;color:#3d2b1f;border:2px solid #3d2b1f;border-radius:0;padding:12px 36px;text-transform:uppercase;letter-spacing:0.18em;font-size:0.78rem;font-weight:700}
    .btn:hover{background:#3d2b1f;color:#f5ede0;transform:none}
    .room-card,.service-card{background:#fffaf3;border:1px solid #d4b896;border-radius:0;box-shadow:4px 4px 0 __PC__50;overflow:hidden}
    .room-card:hover{transform:translate(-3px,-3px);box-shadow:7px 7px 0 __PC__70}
    .room-card img{filter:sepia(28%) contrast(1.06) brightness(0.98);border-radius:0}
    .room-card-body{border-top:2px dashed __PC__60;padding:20px}
    .room-price{color:#3d2b1f;font-size:1.4rem;font-weight:700;font-family:__HF__}
    .room-features span{background:transparent;border-bottom:1px solid __PC__;border-radius:0;font-size:0.7rem;text-transform:uppercase;letter-spacing:0.08em;color:#6b4c36;padding:2px 4px}
    .testimonial-card{background:#fffaf3;border:1px solid #d4b896;box-shadow:3px 3px 0 __PC__40;border-radius:0;padding:30px}
    .testimonial-card p{font-style:italic;color:#3d2b1f;font-size:1.1rem;line-height:1.7}
    .testimonial-card p::before{content:"\\201C";font-size:3rem;color:__PC__;line-height:0;vertical-align:-0.45em;margin-right:6px}
    .site-header.solid,.site-header{background:#f5ede0;border-bottom:3px double #3d2b1f}
    .site-header .logo{color:#3d2b1f;letter-spacing:0.14em;text-transform:uppercase;font-weight:700}
    .site-header nav a{color:#3d2b1f;letter-spacing:0.08em;text-transform:uppercase;font-size:0.8rem}
    .hero h1{letter-spacing:0.1em;text-transform:uppercase;text-shadow:3px 3px 0 __PC__70}
    .hero-overlay{background:rgba(40,20,5,0.42)}
    .gallery-item{filter:sepia(22%) contrast(1.08);border:2px solid #d4b896}
    .gallery-item:hover{filter:sepia(0%) contrast(1.1);transform:scale(1.04)}
    .contact-form input,.contact-form textarea{border-radius:0;background:#fffaf3;border-color:#d4b896;font-family:__BF__;color:#3d2b1f}
    .contact-form input:focus,.contact-form textarea:focus{border-color:__PC__;box-shadow:none}
    """,
    "classic": "",
    "minimal": """
    body{font-family:__BF__}
    h1,h2,h3,h4{font-family:__BF__;font-weight:300;letter-spacing:-0.01em}
    .section{padding:140px 0;background:#fff}
    .section-title{text-align:left;font-size:clamp(1.5rem,2.4vw,2.2rem);font-weight:300;margin-bottom:8px;letter-spacing:-0.02em;border-bottom:1px solid #e5e5e5;padding-bottom:18px}
    .section-subtitle{text-align:left;font-size:0.95rem;letter-spacing:0.04em;text-transform:uppercase;opacity:0.5;margin-bottom:50px}
    .btn{background:transparent;color:__PC__;border:1px solid __PC__;border-radius:0;padding:12px 32px;text-transform:uppercase;letter-spacing:0.15em;font-size:0.78rem;font-weight:500}
    .btn:hover{background:__PC__;color:#fff;transform:none}
    .room-card,.service-card,.testimonial-card{box-shadow:none;border:1px solid #ececec;border-radius:0;background:#fff}
    .room-card:hover,.service-card:hover{transform:none;border-color:__PC__}
    .room-card img{height:280px}
    .site-header{padding:18px 0;background:#fff !important;border-bottom:1px solid #ececec}
    .site-header .logo{color:__SC__;font-size:1.2rem;letter-spacing:0.2em;text-transform:uppercase;font-family:__BF__;font-weight:400}
    .site-header nav a{color:__TC__;text-transform:uppercase;letter-spacing:0.1em;font-size:0.8rem;font-weight:400}
    .hero{min-height:90vh}
    .hero-overlay{background:rgba(0,0,0,0.25)}
    .hero h1{font-weight:300;letter-spacing:-0.03em}
    .room-card-body{padding:30px 25px}
    .room-features span{background:transparent;border:1px solid __PC__40;border-radius:0;font-size:0.7rem;text-transform:uppercase;letter-spacing:0.08em}
    """,
    "luxury-dark": """
    body{background:#0E0E10;color:#D4D4D8}
    h1,h2,h3,h4{color:#FAFAF5}
    .section{padding:130px 0;background:#0E0E10}
    .section:nth-of-type(even){background:#15151A}
    .section-title{color:#FAFAF5;font-size:clamp(2rem,4vw,3.6rem);font-weight:400;letter-spacing:0.02em}
    .section-title::after{content:"";display:block;width:60px;height:1px;background:__PC__;margin:24px auto 0}
    .section-subtitle{color:#A1A1AA;letter-spacing:0.06em;font-size:0.95rem;text-transform:uppercase}
    .btn{background:transparent;color:__PC__;border:1px solid __PC__;border-radius:0;padding:14px 44px;text-transform:uppercase;letter-spacing:0.2em;font-size:0.8rem;font-weight:500}
    .btn:hover{background:__PC__;color:#0E0E10;transform:none}
    .site-header.solid,.site-header{background:rgba(14,14,16,0.85);backdrop-filter:blur(8px);border-bottom:1px solid rgba(255,255,255,0.08)}
    .site-header .logo{color:__PC__;font-family:__HF__;font-weight:400;letter-spacing:0.15em;font-size:1.4rem;text-transform:uppercase}
    .room-card,.service-card,.testimonial-card{background:#15151A;border:1px solid rgba(255,255,255,0.06);box-shadow:none;border-radius:0;color:#D4D4D8}
    .room-card:hover{transform:translateY(-3px);border-color:__PC__}
    .room-card h3,.service-card h3{color:#FAFAF5}
    .room-card p,.service-card p,.testimonial-card p{color:#A1A1AA}
    .room-price{color:__PC__}
    .room-features span{background:rgba(197,165,114,0.1);color:__PC__;border-radius:0}
    .hero-overlay{background:linear-gradient(180deg,rgba(0,0,0,0.6),rgba(0,0,0,0.85))}
    .hero h1{font-weight:400;letter-spacing:0.04em}
    .hero h1::after{content:"";display:block;width:80px;height:1px;background:__PC__;margin:30px auto}
    .gallery-grid{background:transparent}
    .contact-form input,.contact-form textarea{background:#15151A;border:1px solid rgba(255,255,255,0.1);color:#FAFAF5}
    .contact-form input::placeholder,.contact-form textarea::placeholder{color:#71717A}
    """,
    "rustic": """
    body{background:__BG__}
    .section{padding:90px 0}
    .section:nth-of-type(even){background:rgba(0,0,0,0.02)}
    .section-title{font-style:italic;font-weight:400;color:__SC__}
    .section-title::before{content:"~ ";color:__PC__;font-style:normal}
    .section-title::after{content:" ~";color:__PC__;font-style:normal}
    .btn{border-radius:50px;padding:14px 38px;background:__PC__;box-shadow:0 4px 12px __PC__40;font-weight:600}
    .btn:hover{box-shadow:0 6px 18px __PC__60;transform:translateY(-2px)}
    .room-card,.service-card,.testimonial-card{border-radius:20px;background:#FFFCF7;border:2px dashed __PC__30;box-shadow:none}
    .room-card:hover{border-style:solid;border-color:__PC__;transform:translateY(-3px)}
    .room-card img{border-radius:18px 18px 0 0}
    .room-features span{border-radius:50px;padding:5px 14px}
    .site-header.solid{background:__SC__}
    .site-header .logo{font-style:italic}
    .hero h1{font-style:italic;font-weight:400}
    .gallery-item{border-radius:16px}
    .service-card{padding:50px 30px}
    .contact-form input,.contact-form textarea{border-radius:50px;padding:14px 22px}
    .contact-form textarea{border-radius:20px}
    """,
    "bold-modern": """
    h1,h2,h3,h4{font-weight:800;letter-spacing:-0.03em;text-transform:none}
    .section{padding:100px 0}
    .section:nth-of-type(odd){background:__BG__}
    .section:nth-of-type(even){background:__PC__08}
    .section-title{font-size:clamp(2.2rem,5vw,4rem);text-align:left;font-weight:900;line-height:1;margin-bottom:20px;letter-spacing:-0.04em}
    .section-subtitle{text-align:left;font-size:1.1rem;font-weight:500;max-width:600px;margin-left:0;margin-bottom:60px}
    .btn{border-radius:0;padding:18px 48px;text-transform:uppercase;letter-spacing:0.06em;font-weight:800;font-size:0.95rem}
    .btn:hover{transform:translate(-2px,-2px);box-shadow:6px 6px 0 __SC__}
    .room-card,.service-card{background:__SC__;color:#fff;border-radius:0;box-shadow:none;border:none}
    .room-card h3,.service-card h3{color:#fff;font-weight:800}
    .room-card p,.service-card p{color:rgba(255,255,255,0.75)}
    .room-card:hover,.service-card:hover{transform:translate(-4px,-4px);box-shadow:8px 8px 0 __PC__}
    .room-card img{border-radius:0}
    .room-price{color:__PC__;font-size:1.8rem;font-weight:900}
    .room-features span{background:rgba(255,255,255,0.1);color:#fff;border-radius:0;border:1px solid rgba(255,255,255,0.2)}
    .testimonial-card{border-radius:0;border-left:6px solid __PC__;box-shadow:none;background:#fff}
    .gallery-item{border-radius:0}
    .site-header.solid{background:__SC__}
    .site-header .logo{font-weight:900;letter-spacing:-0.02em;text-transform:uppercase}
    .site-header nav a{font-weight:700;text-transform:uppercase;font-size:0.85rem;letter-spacing:0.08em}
    .hero h1{font-weight:900;letter-spacing:-0.04em;text-align:left}
    .hero p{text-align:left;font-weight:500}
    .hero-content{text-align:left;max-width:900px;margin:0;padding:40px 60px}
    .hero{justify-content:flex-start}
    .hero-overlay{background:rgba(0,0,0,0.35)}
    .contact-form input,.contact-form textarea{border-radius:0;border-width:2px;border-color:__SC__}
    .contact-form input:focus,.contact-form textarea:focus{border-color:__PC__}
    """,
    "magazine": """
    body{font-family:__BF__;font-size:1.05rem}
    .section{padding:110px 0}
    .section-title{text-align:left;font-style:italic;font-weight:400;font-size:clamp(2rem,3.2vw,3rem);position:relative;padding-top:30px;margin-bottom:10px}
    .section-title::before{content:"";position:absolute;top:0;left:0;width:50px;height:3px;background:__PC__}
    .section-subtitle{text-align:left;font-size:1.05rem;color:__TC__;opacity:0.8;font-style:italic;margin-bottom:55px;max-width:680px;margin-left:0}
    .btn{background:transparent;color:__SC__;border:none;border-bottom:2px solid __SC__;border-radius:0;padding:8px 0;font-weight:600;font-size:1rem;letter-spacing:0.04em}
    .btn::after{content:" \\2192";transition:margin 0.2s}
    .btn:hover{transform:none;color:__PC__;border-color:__PC__}
    .btn:hover::after{margin-left:6px}
    .room-card,.service-card,.testimonial-card{background:#fff;border:none;border-top:3px solid __PC__;border-radius:0;box-shadow:none;padding-top:0}
    .room-card{padding-top:0}
    .room-card:hover{transform:none;border-top-width:6px;margin-top:-3px}
    .room-card img{border-radius:0;height:230px}
    .room-card-body{padding:25px 0}
    .room-card h3{font-style:italic;font-weight:400}
    .testimonial-card{padding:30px 0;border-top:1px solid #e5e5e5}
    .testimonial-card p{font-style:italic;font-size:1.2rem;line-height:1.6;color:__SC__}
    .testimonial-card p::before{content:"\\201C";font-size:3rem;color:__PC__;line-height:0;vertical-align:-0.5em;margin-right:6px}
    .site-header.solid{background:__SC__}
    .site-header .logo{font-style:italic;font-weight:400;letter-spacing:0;font-size:2rem}
    .hero h1{font-style:italic;font-weight:400}
    .hero h1::first-letter{color:__PC__}
    .hero-overlay{background:rgba(0,0,0,0.45)}
    .gallery-item{border-radius:0}
    .service-card{text-align:left;padding:30px 0}
    .service-icon{display:block;text-align:left}
    .room-features span{border-radius:0;background:transparent;border-bottom:1px solid __PC__;padding:2px 0;margin-right:12px}
    """,
}


def _style_css(style_key: str, pc: str, sc: str, bg: str, tc: str, hf: str, bf: str) -> str:
    raw = _STYLE_OVERRIDES_RAW.get(style_key, "")
    return (raw
            .replace("__PC__", pc)
            .replace("__SC__", sc)
            .replace("__BG__", bg)
            .replace("__TC__", tc)
            .replace("__HF__", hf)
            .replace("__BF__", bf))


def generate_css(theme: Dict[str, Any]) -> str:
    pc = theme.get("primaryColor", "#C5A572")
    sc = theme.get("secondaryColor", "#1A1A2E")
    bg = theme.get("backgroundColor", "#FFFFFF")
    tc = theme.get("textColor", "#333333")
    hf = theme.get("headerFont", "'Playfair Display', serif")
    bf = theme.get("bodyFont", "'Lato', sans-serif")
    style_key = theme.get("style", "classic")
    style_css = _style_css(style_key, pc, sc, bg, tc, hf, bf)
    base = f"""
    *{{margin:0;padding:0;box-sizing:border-box}}
    html{{scroll-padding-top:90px}}
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
    .site-header nav a.nav-active{{opacity:1;font-weight:700;border-bottom:2px solid {pc}}}
    .page-section{{display:block}}
    .mobile-menu{{display:none}}
    .mobile-menu summary{{cursor:pointer;color:inherit;padding:10px;border:1px solid currentColor;border-radius:6px}}
    .mobile-links{{background:{sc};padding:16px;position:absolute;right:20px;max-height:75vh;overflow:auto;border-radius:8px}}
    .mobile-links a{{display:block;color:#fff;padding:10px}}
    @media(max-width:768px){{.site-header .mobile-menu{{display:block}}}}
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
    .booking-section{{background:linear-gradient(135deg,{sc}05,{pc}08);padding:80px 0}}
    .booking-form-container{{max-width:900px;margin:0 auto;background:#fff;border-radius:16px;padding:40px;box-shadow:0 8px 40px rgba(0,0,0,0.1)}}
    .booking-form{{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:20px;margin-top:30px}}
    .booking-field label{{display:block;font-size:0.85rem;font-weight:600;margin-bottom:8px;color:{sc}}}
    .booking-field input,.booking-field select{{width:100%;padding:12px 16px;border:2px solid #eee;border-radius:8px;font-size:1rem;font-family:{bf};transition:border 0.2s}}
    .booking-field input:focus,.booking-field select:focus{{border-color:{pc};outline:none}}
    .booking-submit{{grid-column:1/-1;text-align:center;margin-top:10px}}
    .booking-submit .btn{{padding:16px 60px;font-size:1.1rem}}
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
      .booking-form{{grid-template-columns:1fr}}
    }}
    """
    # Keep real form controls usable even when a theme customizes inputs.
    controls_css = '''
    html{scroll-padding-top:100px}
    .contact-form label{display:flex;flex-direction:column;gap:8px;margin-bottom:16px}
    .contact-form input:not([type=checkbox]),.contact-form textarea,.contact-form select{box-sizing:border-box;width:100%;padding:12px;border:1px solid #aaa!important;background:#fff!important;color:#111!important;min-height:44px}
    .contact-form label:has(input[type=checkbox]){display:flex;flex-direction:row;align-items:flex-start;gap:12px;line-height:1.6}
    .contact-form input[type=checkbox]{width:20px!important;height:20px!important;min-width:20px;margin:3px 0;appearance:auto}
    .contact-form button{min-height:44px}
    .contact-form :focus-visible{outline:3px solid #1769e0;outline-offset:3px}
    '''
    return base + style_css + controls_css


def render_header(props, theme, lang="tr", nav_links=None):
    hotel_name = props.get("hotelName", "Hotel")
    t = get_t(lang)
    if nav_links:
        menu_html = "".join([f'<a href="{link}">{label}</a>' for label, link in nav_links])
    else:
        menu_items = props.get("menuItems", [])
        menu_html = "".join(['<a href="#' + item.lower().replace(" ", "-") + '">' + item + '</a>' for item in menu_items])
    style = props.get("style", "transparent")
    return f'<header class="site-header {style}"><div class="nav-inner"><a class="logo" href="{nav_links[0][1] if nav_links else "#anasayfa"}">{hotel_name}</a><nav aria-label="Main navigation">{menu_html}</nav><details class="mobile-menu"><summary aria-label="Menu">☰ Menu</summary><div class="mobile-links">{menu_html}</div></details></div></header>'


def render_hero(props, theme, lang="tr"):
    title = props.get("title", "")
    subtitle = props.get("subtitle", "")
    bg = props.get("backgroundImage", "")
    cta_text = props.get("ctaText", "")
    cta_link = props.get("ctaLink", "#")
    opacity = props.get("overlayOpacity", "0.5")
    cta_html = f'<a href="{cta_link}" class="btn">{cta_text}</a>' if cta_text else ""
    return f'<section class="hero page-section page-active" id="anasayfa"><div class="hero-bg" style="background-image:url(\'{bg}\')"></div><div class="hero-overlay" style="opacity:{opacity}"></div><div class="hero-content"><h1>{title}</h1><p>{subtitle}</p>{cta_html}</div></section>'


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
    return f'<section class="section page-section" id="hakkimizda"><div class="container"><div class="about-grid">{inner}</div></div></section>'


def render_rooms(props, theme, lang="tr"):
    title = props.get("title", "")
    subtitle = props.get("subtitle", "")
    rooms = props.get("rooms", [])
    rooms_html = ""
    for room in rooms:
        features = room.get("features", [])
        features_html = "".join([f'<span>{f}</span>' for f in features])
        rooms_html += f'<div class="room-card"><img src="{room.get("image", "")}" alt="{room.get("name", "")}"><div class="room-card-body"><h3>{room.get("name", "")}</h3><p>{room.get("description", "")}</p><div class="room-price">{room.get("price", "")}</div><div class="room-features">{features_html}</div></div></div>'
    return f'<section class="section page-section" id="odalar"><div class="container"><h2 class="section-title">{title}</h2><p class="section-subtitle">{subtitle}</p><div class="rooms-grid">{rooms_html}</div></div></section>'


def render_menu(props, theme, lang="tr"):
    title = props.get("title", "")
    subtitle = props.get("subtitle", "")
    items = props.get("items", [])
    items_html = ""
    for item in items:
        price = item.get("price", "")
        price_html = f'<div class="room-price">{price}</div>' if price else ""
        items_html += f'<div class="room-card"><img src="{item.get("image", "")}" alt="{item.get("name", "")}"><div class="room-card-body"><h3>{item.get("name", "")}</h3><p>{item.get("description", "")}</p>{price_html}</div></div>'
    sub_html = f'<p class="section-subtitle">{subtitle}</p>' if subtitle else ""
    return f'<section class="section page-section" id="menu"><div class="container"><h2 class="section-title">{title}</h2>{sub_html}<div class="rooms-grid">{items_html}</div></div></section>'


def render_tours(props, theme, lang="tr"):
    title = props.get("title", "")
    subtitle = props.get("subtitle", "")
    tours = props.get("tours", [])
    items_html = ""
    for tour in tours:
        duration = tour.get("duration", "")
        price = tour.get("price", "")
        features_html = ""
        if duration:
            features_html += f'<span>{duration}</span>'
        price_html = f'<div class="room-price">{price}</div>' if price else ""
        items_html += f'<div class="room-card"><img src="{tour.get("image", "")}" alt="{tour.get("name", "")}"><div class="room-card-body"><h3>{tour.get("name", "")}</h3><p>{tour.get("description", "")}</p>{price_html}<div class="room-features">{features_html}</div></div></div>'
    sub_html = f'<p class="section-subtitle">{subtitle}</p>' if subtitle else ""
    return f'<section class="section page-section" id="turlar"><div class="container"><h2 class="section-title">{title}</h2>{sub_html}<div class="rooms-grid">{items_html}</div></div></section>'


def render_gallery(props, theme, lang="tr"):
    title = props.get("title", "")
    images = props.get("images", [])
    layout = props.get("layout", "grid")
    grid_class = "masonry" if layout == "masonry" else ""
    images_html = "".join([f'<div class="gallery-item"><img src="{img.get("url", "")}" alt="{img.get("alt", "")}"></div>' for img in images])
    return f'<section class="section page-section" style="background:#f8f8f8" id="galeri"><div class="container"><h2 class="section-title">{title}</h2><div class="gallery-grid {grid_class}">{images_html}</div></div></section>'


def render_services(props, theme, lang="tr"):
    title = props.get("title", "")
    services = props.get("services", [])
    svc_html = ""
    for svc in services:
        icon_svg = get_service_icon_svg(svc.get("icon", "spa"))
        svc_html += f'<div class="service-card"><div class="service-icon">{icon_svg}</div><h3>{svc.get("name", "")}</h3><p>{svc.get("description", "")}</p></div>'
    return f'<section class="section page-section" id="hizmetler"><div class="container"><h2 class="section-title">{title}</h2><div class="services-grid">{svc_html}</div></div></section>'


def render_testimonials(props, theme, lang="tr"):
    title = props.get("title", "")
    testimonials = props.get("testimonials", [])
    items_html = ""
    for t in testimonials:
        rating = t.get("rating", 5)
        stars = render_star_svg() * rating
        items_html += f'<div class="testimonial-card"><div class="testimonial-stars">{stars}</div><p>"{t.get("text", "")}"</p><div class="testimonial-author">{t.get("name", "")}</div></div>'
    return f'<section class="section page-section" style="background:#f8f8f8" id="yorumlar"><div class="container"><h2 class="section-title">{title}</h2><div class="testimonials-grid">{items_html}</div></div></section>'


def render_contact(props, theme, lang="tr"):
    title = props.get("title", "")
    address = props.get("address", "")
    phone = props.get("phone", "")
    email = props.get("email", "")
    pc = theme.get("primaryColor", "#C5A572")
    t = get_t(lang)
    endpoint = props.get('_submitUrl', '')
    form = f'''<form class="contact-form" data-site-form action="{endpoint}" method="post">
<label>{t['your_name']}<input name="name" required maxlength="160" autocomplete="name"></label>
<label>{t['your_email']}<input name="email" type="email" required maxlength="254" autocomplete="email"></label>
<label>{t['subject']}<input name="subject" maxlength="200"></label>
<label>{t['message']}<textarea name="message" required maxlength="5000"></textarea></label>
<label><input type="checkbox" name="consent" required> {'Talebimin yanıtlanması için iletişim bilgilerimin kullanılmasını kabul ediyorum.' if lang == 'tr' else 'I agree to the use of my contact details to respond to this request.'}</label>
<input name="website" tabindex="-1" autocomplete="off" aria-hidden="true" style="display:none">
<button class="btn" type="submit" {'' if endpoint else 'disabled'}>{t['send']}</button><p role="status" aria-live="polite">{'' if endpoint else ('Form henüz yayına bağlanmadı.' if lang == 'tr' else 'Form delivery has not been configured.')}</p></form>'''
    # Keep contact text escaped by prepare_project; URLs are generated separately.
    contact_links = f'<p><a href="tel:{re.sub(r"[^+0-9]", "", unescape(phone))}">{phone}</a></p><p><a href="mailto:{email}">{email}</a></p>'
    return f'<section class="section page-section" id="iletisim"><div class="container"><h2 class="section-title">{title}</h2><div class="contact-grid"><div class="contact-info"><h3>{t["contact_info"]}</h3><p>{address}</p>{contact_links}</div>{form}</div></div></section>'


def render_banner(props, theme, lang="tr"):
    title = props.get("title", "")
    subtitle = props.get("subtitle", "")
    bg = props.get("backgroundImage", "")
    cta_text = props.get("ctaText", "")
    cta_link = props.get("ctaLink", "#")
    cta_html = f'<a href="{cta_link}" class="btn">{cta_text}</a>' if cta_text else ""
    return f'<section class="cta-banner"><div class="hero-bg" style="background-image:url(\'{bg}\')"></div><div class="hero-overlay"></div><div class="hero-content"><h2>{title}</h2><p>{subtitle}</p>{cta_html}</div></section>'


def render_booking(props, theme, lang="tr"):
    t = get_t(lang)
    title = props.get("title", t["booking_title"])
    subtitle = props.get("subtitle", t["booking_subtitle"])
    booking_url = props.get("bookingUrl", "")
    phone = props.get("phone", "")
    email = props.get("email", "")
    room_types = props.get("roomTypes", [])
    widget_code = props.get("widgetCode", "")
    pc = theme.get("primaryColor", "#C5A572")

    # If external widget code is provided, render it
    if widget_code:
        return f'<section class="booking-section section page-section" id="rezervasyon"><div class="container"><h2 class="section-title">{title}</h2><p class="section-subtitle">{subtitle}</p><div class="booking-form-container">{widget_code}</div></div></section>'

    if booking_url:
        return f'<section class="booking-section section page-section" id="rezervasyon"><div class="container"><h2 class="section-title">{title}</h2><p>{subtitle}</p><a class="btn" href="{booking_url}" rel="noopener noreferrer">{t["make_reservation"]}</a></div></section>'
    return f'<section class="booking-section section page-section" id="rezervasyon"><div class="container"><h2>{title}</h2><p>{"Rezervasyon bağlantısı henüz yapılandırılmadı." if lang == "tr" else "Reservation link has not been configured."}</p></div></section>'



SECTION_NAV_MAP = {
    "hero": ("#anasayfa", "home"),
    "about": ("#hakkimizda", "about"),
    "services": ("#hizmetler", "services"),
    "booking": ("#rezervasyon", "booking_title"),
    "testimonials": ("#yorumlar", "testimonials"),
    "rooms": ("#odalar", "rooms"),
    "menu": ("#menu", "menu"),
    "tours": ("#turlar", "tours"),
    "gallery": ("#galeri", "gallery"),
    "contact": ("#iletisim", "contact"),
}


def build_quick_links_from_sections(sections, lang="tr"):
    t = get_t(lang)
    seen = set()
    links = []
    for s in sections or []:
        if not s.get("visible", True):
            continue
        st = s.get("type")
        if st in SECTION_NAV_MAP and st not in seen:
            seen.add(st)
            href, key = SECTION_NAV_MAP[st]
            label = t.get(key, key.capitalize())
            links.append((href, label))
    if not links:
        return f'<p><a href="#anasayfa">{t["home"]}</a></p>'
    return "".join(f'<p><a href="{href}">{label}</a></p>' for href, label in links)


def render_footer(props, theme, lang="tr", quick_links_html=None, all_sections=None):
    hotel_name = props.get("hotelName", "Hotel")
    address = props.get("address", "")
    phone = props.get("phone", "")
    email = props.get("email", "")
    social = props.get("socialLinks", {})
    t = get_t(lang)
    social_html = "".join([f'<a href="{link}" title="{escape(p.capitalize())}" rel="noopener noreferrer">{escape(p[0].upper())}</a>' for p, link in social.items() if link and link != '#'])
    if quick_links_html is None:
        if all_sections is not None:
            quick_links_html = build_quick_links_from_sections(all_sections, lang)
        else:
            quick_links_html = f'<p><a href="#anasayfa">{t["home"]}</a></p><p><a href="#odalar">{t["rooms"]}</a></p><p><a href="#galeri">{t["gallery"]}</a></p><p><a href="#iletisim">{t["contact"]}</a></p>'
    return f'<footer class="site-footer"><div class="container"><div class="footer-grid"><div><h3>{hotel_name}</h3><p>{address}</p><div class="footer-social">{social_html}</div></div><div><h3>{t["quick_links"]}</h3>{quick_links_html}</div><div><h3>{t["contact"]}</h3><p>{phone}</p><p>{email}</p></div></div><div class="footer-bottom"><p>&copy; {datetime.now(timezone.utc).year} {hotel_name}. {t["all_rights"]}.</p><a href="https://syroce.com" class="syroce-brand" target="_blank">{t["powered_by"]} <span>Syroce</span></a></div></div></footer>'


SECTION_RENDERERS = {
    "header": render_header,
    "hero": render_hero,
    "about": render_about,
    "rooms": render_rooms,
    "menu": render_menu,
    "tours": render_tours,
    "gallery": render_gallery,
    "services": render_services,
    "testimonials": render_testimonials,
    "contact": render_contact,
    "banner": render_banner,
    "booking": render_booking,
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
    base = project_data.get('site_base_url', '')
    if base:
        meta += f'<link rel="canonical" href="{base}index.html">\n'
    meta += '<meta name="robots" content="index,follow">\n' if base else '<meta name="robots" content="noindex,nofollow">\n'
    return meta


def render_public_content(project):
    """Blog text and configured forms use the exact same renderer in every output."""
    source = ''
    legal = project.get('legal', {})
    if legal:
        links = ''.join(f'<a href="index.html#{key}">{title}</a> ' for key, title in [('privacy', 'Gizlilik / Privacy'), ('terms', 'Kosullar / Terms')] if legal.get(key))
        source += f'<nav class="container" aria-label="Legal">{links}</nav>'
    for key, title in [('privacy', 'Gizlilik / Privacy'), ('terms', 'Kosullar / Terms')]:
        if legal.get(key):
            source += f'<section class="section" id="{key}"><div class="container"><h2>{title}</h2><div style="white-space:pre-wrap">{legal[key]}</div></div></section>'
    for post in project.get('public_blog_posts', []):
        source += f'<article class="section" id="blog-{post.get("id", "")}"><div class="container"><h2>{post.get("title", "")}</h2><div style="white-space:pre-wrap">{post.get("content", "")}</div></div></article>'
    for form in project.get('public_forms', []):
        controls = ''
        for index, field in enumerate(form.get('fields', [])):
            key = field_key(field, index)
            required = 'required' if field.get('required') else ''
            kind = field.get('type', 'text')
            if kind == 'textarea':
                control = f'<textarea name="{key}" {required} maxlength="5000"></textarea>'
            elif kind == 'select':
                options = field.get('options', [])
                if isinstance(options, str):
                    options = options.split(',')
                control = f'<select name="{key}" {required}><option value="">—</option>' + ''.join(f'<option>{str(o).strip()}</option>' for o in options) + '</select>'
            else:
                kind = 'tel' if kind == 'phone' else kind
                kind = kind if kind in {'text', 'email', 'tel', 'date', 'number', 'checkbox'} else 'text'
                control = f'<input type="{kind}" name="{key}" {required} maxlength="5000">'
            controls += f'<label>{field.get("label", key)}{control}</label>'
        source += f'<section class="section" id="form-{form.get("id", "")}"><div class="container"><h2>{form.get("name", "")}</h2><form class="contact-form" data-site-form action="{form.get("submit_url", "")}" method="post">{controls}<input name="website" tabindex="-1" aria-hidden="true" style="display:none"><button type="submit" class="btn">Gonder / Send</button><p role="status" aria-live="polite"></p></form></div></section>'
    return source


def _get_analytics_code(project_data):
    """Generate analytics tracking code from project settings."""
    analytics = project_data.get("analytics", {})
    code = ""
    ga_id = analytics.get("ga_id", "")
    if ga_id and re.fullmatch(r'G-[A-Z0-9]+', ga_id):
        code = f'''<script>
document.addEventListener('DOMContentLoaded', function() {{
  var key = 'syroce-analytics-{ga_id}';
  var box = document.createElement('aside'); box.setAttribute('aria-label','Analytics consent');
  box.style.cssText='position:fixed;bottom:0;left:0;right:0;background:#fff;color:#111;padding:20px;z-index:1000;border:1px solid #ccc';
  var text=document.createElement('p'); text.textContent='Optional analytics / İsteğe bağlı analiz çerezleri'; box.appendChild(text);
  var policy=document.createElement('a'); policy.href='index.html#privacy'; policy.textContent='Privacy / Gizlilik'; box.appendChild(policy);
  function loadAnalytics() {{
    window['ga-disable-{ga_id}']=false;
    if(window.gtag)window.gtag('consent','update',{{analytics_storage:'granted'}});
    if(document.querySelector('script[data-syroce-ga]')) return;
    window.dataLayer=window.dataLayer||[];
    window.gtag=function(){{window.dataLayer.push(arguments);}};
    var script=document.createElement('script'); script.async=true; script.dataset.syroceGa='true'; script.src='https://www.googletagmanager.com/gtag/js?id={ga_id}'; document.head.appendChild(script);
    window.gtag('js',new Date()); window.gtag('config','{ga_id}');
  }}
  ['Accept / Kabul','Reject / Reddet'].forEach(function(label,i){{
    var button=document.createElement('button'); button.type='button'; button.textContent=label; button.style.margin='10px';
    button.onclick=function(){{try{{localStorage.setItem(key,i===0?'yes':'no');}}catch(e){{}} if(i===0)loadAnalytics(); else {{window['ga-disable-{ga_id}']=true; if(window.gtag)window.gtag('consent','update',{{analytics_storage:'denied'}});}} box.remove();}}; box.appendChild(button);
  }});
  var choice; try{{choice=localStorage.getItem(key);}}catch(e){{}}
  if(choice==='yes')loadAnalytics(); else if(choice!=='no')document.body.appendChild(box);
  var reset=document.createElement('button'); reset.type='button'; reset.textContent='Cookie settings / Çerez ayarları';
  reset.onclick=function(){{document.body.appendChild(box);}}; document.body.appendChild(reset);
}});
</script>'''
    return code


def generate_full_html(project_data: Dict[str, Any]) -> str:
    project_data = prepare_project(project_data)
    theme = project_data.get("theme", {})
    sections = project_data.get("sections", [])
    project_name = project_data.get("name", "Hotel Website")
    lang = project_data.get("language", "tr")
    seo = project_data.get("seo", {})
    page_title = seo.get("title") or project_name
    fonts_url = _get_fonts_url(theme)
    seo_meta = _get_seo_meta(project_data)
    analytics_code = _get_analytics_code(project_data)

    sections_html = ""
    for section in sections:
        if section.get("visible", True):
            stype = section.get("type")
            renderer = SECTION_RENDERERS.get(stype)
            if renderer:
                if stype == "footer":
                    sections_html += render_footer(section.get("props", {}), theme, lang, all_sections=sections)
                elif stype == 'header':
                    links = [(get_t(lang).get(SECTION_NAV_MAP[s['type']][1], s['type']), SECTION_NAV_MAP[s['type']][0]) for s in sections if s.get('visible', True) and s.get('type') in SECTION_NAV_MAP]
                    sections_html += render_header(section.get('props', {}), theme, lang, nav_links=links)
                elif stype == 'contact':
                    sections_html += render_contact({**section.get('props', {}), '_submitUrl': project_data.get('public_contact_url', '')}, theme, lang)
                else:
                    sections_html += renderer(section.get("props", {}), theme, lang)

    sections_html += render_public_content(project_data)

    css = generate_css(theme)

    return f"""<!DOCTYPE html>
<html lang="{lang}" dir="{'rtl' if lang == 'ar' else 'ltr'}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title}</title>
    {seo_meta}
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="{fonts_url}" rel="stylesheet">
    {analytics_code}
    <style>{css}</style>
</head>
<body>
{sections_html}
{SITE_RUNTIME}
</body>
</html>"""


def _build_page_html(title, css, fonts_url, seo_meta, lang, header_html, body_sections, footer_html, analytics_code=""):
    return f"""<!DOCTYPE html>
<html lang="{lang}" dir="{'rtl' if lang == 'ar' else 'ltr'}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    {seo_meta}
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="{fonts_url}" rel="stylesheet">
    {analytics_code}
    <style>{css}</style>
</head>
<body>
{header_html}
{body_sections}
{footer_html}
{SITE_RUNTIME}
</body>
</html>"""


# ==================== ASSET BUNDLING ====================
def _extract_image_urls(html_content: str) -> List[str]:
    """Extract all image URLs from HTML content."""
    urls = set()
    class Images(HTMLParser):
        def handle_starttag(self, tag, attrs):
            if tag == 'img':
                value = dict(attrs).get('src', '')
                if value.startswith(('http://', 'https://', '/api/uploads/')):
                    urls.add(value)
    Images().feed(html_content)
    for value in re.findall(r'url\([\"\']?([^\"\')\s]+)', html_content):
        value = unescape(value)
        if value.startswith(('http://', 'https://', '/api/uploads/')):
            urls.add(value)
    # Match src="..." and url('...')
    src_pattern = re.compile(r'(?:src|href)=["\']([^"\']+\.(?:jpg|jpeg|png|gif|webp|svg)(?:\?[^"\']*)?)["\']', re.IGNORECASE)
    url_pattern = re.compile(r'url\(["\']?([^"\')\s]+\.(?:jpg|jpeg|png|gif|webp|svg)(?:\?[^"\')\s]*)?)["\']?\)', re.IGNORECASE)

    for match in src_pattern.finditer(html_content):
        url = match.group(1)
        if url.startswith(('http://', 'https://')):
            urls.add(url)

    for match in url_pattern.finditer(html_content):
        url = match.group(1)
        if url.startswith(('http://', 'https://')):
            urls.add(url)

    return sorted({unescape(url) for url in urls})


async def _download_image(client: httpx.AsyncClient, url: str) -> Tuple[str, bytes, str]:
    """Download an image and return (url, content, filename)."""
    try:
        current = url
        for _ in range(4):
            if not current.startswith(('http://', 'https://')) or urlsplit(current).username or urlsplit(current).password:
                break
            async with client.stream('GET', current) as response:
                if response.status_code in {301, 302, 303, 307, 308}:
                    current = urljoin(current, response.headers.get('location', ''))
                    continue
                content_type = response.headers.get('content-type', '').split(';')[0].lower()
                extensions = {'image/jpeg': '.jpg', 'image/png': '.png', 'image/webp': '.webp', 'image/gif': '.gif'}
                if response.status_code != 200 or content_type not in extensions:
                    break
                chunks = bytearray()
                async for chunk in response.aiter_bytes():
                    chunks.extend(chunk)
                    if len(chunks) > 5 * 1024 * 1024:
                        raise ValueError('Image exceeds 5MB')
                filename = f"img_{hashlib.sha256(url.encode()).hexdigest()[:16]}{extensions[content_type]}"
                return url, bytes(chunks), filename
    except Exception:
        pass
    return url, b"", ""


async def bundle_assets_in_html(html_content: str) -> Tuple[str, Dict[str, bytes]]:
    """Download external images and replace URLs with local paths. Returns modified HTML and asset dict."""
    urls = _extract_image_urls(html_content)
    if not urls:
        return html_content, {}

    assets = {}
    local_urls = []
    remote_urls = []
    public_host = urlsplit(os.getenv('PUBLIC_BASE_URL', '')).netloc
    for url in urls:
        parsed = urlsplit(url)
        if parsed.path.startswith('/api/uploads/') and (not parsed.netloc or parsed.netloc == public_host):
            filename = parsed.path.removeprefix('/api/uploads/')
            if Path(filename).name != filename or Path(filename).suffix.lower() not in {'.jpg', '.jpeg', '.png', '.webp', '.gif'}:
                raise ValueError('Invalid upload path')
            path = UPLOADS_DIR / filename
            if not path.is_file() or path.stat().st_size > 5 * 1024 * 1024:
                raise ValueError(f'Uploaded image missing: {filename}')
            local_urls.append((url, path.read_bytes(), filename))
        else:
            remote_urls.append(url)
    if len(urls) > 100:
        raise ValueError('At most 100 images can be bundled')
    async with image_client() as client:
        semaphore = asyncio.Semaphore(8)
        async def bounded_download(url):
            async with semaphore:
                return await _download_image(client, url)
        tasks = [bounded_download(url) for url in remote_urls]
        results = await asyncio.gather(*tasks)
    results.extend(local_urls)

    for url, content, filename in results:
        if content and filename:
            assets[f"assets/{filename}"] = content
            html_content = html_content.replace(url, f"assets/{filename}")
            html_content = html_content.replace(escape(url, quote=True), f"assets/{filename}")
        else:
            raise ValueError('Image could not be safely bundled; replace the URL or disable external asset bundling')

    return html_content, assets


def create_multipage_export_zip(project_data: Dict[str, Any]) -> bytes:
    project_data = prepare_project(project_data)
    theme = project_data.get("theme", {})
    sections = project_data.get("sections", [])
    project_name = project_data.get("name", "Hotel Website")
    lang = project_data.get("language", "tr")
    t = get_t(lang)
    seo = project_data.get("seo", {})
    page_title = seo.get("title") or project_name
    fonts_url = _get_fonts_url(theme)
    seo_meta = _get_seo_meta(project_data)
    analytics_code = _get_analytics_code(project_data)
    css = generate_css(theme)
    folder = archive_folder(project_name)

    pages, readme_lines = _build_multipage_pages(project_data, sections, theme, lang, t, page_title, css, fonts_url, seo_meta, analytics_code)

    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for page_name, html in pages.items():
            zf.writestr(f"{folder}/{page_name}", bundle_local_images(html, zf, folder))
        write_site_metadata(zf, folder, pages, project_data.get('site_base_url', ''))
        pages_list = "\n".join(f"- {line}" for line in readme_lines)
        readme = f"""# {project_name}

## Pages
{pages_list}

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


def _build_multipage_pages(project_data, sections, theme, lang, t, page_title, css, fonts_url, seo_meta, analytics_code):
    """Segment-aware multipage builder. Emits index + one page per detail section present."""
    header_props = {}
    footer_props = {}
    hero_props = {}
    about_props = {}
    services_props = {}
    testimonials_props = {}
    booking_props = {}
    contact_props = {}
    rooms_props = None
    menu_props = None
    tours_props = None
    gallery_props = None
    banners = []

    for s in sections:
        if not s.get("visible", True):
            continue
        st = s.get("type")
        p = s.get("props", {})
        if st == "header": header_props = p
        elif st == "footer": footer_props = p
        elif st == "hero": hero_props = p
        elif st == "about": about_props = p
        elif st == "services": services_props = p
        elif st == "testimonials": testimonials_props = p
        elif st == "booking": booking_props = p
        elif st == "contact": contact_props = p
        elif st == "rooms": rooms_props = p
        elif st == "menu": menu_props = p
        elif st == "tours": tours_props = p
        elif st == "gallery": gallery_props = p
        elif st == "banner": banners.append(p)

    # Dynamic nav: index + each detail page that exists
    nav_links = [(t["home"], "index.html")]
    if about_props:
        nav_links.append((t["about"], "index.html#hakkimizda"))
    detail_pages = []  # (filename, title, body_html, readme_label)

    if rooms_props is not None:
        nav_links.append((t.get("rooms", "Rooms"), "rooms.html"))
        detail_pages.append(("rooms.html", t.get("rooms", "Rooms"), render_rooms(rooms_props, theme, lang), "rooms.html (Rooms)"))
    if menu_props is not None:
        nav_links.append((t.get("menu", "Menu"), "menu.html"))
        detail_pages.append(("menu.html", t.get("menu", "Menu"), render_menu(menu_props, theme, lang), "menu.html (Menu)"))
    if tours_props is not None:
        nav_links.append((t.get("tours", "Tours"), "tours.html"))
        detail_pages.append(("tours.html", t.get("tours", "Tours"), render_tours(tours_props, theme, lang), "tours.html (Tours)"))
    if gallery_props is not None:
        nav_links.append((t["gallery"], "gallery.html"))
        detail_pages.append(("gallery.html", t["gallery"], render_gallery(gallery_props, theme, lang), "gallery.html (Gallery)"))
    if contact_props:
        nav_links.append((t["contact"], "contact.html"))

    # Quick links pointing to detail pages
    quick_links_html = "".join(f'<p><a href="{href}">{label}</a></p>' for label, href in nav_links)

    header_html = render_header(header_props, theme, lang, nav_links=nav_links)
    footer_html = render_footer(footer_props, theme, lang, quick_links_html=quick_links_html)

    # Home page
    home_body = render_hero(hero_props, theme, lang) if hero_props else ""
    if about_props: home_body += render_about(about_props, theme, lang)
    if services_props: home_body += render_services(services_props, theme, lang)
    if booking_props: home_body += render_booking(booking_props, theme, lang)
    if testimonials_props: home_body += render_testimonials(testimonials_props, theme, lang)
    for bp in banners:
        home_body += render_banner(bp, theme, lang)
    home_body += render_public_content(project_data)

    pages = {"index.html": _build_page_html(page_title, css, fonts_url, seo_meta, lang, header_html, home_body, footer_html, analytics_code)}
    readme_lines = ["index.html (Home)"]

    for filename, ptitle, body_html, readme_label in detail_pages:
        full_body = '<div style="padding-top:80px"></div>' + body_html
        pages[filename] = _build_page_html(f"{ptitle} - {page_title}", css, fonts_url, seo_meta, lang, header_html, full_body, footer_html, analytics_code)
        readme_lines.append(readme_label)

    # Contact page
    if contact_props:
        contact_body = '<div style="padding-top:80px"></div>' + render_contact({**contact_props, '_submitUrl': project_data.get('public_contact_url', '')}, theme, lang)
        pages["contact.html"] = _build_page_html(f"{t['contact']} - {page_title}", css, fonts_url, seo_meta, lang, header_html, contact_body, footer_html, analytics_code)
        readme_lines.append("contact.html (Contact)")

    destinations = {'#anasayfa': 'index.html', '#hakkimizda': 'index.html#hakkimizda', '#hizmetler': 'index.html#hizmetler', '#yorumlar': 'index.html#yorumlar', '#rezervasyon': 'index.html#rezervasyon', '#odalar': 'rooms.html', '#galeri': 'gallery.html', '#iletisim': 'contact.html', '#menu': 'menu.html', '#turlar': 'tours.html'}
    for page_name, source in pages.items():
        if project_data.get('site_base_url'):
            base = project_data['site_base_url']
            source = source.replace(f'<link rel="canonical" href="{base}index.html">', f'<link rel="canonical" href="{base}{page_name}">')
        for anchor, destination in destinations.items():
            source = source.replace(f'href="{anchor}"', f'href="{destination}"')
        pages[page_name] = source

    return pages, readme_lines


async def create_multipage_export_zip_with_assets(project_data: Dict[str, Any]) -> bytes:
    """Create multipage export ZIP with bundled assets."""
    project_data = prepare_project(project_data)
    theme = project_data.get("theme", {})
    sections = project_data.get("sections", [])
    project_name = project_data.get("name", "Hotel Website")
    lang = project_data.get("language", "tr")
    t = get_t(lang)
    seo = project_data.get("seo", {})
    page_title = seo.get("title") or project_name
    fonts_url = _get_fonts_url(theme)
    seo_meta = _get_seo_meta(project_data)
    analytics_code = _get_analytics_code(project_data)
    css = generate_css(theme)
    folder = archive_folder(project_name)

    pages, readme_lines = _build_multipage_pages(project_data, sections, theme, lang, t, page_title, css, fonts_url, seo_meta, analytics_code)

    # Bundle assets for all pages
    all_assets = {}
    bundled_pages = {}
    for page_name, html in pages.items():
        bundled_html, page_assets = await bundle_assets_in_html(html)
        bundled_pages[page_name] = bundled_html
        all_assets.update(page_assets)

    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for page_name, html in bundled_pages.items():
            zf.writestr(f"{folder}/{page_name}", html)
        write_site_metadata(zf, folder, bundled_pages, project_data.get('site_base_url', ''))
        for asset_path, asset_data in all_assets.items():
            zf.writestr(f"{folder}/{asset_path}", asset_data)
        pages_list = "\n".join(f"- {line}" for line in readme_lines)
        readme = f"""# {project_name}\n\n## Pages\n{pages_list}\n\n## Assets\nImages have been bundled in the assets/ folder.\n\n---\nPowered by Syroce"""
        zf.writestr(f"{folder}/README.md", readme)
    buffer.seek(0)
    return buffer.getvalue()


async def create_export_zip_with_assets(project_data: Dict[str, Any]) -> bytes:
    """Create single-page export ZIP with bundled assets."""
    html_content = generate_full_html(project_data)
    project_name = archive_folder(project_data.get('name', 'hotel-website'))

    bundled_html, assets = await bundle_assets_in_html(html_content)

    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(f"{project_name}/index.html", bundled_html)
        write_site_metadata(zf, project_name, {'index.html': bundled_html}, project_data.get('site_base_url', ''))
        for asset_path, asset_data in assets.items():
            zf.writestr(f"{project_name}/{asset_path}", asset_data)
        readme = f"""# {project_data.get('name', 'Hotel Website')}\n\n## Setup\n1. Upload this folder to your web server\n2. Open index.html\n\n## Assets\nImages bundled in assets/ folder.\n\n---\nPowered by Syroce"""
        zf.writestr(f"{project_name}/README.md", readme)
    buffer.seek(0)
    return buffer.getvalue()


def create_export_zip(project_data: Dict[str, Any]) -> bytes:
    html_content = generate_full_html(project_data)
    project_name = archive_folder(project_data.get('name', 'hotel-website'))
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(f"{project_name}/index.html", bundle_local_images(html_content, zf, project_name))
        write_site_metadata(zf, project_name, {'index.html': html_content}, project_data.get('site_base_url', ''))
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


def archive_folder(name):
    return re.sub(r'[^a-zA-Z0-9_-]+', '-', str(name)).strip('-')[:80] or 'hotel-website'


def bundle_local_images(source, archive, folder):
    host = urlsplit(os.getenv('PUBLIC_BASE_URL', '')).netloc
    for url in _extract_image_urls(source):
        parsed = urlsplit(url)
        if not parsed.path.startswith('/api/uploads/') or (parsed.netloc and parsed.netloc != host):
            continue
        name = parsed.path.removeprefix('/api/uploads/')
        if Path(name).name != name or Path(name).suffix.lower() not in {'.jpg', '.jpeg', '.png', '.webp', '.gif'}:
            raise ValueError('Invalid uploaded image')
        path = UPLOADS_DIR / name
        if not path.is_file() or path.stat().st_size > 5 * 1024 * 1024:
            raise ValueError('Uploaded image is missing or too large')
        asset = f'{folder}/assets/{name}'
        if asset not in archive.namelist():
            archive.writestr(asset, path.read_bytes())
        source = source.replace(escape(url, quote=True), f'assets/{name}').replace(url, f'assets/{name}')
    return source


def write_site_metadata(archive, folder, pages, base):
    from xml.sax.saxutils import escape as xml_escape
    base = unescape(base)
    urls = ''.join(f'<url><loc>{xml_escape(base + name)}</loc></url>' for name in pages if name.endswith('.html')) if base else ''
    archive.writestr(f'{folder}/sitemap.xml', f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    archive.writestr(f'{folder}/robots.txt', f'User-agent: *\nAllow: /\nSitemap: {base}sitemap.xml\n' if base else 'User-agent: *\nDisallow: /\n')
