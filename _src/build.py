#!/usr/bin/env python3
"""
Static build for the PD portfolio.

  python3 _src/build.py          # writes *.html into the site root

Each page's <main> content lives in _src/content/<slug>.html.
This script wraps it in the canonical shell (head, skip link, sidebar, prev/next, footer),
so navigation, metadata and accessibility hooks can never drift between pages.
"""
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC = os.path.join(ROOT, '_src', 'content')

UPDATED = '19 October 2026'
SITE_NAME = 'Agustín Martínez Caram · PD Portfolio'

# slug, nav number, nav label, page title, meta description, data-lab, group
PAGES = [
    ('index',              '00', 'Home',                  'PD Assessment Portfolio',
     'Assessment portfolio of Agustín Martínez Caram, Professional Doctorate Arts + Creative, Hanze: four AT-LAB inquiries on AI and data literacy through artistic practice.', None, 'home'),
    ('updates',            '·',  'Updates since March',   'Updates since March 2026',
     'What changed in the PD portfolio between March and October 2026: new work, corrected claims, and what is still open.', None, 'home'),
    ('trajectory',         '01', 'PD Trajectory',         'PD Trajectory',
     'The trajectory of the PD from 2023 to the final assessment: four AT-LABs, what each asked, and what carried forward.', None, 'traj'),
    ('methodology',        '02', 'AT-LAB Methodology',    'AT-LAB Methodology',
     'The AT-LAB inquiry format: design, intervention, reading, reflection and feed-forward, and the evidence it currently has.', None, 'traj'),
    ('boundary-concepts',  '03', 'Boundary Concepts',     'Boundary Concepts',
     'Conceptual clarity, perceived agency and transferability as sensitising lenses for reading AI and data literacy across settings.', None, 'traj'),
    ('emi',                '04', 'EMI Framework',         'EMI Framework',
     'Epistemic Mediation Indicators: an exploratory vocabulary for the artist-researcher’s contribution in transdisciplinary work.', None, 'traj'),
    ('lab-1-health',       '05', 'AT-LAB I — Health',     'AT-LAB I — Health',
     'AT-LAB I: a participatory installation turning wearable sensor data into sound and light at ’t Zandt, June 2023, with a secondary analysis of 27 responses.', '1', 'traj'),
    ('lab-2-teaching',     '06', 'AT-LAB II — Teaching',  'AT-LAB II — Teaching',
     'AT-LAB II: research-based teaching on AI and artistic practice at the Frank Mohr Institute, four iterations from 2023 to 2026.', '2', 'traj'),
    ('lab-3-civic',        '07', 'AT-LAB III — Civic',    'AT-LAB III — Civic',
     'AT-LAB III: the Semiotic Protocol and Promptare, civic formats for reading AI images and prompts together, 2025.', '3', 'traj'),
    ('lab-4-atmosfera',    '08', 'AT-LAB IV — ATMOS_FERA','AT-LAB IV — ATMOS_FERA',
     'AT-LAB IV: ATMOS_FERA, an audiovisual performance translating an atmospheric model into spatial sound and image; accepted at ISEA2026.', '4', 'traj'),
    ('synthesis',          '09', 'Synthesis',             'Synthesis',
     'What the four AT-LABs together support, what they only suggest, and what remains open before the final assessment.', None, 'traj'),
    ('roles',              '10', 'Roles & Learning Goals', 'Roles & Learning Goals',
     'The five learning goals of the PD and the four roles they take over, each read against the evidence on file.', None, 'assess'),
    ('assessment-map',     '11', 'Assessment Map',        'Assessment Map',
     'Where each of the five required portfolio components and each of the five learning goals is evidenced in this portfolio.', None, 'assess'),
    ('supervision',        '12', 'Supervision',           'Supervision',
     'The supervisory team, the meetings on record, and how supervision has shaped the trajectory.', None, 'assess'),
    ('training',           '13', 'Training & Curriculum', 'Training & Curriculum',
     'Training record: the collective programme, individual units and teaching, the conference elements, how the EC are counted, and what remains to be confirmed and written.', None, 'assess'),
    ('research-teaching',  '14', 'Research ↔ Teaching',   'Research ↔ Teaching',
     'How research and teaching feed each other across the four iterations of the AI course.', None, 'assess'),
    ('dissemination',      '15', 'Dissemination',         'Dissemination',
     'Every output with its true status: presented, accepted, in review or in preparation.', None, 'assess'),
    ('evidence',           '16', 'Evidence Archive',      'Evidence Archive',
     'The evidence behind the portfolio, what is public, and what is held on file and available on request.', None, 'assess'),
]

GROUP_LABELS = {'traj': 'Trajectory', 'assess': 'Assessment'}

FONTS = ('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;1,300;1,400;1,500'
         '&family=DM+Mono:wght@300;400;500&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,400&display=swap')

FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E"
           "%3Crect width='32' height='32' fill='%23f5f0e8'/%3E%3Cpath d='M16 4l10 12-10 12L6 16z' fill='%239a6e30'/%3E"
           "%3Ccircle cx='16' cy='16' r='4' fill='%23f5f0e8'/%3E%3C/svg%3E")

EXTRA_SCRIPTS = {'evidence': ['js/evidence.js']}


def esc(s):
    return s.replace('&', '&amp;')


def nav_html():
    out = []
    out.append('<a href="index.html" class="nav-link nav-link-home"><span class="nav-num">00</span>Home</a>')
    out.append('<a href="updates.html" class="nav-link nav-link-sub"><span class="nav-num">·</span>Updates since March<span class="nav-new">New</span></a>')
    for group in ('traj', 'assess'):
        if group == 'assess':
            out.append('<div class="nav-divider"></div>')
        out.append('<div class="nav-group">')
        out.append(f'  <div class="nav-group-label">{GROUP_LABELS[group]}</div>')
        for slug, num, label, *_rest in PAGES:
            if _rest[-1] == group:
                out.append(f'  <a href="{slug}.html" class="nav-link"><span class="nav-num">{num}</span>{esc(label)}</a>')
        out.append('</div>')
    return '\n      '.join(out)


def wrap_tables(html):
    """Wrap bare data tables in a scroll container for small screens."""
    def repl(m):
        return f'<div class="table-wrap" role="region" aria-label="Table, scrollable" tabindex="0">{m.group(0)}</div>'
    parts = re.split(r'(<div class="table-wrap".*?</div>)', html, flags=re.S)
    out = []
    for part in parts:
        if part.startswith('<div class="table-wrap"'):
            out.append(part)
        else:
            out.append(re.sub(r'<table class="data-table[^"]*".*?</table>', repl, part, flags=re.S))
    return ''.join(out)


def label_cells(html):
    """Copy each <th> text onto the matching <td> as data-label, so tables can stack on phones."""
    def strip(t):
        t = re.sub(r'<[^>]+>', '', t)
        return re.sub(r'\s+', ' ', t).replace('&amp;', '&').strip()

    def do_table(m):
        tbl = m.group(0)
        head = re.search(r'<thead>(.*?)</thead>', tbl, flags=re.S)
        if not head:
            return tbl
        labels = [strip(x) for x in re.findall(r'<th[^>]*>(.*?)</th>', head.group(1), flags=re.S)]
        if not labels:
            return tbl

        def do_row(rm):
            row = rm.group(0)
            if '<th' in row:
                return row
            i = [-1]

            def do_td(tm):
                i[0] += 1
                label = labels[i[0]] if i[0] < len(labels) else ''
                attrs, inner = tm.group(1), tm.group(2)
                if not strip(inner) and 'data-label' not in attrs:
                    return f'<td{attrs} data-empty="1">{inner}</td>'
                if 'data-label' in attrs or not label:
                    return tm.group(0)
                return f'<td{attrs} data-label="{label.replace(chr(34), "&quot;")}"><span class="cell">{inner}</span></td>'
            return re.sub(r'<td([^>]*)>(.*?)</td>', do_td, row, flags=re.S)
        return re.sub(r'<tr[^>]*>.*?</tr>', do_row, tbl, flags=re.S)
    def add_roles(m):
        t = m.group(0)
        t = re.sub(r'<table(?![^>]*role=)', '<table role="table"', t, count=1)
        t = re.sub(r'<(thead|tbody|tfoot)>', r'<\1 role="rowgroup">', t)
        t = re.sub(r'<tr(?![^>]*role=)(?=[ >])', '<tr role="row"', t)
        t = re.sub(r'<th(?![^>]*role=)(?=[ >])', '<th role="columnheader"', t)
        t = re.sub(r'<td(?![^>]*role=)(?=[ >])', '<td role="cell"', t)
        return t
    html = re.sub(r'<table class="data-table[^"]*".*?</table>', do_table, html, flags=re.S)
    return re.sub(r'<table class="data-table[^"]*".*?</table>', add_roles, html, flags=re.S)


def inject_hero_geo(html):
    if 'hero-geo' in html:
        return html
    m = re.search(r'<(header|section)\s+class="page-hero"[^>]*>', html)
    if not m:
        return html
    geo = '\n  <div class="hero-geo" aria-hidden="true"><i></i><i></i><i></i></div>'
    return html[:m.end()] + geo + html[m.end():]


