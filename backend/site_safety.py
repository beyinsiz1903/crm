"""Shared, deliberately small trust boundary for generated public websites."""
import copy
import html
import ipaddress
import re
from html.parser import HTMLParser
from urllib.parse import urlsplit


def safe_url(value, *, image=False):
    value = str(value or '').strip()
    if any(ord(c) < 32 for c in value) or '\\' in value or re.search(r'''[<>"'`()\s]''', value):
        return ''
    parsed = urlsplit(value)
    if parsed.scheme in {'https', 'http'}:
        if not parsed.hostname or parsed.username or parsed.password:
            return ''
        return value
    if not image and parsed.scheme in {'mailto', 'tel'}:
        return value
    if not parsed.scheme and not parsed.netloc and not value.startswith('//'):
        return value
    return ''


class _Iframe(HTMLParser):
    def __init__(self):
        super().__init__()
        self.sources = []

    def handle_starttag(self, tag, attrs):
        if tag == 'iframe':
            source = safe_url(dict(attrs).get('src'))
            if source.startswith('https://'):
                self.sources.append(source)


def safe_widget(code):
    parser = _Iframe()
    parser.feed(str(code or ''))
    if len(parser.sources) != 1:
        return ''
    return '<iframe title="Rezervasyon" src="{}" sandbox="allow-scripts allow-forms allow-popups allow-same-origin" referrerpolicy="strict-origin-when-cross-origin" style="width:100%;min-height:760px;border:0" loading="lazy"></iframe>'.format(html.escape(parser.sources[0], quote=True))


URL_KEYS = {'ctaLink', 'bookingUrl', 'backgroundImage', 'image', 'src', 'mapUrl', 'og_image', 'cover_image', 'logo', 'canonical_url'}


def prepare_project(project):
    """Escape ordinary content once, including attribute contexts; never allow raw JS."""
    def clean(value, key=''):
        if isinstance(value, dict):
            return {k: clean(v, k) for k, v in value.items()}
        if isinstance(value, list):
            return [clean(item, key) for item in value]
        if not isinstance(value, str):
            return value
        if key == 'widgetCode':
            return safe_widget(value)
        if key == 'custom_head_code':
            return ''
        if key in URL_KEYS or key in {'facebook', 'instagram', 'twitter', 'youtube', 'linkedin'}:
            value = safe_url(value, image=key in {'backgroundImage', 'image', 'src', 'og_image', 'cover_image', 'logo'})
        if key == 'ga_id' and not re.fullmatch(r'G-[A-Z0-9]+', value):
            return ''
        if key == 'overlayOpacity':
            try:
                return str(min(1, max(0, float(value))))
            except ValueError:
                return '0.5'
        return html.escape(value, quote=True)

    result = clean(copy.deepcopy(project))
    theme = result.get('theme') or {}
    for key in ['primaryColor', 'secondaryColor', 'backgroundColor', 'textColor']:
        if key in theme and not re.fullmatch(r'#[0-9a-fA-F]{3,8}', theme[key]):
            theme.pop(key)
    # Fonts are CSS, not HTML; allow only names and the two font-family separators.
    for key in ['headerFont', 'bodyFont']:
        raw = (project.get('theme') or {}).get(key)
        if isinstance(raw, str) and re.fullmatch(r"[A-Za-z0-9 ,'\-]+", raw):
            theme[key] = raw
        else:
            theme.pop(key, None)
    result['theme'] = theme
    result['language'] = project.get('language') if project.get('language') in {'tr', 'en', 'de', 'fr', 'es', 'it', 'ru', 'ar', 'ja', 'zh'} else 'tr'
    return result


def public_address(address):
    """Used by asset transport, including every redirect and DNS result."""
    try:
        return ipaddress.ip_address(address).is_global
    except ValueError:
        return False
