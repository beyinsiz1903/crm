import uuid
from datetime import datetime, timezone

# ============================================================
# IMAGE POOLS
# ============================================================

HOTEL_HERO_IMAGES = [
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
    "https://images.unsplash.com/photo-1519302959554-a75be0afc82a?w=1600&q=80",
    "https://images.unsplash.com/photo-1590490360182-c33d955e1740?w=1600&q=80",
]

HOTEL_ROOM_IMAGES = [
    "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=800&q=80",
    "https://images.unsplash.com/photo-1618773928121-c32242e63f39?w=800&q=80",
    "https://images.unsplash.com/photo-1590490360182-c33d955e1740?w=800&q=80",
    "https://images.unsplash.com/photo-1596394516093-501ba68a0ba6?w=800&q=80",
    "https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=800&q=80",
    "https://images.unsplash.com/photo-1611892440504-42a792e24d32?w=800&q=80",
]

HOTEL_GALLERY_IMAGES = [
    "https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=600&q=80",
    "https://images.unsplash.com/photo-1584132967334-10e028bd69f7?w=600&q=80",
    "https://images.unsplash.com/photo-1560200353-ce0a76b1d438?w=600&q=80",
    "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=600&q=80",
    "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=600&q=80",
    "https://images.unsplash.com/photo-1445019980597-93fa8acb246c?w=600&q=80",
    "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=600&q=80",
    "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=600&q=80",
]

HOTEL_ABOUT_IMAGES = [
    "https://images.unsplash.com/photo-1455587734955-081b22074882?w=800&q=80",
    "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800&q=80",
    "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800&q=80",
    "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
]

RESTAURANT_HERO_IMAGES = [
    "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=1600&q=80",
    "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=1600&q=80",
    "https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=1600&q=80",
    "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=1600&q=80",
    "https://images.unsplash.com/photo-1559339352-11d035aa65de?w=1600&q=80",
    "https://images.unsplash.com/photo-1551632436-cbf8dd35adfa?w=1600&q=80",
    "https://images.unsplash.com/photo-1578474846511-04ba529f0b88?w=1600&q=80",
    "https://images.unsplash.com/photo-1590846406792-0adc7f938f1d?w=1600&q=80",
    "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=1600&q=80",
    "https://images.unsplash.com/photo-1537047902294-62a40c20a6ae?w=1600&q=80",
    "https://images.unsplash.com/photo-1600891964092-4316c288032e?w=1600&q=80",
    "https://images.unsplash.com/photo-1424847651672-bf20a4b0982b?w=1600&q=80",
]

RESTAURANT_DISH_IMAGES = [
    "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800&q=80",
    "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=800&q=80",
    "https://images.unsplash.com/photo-1565958011703-44f9829ba187?w=800&q=80",
    "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=800&q=80",
    "https://images.unsplash.com/photo-1546793665-c74683f339c1?w=800&q=80",
    "https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=800&q=80",
    "https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=800&q=80",
    "https://images.unsplash.com/photo-1551024506-0bccd828d307?w=800&q=80",
    "https://images.unsplash.com/photo-1551782450-a2132b4ba21d?w=800&q=80",
    "https://images.unsplash.com/photo-1544025162-d76694265947?w=800&q=80",
    "https://images.unsplash.com/photo-1432139509613-5c4255815697?w=800&q=80",
    "https://images.unsplash.com/photo-1484723091739-30a097e8f929?w=800&q=80",
]

RESTAURANT_GALLERY_IMAGES = [
    "https://images.unsplash.com/photo-1555992336-fb0d29498b13?w=600&q=80",
    "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=600&q=80",
    "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=600&q=80",
    "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=600&q=80",
    "https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=600&q=80",
    "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=600&q=80",
    "https://images.unsplash.com/photo-1559339352-11d035aa65de?w=600&q=80",
    "https://images.unsplash.com/photo-1551632436-cbf8dd35adfa?w=600&q=80",
]

RESTAURANT_ABOUT_IMAGES = [
    "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&q=80",
    "https://images.unsplash.com/photo-1550966871-3ed3cdb5ed0c?w=800&q=80",
    "https://images.unsplash.com/photo-1578474846511-04ba529f0b88?w=800&q=80",
    "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=800&q=80",
]

AGENCY_HERO_IMAGES = [
    "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=1600&q=80",
    "https://images.unsplash.com/photo-1488085061387-422e29b40080?w=1600&q=80",
    "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=1600&q=80",
    "https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?w=1600&q=80",
    "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1600&q=80",
    "https://images.unsplash.com/photo-1528127269322-539801943592?w=1600&q=80",
    "https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=1600&q=80",
    "https://images.unsplash.com/photo-1506929562872-bb421503ef21?w=1600&q=80",
    "https://images.unsplash.com/photo-1530521954074-e64f6810b32d?w=1600&q=80",
    "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=1600&q=80",
    "https://images.unsplash.com/photo-1533105079780-92b9be482077?w=1600&q=80",
    "https://images.unsplash.com/photo-1524850011238-e3d235c7d4c9?w=1600&q=80",
]

AGENCY_TOUR_IMAGES = [
    "https://images.unsplash.com/photo-1548013146-72479768bada?w=800&q=80",
    "https://images.unsplash.com/photo-1539650116574-75c0c6d73f6e?w=800&q=80",
    "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=800&q=80",
    "https://images.unsplash.com/photo-1506973035872-a4ec16b8e8d9?w=800&q=80",
    "https://images.unsplash.com/photo-1467269204594-9661b134dd2b?w=800&q=80",
    "https://images.unsplash.com/photo-1530789253388-582c481c54b0?w=800&q=80",
    "https://images.unsplash.com/photo-1504214208698-ea1916a2195a?w=800&q=80",
    "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=80",
    "https://images.unsplash.com/photo-1523906834658-6e24ef2386f9?w=800&q=80",
    "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&q=80",
]

AGENCY_GALLERY_IMAGES = [
    "https://images.unsplash.com/photo-1488085061387-422e29b40080?w=600&q=80",
    "https://images.unsplash.com/photo-1433086966358-54859d0ed716?w=600&q=80",
    "https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=600&q=80",
    "https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?w=600&q=80",
    "https://images.unsplash.com/photo-1506929562872-bb421503ef21?w=600&q=80",
    "https://images.unsplash.com/photo-1530521954074-e64f6810b32d?w=600&q=80",
    "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=600&q=80",
    "https://images.unsplash.com/photo-1533105079780-92b9be482077?w=600&q=80",
]

AGENCY_ABOUT_IMAGES = [
    "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=800&q=80",
    "https://images.unsplash.com/photo-1551836022-deb4988cc6c0?w=800&q=80",
    "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=800&q=80",
]


# ============================================================
# HOTEL SECTION BUILDER
# ============================================================

def make_hotel_sections(hero_img, about_img, room_imgs, gallery_imgs, layouts, include_restaurant=False):
    sections = [
        {
            "id": str(uuid.uuid4()),
            "type": "header",
            "title": "Header",
            "visible": True,
            "props": {
                "hotelName": "Otel Adi",
                "logo": "",
                "menuItems": ["Anasayfa", "Hakkimizda", "Odalar", "Galeri", "Iletisim"],
                "style": layouts.get("header", "transparent"),
            },
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
                "overlayOpacity": "0.5",
            },
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
                "layout": layouts.get("about", "left-image"),
            },
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
                    {"name": "Deluxe Oda", "description": "Genis alan ve premium donanimlarla donanimli.", "image": room_imgs[1 % len(room_imgs)], "price": "850 TL", "features": ["Wi-Fi", "Klima", "Mini Bar", "Deniz Manzarasi"]},
                    {"name": "Suite", "description": "Luks ve konforun en ust seviyesi.", "image": room_imgs[2 % len(room_imgs)], "price": "1500 TL", "features": ["Wi-Fi", "Klima", "Mini Bar", "Jakuzi", "Ozel Teras"]},
                ],
                "layout": layouts.get("rooms", "grid"),
            },
        },
    ]

    if include_restaurant:
        sections.append({
            "id": str(uuid.uuid4()),
            "type": "menu",
            "title": "Restoran",
            "visible": True,
            "props": {
                "title": "Otel Restoranimiz",
                "subtitle": "Sef imzali lezzetler ve zarif bir ortam",
                "items": [
                    {"name": "Kahvalti Acik Bufesi", "description": "Zengin secenekli kahvalti bufesi.", "image": RESTAURANT_DISH_IMAGES[0], "price": "450 TL"},
                    {"name": "A La Carte Aksam Yemegi", "description": "Sef imzali ozel menu secenekleri.", "image": RESTAURANT_DISH_IMAGES[1], "price": "850 TL"},
                    {"name": "Ozel Akdeniz Tabagi", "description": "Mevsim urunleriyle hazirlanan zarif tabak.", "image": RESTAURANT_DISH_IMAGES[2], "price": "650 TL"},
                ],
                "layout": layouts.get("menu", "grid"),
            },
        })

    sections.extend([
        {
            "id": str(uuid.uuid4()),
            "type": "gallery",
            "title": "Galeri",
            "visible": True,
            "props": {
                "title": "Foto Galeri",
                "images": [{"url": img, "alt": f"Otel Gorsel {i+1}"} for i, img in enumerate(gallery_imgs)],
                "layout": layouts.get("gallery", "grid"),
            },
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
                    {"name": "Transfer", "icon": "transfer", "description": "Havaalani transfer hizmeti."},
                ],
                "layout": layouts.get("services", "grid"),
            },
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
                    {"name": "Zeynep K.", "text": "Muhtesem manzara ve kusursuz hizmet. Kesinlikle tekrar gelecegiz.", "rating": 5},
                    {"name": "Mehmet A.", "text": "Is seyahati icin ideal. Her sey dusunulmus.", "rating": 4},
                ],
                "layout": layouts.get("testimonials", "slider"),
            },
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
                "layout": layouts.get("contact", "split"),
            },
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
                "socialLinks": {"facebook": "#", "instagram": "#", "twitter": "#"},
            },
        },
    ])
    return sections


# ============================================================
# RESTAURANT SECTION BUILDER
# ============================================================