def render(idx):
    slug, num, label, title, desc, lab, group = PAGES[idx]
    path = os.path.join(SRC, slug + '.html')
    if not os.path.exists(path):
        print(f'  ! missing content for {slug}')
        return None
    content = open(path, encoding='utf-8').read()
    content = content.replace('{{UPDATED}}', UPDATED)
    content = inject_hero_geo(content)
    content = label_cells(content)
    content = wrap_tables(content)
    content = '\n'.join(('  ' + l if l.strip() else l) for l in content.rstrip('\n').split('\n'))

    # "Updates since March" sits beside the main sequence, not in it: Home runs on to the
    # Trajectory, and the Updates page itself sits between Home and the Trajectory.
    chain = [pg for pg in PAGES if pg[0] != 'updates']
    if slug == 'updates':
        prev_p, next_p = chain[0], chain[1]
    else:
        i = chain.index(PAGES[idx])
        prev_p = chain[i - 1] if i > 0 else None
        next_p = chain[i + 1] if i < len(chain) - 1 else None
    pn = []
    if prev_p:
        pn.append(f'<a class="pn-prev" href="{prev_p[0]}.html" rel="prev"><span class="pn-dir">← Previous</span><span class="pn-title">{esc(prev_p[3])}</span></a>')
    if next_p:
        pn.append(f'<a class="pn-next" href="{next_p[0]}.html" rel="next"><span class="pn-dir">Next →</span><span class="pn-title">{esc(next_p[3])}</span></a>')
    page_nav = '\n      '.join(pn)

    body_attr = f' data-lab="{lab}"' if lab else ''
    full_title = title if slug == 'index' else f'{title} — {SITE_NAME}'
    if slug == 'index':
        full_title = f'{SITE_NAME} — PD Assessment Portfolio'
    scripts = ['js/nav.js', 'js/animations.js'] + EXTRA_SCRIPTS.get(slug, [])
    script_tags = '\n  '.join(f'<script src="{s}" defer></script>' for s in scripts)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(full_title)}</title>
  <meta name="description" content="{desc.replace('"', '&quot;')}">
  <meta name="theme-color" content="#f5f0e8">
  <meta property="og:title" content="{esc(full_title)}">
  <meta property="og:description" content="{desc.replace('"', '&quot;')}">
  <meta property="og:type" content="website">
  <link rel="icon" href="{FAVICON}">
  <script>document.documentElement.classList.add('js');window.__revealGuard=setTimeout(function(){{document.documentElement.classList.remove('js');}},3500);</script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="{FONTS}" rel="stylesheet">
  <link rel="stylesheet" href="css/tokens.css">
  <link rel="stylesheet" href="css/layout.css">
  <link rel="stylesheet" href="css/components.css">
  <link rel="stylesheet" href="css/animations.css">
  <link rel="stylesheet" href="css/print.css" media="print">
</head>
<body{body_attr}>
  <a class="skip-link" href="#main">Skip to content</a>
  <button class="hamburger" id="menuToggle" type="button" aria-label="Open navigation menu"><span></span><span></span><span></span></button>
  <div class="sidebar-overlay" aria-hidden="true"></div>
  <aside id="sidebar" aria-label="Site navigation">
    <div class="sb-header">
      <div class="sb-name"><a href="index.html">Agustín Martínez Caram</a></div>
      <div class="sb-programme">PD Arts + Creative · Hanze</div>
    </div>
    <nav aria-label="Portfolio sections">
      {nav_html()}
    </nav>
    <div class="sb-footer">
      <a href="https://martinezcaram.com" target="_blank" rel="noopener">martinezcaram.com ↗</a>
      <a href="https://jannacek.github.io/teaching/" target="_blank" rel="noopener">Teaching site ↗</a>
      <a href="https://jannacek.github.io/ATMOS_FERA/" target="_blank" rel="noopener">ATMOS_FERA site ↗</a>
      <a href="https://www.hanze.nl" target="_blank" rel="noopener">Hanze University ↗</a>
      <span class="sb-updated">Updated {UPDATED}</span>
    </div>
  </aside>

  <main id="main" tabindex="-1">
{content}

    <nav class="page-nav" aria-label="Previous and next page">
      {page_nav}
    </nav>
    <footer class="site-footer">
      <span>© 2023–2026 Agustín Martínez Caram · PD Arts + Creative, Hanze University of Applied Sciences · Registered trajectory June 2023 – May 2027</span>
      <span>Updated {UPDATED} · <a href="updates.html">What changed since March</a></span>
      <span class="footer-elsewhere">Elsewhere: <a href="https://www.martinezcaram.com/" target="_blank" rel="noopener">martinezcaram.com ↗</a> · <a href="https://www.researchcatalogue.net/view/2952757/3715989" target="_blank" rel="noopener">Research Catalogue ↗</a> · <a href="https://www.pd-arts-creative.nl/about/how" target="_blank" rel="noopener">PD programme ↗</a> · <a href="https://github.com/jannacek?tab=repositories" target="_blank" rel="noopener">GitHub ↗</a></span>
    </footer>
  </main>
  {script_tags}
</body>
</html>
'''


def main():
    only = set(sys.argv[1:])
    for i, p in enumerate(PAGES):
        if only and p[0] not in only:
            continue
        html = render(i)
        if html is None:
            continue
        with open(os.path.join(ROOT, p[0] + '.html'), 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'  built {p[0]}.html')


if __name__ == '__main__':
    main()
