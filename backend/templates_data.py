import uuid
from datetime import datetime, timezone

# Image pools
HERO_IMAGES = [
    "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=1600&q=80",
    "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=1600&q=80",
    "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=1600&q=80",
    "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=1600&q=80",
    "https://images.unsplash.com/photo-1455587734955-081b22074882?w=1600&q=80",
    "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=1600&q=80",
    "https://images.unsplash.com/photo-1564501049412-61c2a3083791?w=1600&q=80",
    "https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?w=1600&q=80",
    "https://images.unsplash.com/photo-1445019980597-93fa8acb246c?w=1600&q=80",
    "https://images.unsplash.com/photo-1584132967334-10e028bd69f7?w=1600&q=80",
]

ROOM_IMAGES = [
    "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=800&q=80",
    "https://images.unsplash.com/photo-1618773928121-c32242e63f39?w=800&q=80",
    "https://images.unsplash.com/photo-1590490360182-c33d955e1740?w=800&q=80",
    "https://images.unsplash.com/photo-1596394516093-501ba68a0ba6?w=800&q=80",
]

GALLERY_IMAGES = [
    "https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=600&q=80",
    "https://images.unsplash.com/photo-1584132967334-10e028bd69f7?w=600&q=80",
    "https://images.unsplash.com/photo-1560200353-ce0a76b1d438?w=600&q=80",
    "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=600&q=80",
    "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=600&q=80",
    "https://images.unsplash.com/photo-1445019980597-93fa8acb246c?w=600&q=80",
]

ABOUT_IMAGES = [
    "https://images.unsplash.com/photo-1455587734955-081b22074882?w=800&q=80",
    "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800&q=80",
    "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800&q=80",
]