def make_restaurant_sections(hero_img, about_img, dish_imgs, gallery_imgs, layouts, cuisine="Akdeniz"):
    cuisine_items = {
        "Akdeniz": [
            ("Mezeler Tabagi", "Humus, cacik, kisir, patlican salata", "180 TL"),
            ("Izgara Levrek", "Mevsim sebzeleri ile taze levrek", "420 TL"),
            ("Kuzu Sis", "El acmasi lavas ve soslariyla", "380 TL"),
            ("Kunefe", "Antep fistigi ile sicak servis", "150 TL"),
        ],
        "Italyan": [
            ("Bruschetta Trio", "Uc farkli lezzet, taze fesleğen", "140 TL"),
            ("Trufflu Risotto", "Parmesan ve siyah trufel ile", "380 TL"),
            ("Tagliatelle Bolognese", "Ev yapimi makarna, dana bonfile", "320 TL"),
            ("Tiramisu", "Ikramiya mascarpone ve espresso", "160 TL"),
        ],
        "Suşi": [
            ("Salmon Sashimi", "Taze atlantik somon", "280 TL"),
            ("Dragon Roll", "Tempura karides, avokado", "320 TL"),
            ("Beef Tataki", "Wagyu dana, ponzu sos", "450 TL"),
            ("Mochi Ice Cream", "Uc farkli aroma", "140 TL"),
        ],
        "Steakhouse": [
            ("Dry Aged Ribeye", "28 gun dinlendirilmis 350g bonfile", "980 TL"),
            ("Bone-in Tomahawk", "900g, iki kisilik", "1.850 TL"),
            ("Wagyu Burger", "Japon wagyu, trufflu mayo", "520 TL"),
            ("Creme Brulee", "Vanilyali, karamelize", "170 TL"),
        ],
        "Kafe": [
            ("Ozel Kahve Tabagi", "3 cesit kahve degustasyonu", "160 TL"),
            ("Eggs Benedict", "Kacak yumurta, hollandaise sos", "220 TL"),
            ("Avokado Toast", "Cherry domates, fetapeyniri", "180 TL"),
            ("Cheesecake", "Orman meyveli, ev yapimi", "140 TL"),
        ],
        "Türk Mutfagi": [
            ("Iskender Kebap", "El acmasi yufka, domates sos, yogurt", "320 TL"),
            ("Adana Durum", "Tam acili, sumak ve sogan", "180 TL"),
            ("Manti", "Kayseri usulu, yogurtlu tereyag", "240 TL"),
            ("Baklava", "Antep fistikli, 6 dilim", "190 TL"),
        ],
        "Deniz Urunleri": [
            ("Karides Guvec", "Krema ve kasar peyniri", "380 TL"),
            ("Kalamar Tava", "El acmasi tartar sos", "260 TL"),
            ("Izgara Cupra", "Limonlu zeytinyagi", "420 TL"),
            ("Midye Dolma", "12 adet, limonlu", "180 TL"),
        ],
        "Veggie": [
            ("Quinoa Buddha Bowl", "Kinoa, humus, avokado, yesil sebze", "220 TL"),
            ("Vegan Burger", "Bitki bazli, houmous soslu", "180 TL"),
            ("Carrot Cake", "Tarcin ve cevizli", "140 TL"),
            ("Cold Press Juice", "Yesil detoks, 300 ml", "90 TL"),
        ],
    }
    items_src = cuisine_items.get(cuisine, cuisine_items["Akdeniz"])
    menu_items = [
        {
            "name": name,
            "description": desc,
            "image": dish_imgs[i % len(dish_imgs)],
            "price": price,
        }
        for i, (name, desc, price) in enumerate(items_src)
    ]

    return [
        {
            "id": str(uuid.uuid4()),
            "type": "header",
            "title": "Header",
            "visible": True,
            "props": {
                "hotelName": "Restoran Adi",
                "logo": "",
                "menuItems": ["Anasayfa", "Hakkimizda", "Menu", "Galeri", "Iletisim"],
                "style": layouts.get("header", "transparent"),
            },
        },
        {
            "id": str(uuid.uuid4()),
            "type": "hero",
            "title": "Hero",
            "visible": True,
            "props": {
                "title": f"{cuisine} Mutfagindan Essiz Lezzetler",
                "subtitle": "Taze malzemeler, ozenli sunum, unutulmaz tatlar",
                "backgroundImage": hero_img,
                "ctaText": "Rezervasyon Yap",
                "ctaLink": "#iletisim",
                "layout": layouts.get("hero", "fullscreen"),
                "overlayOpacity": "0.55",
            },
        },
        {
            "id": str(uuid.uuid4()),
            "type": "about",
            "title": "Hakkimizda",
            "visible": True,
            "props": {
                "title": "Bizim Hikayemiz",
                "description": f"Sef ve ekibimizin tutkusu, her tabagimizda kendini gosterir. {cuisine} mutfaginin zengin lezzetlerini, yerli ve mevsimlik malzemelerle modern bir yorumla masaniza getiriyoruz. Sicak atmosferimiz ve ozenli servisimizle, her ziyaretinizi ozel bir deneyime donusturuyoruz.",
                "image": about_img,
                "layout": layouts.get("about", "left-image"),
            },
        },
        {
            "id": str(uuid.uuid4()),
            "type": "menu",
            "title": "Menu",
            "visible": True,
            "props": {
                "title": "Ozel Menumuz",
                "subtitle": "Sef secimi ve imza lezzetler",
                "items": menu_items,
                "layout": layouts.get("menu", "grid"),
            },
        },
        {
            "id": str(uuid.uuid4()),
            "type": "gallery",
            "title": "Galeri",
            "visible": True,
            "props": {
                "title": "Foto Galeri",
                "images": [{"url": img, "alt": f"Restoran Gorsel {i+1}"} for i, img in enumerate(gallery_imgs)],
                "layout": layouts.get("gallery", "grid"),
            },
        },
        {
            "id": str(uuid.uuid4()),
            "type": "services",
            "title": "Ozelliklerimiz",
            "visible": True,
            "props": {
                "title": "Neden Biz?",
                "services": [
                    {"name": "Taze Malzeme", "icon": "restaurant", "description": "Her gun yerli urunlerle hazirlanan taze tabaklar."},
                    {"name": "Sef Imzali", "icon": "spa", "description": "Deneyimli seflerimizden ozel lezzetler."},
                    {"name": "Sicak Atmosfer", "icon": "pool", "description": "Rahat, sik ve davetkar ortam."},
                    {"name": "Rezervasyon", "icon": "parking", "description": "Online rezervasyon ile masaniz hazir."},
                    {"name": "Etkinlik Mekani", "icon": "transfer", "description": "Ozel gununuz icin tum mekan."},
                    {"name": "Paket Servis", "icon": "fitness", "description": "Eve ve ofise lezzet tasima."},
                ],
                "layout": layouts.get("services", "grid"),
            },
        },
        {
            "id": str(uuid.uuid4()),
            "type": "testimonials",
            "title": "Yorumlar",
            "visible": True,
            "props": {
                "title": "Misafir Yorumlari",
                "testimonials": [
                    {"name": "Burak T.", "text": "Lezzetler muhtesem, servis kusursuz. Tekrar gelecegiz.", "rating": 5},
                    {"name": "Selin O.", "text": "Ozel gun kutlamasi icin mukemmel bir mekan.", "rating": 5},
                    {"name": "Can D.", "text": "Sef imzali tabaklar gercekten farkli.", "rating": 4},
                ],
                "layout": layouts.get("testimonials", "slider"),
            },
        },
        {
            "id": str(uuid.uuid4()),
            "type": "contact",
            "title": "Iletisim",
            "visible": True,
            "props": {
                "title": "Rezervasyon ve Iletisim",
                "address": "Ornek Mahallesi, Restoran Caddesi No:1, Istanbul",
                "phone": "+90 212 000 00 00",
                "email": "info@restoran.com",
                "mapUrl": "",
                "layout": layouts.get("contact", "split"),
            },
        },
        {
            "id": str(uuid.uuid4()),
            "type": "footer",
            "title": "Footer",
            "visible": True,
            "props": {
                "hotelName": "Restoran Adi",
                "address": "Ornek Mahallesi, Restoran Caddesi No:1, Istanbul",
                "phone": "+90 212 000 00 00",
                "email": "info@restoran.com",
                "socialLinks": {"facebook": "#", "instagram": "#", "twitter": "#"},
            },
        },
    ]


# ============================================================
# AGENCY (ACENTE) SECTION BUILDER
# ============================================================

def make_agency_sections(hero_img, about_img, tour_imgs, gallery_imgs, layouts, focus="Yurtdisi"):
    focus_tours = {
        "Yurtdisi": [
            ("Paris & Disneyland Turu", "5 gece 6 gun, 4* otel, rehberli", "14.900 TL", "6 Gun"),
            ("Dubai Expo Turu", "4 gece 5 gun, 5* otel, tur+transfer", "19.500 TL", "5 Gun"),
            ("Barcelona & Madrid", "6 gece 7 gun, otel, ucus dahil", "24.800 TL", "7 Gun"),
            ("Bali Cennet Turu", "7 gece 8 gun, villa konaklama", "34.500 TL", "8 Gun"),
        ],
        "Yurtici": [
            ("Kapadokya Balon Turu", "2 gece 3 gun, balon turu dahil", "4.200 TL", "3 Gun"),
            ("Karadeniz Yaylalari", "3 gece 4 gun, butik oteller", "5.900 TL", "4 Gun"),
            ("GAP Turu", "4 gece 5 gun, rehberli, tum muzeler", "6.500 TL", "5 Gun"),
            ("Ege Kiyilari Turu", "5 gece 6 gun, premium kategori", "8.900 TL", "6 Gun"),
        ],
        "Kultur": [
            ("Istanbul Klasik Turu", "2 gece 3 gun, tarihi yarimada", "2.900 TL", "3 Gun"),
            ("Efes & Pamukkale", "3 gece 4 gun, antik kentler", "4.800 TL", "4 Gun"),
            ("Likya Yolu Yuruyusu", "5 gece 6 gun, kamp+otel", "6.200 TL", "6 Gun"),
            ("Mardin & Midyat", "3 gece 4 gun, tarih ve kultur", "5.400 TL", "4 Gun"),
        ],
        "Macera": [
            ("Rafting Macera Turu", "1 gun, tam ekipman dahil", "1.200 TL", "1 Gun"),
            ("Heliski Kackar", "3 gece 4 gun, rehberli", "28.500 TL", "4 Gun"),
            ("Dalgic Sertifikasi", "5 gun, PADI Open Water", "12.900 TL", "5 Gun"),
            ("Paragliding Olu Deniz", "Tandem atlayis, video dahil", "2.400 TL", "1 Gun"),
        ],
        "Balayi": [
            ("Maldivler Balayi", "7 gece 8 gun, su ustu bungalov", "89.500 TL", "8 Gun"),
            ("Bodrum Luks Villa", "5 gece 6 gun, ozel havuzlu villa", "24.500 TL", "6 Gun"),
            ("Santorini Balayi", "4 gece 5 gun, kalder manzarali", "31.800 TL", "5 Gun"),
            ("Phuket Romantik", "6 gece 7 gun, spa paketi dahil", "42.300 TL", "7 Gun"),
        ],
        "Transfer": [
            ("Havaalani Transfer", "VIP arac, 7/24 hizmet", "650 TL", "Tek Yon"),
            ("Sehir Turu Transfer", "Tam gun, rehberli", "2.200 TL", "1 Gun"),
            ("Uzun Yol Transfer", "Mercedes Vito, su ve ikram", "Teklifle", "Esnek"),
            ("Grup Transfer", "16 kisilik minibus", "4.500 TL", "Tek Yon"),
        ],
        "Hac Umre": [
            ("Umre Programi - 10 Gun", "Mekke+Medine, 4* otel", "42.500 TL", "10 Gun"),
            ("Umre Programi - 15 Gun", "Tam pansiyon, rehberli", "54.800 TL", "15 Gun"),
            ("Hac Programi", "Kura ile genis paket", "Basvuruyla", "Ozel"),
            ("Kuds Ziyareti", "4 gece 5 gun, kutsal topraklar", "28.900 TL", "5 Gun"),
        ],
    }
    items_src = focus_tours.get(focus, focus_tours["Yurtdisi"])
    tours = [
        {
            "name": name,
            "description": desc,
            "image": tour_imgs[i % len(tour_imgs)],
            "price": price,
            "duration": duration,
        }
        for i, (name, desc, price, duration) in enumerate(items_src)
    ]

    return [
        {
            "id": str(uuid.uuid4()),
            "type": "header",
            "title": "Header",
            "visible": True,
            "props": {
                "hotelName": "Acente Adi",
                "logo": "",
                "menuItems": ["Anasayfa", "Hakkimizda", "Turlar", "Galeri", "Iletisim"],
                "style": layouts.get("header", "transparent"),
            },
        },
        {
            "id": str(uuid.uuid4()),
            "type": "hero",
            "title": "Hero",
            "visible": True,
            "props": {
                "title": "Hayalinizdeki Tatil Burada Baslar",
                "subtitle": f"{focus} turlari, ozel paketler ve guvenli rezervasyon",
                "backgroundImage": hero_img,
                "ctaText": "Turlari Incele",
                "ctaLink": "#turlar",
                "layout": layouts.get("hero", "fullscreen"),
                "overlayOpacity": "0.5",
            },
        },
        {
            "id": str(uuid.uuid4()),
            "type": "about",
            "title": "Hakkimizda",
            "visible": True,
            "props": {
                "title": "Biz Kimiz?",
                "description": f"Tursab belgeli bir seyahat acentasi olarak, yillardir binlerce misafirimize unutulmaz tatiller yasattik. {focus} turlarinda uzmanlasmis ekibimiz, her detayi sizin icin planliyor. Guvenli rezervasyon, 7/24 destek ve en uygun fiyat garantisi ile hayalinizdeki seyahati gerceklestiriyoruz.",
                "image": about_img,
                "layout": layouts.get("about", "left-image"),
            },
        },
        {
            "id": str(uuid.uuid4()),
            "type": "tours",
            "title": "Turlar",
            "visible": True,
            "props": {
                "title": "One Cikan Turlar",
                "subtitle": "Secilmis tur paketleri ve erken rezervasyon firsatlari",
                "tours": tours,
                "layout": layouts.get("tours", "grid"),
            },
        },
        {
            "id": str(uuid.uuid4()),
            "type": "gallery",
            "title": "Galeri",
            "visible": True,
            "props": {
                "title": "Galeri",
                "images": [{"url": img, "alt": f"Seyahat Gorsel {i+1}"} for i, img in enumerate(gallery_imgs)],
                "layout": layouts.get("gallery", "grid"),
            },
        },
        {
            "id": str(uuid.uuid4()),
            "type": "services",
            "title": "Hizmetler",
            "visible": True,
            "props": {
                "title": "Hizmetlerimiz",
                "services": [
                    {"name": "Ucak Bileti", "icon": "transfer", "description": "Tum dunya ucus bileti rezervasyonu."},
                    {"name": "Otel Rezervasyonu", "icon": "pool", "description": "Global otel zincirleri ile anlasmali."},
                    {"name": "Vize Islemleri", "icon": "parking", "description": "Ornek basvuru ve takip hizmeti."},
                    {"name": "Seyahat Sigortasi", "icon": "spa", "description": "Genis teminatli sigorta paketleri."},
                    {"name": "Arac Kiralama", "icon": "fitness", "description": "Global arac kiralama partnerlikleri."},
                    {"name": "Rehberli Turlar", "icon": "restaurant", "description": "Profesyonel yerel rehberler."},
                ],
                "layout": layouts.get("services", "grid"),
            },
        },
        {
            "id": str(uuid.uuid4()),
            "type": "testimonials",
            "title": "Yorumlar",
            "visible": True,
            "props": {
                "title": "Misafir Yorumlari",
                "testimonials": [
                    {"name": "Ece K.", "text": "Tatil planlamasi cok kolaydi, her sey dusunulmustu.", "rating": 5},
                    {"name": "Emre S.", "text": "Rehberimiz harikaydi. Programimiz kusursuz akti.", "rating": 5},
                    {"name": "Dilara A.", "text": "Fiyat-performans acisindan cok iyi, tavsiye ederim.", "rating": 4},
                ],
                "layout": layouts.get("testimonials", "slider"),
            },
        },
        {
            "id": str(uuid.uuid4()),
            "type": "contact",
            "title": "Iletisim",
            "visible": True,
            "props": {
                "title": "Bize Ulasin",
                "address": "Ornek Mahallesi, Acente Caddesi No:1, Istanbul",
                "phone": "+90 212 000 00 00",
                "email": "info@acente.com",
                "mapUrl": "",
                "layout": layouts.get("contact", "split"),
            },
        },
        {
            "id": str(uuid.uuid4()),
            "type": "footer",
            "title": "Footer",
            "visible": True,
            "props": {
                "hotelName": "Acente Adi",
                "address": "Ornek Mahallesi, Acente Caddesi No:1, Istanbul",
                "phone": "+90 212 000 00 00",
                "email": "info@acente.com",
                "socialLinks": {"facebook": "#", "instagram": "#", "twitter": "#"},
            },
        },
    ]


# ============================================================
# TEMPLATE CONFIGS
# ============================================================

# ---------- HOTEL CONFIGS (40) ----------
HOTEL_CONFIGS = [
    # LUXURY (8)
    {"id": "hotel-grand-palace", "name": "Grand Palace", "category": "luxury", "description": "Gorkemli ve zarif luks otel sablonu. Altin ve koyu tonlar.",
     "theme": {"primaryColor": "#C5A572", "secondaryColor": "#1A1A2E", "backgroundColor": "#FFFFFF", "textColor": "#2D2D2D", "accentColor": "#8B6914", "headerFont": "'Playfair Display', serif", "bodyFont": "'Lato', sans-serif"},
     "layouts": {"hero": "fullscreen", "about": "left-image", "rooms": "grid", "gallery": "masonry", "services": "grid", "testimonials": "slider", "contact": "split"}, "heroIdx": 0, "aboutIdx": 0},
    {"id": "hotel-royal-suite", "name": "Royal Suite", "category": "luxury", "description": "Kraliyet temali, derin mavi ve altin tonlarinda luks sablon.",
     "theme": {"primaryColor": "#D4AF37", "secondaryColor": "#1B3A5C", "backgroundColor": "#F8F6F0", "textColor": "#1B3A5C", "accentColor": "#B8860B", "headerFont": "'Cormorant Garamond', serif", "bodyFont": "'Montserrat', sans-serif"},
     "layouts": {"hero": "split", "about": "right-image", "rooms": "grid", "gallery": "grid", "services": "list", "testimonials": "grid", "contact": "centered"}, "heroIdx": 1, "aboutIdx": 1},
    {"id": "hotel-the-ritz", "name": "The Ritz", "category": "luxury", "description": "Siyah ve altin ile modern luks tarzi.",
     "theme": {"primaryColor": "#B8860B", "secondaryColor": "#111111", "backgroundColor": "#FAFAFA", "textColor": "#111111", "accentColor": "#DAA520", "headerFont": "'Didot', serif", "bodyFont": "'Helvetica Neue', sans-serif"},
     "layouts": {"hero": "centered", "about": "left-image", "rooms": "grid", "gallery": "grid", "services": "icons", "testimonials": "slider", "contact": "split"}, "heroIdx": 2, "aboutIdx": 2},
    {"id": "hotel-crown-jewel", "name": "Crown Jewel", "category": "luxury", "description": "Bordo ve altin tonlarinda klasik luks.",
     "theme": {"primaryColor": "#722F37", "secondaryColor": "#2C1810", "backgroundColor": "#FDF8F5", "textColor": "#2C1810", "accentColor": "#C5A572", "headerFont": "'Libre Baskerville', serif", "bodyFont": "'Open Sans', sans-serif"},
     "layouts": {"hero": "fullscreen", "about": "right-image", "rooms": "grid", "gallery": "masonry", "services": "grid", "testimonials": "grid", "contact": "centered"}, "heroIdx": 3, "aboutIdx": 0, "include_restaurant": True},
    {"id": "hotel-golden-gate", "name": "Golden Gate", "category": "luxury", "description": "Krem ve sicak tonlarda zarif sablon.",
     "theme": {"primaryColor": "#8B7355", "secondaryColor": "#2C2C2C", "backgroundColor": "#F5F0EB", "textColor": "#2C2C2C", "accentColor": "#C5A572", "headerFont": "'Playfair Display', serif", "bodyFont": "'Raleway', sans-serif"},
     "layouts": {"hero": "split", "about": "left-image", "rooms": "grid", "gallery": "grid", "services": "list", "testimonials": "slider", "contact": "split"}, "heroIdx": 4, "aboutIdx": 1},
    {"id": "hotel-marble-hall", "name": "Marble Hall", "category": "luxury", "description": "Mermer dokusunda zarif sablon.",
     "theme": {"primaryColor": "#A67C52", "secondaryColor": "#333333", "backgroundColor": "#F8F6F2", "textColor": "#2B2B2B", "accentColor": "#C9A66B", "headerFont": "'Cinzel', serif", "bodyFont": "'Inter', sans-serif"},
     "layouts": {"hero": "fullscreen", "about": "right-image", "rooms": "grid", "gallery": "masonry", "services": "grid", "testimonials": "slider", "contact": "split"}, "heroIdx": 5, "aboutIdx": 2},
    {"id": "hotel-imperial", "name": "Imperial", "category": "luxury", "description": "Imparatorluk gorkeminde klasik otel.",
     "theme": {"primaryColor": "#4A2F2F", "secondaryColor": "#DAA520", "backgroundColor": "#FAF5ED", "textColor": "#2C1810", "accentColor": "#8B4513", "headerFont": "'Cormorant', serif", "bodyFont": "'Lora', serif"},
     "layouts": {"hero": "centered", "about": "left-image", "rooms": "grid", "gallery": "grid", "services": "icons", "testimonials": "grid", "contact": "centered"}, "heroIdx": 10, "aboutIdx": 3, "include_restaurant": True},
    {"id": "hotel-platinum", "name": "Platinum", "category": "luxury", "description": "Platin ve siyah tonlarinda ultra luks.",
     "theme": {"primaryColor": "#C0C0C0", "secondaryColor": "#0A0A0A", "backgroundColor": "#FFFFFF", "textColor": "#1A1A1A", "accentColor": "#E5E4E2", "headerFont": "'Bodoni Moda', serif", "bodyFont": "'Poppins', sans-serif"},
     "layouts": {"hero": "split", "about": "right-image", "rooms": "grid", "gallery": "masonry", "services": "list", "testimonials": "slider", "contact": "split"}, "heroIdx": 11, "aboutIdx": 0},

    # BOUTIQUE (7)
    {"id": "hotel-urban-chic", "name": "Urban Chic", "category": "boutique", "description": "Sehirli ve modern butik otel sablonu.",
     "theme": {"primaryColor": "#008080", "secondaryColor": "#36454F", "backgroundColor": "#FFFFFF", "textColor": "#36454F", "accentColor": "#20B2AA", "headerFont": "'Poppins', sans-serif", "bodyFont": "'Inter', sans-serif"},
     "layouts": {"hero": "centered", "about": "left-image", "rooms": "grid", "gallery": "grid", "services": "icons", "testimonials": "grid", "contact": "split"}, "heroIdx": 5, "aboutIdx": 2},
    {"id": "hotel-cozy-corner", "name": "Cozy Corner", "category": "boutique", "description": "Sicak ve samimi butik otel sablonu.",
     "theme": {"primaryColor": "#8B7355", "secondaryColor": "#5C4033", "backgroundColor": "#FFF8E7", "textColor": "#3E2723", "accentColor": "#A0826D", "headerFont": "'Merriweather', serif", "bodyFont": "'Source Sans Pro', sans-serif"},
     "layouts": {"hero": "fullscreen", "about": "right-image", "rooms": "grid", "gallery": "masonry", "services": "grid", "testimonials": "slider", "contact": "centered"}, "heroIdx": 6, "aboutIdx": 0},
    {"id": "hotel-the-loft", "name": "The Loft", "category": "boutique", "description": "Endustriyel tarzda modern butik sablon.",
     "theme": {"primaryColor": "#E87040", "secondaryColor": "#4A4A4A", "backgroundColor": "#F5F5F5", "textColor": "#333333", "accentColor": "#D4602E", "headerFont": "'Space Grotesk', sans-serif", "bodyFont": "'DM Sans', sans-serif"},
     "layouts": {"hero": "split", "about": "left-image", "rooms": "grid", "gallery": "grid", "services": "list", "testimonials": "grid", "contact": "split"}, "heroIdx": 7, "aboutIdx": 1},
    {"id": "hotel-artisan-stay", "name": "Artisan Stay", "category": "boutique", "description": "Sanatsal ve dogal tonlarda butik sablon.",
     "theme": {"primaryColor": "#87AE73", "secondaryColor": "#5D4E37", "backgroundColor": "#FAF7F2", "textColor": "#3D3D3D", "accentColor": "#C07050", "headerFont": "'Josefin Sans', sans-serif", "bodyFont": "'Nunito', sans-serif"},
     "layouts": {"hero": "fullscreen", "about": "left-image", "rooms": "grid", "gallery": "masonry", "services": "icons", "testimonials": "slider", "contact": "centered"}, "heroIdx": 8, "aboutIdx": 2},
    {"id": "hotel-velvet-room", "name": "Velvet Room", "category": "boutique", "description": "Dramatik ve sofistike butik sablon.",
     "theme": {"primaryColor": "#7B3F6E", "secondaryColor": "#2D1B2E", "backgroundColor": "#FBF5F9", "textColor": "#2D1B2E", "accentColor": "#C47A9B", "headerFont": "'Italiana', serif", "bodyFont": "'Quicksand', sans-serif"},
     "layouts": {"hero": "centered", "about": "right-image", "rooms": "grid", "gallery": "grid", "services": "grid", "testimonials": "grid", "contact": "split"}, "heroIdx": 9, "aboutIdx": 0},
    {"id": "hotel-old-town", "name": "Old Town Charm", "category": "boutique", "description": "Eski sehir cazibesinde butik sablon.",
     "theme": {"primaryColor": "#7A4E2D", "secondaryColor": "#2F1B0C", "backgroundColor": "#FFF8F0", "textColor": "#3E2C1C", "accentColor": "#C19A6B", "headerFont": "'Playfair Display', serif", "bodyFont": "'Karla', sans-serif"},
     "layouts": {"hero": "split", "about": "left-image", "rooms": "grid", "gallery": "masonry", "services": "list", "testimonials": "slider", "contact": "split"}, "heroIdx": 10, "aboutIdx": 1},
    {"id": "hotel-garden-house", "name": "Garden House", "category": "boutique", "description": "Bahce icinde dogal butik otel.",
     "theme": {"primaryColor": "#6B9F7B", "secondaryColor": "#2D4A3E", "backgroundColor": "#F5FBF3", "textColor": "#2A3D30", "accentColor": "#A8C8A1", "headerFont": "'DM Serif Display', serif", "bodyFont": "'Work Sans', sans-serif"},
     "layouts": {"hero": "fullscreen", "about": "right-image", "rooms": "grid", "gallery": "grid", "services": "icons", "testimonials": "grid", "contact": "centered"}, "heroIdx": 11, "aboutIdx": 3},

    # RESORT & SPA (7)
    {"id": "hotel-paradise-bay", "name": "Paradise Bay", "category": "resort", "description": "Tropik cennet temasi.",
     "theme": {"primaryColor": "#00BCD4", "secondaryColor": "#006064", "backgroundColor": "#FFFFFF", "textColor": "#263238", "accentColor": "#4DD0E1", "headerFont": "'Comfortaa', sans-serif", "bodyFont": "'Karla', sans-serif"},
     "layouts": {"hero": "fullscreen", "about": "left-image", "rooms": "grid", "gallery": "masonry", "services": "icons", "testimonials": "slider", "contact": "split"}, "heroIdx": 2, "aboutIdx": 1, "include_restaurant": True},
    {"id": "hotel-zen-garden", "name": "Zen Garden", "category": "resort", "description": "Huzurlu ve dogal spa oteli.",
     "theme": {"primaryColor": "#5C8A51", "secondaryColor": "#2E4600", "backgroundColor": "#F5F0E1", "textColor": "#333333", "accentColor": "#8BC34A", "headerFont": "'Noto Serif', serif", "bodyFont": "'Noto Sans', sans-serif"},
     "layouts": {"hero": "centered", "about": "right-image", "rooms": "grid", "gallery": "grid", "services": "grid", "testimonials": "grid", "contact": "centered"}, "heroIdx": 8, "aboutIdx": 2},
    {"id": "hotel-ocean-breeze", "name": "Ocean Breeze", "category": "resort", "description": "Okyanus esintili mavi tonlar.",
     "theme": {"primaryColor": "#1B5E7B", "secondaryColor": "#0D3B4F", "backgroundColor": "#F0F8FF", "textColor": "#1A3C4F", "accentColor": "#87CEEB", "headerFont": "'Crimson Text', serif", "bodyFont": "'Work Sans', sans-serif"},
     "layouts": {"hero": "fullscreen", "about": "left-image", "rooms": "grid", "gallery": "masonry", "services": "list", "testimonials": "slider", "contact": "split"}, "heroIdx": 0, "aboutIdx": 0},
    {"id": "hotel-tropical-haven", "name": "Tropical Haven", "category": "resort", "description": "Canli renklerle tropik sablon.",
     "theme": {"primaryColor": "#FF7F50", "secondaryColor": "#2E8B57", "backgroundColor": "#FFFAF5", "textColor": "#2D3436", "accentColor": "#FF6347", "headerFont": "'Abril Fatface', serif", "bodyFont": "'Lato', sans-serif"},
     "layouts": {"hero": "split", "about": "left-image", "rooms": "grid", "gallery": "grid", "services": "icons", "testimonials": "grid", "contact": "centered"}, "heroIdx": 1, "aboutIdx": 1},
    {"id": "hotel-sunset-villa", "name": "Sunset Villa", "category": "resort", "description": "Romantik gun batimi temasi.",
     "theme": {"primaryColor": "#E86420", "secondaryColor": "#8B4513", "backgroundColor": "#FFF4E6", "textColor": "#3E2723", "accentColor": "#FF8C00", "headerFont": "'Dancing Script', cursive", "bodyFont": "'Nunito Sans', sans-serif"},
     "layouts": {"hero": "fullscreen", "about": "right-image", "rooms": "grid", "gallery": "masonry", "services": "grid", "testimonials": "slider", "contact": "split"}, "heroIdx": 4, "aboutIdx": 2},
    {"id": "hotel-palm-resort", "name": "Palm Resort", "category": "resort", "description": "Palmiye ve kum, plaj resort.",
     "theme": {"primaryColor": "#EAC086", "secondaryColor": "#0B6BA8", "backgroundColor": "#FFFEF9", "textColor": "#1F3A52", "accentColor": "#FFB13C", "headerFont": "'Montserrat', sans-serif", "bodyFont": "'Poppins', sans-serif"},
     "layouts": {"hero": "fullscreen", "about": "left-image", "rooms": "grid", "gallery": "grid", "services": "icons", "testimonials": "slider", "contact": "split"}, "heroIdx": 2, "aboutIdx": 0, "include_restaurant": True},
    {"id": "hotel-thermal-spa", "name": "Thermal Spa", "category": "resort", "description": "Termal ve wellness odakli sablon.",
     "theme": {"primaryColor": "#8E6E53", "secondaryColor": "#3C2A1E", "backgroundColor": "#F7F1E8", "textColor": "#2F2016", "accentColor": "#C9A87A", "headerFont": "'Cormorant Garamond', serif", "bodyFont": "'Lato', sans-serif"},
     "layouts": {"hero": "split", "about": "right-image", "rooms": "grid", "gallery": "masonry", "services": "list", "testimonials": "grid", "contact": "centered"}, "heroIdx": 5, "aboutIdx": 1},

    # BEACH (6)
    {"id": "hotel-coastal-dreams", "name": "Coastal Dreams", "category": "beach", "description": "Sahil ruyasi temasi.",
     "theme": {"primaryColor": "#4ECDC4", "secondaryColor": "#2C3E50", "backgroundColor": "#F0FFFE", "textColor": "#2C3E50", "accentColor": "#F4A460", "headerFont": "'Caveat', cursive", "bodyFont": "'Poppins', sans-serif"},
     "layouts": {"hero": "fullscreen", "about": "left-image", "rooms": "grid", "gallery": "masonry", "services": "icons", "testimonials": "slider", "contact": "split"}, "heroIdx": 0, "aboutIdx": 2},
    {"id": "hotel-seaside-escape", "name": "Seaside Escape", "category": "beach", "description": "Turkuaz tonlarda deniz kenari.",
     "theme": {"primaryColor": "#40E0D0", "secondaryColor": "#1A5276", "backgroundColor": "#FFFFFF", "textColor": "#2C3E50", "accentColor": "#48C9B0", "headerFont": "'Josefin Sans', sans-serif", "bodyFont": "'Open Sans', sans-serif"},
     "layouts": {"hero": "split", "about": "right-image", "rooms": "grid", "gallery": "grid", "services": "grid", "testimonials": "grid", "contact": "centered"}, "heroIdx": 2, "aboutIdx": 0},
    {"id": "hotel-blue-lagoon", "name": "Blue Lagoon", "category": "beach", "description": "Derin mavi dramatik sahil.",
     "theme": {"primaryColor": "#006994", "secondaryColor": "#002244", "backgroundColor": "#F5FAFF", "textColor": "#003366", "accentColor": "#00CED1", "headerFont": "'Cinzel', serif", "bodyFont": "'Lato', sans-serif"},
     "layouts": {"hero": "fullscreen", "about": "left-image", "rooms": "grid", "gallery": "masonry", "services": "list", "testimonials": "slider", "contact": "split"}, "heroIdx": 1, "aboutIdx": 1},
    {"id": "hotel-sandy-shores", "name": "Sandy Shores", "category": "beach", "description": "Kumsal temasli rahat sahil.",
     "theme": {"primaryColor": "#DEB887", "secondaryColor": "#8B6914", "backgroundColor": "#FFFEF7", "textColor": "#5D4E37", "accentColor": "#4169E1", "headerFont": "'Lobster', cursive", "bodyFont": "'Raleway', sans-serif"},
     "layouts": {"hero": "centered", "about": "right-image", "rooms": "grid", "gallery": "grid", "services": "icons", "testimonials": "grid", "contact": "centered"}, "heroIdx": 4, "aboutIdx": 2},
    {"id": "hotel-marina-view", "name": "Marina View", "category": "beach", "description": "Yat limani manzarali.",
     "theme": {"primaryColor": "#1E5B7B", "secondaryColor": "#D4E4F1", "backgroundColor": "#F8FBFF", "textColor": "#112F45", "accentColor": "#F9A825", "headerFont": "'Raleway', sans-serif", "bodyFont": "'Open Sans', sans-serif"},
     "layouts": {"hero": "fullscreen", "about": "right-image", "rooms": "grid", "gallery": "grid", "services": "list", "testimonials": "slider", "contact": "split"}, "heroIdx": 11, "aboutIdx": 3},
    {"id": "hotel-pearl-beach", "name": "Pearl Beach", "category": "beach", "description": "Inci tonlarinda zarif sahil.",
     "theme": {"primaryColor": "#E8DCC6", "secondaryColor": "#355070", "backgroundColor": "#FFFFFF", "textColor": "#2E3B55", "accentColor": "#6D9DC5", "headerFont": "'Italiana', serif", "bodyFont": "'Inter', sans-serif"},
     "layouts": {"hero": "split", "about": "left-image", "rooms": "grid", "gallery": "masonry", "services": "grid", "testimonials": "grid", "contact": "centered"}, "heroIdx": 5, "aboutIdx": 0},

    # MOUNTAIN (4)
    {"id": "hotel-alpine-lodge", "name": "Alpine Lodge", "category": "mountain", "description": "Dag evi temasli rustik sablon.",
     "theme": {"primaryColor": "#5D7B3A", "secondaryColor": "#2E4600", "backgroundColor": "#F5F2EB", "textColor": "#2E2E2E", "accentColor": "#8B4513", "headerFont": "'Cabin', sans-serif", "bodyFont": "'Merriweather', serif"},
     "layouts": {"hero": "fullscreen", "about": "left-image", "rooms": "grid", "gallery": "masonry", "services": "grid", "testimonials": "slider", "contact": "split"}, "heroIdx": 8, "aboutIdx": 0},
    {"id": "hotel-mountain-retreat", "name": "Mountain Retreat", "category": "mountain", "description": "Dogayla ic ice dag oteli.",
     "theme": {"primaryColor": "#696969", "secondaryColor": "#2F4F2F", "backgroundColor": "#F8F8F0", "textColor": "#333333", "accentColor": "#228B22", "headerFont": "'Libre Baskerville', serif", "bodyFont": "'Karla', sans-serif"},
     "layouts": {"hero": "split", "about": "right-image", "rooms": "grid", "gallery": "grid", "services": "list", "testimonials": "grid", "contact": "centered"}, "heroIdx": 6, "aboutIdx": 1},
    {"id": "hotel-pine-valley", "name": "Pine Valley", "category": "mountain", "description": "Cam ormaninda dag oteli.",
     "theme": {"primaryColor": "#2E7D32", "secondaryColor": "#1B5E20", "backgroundColor": "#FAEBD7", "textColor": "#263238", "accentColor": "#4CAF50", "headerFont": "'Cormorant', serif", "bodyFont": "'Work Sans', sans-serif"},
     "layouts": {"hero": "centered", "about": "left-image", "rooms": "grid", "gallery": "masonry", "services": "icons", "testimonials": "slider", "contact": "split"}, "heroIdx": 7, "aboutIdx": 2},
    {"id": "hotel-snow-peak", "name": "Snow Peak", "category": "mountain", "description": "Kar zirvesi kayak oteli.",
     "theme": {"primaryColor": "#2F5B84", "secondaryColor": "#EEF5FD", "backgroundColor": "#FFFFFF", "textColor": "#1B3D5A", "accentColor": "#C3352A", "headerFont": "'Outfit', sans-serif", "bodyFont": "'Inter', sans-serif"},
     "layouts": {"hero": "fullscreen", "about": "right-image", "rooms": "grid", "gallery": "grid", "services": "grid", "testimonials": "grid", "contact": "split"}, "heroIdx": 10, "aboutIdx": 3},

    # CITY & BUSINESS (5)
    {"id": "hotel-downtown-living", "name": "Downtown Living", "category": "city", "description": "Minimalist siyah-beyaz sehir.",
     "theme": {"primaryColor": "#000000", "secondaryColor": "#1A1A1A", "backgroundColor": "#FFFFFF", "textColor": "#1A1A1A", "accentColor": "#FF4444", "headerFont": "'Bebas Neue', sans-serif", "bodyFont": "'Inter', sans-serif"},
     "layouts": {"hero": "fullscreen", "about": "left-image", "rooms": "grid", "gallery": "grid", "services": "list", "testimonials": "slider", "contact": "split"}, "heroIdx": 3, "aboutIdx": 0},
    {"id": "hotel-metro-style", "name": "Metro Style", "category": "city", "description": "Cagdas ve dinamik sehir oteli.",
     "theme": {"primaryColor": "#00B4D8", "secondaryColor": "#023E8A", "backgroundColor": "#F8FAFC", "textColor": "#1E293B", "accentColor": "#00FFD5", "headerFont": "'Space Grotesk', sans-serif", "bodyFont": "'Sora', sans-serif"},
     "layouts": {"hero": "split", "about": "right-image", "rooms": "grid", "gallery": "masonry", "services": "icons", "testimonials": "grid", "contact": "centered"}, "heroIdx": 5, "aboutIdx": 1},
    {"id": "hotel-urban-escape", "name": "Urban Escape", "category": "city", "description": "Trendy ve sicak sehir oteli.",
     "theme": {"primaryColor": "#FFBF00", "secondaryColor": "#5D4E37", "backgroundColor": "#FAFAF5", "textColor": "#3D3D3D", "accentColor": "#F59E0B", "headerFont": "'DM Serif Display', serif", "bodyFont": "'DM Sans', sans-serif"},
     "layouts": {"hero": "fullscreen", "about": "left-image", "rooms": "grid", "gallery": "grid", "services": "grid", "testimonials": "slider", "contact": "split"}, "heroIdx": 9, "aboutIdx": 2},
    {"id": "hotel-executive-tower", "name": "Executive Tower", "category": "business", "description": "Ust duzey yonetici oteli.",
     "theme": {"primaryColor": "#1E3A5F", "secondaryColor": "#0F1B2D", "backgroundColor": "#F8F9FA", "textColor": "#1E3A5F", "accentColor": "#C0C0C0", "headerFont": "'Outfit', sans-serif", "bodyFont": "'Barlow', sans-serif"},
     "layouts": {"hero": "fullscreen", "about": "right-image", "rooms": "grid", "gallery": "grid", "services": "icons", "testimonials": "slider", "contact": "centered"}, "heroIdx": 5, "aboutIdx": 1},
    {"id": "hotel-prime-business", "name": "Prime Business", "category": "business", "description": "Temiz ve profesyonel is oteli.",
     "theme": {"primaryColor": "#10B981", "secondaryColor": "#1B2A4A", "backgroundColor": "#FFFFFF", "textColor": "#1F2937", "accentColor": "#34D399", "headerFont": "'Space Grotesk', sans-serif", "bodyFont": "'DM Sans', sans-serif"},
     "layouts": {"hero": "centered", "about": "left-image", "rooms": "grid", "gallery": "grid", "services": "list", "testimonials": "slider", "contact": "centered"}, "heroIdx": 7, "aboutIdx": 0},

    # DESIGN & TREND (3)
    {"id": "hotel-minimal-lines", "name": "Minimal Lines", "category": "design", "description": "Minimalist ve net cizgiler.",
     "theme": {"primaryColor": "#111111", "secondaryColor": "#BDBDBD", "backgroundColor": "#FFFFFF", "textColor": "#111111", "accentColor": "#FF5722", "headerFont": "'Archivo', sans-serif", "bodyFont": "'Inter', sans-serif"},
     "layouts": {"hero": "split", "about": "right-image", "rooms": "grid", "gallery": "grid", "services": "grid", "testimonials": "grid", "contact": "centered"}, "heroIdx": 11, "aboutIdx": 1},
    {"id": "hotel-soft-pastel", "name": "Soft Pastel", "category": "design", "description": "Pastel tonlarda yumusak tasarim.",
     "theme": {"primaryColor": "#F4B6C2", "secondaryColor": "#6B4E51", "backgroundColor": "#FFF9FB", "textColor": "#4C2C2E", "accentColor": "#AEC6CF", "headerFont": "'Playfair Display', serif", "bodyFont": "'Quicksand', sans-serif"},
     "layouts": {"hero": "fullscreen", "about": "left-image", "rooms": "grid", "gallery": "masonry", "services": "icons", "testimonials": "slider", "contact": "split"}, "heroIdx": 6, "aboutIdx": 3},
    {"id": "hotel-dark-mode", "name": "Dark Mode", "category": "design", "description": "Koyu tema, modern ve cesur.",
     "theme": {"primaryColor": "#FFC107", "secondaryColor": "#0F0F10", "backgroundColor": "#141416", "textColor": "#F4F4F5", "accentColor": "#EAB308", "headerFont": "'Space Grotesk', sans-serif", "bodyFont": "'Inter', sans-serif"},
     "layouts": {"hero": "fullscreen", "about": "right-image", "rooms": "grid", "gallery": "grid", "services": "list", "testimonials": "slider", "contact": "split"}, "heroIdx": 2, "aboutIdx": 0},
]