def make_sections(hero_img, about_img, room_imgs, gallery_imgs, layouts):
    return [
        {
            "id": str(uuid.uuid4()),
            "type": "header",
            "title": "Header",
            "visible": True,
            "props": {
                "hotelName": "Otel Adi",
                "logo": "",
                "menuItems": ["Anasayfa", "Hakkimizda", "Odalar", "Galeri", "Iletisim"],
                "style": layouts.get("header", "transparent")
            }
        },
        {
            "id": str(uuid.uuid4()),
            "type": "hero",
            "title": "Hero",
            "visible": True,
            "props": {
                "title": "Luks ve Konfor Bir Arada",
                "subtitle": "Unutulmaz bir konaklama deneyimi icin sizi bekliyoruz",
                "backgroundImage": hero_img,
                "ctaText": "Rezervasyon Yap",
                "ctaLink": "#iletisim",
                "layout": layouts.get("hero", "fullscreen"),
                "overlayOpacity": "0.5"
            }
        },
        {
            "id": str(uuid.uuid4()),
            "type": "about",
            "title": "Hakkimizda",
            "visible": True,
            "props": {
                "title": "Otelimiz Hakkinda",
                "description": "Yillardir misafirlerimize en iyi hizmeti sunmak icin calisiyor, konfor ve zarafeti bir araya getiriyoruz. Modern mimarimiz ve sicak atmosferimizle sizleri agirlamaktan mutluluk duyuyoruz. Her detayi dusunulmus odalarimiz ve ozel hizmetlerimizle unutulmaz bir konaklama deneyimi yasayacaksiniz.",
                "image": about_img,
                "layout": layouts.get("about", "left-image")
            }
        },
        {
            "id": str(uuid.uuid4()),
            "type": "rooms",
            "title": "Odalar",
            "visible": True,
            "props": {
                "title": "Odalarimiz & Suitler",
                "subtitle": "Her butceye uygun, ozenle tasarlanmis odalar",
                "rooms": [
                    {"name": "Standart Oda", "description": "Konforlu ve ferah, tum ihtiyaclariniz icin tasarlanmis.", "image": room_imgs[0], "price": "500 TL", "features": ["Wi-Fi", "Klima", "Mini Bar"]},
                    {"name": "Deluxe Oda", "description": "Genis alan ve premium donanımlarla donanimli.", "image": room_imgs[1], "price": "850 TL", "features": ["Wi-Fi", "Klima", "Mini Bar", "Deniz Manzarasi"]},
                    {"name": "Suite", "description": "Luks ve konforun en ust seviyesi.", "image": room_imgs[2], "price": "1500 TL", "features": ["Wi-Fi", "Klima", "Mini Bar", "Jakuzi", "Ozel Teras"]}
                ],
                "layout": layouts.get("rooms", "grid")
            }
        },
        {
            "id": str(uuid.uuid4()),
            "type": "gallery",
            "title": "Galeri",
            "visible": True,
            "props": {
                "title": "Foto Galeri",
                "images": [{"url": img, "alt": f"Otel Gorsel {i+1}"} for i, img in enumerate(gallery_imgs)],
                "layout": layouts.get("gallery", "grid")
            }
        },
        {
            "id": str(uuid.uuid4()),
            "type": "services",
            "title": "Hizmetler",
            "visible": True,
            "props": {
                "title": "Hizmetlerimiz",
                "services": [
                    {"name": "Spa & Wellness", "icon": "spa", "description": "Profesyonel terapistlerimizle dinlenin."},
                    {"name": "Restoran", "icon": "restaurant", "description": "Dunya mutfagindan lezzetler."},
                    {"name": "Yuzme Havuzu", "icon": "pool", "description": "Acik ve kapali havuz keyfi."},
                    {"name": "Fitness", "icon": "fitness", "description": "Modern ekipmanlarla donatilmis."},
                    {"name": "Otopark", "icon": "parking", "description": "Ucretsiz vale otopark hizmeti."},
                    {"name": "Transfer", "icon": "transfer", "description": "Havaalani transfer hizmeti."}
                ],
                "layout": layouts.get("services", "grid")
            }
        },
        {
            "id": str(uuid.uuid4()),
            "type": "testimonials",
            "title": "Yorumlar",
            "visible": True,
            "props": {
                "title": "Misafir Yorumlari",
                "testimonials": [
                    {"name": "Ahmet Y.", "text": "Harika bir deneyimdi. Personel cok ilgili ve odalar muhtesemdi.", "rating": 5},
                    {"name": "Zeynep K.", "text": "Muhteşem manzara ve kusursuz hizmet. Kesinlikle tekrar gelecegiz.", "rating": 5},
                    {"name": "Mehmet A.", "text": "Is seyahati icin ideal. Her sey dusunulmus.", "rating": 4}
                ],
                "layout": layouts.get("testimonials", "slider")
            }
        },
        {
            "id": str(uuid.uuid4()),
            "type": "contact",
            "title": "Iletisim",
            "visible": True,
            "props": {
                "title": "Bize Ulasin",
                "address": "Ornek Mahallesi, Otel Caddesi No:1, Antalya",
                "phone": "+90 242 000 00 00",
                "email": "info@otel.com",
                "mapUrl": "",
                "layout": layouts.get("contact", "split")
            }
        },
        {
            "id": str(uuid.uuid4()),
            "type": "footer",
            "title": "Footer",
            "visible": True,
            "props": {
                "hotelName": "Otel Adi",
                "address": "Ornek Mahallesi, Otel Caddesi No:1, Antalya",
                "phone": "+90 242 000 00 00",
                "email": "info@otel.com",
                "socialLinks": {
                    "facebook": "#",
                    "instagram": "#",
                    "twitter": "#"
                }
            }
        }
    ]