# ---------- RESTAURANT CONFIGS (35) ----------
def _r(id_, name, category, desc, theme, layouts, heroIdx, aboutIdx, cuisine):
    return {"id": id_, "name": name, "category": category, "description": desc, "theme": theme, "layouts": layouts, "heroIdx": heroIdx, "aboutIdx": aboutIdx, "cuisine": cuisine}


RESTAURANT_CONFIGS = [
    # AKDENIZ / MEDITERRANEAN
    _r("rest-med-olive", "Olive Tree", "mediterranean", "Akdeniz esintisi, zeytin yesili tonlar.",
       {"primaryColor": "#6B8E23", "secondaryColor": "#2E4600", "backgroundColor": "#FBF9F4", "textColor": "#2E2E2E", "accentColor": "#CC7722", "headerFont": "'Playfair Display', serif", "bodyFont": "'Lato', sans-serif"},
       {"hero": "fullscreen", "about": "left-image", "menu": "grid", "gallery": "masonry", "services": "icons", "testimonials": "slider", "contact": "split"}, 0, 0, "Akdeniz"),
    _r("rest-med-lemon", "Lemon Grove", "mediterranean", "Limon sarisi canli Akdeniz sablonu.",
       {"primaryColor": "#F4C430", "secondaryColor": "#1B5E7B", "backgroundColor": "#FFFEF3", "textColor": "#1F3A52", "accentColor": "#F39C12", "headerFont": "'Cormorant Garamond', serif", "bodyFont": "'Poppins', sans-serif"},
       {"hero": "split", "about": "right-image", "menu": "grid", "gallery": "grid", "services": "grid", "testimonials": "grid", "contact": "centered"}, 1, 1, "Akdeniz"),
    _r("rest-med-terra", "Terra Nostra", "mediterranean", "Toprak tonlari ve sicak atmosfer.",
       {"primaryColor": "#A0522D", "secondaryColor": "#3E2723", "backgroundColor": "#FAF5EF", "textColor": "#3E2723", "accentColor": "#DAA520", "headerFont": "'Libre Caslon Text', serif", "bodyFont": "'Open Sans', sans-serif"},
       {"hero": "centered", "about": "left-image", "menu": "grid", "gallery": "masonry", "services": "list", "testimonials": "slider", "contact": "split"}, 2, 2, "Akdeniz"),
    _r("rest-med-azure", "Azure Coast", "mediterranean", "Mavi-beyaz sahil restorani.",
       {"primaryColor": "#1E6091", "secondaryColor": "#F5F5F5", "backgroundColor": "#FFFFFF", "textColor": "#1E2A38", "accentColor": "#F4A460", "headerFont": "'Playfair Display', serif", "bodyFont": "'Lato', sans-serif"},
       {"hero": "fullscreen", "about": "right-image", "menu": "grid", "gallery": "grid", "services": "icons", "testimonials": "slider", "contact": "centered"}, 3, 3, "Akdeniz"),
    # ITALYAN
    _r("rest-ita-bella", "Bella Vita", "italian", "Klasik Italyan trattoria.",
       {"primaryColor": "#C62828", "secondaryColor": "#1B5E20", "backgroundColor": "#FFFBF5", "textColor": "#2C1810", "accentColor": "#FFD700", "headerFont": "'Libre Baskerville', serif", "bodyFont": "'Merriweather', serif"},
       {"hero": "fullscreen", "about": "left-image", "menu": "grid", "gallery": "masonry", "services": "grid", "testimonials": "slider", "contact": "split"}, 4, 0, "Italyan"),
    _r("rest-ita-tavola", "La Tavola", "italian", "Zarif bir Italyan mutfagi.",
       {"primaryColor": "#6D1B1B", "secondaryColor": "#F2E6CE", "backgroundColor": "#FFFAF0", "textColor": "#2C1810", "accentColor": "#B87333", "headerFont": "'Cormorant', serif", "bodyFont": "'Lora', serif"},
       {"hero": "split", "about": "right-image", "menu": "grid", "gallery": "grid", "services": "list", "testimonials": "grid", "contact": "centered"}, 5, 1, "Italyan"),
    _r("rest-ita-piazza", "La Piazza", "italian", "Meydan restorani, canli atmosfer.",
       {"primaryColor": "#2E7D32", "secondaryColor": "#C62828", "backgroundColor": "#FFFFFF", "textColor": "#1C1C1C", "accentColor": "#FFCA28", "headerFont": "'Playfair Display', serif", "bodyFont": "'Open Sans', sans-serif"},
       {"hero": "centered", "about": "left-image", "menu": "grid", "gallery": "masonry", "services": "icons", "testimonials": "slider", "contact": "split"}, 6, 2, "Italyan"),
    _r("rest-ita-nonna", "Nonna's Kitchen", "italian", "Ev yapimi, samimi Italyan.",
       {"primaryColor": "#B71C1C", "secondaryColor": "#3E2723", "backgroundColor": "#FFF8E1", "textColor": "#3E2723", "accentColor": "#FFA000", "headerFont": "'Abril Fatface', serif", "bodyFont": "'Karla', sans-serif"},
       {"hero": "fullscreen", "about": "right-image", "menu": "grid", "gallery": "grid", "services": "grid", "testimonials": "grid", "contact": "centered"}, 7, 3, "Italyan"),
    # SUSI
    _r("rest-sus-sakura", "Sakura", "sushi", "Japon minimalizmi, kiraz cicegi.",
       {"primaryColor": "#E91E63", "secondaryColor": "#212121", "backgroundColor": "#FAFAFA", "textColor": "#212121", "accentColor": "#F48FB1", "headerFont": "'Noto Serif JP', serif", "bodyFont": "'Noto Sans JP', sans-serif"},
       {"hero": "split", "about": "left-image", "menu": "grid", "gallery": "grid", "services": "icons", "testimonials": "slider", "contact": "split"}, 8, 0, "Suşi"),
    _r("rest-sus-ume", "Ume", "sushi", "Sade ve estetik Japon restorani.",
       {"primaryColor": "#000000", "secondaryColor": "#8B0000", "backgroundColor": "#FFFFFF", "textColor": "#111111", "accentColor": "#C69C6D", "headerFont": "'Cinzel', serif", "bodyFont": "'Inter', sans-serif"},
       {"hero": "fullscreen", "about": "right-image", "menu": "grid", "gallery": "masonry", "services": "list", "testimonials": "grid", "contact": "centered"}, 9, 1, "Suşi"),
    _r("rest-sus-kaisen", "Kaisen", "sushi", "Deniz urunu odakli suşi.",
       {"primaryColor": "#0E4D64", "secondaryColor": "#0B0C10", "backgroundColor": "#F0FAFC", "textColor": "#0B0C10", "accentColor": "#EAB308", "headerFont": "'Unica One', sans-serif", "bodyFont": "'Roboto', sans-serif"},
       {"hero": "centered", "about": "left-image", "menu": "grid", "gallery": "grid", "services": "grid", "testimonials": "slider", "contact": "split"}, 10, 2, "Suşi"),
    _r("rest-sus-nori", "Nori House", "sushi", "Modern suşi ev atmosferi.",
       {"primaryColor": "#2C3E50", "secondaryColor": "#D35400", "backgroundColor": "#FCFCFC", "textColor": "#1C2A36", "accentColor": "#F5B841", "headerFont": "'Josefin Sans', sans-serif", "bodyFont": "'Open Sans', sans-serif"},
       {"hero": "split", "about": "right-image", "menu": "grid", "gallery": "masonry", "services": "icons", "testimonials": "grid", "contact": "centered"}, 11, 3, "Suşi"),
    # STEAKHOUSE
    _r("rest-stk-prime", "Prime Cut", "steakhouse", "Koyu ahsap, premium steakhouse.",
       {"primaryColor": "#8B0000", "secondaryColor": "#1B1B1B", "backgroundColor": "#F5F1EC", "textColor": "#1B1B1B", "accentColor": "#B8860B", "headerFont": "'Oswald', sans-serif", "bodyFont": "'Lora', serif"},
       {"hero": "fullscreen", "about": "left-image", "menu": "grid", "gallery": "masonry", "services": "grid", "testimonials": "slider", "contact": "split"}, 0, 0, "Steakhouse"),
    _r("rest-stk-bull", "The Bull", "steakhouse", "Dumanli ve gucl atmosfer.",
       {"primaryColor": "#5D4037", "secondaryColor": "#212121", "backgroundColor": "#EFEBE9", "textColor": "#1F1F1F", "accentColor": "#FF8F00", "headerFont": "'Playfair Display', serif", "bodyFont": "'Roboto Slab', serif"},
       {"hero": "split", "about": "right-image", "menu": "grid", "gallery": "grid", "services": "list", "testimonials": "grid", "contact": "centered"}, 1, 1, "Steakhouse"),
    _r("rest-stk-ember", "Ember Room", "steakhouse", "Kor ates ve kirmizi et ustasi.",
       {"primaryColor": "#C0392B", "secondaryColor": "#1C1C1C", "backgroundColor": "#FAF4EE", "textColor": "#1C1C1C", "accentColor": "#E67E22", "headerFont": "'Bodoni Moda', serif", "bodyFont": "'Lato', sans-serif"},
       {"hero": "centered", "about": "left-image", "menu": "grid", "gallery": "masonry", "services": "icons", "testimonials": "slider", "contact": "split"}, 2, 2, "Steakhouse"),
    _r("rest-stk-black", "Black Angus", "steakhouse", "Siyah Angus premium et evi.",
       {"primaryColor": "#111111", "secondaryColor": "#424242", "backgroundColor": "#FAFAFA", "textColor": "#111111", "accentColor": "#C0392B", "headerFont": "'Cinzel', serif", "bodyFont": "'Inter', sans-serif"},
       {"hero": "fullscreen", "about": "right-image", "menu": "grid", "gallery": "grid", "services": "grid", "testimonials": "grid", "contact": "centered"}, 3, 3, "Steakhouse"),
    # TURK MUTFAGI
    _r("rest-tur-kebap", "Adana Dunyasi", "turkish", "Gerçek Adana kebap evi.",
       {"primaryColor": "#D32F2F", "secondaryColor": "#3E2723", "backgroundColor": "#FFF8F0", "textColor": "#3E2723", "accentColor": "#FFA000", "headerFont": "'Ubuntu', sans-serif", "bodyFont": "'Lato', sans-serif"},
       {"hero": "fullscreen", "about": "left-image", "menu": "grid", "gallery": "masonry", "services": "grid", "testimonials": "slider", "contact": "split"}, 4, 0, "Türk Mutfagi"),
    _r("rest-tur-ocakbasi", "Ocakbasi", "turkish", "Geleneksel ocakbasi kebap.",
       {"primaryColor": "#6D4C41", "secondaryColor": "#3E2723", "backgroundColor": "#FFF8E1", "textColor": "#3E2723", "accentColor": "#C62828", "headerFont": "'Merriweather', serif", "bodyFont": "'Open Sans', sans-serif"},
       {"hero": "split", "about": "right-image", "menu": "grid", "gallery": "grid", "services": "list", "testimonials": "grid", "contact": "centered"}, 5, 1, "Türk Mutfagi"),
    _r("rest-tur-sofrasi", "Anadolu Sofrasi", "turkish", "Ev yapimi, geleneksel Turk mutfagi.",
       {"primaryColor": "#8B4513", "secondaryColor": "#5D4037", "backgroundColor": "#FAF3E7", "textColor": "#3E2C1C", "accentColor": "#F57C00", "headerFont": "'DM Serif Display', serif", "bodyFont": "'Karla', sans-serif"},
       {"hero": "centered", "about": "left-image", "menu": "grid", "gallery": "masonry", "services": "icons", "testimonials": "slider", "contact": "split"}, 6, 2, "Türk Mutfagi"),
    _r("rest-tur-istanbul", "Istanbul Lokantasi", "turkish", "Sehir klasigi, tertemiz esnaf lokantasi.",
       {"primaryColor": "#1B5E20", "secondaryColor": "#B71C1C", "backgroundColor": "#FFFFFF", "textColor": "#1C2A36", "accentColor": "#FFEB3B", "headerFont": "'Playfair Display', serif", "bodyFont": "'Roboto', sans-serif"},
       {"hero": "fullscreen", "about": "right-image", "menu": "grid", "gallery": "grid", "services": "grid", "testimonials": "grid", "contact": "centered"}, 7, 3, "Türk Mutfagi"),
    # KAFE
    _r("rest-caf-coffee", "The Bean House", "cafe", "Uçuncu dalga kahve deneyimi.",
       {"primaryColor": "#6F4E37", "secondaryColor": "#3E2723", "backgroundColor": "#FFFDF9", "textColor": "#3E2723", "accentColor": "#D2B48C", "headerFont": "'Lora', serif", "bodyFont": "'Karla', sans-serif"},
       {"hero": "fullscreen", "about": "left-image", "menu": "grid", "gallery": "masonry", "services": "icons", "testimonials": "slider", "contact": "split"}, 8, 0, "Kafe"),
    _r("rest-caf-morning", "Morning Glory", "cafe", "Kahvalti ve brunch konsepti.",
       {"primaryColor": "#F57C00", "secondaryColor": "#4E342E", "backgroundColor": "#FFFAF3", "textColor": "#3E2723", "accentColor": "#8BC34A", "headerFont": "'Pacifico', cursive", "bodyFont": "'Quicksand', sans-serif"},
       {"hero": "split", "about": "right-image", "menu": "grid", "gallery": "grid", "services": "grid", "testimonials": "grid", "contact": "centered"}, 9, 1, "Kafe"),
    _r("rest-caf-roastery", "Roastery", "cafe", "Kendi cekirdegini kavuran kafe.",
       {"primaryColor": "#3E2723", "secondaryColor": "#8D6E63", "backgroundColor": "#F5F1E6", "textColor": "#2C1810", "accentColor": "#D7A960", "headerFont": "'Bitter', serif", "bodyFont": "'Inter', sans-serif"},
       {"hero": "centered", "about": "left-image", "menu": "grid", "gallery": "masonry", "services": "list", "testimonials": "slider", "contact": "split"}, 10, 2, "Kafe"),
    _r("rest-caf-bloom", "Bloom Cafe", "cafe", "Çiçekli, feminen atmosferli kafe.",
       {"primaryColor": "#E91E63", "secondaryColor": "#AD1457", "backgroundColor": "#FFF5F7", "textColor": "#4A1C2A", "accentColor": "#F8BBD0", "headerFont": "'Dancing Script', cursive", "bodyFont": "'Poppins', sans-serif"},
       {"hero": "fullscreen", "about": "right-image", "menu": "grid", "gallery": "grid", "services": "icons", "testimonials": "grid", "contact": "centered"}, 11, 3, "Kafe"),
    # DENIZ URUNLERI
    _r("rest-sea-marina", "Marina Fish", "seafood", "Liman kenari balik restorani.",
       {"primaryColor": "#006064", "secondaryColor": "#002F34", "backgroundColor": "#F0FAFC", "textColor": "#00363A", "accentColor": "#FFB74D", "headerFont": "'Cormorant', serif", "bodyFont": "'Open Sans', sans-serif"},
       {"hero": "fullscreen", "about": "left-image", "menu": "grid", "gallery": "masonry", "services": "grid", "testimonials": "slider", "contact": "split"}, 0, 0, "Deniz Urunleri"),
    _r("rest-sea-wave", "Blue Wave", "seafood", "Canli mavi, modern deniz restorani.",
       {"primaryColor": "#0288D1", "secondaryColor": "#01579B", "backgroundColor": "#E3F2FD", "textColor": "#0D47A1", "accentColor": "#FFC107", "headerFont": "'Josefin Sans', sans-serif", "bodyFont": "'Inter', sans-serif"},
       {"hero": "split", "about": "right-image", "menu": "grid", "gallery": "grid", "services": "list", "testimonials": "grid", "contact": "centered"}, 1, 1, "Deniz Urunleri"),
    _r("rest-sea-pearl", "Pearl Oyster", "seafood", "Istiridye ve sarap barlari.",
       {"primaryColor": "#37474F", "secondaryColor": "#ECEFF1", "backgroundColor": "#FAFAFA", "textColor": "#263238", "accentColor": "#D4AF37", "headerFont": "'Bodoni Moda', serif", "bodyFont": "'Lato', sans-serif"},
       {"hero": "centered", "about": "left-image", "menu": "grid", "gallery": "masonry", "services": "icons", "testimonials": "slider", "contact": "split"}, 2, 2, "Deniz Urunleri"),
    # VEGGIE / HEALTHY
    _r("rest-veg-green", "Green Bowl", "healthy", "Saglikli, bitki bazli mutfak.",
       {"primaryColor": "#2E7D32", "secondaryColor": "#1B5E20", "backgroundColor": "#F1F8E9", "textColor": "#1B5E20", "accentColor": "#FF8F00", "headerFont": "'Nunito', sans-serif", "bodyFont": "'Inter', sans-serif"},
       {"hero": "fullscreen", "about": "left-image", "menu": "grid", "gallery": "grid", "services": "icons", "testimonials": "grid", "contact": "centered"}, 3, 3, "Veggie"),
    _r("rest-veg-sprout", "Sprout", "healthy", "Vegan ve vejetaryen dostu.",
       {"primaryColor": "#7CB342", "secondaryColor": "#33691E", "backgroundColor": "#FFFFFF", "textColor": "#212121", "accentColor": "#FFA726", "headerFont": "'DM Serif Display', serif", "bodyFont": "'Karla', sans-serif"},
       {"hero": "split", "about": "right-image", "menu": "grid", "gallery": "masonry", "services": "grid", "testimonials": "slider", "contact": "split"}, 4, 0, "Veggie"),
    _r("rest-veg-harvest", "Harvest", "healthy", "Çiftlikten masaya taze mutfak.",
       {"primaryColor": "#558B2F", "secondaryColor": "#33691E", "backgroundColor": "#F9FBE7", "textColor": "#2E4600", "accentColor": "#EF6C00", "headerFont": "'Lora', serif", "bodyFont": "'Open Sans', sans-serif"},
       {"hero": "centered", "about": "left-image", "menu": "grid", "gallery": "grid", "services": "list", "testimonials": "grid", "contact": "centered"}, 5, 1, "Veggie"),
    # EXTRA VARIATIONS
    _r("rest-fus-spice", "Spice Route", "fusion", "Asya-Akdeniz fuzyon lezzet.",
       {"primaryColor": "#F57F17", "secondaryColor": "#4E342E", "backgroundColor": "#FFF8E1", "textColor": "#3E2723", "accentColor": "#D84315", "headerFont": "'Abril Fatface', serif", "bodyFont": "'Poppins', sans-serif"},
       {"hero": "fullscreen", "about": "right-image", "menu": "grid", "gallery": "masonry", "services": "icons", "testimonials": "slider", "contact": "split"}, 6, 2, "Akdeniz"),
    _r("rest-fus-asian", "Wok & Fire", "fusion", "Wok atesi ve pan-Asya mutfagi.",
       {"primaryColor": "#D32F2F", "secondaryColor": "#1A1A1A", "backgroundColor": "#FAFAFA", "textColor": "#212121", "accentColor": "#FFCA28", "headerFont": "'Oswald', sans-serif", "bodyFont": "'Inter', sans-serif"},
       {"hero": "split", "about": "left-image", "menu": "grid", "gallery": "grid", "services": "list", "testimonials": "grid", "contact": "centered"}, 7, 3, "Suşi"),
    _r("rest-street-urban", "Urban Eats", "street", "Sokak yemegi ve burger konsepti.",
       {"primaryColor": "#FF5722", "secondaryColor": "#263238", "backgroundColor": "#FFFFFF", "textColor": "#263238", "accentColor": "#FFD600", "headerFont": "'Bebas Neue', sans-serif", "bodyFont": "'Inter', sans-serif"},
       {"hero": "fullscreen", "about": "left-image", "menu": "grid", "gallery": "grid", "services": "icons", "testimonials": "slider", "contact": "split"}, 8, 0, "Steakhouse"),
    _r("rest-vintage-belle", "Belle Epoque", "vintage", "Nostaljik ve art nouveau.",
       {"primaryColor": "#6A1B9A", "secondaryColor": "#311B92", "backgroundColor": "#FBF7FF", "textColor": "#2E1A47", "accentColor": "#FFB300", "headerFont": "'Italiana', serif", "bodyFont": "'Cormorant', serif"},
       {"hero": "centered", "about": "right-image", "menu": "grid", "gallery": "masonry", "services": "grid", "testimonials": "grid", "contact": "centered"}, 9, 1, "Italyan"),
    _r("rest-trend-neon", "Neon Diner", "trend", "Retro-modern neon diner.",
       {"primaryColor": "#FF006E", "secondaryColor": "#3A0CA3", "backgroundColor": "#0A0A0F", "textColor": "#F8F9FA", "accentColor": "#FFD60A", "headerFont": "'Bungee', cursive", "bodyFont": "'Poppins', sans-serif"},
       {"hero": "fullscreen", "about": "left-image", "menu": "grid", "gallery": "grid", "services": "icons", "testimonials": "slider", "contact": "split"}, 10, 2, "Kafe"),
]


# ---------- AGENCY CONFIGS (30) ----------
def _a(id_, name, category, desc, theme, layouts, heroIdx, aboutIdx, focus):
    return {"id": id_, "name": name, "category": category, "description": desc, "theme": theme, "layouts": layouts, "heroIdx": heroIdx, "aboutIdx": aboutIdx, "focus": focus}


AGENCY_CONFIGS = [
    # YURTDISI (7)
    _a("agent-int-globe", "Globe Tours", "international", "Dunya çapinda turlar, modern tasarim.",
       {"primaryColor": "#1565C0", "secondaryColor": "#0D47A1", "backgroundColor": "#FFFFFF", "textColor": "#0D1B2A", "accentColor": "#FFB300", "headerFont": "'Montserrat', sans-serif", "bodyFont": "'Inter', sans-serif"},
       {"hero": "fullscreen", "about": "left-image", "tours": "grid", "gallery": "masonry", "services": "icons", "testimonials": "slider", "contact": "split"}, 0, 0, "Yurtdisi"),
    _a("agent-int-horizon", "Horizon Travel", "international", "Genis ufuklar, premium seyahat.",
       {"primaryColor": "#FF6B35", "secondaryColor": "#1B263B", "backgroundColor": "#FAFAFA", "textColor": "#1B263B", "accentColor": "#F77F00", "headerFont": "'Playfair Display', serif", "bodyFont": "'Lato', sans-serif"},
       {"hero": "split", "about": "right-image", "tours": "grid", "gallery": "grid", "services": "grid", "testimonials": "grid", "contact": "centered"}, 1, 1, "Yurtdisi"),
    _a("agent-int-avenir", "Avenir", "international", "Gelecegin seyahat deneyimi.",
       {"primaryColor": "#00838F", "secondaryColor": "#263238", "backgroundColor": "#E0F7FA", "textColor": "#006064", "accentColor": "#FF5722", "headerFont": "'Josefin Sans', sans-serif", "bodyFont": "'Open Sans', sans-serif"},
       {"hero": "centered", "about": "left-image", "tours": "grid", "gallery": "grid", "services": "list", "testimonials": "slider", "contact": "split"}, 2, 2, "Yurtdisi"),
    _a("agent-int-explorer", "World Explorer", "international", "Kâşif ruhu, sinirsiz seyahat.",
       {"primaryColor": "#6A1B9A", "secondaryColor": "#4A148C", "backgroundColor": "#F3E5F5", "textColor": "#311B92", "accentColor": "#FFCA28", "headerFont": "'Oswald', sans-serif", "bodyFont": "'Raleway', sans-serif"},
       {"hero": "fullscreen", "about": "right-image", "tours": "grid", "gallery": "masonry", "services": "icons", "testimonials": "grid", "contact": "centered"}, 3, 0, "Yurtdisi"),
    _a("agent-int-vista", "Vista Travel", "international", "Manzaralar ve unutulmaz anlar.",
       {"primaryColor": "#D84315", "secondaryColor": "#3E2723", "backgroundColor": "#FFF3E0", "textColor": "#3E2723", "accentColor": "#00796B", "headerFont": "'Abril Fatface', serif", "bodyFont": "'Poppins', sans-serif"},
       {"hero": "split", "about": "left-image", "tours": "grid", "gallery": "grid", "services": "grid", "testimonials": "slider", "contact": "split"}, 4, 1, "Yurtdisi"),
    _a("agent-int-passport", "Passport", "international", "Dunyanin kapilarini aralik tutun.",
       {"primaryColor": "#283593", "secondaryColor": "#1A237E", "backgroundColor": "#FFFFFF", "textColor": "#1A237E", "accentColor": "#FFB300", "headerFont": "'DM Serif Display', serif", "bodyFont": "'Inter', sans-serif"},
       {"hero": "centered", "about": "right-image", "tours": "grid", "gallery": "masonry", "services": "list", "testimonials": "grid", "contact": "centered"}, 5, 2, "Yurtdisi"),
    _a("agent-int-wander", "Wanderlust", "international", "Seyahat tutkunlari icin acente.",
       {"primaryColor": "#00695C", "secondaryColor": "#004D40", "backgroundColor": "#E0F2F1", "textColor": "#004D40", "accentColor": "#FF6F00", "headerFont": "'Pacifico', cursive", "bodyFont": "'Quicksand', sans-serif"},
       {"hero": "fullscreen", "about": "left-image", "tours": "grid", "gallery": "grid", "services": "icons", "testimonials": "slider", "contact": "split"}, 6, 0, "Yurtdisi"),
    # YURTICI (6)
    _a("agent-dom-anadolu", "Anadolu Turlari", "domestic", "Turkiye'nin her koşesi.",
       {"primaryColor": "#C62828", "secondaryColor": "#B71C1C", "backgroundColor": "#FFFFFF", "textColor": "#212121", "accentColor": "#FFCA28", "headerFont": "'Ubuntu', sans-serif", "bodyFont": "'Open Sans', sans-serif"},
       {"hero": "fullscreen", "about": "left-image", "tours": "grid", "gallery": "masonry", "services": "grid", "testimonials": "slider", "contact": "split"}, 7, 1, "Yurtici"),
    _a("agent-dom-rota", "Rota 41", "domestic", "Yurt ici rotalar ve kulturu.",
       {"primaryColor": "#1565C0", "secondaryColor": "#0D47A1", "backgroundColor": "#E3F2FD", "textColor": "#0D47A1", "accentColor": "#F57C00", "headerFont": "'Roboto Slab', serif", "bodyFont": "'Roboto', sans-serif"},
       {"hero": "split", "about": "right-image", "tours": "grid", "gallery": "grid", "services": "list", "testimonials": "grid", "contact": "centered"}, 8, 2, "Yurtici"),
    _a("agent-dom-gezgin", "Gezgin", "domestic", "Gezgin ruhlu yurt ici turlar.",
       {"primaryColor": "#4CAF50", "secondaryColor": "#1B5E20", "backgroundColor": "#F1F8E9", "textColor": "#1B5E20", "accentColor": "#FF6F00", "headerFont": "'Nunito', sans-serif", "bodyFont": "'Inter', sans-serif"},
       {"hero": "centered", "about": "left-image", "tours": "grid", "gallery": "masonry", "services": "icons", "testimonials": "slider", "contact": "split"}, 9, 0, "Yurtici"),
    _a("agent-dom-yollar", "Gizli Yollar", "domestic", "Az bilinen rotalar ve sürprizler.",
       {"primaryColor": "#6D4C41", "secondaryColor": "#3E2723", "backgroundColor": "#FFF8E1", "textColor": "#3E2723", "accentColor": "#2E7D32", "headerFont": "'Lora', serif", "bodyFont": "'Karla', sans-serif"},
       {"hero": "fullscreen", "about": "right-image", "tours": "grid", "gallery": "grid", "services": "grid", "testimonials": "grid", "contact": "centered"}, 10, 1, "Yurtici"),
    _a("agent-dom-mavi", "Mavi Yolculuk", "domestic", "Ege ve Akdeniz mavi turlari.",
       {"primaryColor": "#0277BD", "secondaryColor": "#01579B", "backgroundColor": "#E1F5FE", "textColor": "#01579B", "accentColor": "#FFA000", "headerFont": "'Italiana', serif", "bodyFont": "'Poppins', sans-serif"},
       {"hero": "split", "about": "left-image", "tours": "grid", "gallery": "masonry", "services": "list", "testimonials": "slider", "contact": "split"}, 11, 2, "Yurtici"),
    _a("agent-dom-bizim", "Bizim Turlar", "domestic", "Sicak ve samimi yerel acenta.",
       {"primaryColor": "#F57C00", "secondaryColor": "#E65100", "backgroundColor": "#FFF8E1", "textColor": "#3E2723", "accentColor": "#0288D1", "headerFont": "'DM Serif Display', serif", "bodyFont": "'Open Sans', sans-serif"},
       {"hero": "centered", "about": "right-image", "tours": "grid", "gallery": "grid", "services": "icons", "testimonials": "grid", "contact": "centered"}, 0, 0, "Yurtici"),
    # KULTUR (5)
    _a("agent-cul-tarih", "Tarihin Izinde", "culture", "Kultur ve tarih turlari uzmani.",
       {"primaryColor": "#6D4C41", "secondaryColor": "#3E2723", "backgroundColor": "#FAF5EE", "textColor": "#3E2723", "accentColor": "#B8860B", "headerFont": "'Cinzel', serif", "bodyFont": "'Merriweather', serif"},
       {"hero": "fullscreen", "about": "left-image", "tours": "grid", "gallery": "masonry", "services": "grid", "testimonials": "slider", "contact": "split"}, 1, 1, "Kultur"),
    _a("agent-cul-antik", "Antik Yollar", "culture", "Antik sehirler ve rehberli turlar.",
       {"primaryColor": "#8E6E53", "secondaryColor": "#4E342E", "backgroundColor": "#FFF8E1", "textColor": "#3E2723", "accentColor": "#D84315", "headerFont": "'Libre Caslon Text', serif", "bodyFont": "'Lato', sans-serif"},
       {"hero": "split", "about": "right-image", "tours": "grid", "gallery": "grid", "services": "list", "testimonials": "grid", "contact": "centered"}, 2, 2, "Kultur"),
    _a("agent-cul-mozaik", "Mozaik", "culture", "Medeniyetler mozaigi.",
       {"primaryColor": "#283593", "secondaryColor": "#1A237E", "backgroundColor": "#FFFFFF", "textColor": "#1A237E", "accentColor": "#FFB300", "headerFont": "'Playfair Display', serif", "bodyFont": "'Inter', sans-serif"},
       {"hero": "centered", "about": "left-image", "tours": "grid", "gallery": "masonry", "services": "icons", "testimonials": "slider", "contact": "split"}, 3, 0, "Kultur"),
    _a("agent-cul-hikaye", "Hikayeler", "culture", "Hikayelerle dolu turlar.",
       {"primaryColor": "#AD1457", "secondaryColor": "#880E4F", "backgroundColor": "#FCE4EC", "textColor": "#880E4F", "accentColor": "#FFA000", "headerFont": "'Cormorant Garamond', serif", "bodyFont": "'Karla', sans-serif"},
       {"hero": "fullscreen", "about": "right-image", "tours": "grid", "gallery": "grid", "services": "grid", "testimonials": "grid", "contact": "centered"}, 4, 1, "Kultur"),
    _a("agent-cul-rumi", "Rumi Gezileri", "culture", "Manevi ve kultur turlari.",
       {"primaryColor": "#00695C", "secondaryColor": "#004D40", "backgroundColor": "#E0F2F1", "textColor": "#004D40", "accentColor": "#FFCA28", "headerFont": "'Italiana', serif", "bodyFont": "'Open Sans', sans-serif"},
       {"hero": "split", "about": "left-image", "tours": "grid", "gallery": "masonry", "services": "icons", "testimonials": "grid", "contact": "split"}, 5, 2, "Kultur"),
    # MACERA (4)
    _a("agent-adv-extreme", "Extreme Travel", "adventure", "Macera ve adrenalin turlari.",
       {"primaryColor": "#D84315", "secondaryColor": "#263238", "backgroundColor": "#FFFFFF", "textColor": "#212121", "accentColor": "#FFCA28", "headerFont": "'Oswald', sans-serif", "bodyFont": "'Inter', sans-serif"},
       {"hero": "fullscreen", "about": "left-image", "tours": "grid", "gallery": "masonry", "services": "icons", "testimonials": "slider", "contact": "split"}, 6, 0, "Macera"),
    _a("agent-adv-peak", "Peak Pursuit", "adventure", "Zirveler ve trekking turlari.",
       {"primaryColor": "#1B5E20", "secondaryColor": "#0D3B4F", "backgroundColor": "#F1F8E9", "textColor": "#1B5E20", "accentColor": "#FF5722", "headerFont": "'Bebas Neue', sans-serif", "bodyFont": "'Roboto', sans-serif"},
       {"hero": "split", "about": "right-image", "tours": "grid", "gallery": "grid", "services": "list", "testimonials": "grid", "contact": "centered"}, 7, 1, "Macera"),
    _a("agent-adv-rota", "Off Route", "adventure", "Rota disi kesifler.",
       {"primaryColor": "#33691E", "secondaryColor": "#212121", "backgroundColor": "#F1F8E9", "textColor": "#1B5E20", "accentColor": "#F57C00", "headerFont": "'Space Grotesk', sans-serif", "bodyFont": "'Inter', sans-serif"},
       {"hero": "centered", "about": "left-image", "tours": "grid", "gallery": "masonry", "services": "grid", "testimonials": "slider", "contact": "split"}, 8, 2, "Macera"),
    _a("agent-adv-wild", "Wild Expeditions", "adventure", "Vahsi dogada ekspedisyonlar.",
       {"primaryColor": "#2E7D32", "secondaryColor": "#1B5E20", "backgroundColor": "#FFFFFF", "textColor": "#1B1B1B", "accentColor": "#FF6F00", "headerFont": "'Archivo Black', sans-serif", "bodyFont": "'Open Sans', sans-serif"},
       {"hero": "fullscreen", "about": "right-image", "tours": "grid", "gallery": "grid", "services": "icons", "testimonials": "grid", "contact": "centered"}, 9, 0, "Macera"),
    # BALAYI (3)
    _a("agent-hny-romance", "Romance Travel", "honeymoon", "Balayi ve romantik kacamaklar.",
       {"primaryColor": "#EC407A", "secondaryColor": "#880E4F", "backgroundColor": "#FCE4EC", "textColor": "#880E4F", "accentColor": "#FFB300", "headerFont": "'Dancing Script', cursive", "bodyFont": "'Poppins', sans-serif"},
       {"hero": "fullscreen", "about": "left-image", "tours": "grid", "gallery": "masonry", "services": "icons", "testimonials": "slider", "contact": "split"}, 10, 1, "Balayi"),
    _a("agent-hny-sunset", "Sunset Honeymoon", "honeymoon", "Gun batimi balayilari.",
       {"primaryColor": "#FF7043", "secondaryColor": "#4A148C", "backgroundColor": "#FFF3E0", "textColor": "#3E2723", "accentColor": "#FFC107", "headerFont": "'Great Vibes', cursive", "bodyFont": "'Quicksand', sans-serif"},
       {"hero": "split", "about": "right-image", "tours": "grid", "gallery": "grid", "services": "grid", "testimonials": "grid", "contact": "centered"}, 11, 2, "Balayi"),
    _a("agent-hny-twoheart", "Two Hearts", "honeymoon", "Iki kalp, bir tatil.",
       {"primaryColor": "#D81B60", "secondaryColor": "#AD1457", "backgroundColor": "#FFFFFF", "textColor": "#4A1C2A", "accentColor": "#6A1B9A", "headerFont": "'Italiana', serif", "bodyFont": "'Lato', sans-serif"},
       {"hero": "centered", "about": "left-image", "tours": "grid", "gallery": "masonry", "services": "list", "testimonials": "slider", "contact": "split"}, 0, 0, "Balayi"),
    # TRANSFER (3)
    _a("agent-trf-vip", "VIP Transfer", "transfer", "Lüks havaalani ve sehir transferi.",
       {"primaryColor": "#1A237E", "secondaryColor": "#0D47A1", "backgroundColor": "#FFFFFF", "textColor": "#0D1B2A", "accentColor": "#FFB300", "headerFont": "'Montserrat', sans-serif", "bodyFont": "'Inter', sans-serif"},
       {"hero": "fullscreen", "about": "left-image", "tours": "grid", "gallery": "grid", "services": "icons", "testimonials": "slider", "contact": "split"}, 1, 1, "Transfer"),
    _a("agent-trf-swift", "Swift Transfer", "transfer", "Hizli ve guvenli transfer hizmeti.",
       {"primaryColor": "#B71C1C", "secondaryColor": "#263238", "backgroundColor": "#FAFAFA", "textColor": "#263238", "accentColor": "#FFD600", "headerFont": "'Bebas Neue', sans-serif", "bodyFont": "'Roboto', sans-serif"},
       {"hero": "split", "about": "right-image", "tours": "grid", "gallery": "masonry", "services": "list", "testimonials": "grid", "contact": "centered"}, 2, 2, "Transfer"),
    _a("agent-trf-comfort", "Comfort Transfer", "transfer", "Konforlu transfer cozumleri.",
       {"primaryColor": "#37474F", "secondaryColor": "#263238", "backgroundColor": "#ECEFF1", "textColor": "#263238", "accentColor": "#00BCD4", "headerFont": "'Oswald', sans-serif", "bodyFont": "'Open Sans', sans-serif"},
       {"hero": "centered", "about": "left-image", "tours": "grid", "gallery": "grid", "services": "grid", "testimonials": "slider", "contact": "split"}, 3, 0, "Transfer"),
    # HAC UMRE (2)
    _a("agent-hac-diyar", "Kutsal Diyar", "hajj", "Hac ve Umre programlari uzmani.",
       {"primaryColor": "#006064", "secondaryColor": "#004D40", "backgroundColor": "#E0F7FA", "textColor": "#004D40", "accentColor": "#FFB300", "headerFont": "'Scheherazade New', serif", "bodyFont": "'Noto Sans Arabic', sans-serif"},
       {"hero": "fullscreen", "about": "right-image", "tours": "grid", "gallery": "masonry", "services": "icons", "testimonials": "grid", "contact": "centered"}, 4, 1, "Hac Umre"),
    _a("agent-hac-nur", "Nur Umre", "hajj", "Kutsal topraklar manevi seyahat.",
       {"primaryColor": "#1B5E20", "secondaryColor": "#0B4D0B", "backgroundColor": "#F1F8E9", "textColor": "#1B5E20", "accentColor": "#FFB300", "headerFont": "'Amiri', serif", "bodyFont": "'Cairo', sans-serif"},
       {"hero": "split", "about": "left-image", "tours": "grid", "gallery": "grid", "services": "list", "testimonials": "slider", "contact": "split"}, 5, 2, "Hac Umre"),
]