TEMPLATE_CONFIGS = [
    # LUXURY (5)
    {
        "id": "luxury-grand-palace", "name": "Grand Palace", "category": "luxury",
        "description": "Gorkemli ve zarif bir luks otel sablonu. Altin ve koyu tonlar.",
        "theme": {"primaryColor": "#C5A572", "secondaryColor": "#1A1A2E", "backgroundColor": "#FFFFFF", "textColor": "#2D2D2D", "accentColor": "#8B6914", "headerFont": "'Playfair Display', serif", "bodyFont": "'Lato', sans-serif"},
        "layouts": {"hero": "fullscreen", "about": "left-image", "rooms": "grid", "gallery": "masonry", "services": "grid", "testimonials": "slider", "contact": "split"},
        "heroIdx": 0, "aboutIdx": 0
    },
    {
        "id": "luxury-royal-suite", "name": "Royal Suite", "category": "luxury",
        "description": "Kraliyet temasli, derin mavi ve altin tonlarinda luks sablon.",
        "theme": {"primaryColor": "#D4AF37", "secondaryColor": "#1B3A5C", "backgroundColor": "#F8F6F0", "textColor": "#1B3A5C", "accentColor": "#B8860B", "headerFont": "'Cormorant Garamond', serif", "bodyFont": "'Montserrat', sans-serif"},
        "layouts": {"hero": "split", "about": "right-image", "rooms": "grid", "gallery": "grid", "services": "list", "testimonials": "grid", "contact": "centered"},
        "heroIdx": 1, "aboutIdx": 1
    },
    {
        "id": "luxury-the-ritz", "name": "The Ritz", "category": "luxury",
        "description": "Siyah ve altin ile modern luks tarzinda sablon.",
        "theme": {"primaryColor": "#B8860B", "secondaryColor": "#111111", "backgroundColor": "#FAFAFA", "textColor": "#111111", "accentColor": "#DAA520", "headerFont": "'Didot', serif", "bodyFont": "'Helvetica Neue', sans-serif"},
        "layouts": {"hero": "centered", "about": "left-image", "rooms": "grid", "gallery": "grid", "services": "icons", "testimonials": "slider", "contact": "split"},
        "heroIdx": 2, "aboutIdx": 2
    },
    {
        "id": "luxury-crown-jewel", "name": "Crown Jewel", "category": "luxury",
        "description": "Bordo ve altin tonlarinda klasik luks otel sablonu.",
        "theme": {"primaryColor": "#722F37", "secondaryColor": "#2C1810", "backgroundColor": "#FDF8F5", "textColor": "#2C1810", "accentColor": "#C5A572", "headerFont": "'Libre Baskerville', serif", "bodyFont": "'Open Sans', sans-serif"},
        "layouts": {"hero": "fullscreen", "about": "right-image", "rooms": "grid", "gallery": "masonry", "services": "grid", "testimonials": "grid", "contact": "centered"},
        "heroIdx": 3, "aboutIdx": 0
    },
    {
        "id": "luxury-golden-gate", "name": "Golden Gate", "category": "luxury",
        "description": "Krem ve sicak tonlarda zarif luks sablon.",
        "theme": {"primaryColor": "#8B7355", "secondaryColor": "#2C2C2C", "backgroundColor": "#F5F0EB", "textColor": "#2C2C2C", "accentColor": "#C5A572", "headerFont": "'Playfair Display', serif", "bodyFont": "'Raleway', sans-serif"},
        "layouts": {"hero": "split", "about": "left-image", "rooms": "grid", "gallery": "grid", "services": "list", "testimonials": "slider", "contact": "split"},
        "heroIdx": 4, "aboutIdx": 1
    },
    # BOUTIQUE (5)
    {
        "id": "boutique-urban-chic", "name": "Urban Chic", "category": "boutique",
        "description": "Sehirli ve modern butik otel sablonu.",
        "theme": {"primaryColor": "#008080", "secondaryColor": "#36454F", "backgroundColor": "#FFFFFF", "textColor": "#36454F", "accentColor": "#20B2AA", "headerFont": "'Poppins', sans-serif", "bodyFont": "'Inter', sans-serif"},
        "layouts": {"hero": "centered", "about": "left-image", "rooms": "grid", "gallery": "grid", "services": "icons", "testimonials": "grid", "contact": "split"},
        "heroIdx": 5, "aboutIdx": 2
    },
    {
        "id": "boutique-cozy-corner", "name": "Cozy Corner", "category": "boutique",
        "description": "Sicak ve samimi butik otel sablonu.",
        "theme": {"primaryColor": "#8B7355", "secondaryColor": "#5C4033", "backgroundColor": "#FFF8E7", "textColor": "#3E2723", "accentColor": "#A0826D", "headerFont": "'Merriweather', serif", "bodyFont": "'Source Sans Pro', sans-serif"},
        "layouts": {"hero": "fullscreen", "about": "right-image", "rooms": "grid", "gallery": "masonry", "services": "grid", "testimonials": "slider", "contact": "centered"},
        "heroIdx": 6, "aboutIdx": 0
    },
    {
        "id": "boutique-the-loft", "name": "The Loft", "category": "boutique",
        "description": "Endustriyel tarzda modern butik sablon.",
        "theme": {"primaryColor": "#E87040", "secondaryColor": "#4A4A4A", "backgroundColor": "#F5F5F5", "textColor": "#333333", "accentColor": "#D4602E", "headerFont": "'Space Grotesk', sans-serif", "bodyFont": "'DM Sans', sans-serif"},
        "layouts": {"hero": "split", "about": "left-image", "rooms": "grid", "gallery": "grid", "services": "list", "testimonials": "grid", "contact": "split"},
        "heroIdx": 7, "aboutIdx": 1
    },
    {
        "id": "boutique-artisan-stay", "name": "Artisan Stay", "category": "boutique",
        "description": "Sanatsal ve dogal tonlarda butik sablon.",
        "theme": {"primaryColor": "#87AE73", "secondaryColor": "#5D4E37", "backgroundColor": "#FAF7F2", "textColor": "#3D3D3D", "accentColor": "#C07050", "headerFont": "'Josefin Sans', sans-serif", "bodyFont": "'Nunito', sans-serif"},
        "layouts": {"hero": "fullscreen", "about": "left-image", "rooms": "grid", "gallery": "masonry", "services": "icons", "testimonials": "slider", "contact": "centered"},
        "heroIdx": 8, "aboutIdx": 2
    },
    {
        "id": "boutique-velvet-room", "name": "Velvet Room", "category": "boutique",
        "description": "Dramatik ve sofistike butik otel sablonu.",
        "theme": {"primaryColor": "#7B3F6E", "secondaryColor": "#2D1B2E", "backgroundColor": "#FBF5F9", "textColor": "#2D1B2E", "accentColor": "#C47A9B", "headerFont": "'Italiana', serif", "bodyFont": "'Quicksand', sans-serif"},
        "layouts": {"hero": "centered", "about": "right-image", "rooms": "grid", "gallery": "grid", "services": "grid", "testimonials": "grid", "contact": "split"},
        "heroIdx": 9, "aboutIdx": 0
    },
    # RESORT & SPA (5)
    {
        "id": "resort-paradise-bay", "name": "Paradise Bay", "category": "resort",
        "description": "Tropik cennet temasli resort sablon.",
        "theme": {"primaryColor": "#00BCD4", "secondaryColor": "#006064", "backgroundColor": "#FFFFFF", "textColor": "#263238", "accentColor": "#4DD0E1", "headerFont": "'Comfortaa', sans-serif", "bodyFont": "'Karla', sans-serif"},
        "layouts": {"hero": "fullscreen", "about": "left-image", "rooms": "grid", "gallery": "masonry", "services": "icons", "testimonials": "slider", "contact": "split"},
        "heroIdx": 2, "aboutIdx": 1
    },
    {
        "id": "resort-zen-garden", "name": "Zen Garden", "category": "resort",
        "description": "Huzurlu ve dogal spa oteli sablonu.",
        "theme": {"primaryColor": "#5C8A51", "secondaryColor": "#2E4600", "backgroundColor": "#F5F0E1", "textColor": "#333333", "accentColor": "#8BC34A", "headerFont": "'Noto Serif', serif", "bodyFont": "'Noto Sans', sans-serif"},
        "layouts": {"hero": "centered", "about": "right-image", "rooms": "grid", "gallery": "grid", "services": "grid", "testimonials": "grid", "contact": "centered"},
        "heroIdx": 8, "aboutIdx": 2
    },
    {
        "id": "resort-ocean-breeze", "name": "Ocean Breeze", "category": "resort",
        "description": "Okyanus esintili, mavi tonlarda resort sablonu.",
        "theme": {"primaryColor": "#1B5E7B", "secondaryColor": "#0D3B4F", "backgroundColor": "#F0F8FF", "textColor": "#1A3C4F", "accentColor": "#87CEEB", "headerFont": "'Crimson Text', serif", "bodyFont": "'Work Sans', sans-serif"},
        "layouts": {"hero": "fullscreen", "about": "left-image", "rooms": "grid", "gallery": "masonry", "services": "list", "testimonials": "slider", "contact": "split"},
        "heroIdx": 0, "aboutIdx": 0
    },
    {
        "id": "resort-tropical-haven", "name": "Tropical Haven", "category": "resort",
        "description": "Canli renklerle tropik otel sablonu.",
        "theme": {"primaryColor": "#FF7F50", "secondaryColor": "#2E8B57", "backgroundColor": "#FFFAF5", "textColor": "#2D3436", "accentColor": "#FF6347", "headerFont": "'Abril Fatface', serif", "bodyFont": "'Lato', sans-serif"},
        "layouts": {"hero": "split", "about": "left-image", "rooms": "grid", "gallery": "grid", "services": "icons", "testimonials": "grid", "contact": "centered"},
        "heroIdx": 1, "aboutIdx": 1
    },
    {
        "id": "resort-sunset-villa", "name": "Sunset Villa", "category": "resort",
        "description": "Romantik gun batimi temasli villa sablonu.",
        "theme": {"primaryColor": "#E86420", "secondaryColor": "#8B4513", "backgroundColor": "#FFF4E6", "textColor": "#3E2723", "accentColor": "#FF8C00", "headerFont": "'Dancing Script', cursive", "bodyFont": "'Nunito Sans', sans-serif"},
        "layouts": {"hero": "fullscreen", "about": "right-image", "rooms": "grid", "gallery": "masonry", "services": "grid", "testimonials": "slider", "contact": "split"},
        "heroIdx": 4, "aboutIdx": 2
    },
    # BUSINESS (5)
    {
        "id": "business-metro-hub", "name": "Metro Hub", "category": "business",
        "description": "Kurumsal ve profesyonel is oteli sablonu.",
        "theme": {"primaryColor": "#3B82F6", "secondaryColor": "#1E293B", "backgroundColor": "#FFFFFF", "textColor": "#1E293B", "accentColor": "#60A5FA", "headerFont": "'Inter', sans-serif", "bodyFont": "'Roboto', sans-serif"},
        "layouts": {"hero": "centered", "about": "left-image", "rooms": "grid", "gallery": "grid", "services": "list", "testimonials": "grid", "contact": "split"},
        "heroIdx": 3, "aboutIdx": 0
    },
    {
        "id": "business-executive-tower", "name": "Executive Tower", "category": "business",
        "description": "Ust duzey yonetici oteli sablonu.",
        "theme": {"primaryColor": "#1E3A5F", "secondaryColor": "#0F1B2D", "backgroundColor": "#F8F9FA", "textColor": "#1E3A5F", "accentColor": "#C0C0C0", "headerFont": "'Outfit', sans-serif", "bodyFont": "'Barlow', sans-serif"},
        "layouts": {"hero": "fullscreen", "about": "right-image", "rooms": "grid", "gallery": "grid", "services": "icons", "testimonials": "slider", "contact": "centered"},
        "heroIdx": 5, "aboutIdx": 1
    },
    {
        "id": "business-city-center", "name": "City Center", "category": "business",
        "description": "Sehir merkezinde modern is oteli.",
        "theme": {"primaryColor": "#E53935", "secondaryColor": "#424242", "backgroundColor": "#FAFAFA", "textColor": "#333333", "accentColor": "#FF5252", "headerFont": "'Montserrat', sans-serif", "bodyFont": "'Source Sans Pro', sans-serif"},
        "layouts": {"hero": "split", "about": "left-image", "rooms": "grid", "gallery": "masonry", "services": "grid", "testimonials": "grid", "contact": "split"},
        "heroIdx": 6, "aboutIdx": 2
    },
    {
        "id": "business-prime", "name": "Prime Business", "category": "business",
        "description": "Temiz ve profesyonel is otel sablonu.",
        "theme": {"primaryColor": "#10B981", "secondaryColor": "#1B2A4A", "backgroundColor": "#FFFFFF", "textColor": "#1F2937", "accentColor": "#34D399", "headerFont": "'Space Grotesk', sans-serif", "bodyFont": "'DM Sans', sans-serif"},
        "layouts": {"hero": "centered", "about": "left-image", "rooms": "grid", "gallery": "grid", "services": "list", "testimonials": "slider", "contact": "centered"},
        "heroIdx": 7, "aboutIdx": 0
    },
    {
        "id": "business-corporate-suite", "name": "Corporate Suite", "category": "business",
        "description": "Kurumsal zarafet suiten otel sablonu.",
        "theme": {"primaryColor": "#D4AF37", "secondaryColor": "#1A1A1A", "backgroundColor": "#FAFAFA", "textColor": "#1A1A1A", "accentColor": "#B8860B", "headerFont": "'Playfair Display', serif", "bodyFont": "'Roboto', sans-serif"},
        "layouts": {"hero": "fullscreen", "about": "right-image", "rooms": "grid", "gallery": "masonry", "services": "icons", "testimonials": "grid", "contact": "split"},
        "heroIdx": 9, "aboutIdx": 1
    },
    # BEACH (4)
    {
        "id": "beach-coastal-dreams", "name": "Coastal Dreams", "category": "beach",
        "description": "Sahil ruyasi temasli otel sablonu.",
        "theme": {"primaryColor": "#4ECDC4", "secondaryColor": "#2C3E50", "backgroundColor": "#F0FFFE", "textColor": "#2C3E50", "accentColor": "#F4A460", "headerFont": "'Caveat', cursive", "bodyFont": "'Poppins', sans-serif"},
        "layouts": {"hero": "fullscreen", "about": "left-image", "rooms": "grid", "gallery": "masonry", "services": "icons", "testimonials": "slider", "contact": "split"},
        "heroIdx": 0, "aboutIdx": 2
    },
    {
        "id": "beach-seaside-escape", "name": "Seaside Escape", "category": "beach",
        "description": "Turkuaz tonlarda deniz kenari sablonu.",
        "theme": {"primaryColor": "#40E0D0", "secondaryColor": "#1A5276", "backgroundColor": "#FFFFFF", "textColor": "#2C3E50", "accentColor": "#48C9B0", "headerFont": "'Josefin Sans', sans-serif", "bodyFont": "'Open Sans', sans-serif"},
        "layouts": {"hero": "split", "about": "right-image", "rooms": "grid", "gallery": "grid", "services": "grid", "testimonials": "grid", "contact": "centered"},
        "heroIdx": 2, "aboutIdx": 0
    },
    {
        "id": "beach-blue-lagoon", "name": "Blue Lagoon", "category": "beach",
        "description": "Derin mavi tonlarda dramatik sahil sablonu.",
        "theme": {"primaryColor": "#006994", "secondaryColor": "#002244", "backgroundColor": "#F5FAFF", "textColor": "#003366", "accentColor": "#00CED1", "headerFont": "'Cinzel', serif", "bodyFont": "'Lato', sans-serif"},
        "layouts": {"hero": "fullscreen", "about": "left-image", "rooms": "grid", "gallery": "masonry", "services": "list", "testimonials": "slider", "contact": "split"},
        "heroIdx": 1, "aboutIdx": 1
    },
    {
        "id": "beach-sandy-shores", "name": "Sandy Shores", "category": "beach",
        "description": "Kumsal temasli rahat sahil oteli sablonu.",
        "theme": {"primaryColor": "#DEB887", "secondaryColor": "#8B6914", "backgroundColor": "#FFFEF7", "textColor": "#5D4E37", "accentColor": "#4169E1", "headerFont": "'Lobster', cursive", "bodyFont": "'Raleway', sans-serif"},
        "layouts": {"hero": "centered", "about": "right-image", "rooms": "grid", "gallery": "grid", "services": "icons", "testimonials": "grid", "contact": "centered"},
        "heroIdx": 4, "aboutIdx": 2
    },
    # MOUNTAIN (3)
    {
        "id": "mountain-alpine-lodge", "name": "Alpine Lodge", "category": "mountain",
        "description": "Dag evi temasli rustik otel sablonu.",
        "theme": {"primaryColor": "#5D7B3A", "secondaryColor": "#2E4600", "backgroundColor": "#F5F2EB", "textColor": "#2E2E2E", "accentColor": "#8B4513", "headerFont": "'Cabin', sans-serif", "bodyFont": "'Merriweather', serif"},
        "layouts": {"hero": "fullscreen", "about": "left-image", "rooms": "grid", "gallery": "masonry", "services": "grid", "testimonials": "slider", "contact": "split"},
        "heroIdx": 8, "aboutIdx": 0
    },
    {
        "id": "mountain-retreat", "name": "Mountain Retreat", "category": "mountain",
        "description": "Dogayla ic ice dag oteli sablonu.",
        "theme": {"primaryColor": "#696969", "secondaryColor": "#2F4F2F", "backgroundColor": "#F8F8F0", "textColor": "#333333", "accentColor": "#228B22", "headerFont": "'Libre Baskerville', serif", "bodyFont": "'Karla', sans-serif"},
        "layouts": {"hero": "split", "about": "right-image", "rooms": "grid", "gallery": "grid", "services": "list", "testimonials": "grid", "contact": "centered"},
        "heroIdx": 6, "aboutIdx": 1
    },
    {
        "id": "mountain-pine-valley", "name": "Pine Valley", "category": "mountain",
        "description": "Cam ormanlarinda huzurlu dag oteli.",
        "theme": {"primaryColor": "#2E7D32", "secondaryColor": "#1B5E20", "backgroundColor": "#FAEBD7", "textColor": "#263238", "accentColor": "#4CAF50", "headerFont": "'Cormorant', serif", "bodyFont": "'Work Sans', sans-serif"},
        "layouts": {"hero": "centered", "about": "left-image", "rooms": "grid", "gallery": "masonry", "services": "icons", "testimonials": "slider", "contact": "split"},
        "heroIdx": 7, "aboutIdx": 2
    },
    # CITY (3)
    {
        "id": "city-downtown-living", "name": "Downtown Living", "category": "city",
        "description": "Minimalist siyah-beyaz sehir oteli sablonu.",
        "theme": {"primaryColor": "#000000", "secondaryColor": "#1A1A1A", "backgroundColor": "#FFFFFF", "textColor": "#1A1A1A", "accentColor": "#FF4444", "headerFont": "'Bebas Neue', sans-serif", "bodyFont": "'Inter', sans-serif"},
        "layouts": {"hero": "fullscreen", "about": "left-image", "rooms": "grid", "gallery": "grid", "services": "list", "testimonials": "slider", "contact": "split"},
        "heroIdx": 3, "aboutIdx": 0
    },
    {
        "id": "city-metro-style", "name": "Metro Style", "category": "city",
        "description": "Cagdas ve dinamik sehir oteli sablonu.",
        "theme": {"primaryColor": "#00B4D8", "secondaryColor": "#023E8A", "backgroundColor": "#F8FAFC", "textColor": "#1E293B", "accentColor": "#00FFD5", "headerFont": "'Space Grotesk', sans-serif", "bodyFont": "'Sora', sans-serif"},
        "layouts": {"hero": "split", "about": "right-image", "rooms": "grid", "gallery": "masonry", "services": "icons", "testimonials": "grid", "contact": "centered"},
        "heroIdx": 5, "aboutIdx": 1
    },
    {
        "id": "city-urban-escape", "name": "Urban Escape", "category": "city",
        "description": "Trendy ve sicak sehir oteli sablonu.",
        "theme": {"primaryColor": "#FFBF00", "secondaryColor": "#5D4E37", "backgroundColor": "#FAFAF5", "textColor": "#3D3D3D", "accentColor": "#F59E0B", "headerFont": "'DM Serif Display', serif", "bodyFont": "'DM Sans', sans-serif"},
        "layouts": {"hero": "fullscreen", "about": "left-image", "rooms": "grid", "gallery": "grid", "services": "grid", "testimonials": "slider", "contact": "split"},
        "heroIdx": 9, "aboutIdx": 2
    },
]


def generate_all_templates():
    templates = []
    for cfg in TEMPLATE_CONFIGS:
        hero_img = HERO_IMAGES[cfg.get("heroIdx", 0) % len(HERO_IMAGES)]
        about_img = ABOUT_IMAGES[cfg.get("aboutIdx", 0) % len(ABOUT_IMAGES)]
        room_imgs = ROOM_IMAGES[:3]
        gallery_imgs = GALLERY_IMAGES[:6]
        sections = make_sections(hero_img, about_img, room_imgs, gallery_imgs, cfg["layouts"])
        templates.append({
            "id": cfg["id"],
            "name": cfg["name"],
            "category": cfg["category"],
            "description": cfg["description"],
            "thumbnail": hero_img,
            "theme": cfg["theme"],
            "sections": sections,
            "is_custom": False,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        })
    return templates