# ============================================================
# TEMPLATE GENERATION
# ============================================================

# Distinct visual design styles. Each produces dramatically different CSS treatment
# (typography, button shapes, card styles, spacing, color application).
DESIGN_STYLES = ["classic", "minimal", "luxury-dark", "rustic", "bold-modern", "magazine"]

# Default style by category - gives each category a coherent visual identity.
# Templates within the same category get rotated through 2-3 styles for variety.
_CATEGORY_STYLE_POOLS = {
    # hotel
    "luxury": ["luxury-dark", "classic", "magazine"],
    "boutique": ["magazine", "minimal", "rustic"],
    "resort": ["classic", "rustic", "bold-modern"],
    "beach": ["minimal", "bold-modern", "classic"],
    "mountain": ["rustic", "luxury-dark", "classic"],
    "city": ["bold-modern", "minimal", "luxury-dark"],
    "business": ["minimal", "bold-modern"],
    "design": ["bold-modern", "minimal", "luxury-dark"],
    # restaurant
    "mediterranean": ["rustic", "classic", "minimal"],
    "italian": ["magazine", "rustic", "classic"],
    "turkish": ["rustic", "classic", "magazine"],
    "vintage": ["magazine", "classic", "rustic"],
    "steakhouse": ["luxury-dark", "bold-modern", "magazine"],
    "cafe": ["minimal", "magazine", "rustic"],
    "seafood": ["minimal", "classic", "luxury-dark"],
    "vegan": ["minimal", "rustic", "magazine"],
    "asian": ["minimal", "luxury-dark", "magazine"],
    "japanese": ["minimal", "luxury-dark"],
    "indian": ["luxury-dark", "rustic", "bold-modern"],
    "mexican": ["bold-modern", "rustic"],
    "french": ["luxury-dark", "magazine", "classic"],
    "fusion": ["bold-modern", "magazine", "minimal"],
    "fastfood": ["bold-modern", "minimal"],
    "brunch": ["minimal", "magazine", "rustic"],
    "patisserie": ["magazine", "minimal", "rustic"],
    # agency
    "international": ["bold-modern", "magazine", "classic"],
    "domestic": ["classic", "rustic", "magazine"],
    "cultural": ["magazine", "classic", "luxury-dark"],
    "adventure": ["bold-modern", "rustic", "minimal"],
    "luxury-travel": ["luxury-dark", "magazine", "classic"],
    "honeymoon": ["magazine", "classic", "luxury-dark"],
    "corporate": ["minimal", "bold-modern"],
    "religious": ["classic", "luxury-dark", "magazine"],
    "ski": ["minimal", "bold-modern", "rustic"],
    "cruise": ["luxury-dark", "classic", "minimal"],
    "safari": ["rustic", "bold-modern", "magazine"],
}


def _pick_style(category, template_id):
    pool = _CATEGORY_STYLE_POOLS.get(category)
    if not pool:
        # fallback: deterministic rotation across all 6 styles based on id
        return DESIGN_STYLES[sum(ord(c) for c in template_id) % len(DESIGN_STYLES)]
    return pool[sum(ord(c) for c in template_id) % len(pool)]


def _build_template(cfg, category_key, sections):
    hero_idx = cfg.get("heroIdx", 0)
    if category_key == "hotel":
        thumb = HOTEL_HERO_IMAGES[hero_idx % len(HOTEL_HERO_IMAGES)]
    elif category_key == "restaurant":
        thumb = RESTAURANT_HERO_IMAGES[hero_idx % len(RESTAURANT_HERO_IMAGES)]
    else:
        thumb = AGENCY_HERO_IMAGES[hero_idx % len(AGENCY_HERO_IMAGES)]

    # Inject visual design style into theme
    theme = dict(cfg["theme"])
    if "style" not in theme:
        theme["style"] = _pick_style(cfg["category"], cfg["id"])

    return {
        "id": cfg["id"],
        "name": cfg["name"],
        "category": cfg["category"],
        "segment": category_key,  # "hotel" | "restaurant" | "agency"
        "description": cfg["description"],
        "thumbnail": thumb,
        "theme": theme,
        "sections": sections,
        "is_custom": False,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }


def generate_all_templates():
    templates = []

    for cfg in HOTEL_CONFIGS:
        hero_img = HOTEL_HERO_IMAGES[cfg.get("heroIdx", 0) % len(HOTEL_HERO_IMAGES)]
        about_img = HOTEL_ABOUT_IMAGES[cfg.get("aboutIdx", 0) % len(HOTEL_ABOUT_IMAGES)]
        room_imgs = HOTEL_ROOM_IMAGES
        gallery_imgs = HOTEL_GALLERY_IMAGES[:6]
        sections = make_hotel_sections(
            hero_img, about_img, room_imgs, gallery_imgs, cfg["layouts"],
            include_restaurant=cfg.get("include_restaurant", False),
        )
        templates.append(_build_template(cfg, "hotel", sections))

    for cfg in RESTAURANT_CONFIGS:
        hero_img = RESTAURANT_HERO_IMAGES[cfg.get("heroIdx", 0) % len(RESTAURANT_HERO_IMAGES)]
        about_img = RESTAURANT_ABOUT_IMAGES[cfg.get("aboutIdx", 0) % len(RESTAURANT_ABOUT_IMAGES)]
        dish_imgs = RESTAURANT_DISH_IMAGES
        gallery_imgs = RESTAURANT_GALLERY_IMAGES[:6]
        sections = make_restaurant_sections(
            hero_img, about_img, dish_imgs, gallery_imgs, cfg["layouts"],
            cuisine=cfg.get("cuisine", "Akdeniz"),
        )
        templates.append(_build_template(cfg, "restaurant", sections))

    for cfg in AGENCY_CONFIGS:
        hero_img = AGENCY_HERO_IMAGES[cfg.get("heroIdx", 0) % len(AGENCY_HERO_IMAGES)]
        about_img = AGENCY_ABOUT_IMAGES[cfg.get("aboutIdx", 0) % len(AGENCY_ABOUT_IMAGES)]
        tour_imgs = AGENCY_TOUR_IMAGES
        gallery_imgs = AGENCY_GALLERY_IMAGES[:6]
        sections = make_agency_sections(
            hero_img, about_img, tour_imgs, gallery_imgs, cfg["layouts"],
            focus=cfg.get("focus", "Yurtdisi"),
        )
        templates.append(_build_template(cfg, "agency", sections))

    return templates


# Back-compat alias for any code still referencing TEMPLATE_CONFIGS
TEMPLATE_CONFIGS = HOTEL_CONFIGS + RESTAURANT_CONFIGS + AGENCY_CONFIGS
