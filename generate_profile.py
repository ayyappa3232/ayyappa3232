#!/usr/bin/env python3
"""Generate animated GitHub profile assets — Cosmic 3D theme."""

import base64
from pathlib import Path

ROOT = Path(__file__).parent
AVATAR_B64 = (ROOT / "avatar.b64.txt").read_text().strip()

# ── Dummy profile data (replace later — see CUSTOMIZATION.md) ──
PROFILE = {
    "name": "Ayyappa",
    "full_name": "Ayyappa Kumar",
    "role": "AI Native Engineer",
    "roles_cycle": ["AI Native Engineer", "Full Stack Developer", "React Native Dev"],
    "username": "ayyappa3232",
    "email": "your.email@example.com",
    "location": "India",
    "tagline": "Always learning, always building ✨",
    "about": [
        "Building intelligent apps with AI and modern web tech",
        "Passionate about clean code and great UX",
        "Open to collaborate on exciting projects",
    ],
    "skills": ["React", "TypeScript", "Node.js", "Python", "AI/LLMs", "React Native", "SQL", "Three.js"],
    "stats": {"stars": "12+", "commits": "500+", "repos": "5+", "prs": "8+", "grade": "B+"},
    "langs": [("TypeScript", 35), ("JavaScript", 30), ("Python", 20), ("HTML/CSS", 15)],
    "trophies": [("S", "Commits"), ("A", "Stars"), ("B+", "Repos"), ("A", "PRs"), ("B", "Issues"), ("C", "Followers")],
    "projects": [
        ("Ayyappa-Full-Stack-Engineer", "TypeScript, React, Node", "0"),
        ("RN_ASP_Server", "C#, React Native, ASP.NET", "0"),
        ("reactnativefirebasedemo", "React Native, Firebase", "0"),
        ("LeaveManagementSystem", "JavaScript, React Native", "0"),
        ("LMS", "JavaScript, Node.js", "0"),
    ],
    "social": {
        "linkedin": "https://linkedin.com/in/your-profile",
        "portfolio": "https://your-portfolio.com",
        "email": "mailto:your.email@example.com",
    },
    "cache_v": "6",
}

def xml_escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )

# Cosmic 3D palette — deep space + electric cyan + violet + gold
C = {
    "bg1": "#070b1a",
    "bg2": "#12103a",
    "panel_hi": "#1c1c4a",
    "panel_lo": "#080812",
    "glass": "#141432",
    "glass2": "#1a1a42",
    "cyan": "#00e5ff",
    "cyan_dim": "#0891b2",
    "violet": "#a855f7",
    "pink": "#ec4899",
    "gold": "#fbbf24",
    "text": "#e2e8f0",
    "text_dim": "#94a3b8",
    "border": "#6366f1",
    "shadow": "#000000",
}


def banner_svg(light=False):
    if light:
        bg1, bg2 = "#eef2ff", "#e0e7ff"
        panel_hi, panel_lo = "#ffffff", "#f1f5f9"
        glass, glass2 = "#ffffff", "#f8fafc"
        text, text_dim = "#0f172a", "#475569"
        cyan, violet, pink, gold = "#0891b2", "#7c3aed", "#db2777", "#d97706"
        term_bg, code_bg = "#1e293b", "#0f172a"
        term_text, code_text = "#67e8f9", "#a5f3fc"
        glow = "#0891b2"
    else:
        bg1, bg2 = C["bg1"], C["bg2"]
        panel_hi, panel_lo = C["panel_hi"], C["panel_lo"]
        glass, glass2 = C["glass"], C["glass2"]
        text, text_dim = C["text"], C["text_dim"]
        cyan, violet, pink, gold = C["cyan"], C["violet"], C["pink"], C["gold"]
        term_bg, code_bg = "#0c1222", "#060a14"
        term_text, code_text = C["cyan"], "#7dd3fc"
        glow = C["cyan"]

    roles = PROFILE["roles_cycle"]
    role_dur = 4
    cycle_total = len(roles) * role_dur

    # ── Name letters pop-in ──
    name_letters = ""
    for i, ch in enumerate(PROFILE["name"]):
        name_letters += f'''
      <tspan opacity="0" fill="url(#nameGrad)">
        <animate attributeName="opacity" from="0" to="1" begin="{0.6 + i * 0.07}s" dur="0.35s" fill="freeze"/>
        <animate attributeName="dy" from="-16" to="0" begin="{0.6 + i * 0.07}s" dur="0.4s" fill="freeze"/>
        {xml_escape(ch)}
      </tspan>'''

    # ── Roles — one visible at a time (no overlap) ──
    role_anims = ""
    n = len(roles)
    for i, role in enumerate(roles):
        t0 = i / n
        t_in = t0 + 0.015
        t_out = (i + 1) / n - 0.015
        t_end = (i + 1) / n
        role_anims += f'''
      <text x="52" y="196" fill="{cyan}" font-family="'SF Mono',monospace" font-size="14" opacity="0">
        <animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;{t0:.3f};{t_in:.3f};{t_out:.3f};{t_end:.3f};1" dur="{cycle_total}s" repeatCount="indefinite"/>
        &gt; {xml_escape(role)}<tspan fill="{violet}"><animate attributeName="opacity" values="1;0;1" dur="0.9s" repeatCount="indefinite"/>▌</tspan>
      </text>'''

    # ── About lines ──
    about_lines = ""
    for i, line in enumerate(PROFILE["about"]):
        about_lines += f'''
      <text x="44" y="{302 + i * 24}" fill="{text_dim}" font-family="system-ui,sans-serif" font-size="12.5" opacity="0">
        <animate attributeName="opacity" from="0" to="1" begin="{1.6 + i * 0.25}s" dur="0.4s" fill="freeze"/>
        {xml_escape("• " + line)}
      </text>'''

    # ── Tech pills (2 rows, fixed grid) ──
    skills_pills = ""
    pill_w = [88, 98, 88, 88]
    for i, sk in enumerate(PROFILE["skills"][:8]):
        col = i % 4
        row = i // 4
        x = 44 + col * 148
        y = 410 + row * 34
        w = max(len(sk) * 8 + 22, 72)
        skills_pills += f'''
      <g opacity="0">
        <animate attributeName="opacity" from="0" to="1" begin="{2.2 + i * 0.1}s" dur="0.4s" fill="freeze"/>
        <rect x="{x}" y="{y}" width="{w}" height="24" rx="12" fill="url(#pillGrad)" stroke="{cyan}" stroke-width="0.8" opacity="0.9"/>
        <text x="{x + 11}" y="{y + 16}" fill="{text}" font-family="system-ui,sans-serif" font-size="11">{xml_escape(sk)}</text>
      </g>'''

    # ── Code card — absolute coords only (GitHub SVG sanitizer strips transform) ──
    code_y = 478
    code_lines = [
        "const buildDreams = () => {",
        "  return ['React','AI','Node']",
        "    .map(idea => ship(idea));",
        "};",
    ]
    code_svg = ""
    for i, line in enumerate(code_lines):
        code_svg += f'''
    <text x="50" y="{code_y + 50 + i * 17}" fill="{code_text}" font-family="monospace" font-size="10.5" opacity="0">
      <animate attributeName="opacity" from="0" to="1" begin="{3.2 + i * 0.35}s" dur="0.3s" fill="freeze"/>
      {xml_escape(line)}
    </text>'''

    stats = PROFILE["stats"]

    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 1280 740" width="1280" height="740">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{bg1}"/>
      <stop offset="100%" stop-color="{bg2}"/>
    </linearGradient>
    <linearGradient id="panelGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{panel_hi}"/>
      <stop offset="100%" stop-color="{panel_lo}"/>
    </linearGradient>
    <linearGradient id="nameGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{cyan}">
        <animate attributeName="stop-color" values="{cyan};{violet};{pink};{cyan}" dur="5s" repeatCount="indefinite"/>
      </stop>
      <stop offset="100%" stop-color="{violet}">
        <animate attributeName="stop-color" values="{violet};{pink};{cyan};{violet}" dur="5s" repeatCount="indefinite"/>
      </stop>
    </linearGradient>
    <linearGradient id="pillGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{glass2}"/>
      <stop offset="100%" stop-color="{glass}"/>
    </linearGradient>
    <linearGradient id="frameGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{cyan}" stop-opacity="0.8"/>
      <stop offset="50%" stop-color="{violet}" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="{pink}" stop-opacity="0.8"/>
    </linearGradient>
    <linearGradient id="scanGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{cyan}" stop-opacity="0"/>
      <stop offset="50%" stop-color="{cyan}" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="{cyan}" stop-opacity="0"/>
    </linearGradient>
    <filter id="drop3d" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#000" flood-opacity="0.55"/>
    </filter>
    <filter id="glow3d" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="4" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <clipPath id="roleClip"><rect x="44" y="176" width="580" height="28"/></clipPath>
    <clipPath id="photoClip"><rect x="700" y="72" width="520" height="596" rx="14"/></clipPath>
    <clipPath id="photoReveal"><rect x="700" y="668" width="520" height="0">
      <animate attributeName="y" from="668" to="72" dur="1.6s" begin="0.4s" fill="freeze"/>
      <animate attributeName="height" from="0" to="596" dur="1.6s" begin="0.4s" fill="freeze"/>
    </rect></clipPath>
  </defs>

  <!-- Background -->
  <rect width="1280" height="740" fill="url(#bgGrad)" rx="14"/>
  <circle cx="180" cy="120" r="120" fill="{violet}" opacity="0.07"/>
  <circle cx="1050" cy="620" r="140" fill="{cyan}" opacity="0.06"/>
  <circle cx="640" cy="370" r="200" fill="{pink}" opacity="0.03"/>

  <!-- ═══ LEFT PANEL (3D card) ═══ -->
  <g filter="url(#drop3d)">
    <rect x="22" y="22" width="636" height="696" rx="18" fill="{panel_lo}" opacity="0.5"/>
    <rect x="20" y="20" width="636" height="696" rx="18" fill="url(#panelGrad)" stroke="url(#frameGrad)" stroke-width="1.5"/>
    <rect x="24" y="22" width="628" height="4" rx="2" fill="white" opacity="0.07"/>
  </g>

  <!-- Terminal -->
  <rect x="36" y="36" width="604" height="34" rx="8" fill="{term_bg}" stroke="{cyan}" stroke-width="0.6" opacity="0.95"/>
  <circle cx="50" cy="53" r="5" fill="#ff5f57"/><circle cx="66" cy="53" r="5" fill="#febc2e"/><circle cx="82" cy="53" r="5" fill="#28c840"/>
  <text x="98" y="57" fill="{term_text}" font-family="monospace" font-size="13">
    user@dev:~$ cat README.md<tspan fill="{gold}"><animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/>█</tspan>
  </text>

  <!-- Greeting + Name -->
  <text x="44" y="98" fill="{text_dim}" font-family="system-ui,sans-serif" font-size="14" opacity="0">
    <animate attributeName="opacity" from="0" to="1" begin="0.4s" dur="0.5s" fill="freeze"/>
    Hi, I'm 👋
  </text>
  <text x="44" y="148" font-family="Georgia,'Times New Roman',serif" font-size="46" font-weight="bold">{name_letters}</text>

  <!-- Role (cycling, clipped) -->
  <rect x="36" y="168" width="604" height="36" rx="8" fill="{glass}" stroke="{violet}" stroke-width="0.6" opacity="0.85"/>
  <g clip-path="url(#roleClip)">{role_anims}</g>

  <!-- Tagline -->
  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" begin="1.2s" dur="0.5s" fill="freeze"/>
    <rect x="36" y="216" width="520" height="38" rx="8" fill="{glass2}" stroke="{pink}" stroke-width="0.6"/>
    <text x="50" y="240" fill="{text}" font-family="system-ui,sans-serif" font-size="13" font-style="italic">"{xml_escape(PROFILE['tagline'])}"</text>
  </g>

  <!-- About Me -->
  <text x="44" y="282" fill="{gold}" font-family="system-ui,sans-serif" font-size="13" font-weight="bold" opacity="0">
    <animate attributeName="opacity" from="0" to="1" begin="1.4s" dur="0.4s" fill="freeze"/>
    ✦ About Me
  </text>
  {about_lines}

  <!-- Stats bar -->
  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" begin="2.0s" dur="0.5s" fill="freeze"/>
    <rect x="36" y="368" width="604" height="30" rx="8" fill="{glass}" stroke="{cyan}" stroke-width="0.5"/>
    <text x="50" y="388" fill="{text_dim}" font-family="monospace" font-size="11">
      ⭐ {stats['stars']} stars   ·   📝 {stats['commits']} commits   ·   📦 {stats['repos']} repos   ·   🔀 {stats['prs']} PRs
    </text>
  </g>

  <!-- Tech stack label + pills -->
  <text x="44" y="398" fill="{violet}" font-family="system-ui,sans-serif" font-size="12" font-weight="bold" opacity="0">
    <animate attributeName="opacity" from="0" to="1" begin="2.1s" dur="0.4s" fill="freeze"/>
    ⚡ Tech Stack
  </text>
  {skills_pills}

  <!-- Code editor (3D inset) — absolute positions, no transform -->
  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" begin="2.8s" dur="0.5s" fill="freeze"/>
    <rect x="36" y="{code_y}" width="290" height="108" rx="10" fill="{code_bg}" stroke="{cyan}" stroke-width="0.8"/>
    <rect x="36" y="{code_y}" width="290" height="24" rx="10" fill="{panel_hi}"/>
    <rect x="36" y="{code_y + 16}" width="290" height="8" fill="{panel_hi}"/>
    <circle cx="50" cy="{code_y + 12}" r="4" fill="#ff5f57"/><circle cx="64" cy="{code_y + 12}" r="4" fill="#febc2e"/><circle cx="78" cy="{code_y + 12}" r="4" fill="#28c840"/>
    <text x="92" y="{code_y + 16}" fill="{text_dim}" font-family="monospace" font-size="9">dreams.jsx</text>
    {code_svg}
  </g>

  <!-- Neon sign -->
  <g filter="url(#glow3d)" opacity="0">
    <animate attributeName="opacity" from="0" to="1" begin="3.8s" dur="0.4s" fill="freeze"/>
    <text x="360" y="690" fill="{cyan}" font-family="monospace" font-size="12" font-weight="bold" text-anchor="middle">
      <animate attributeName="opacity" values="1;0.55;1;0.75;1" dur="2.5s" repeatCount="indefinite"/>
      KEEP CODING  ·  KEEP GROWING
    </text>
  </g>

  <!-- ═══ RIGHT PANEL — 3D photo frame ═══ -->
  <g filter="url(#drop3d)">
    <rect x="692" y="52" width="556" height="636" rx="18" fill="{panel_lo}" opacity="0.4"/>
    <rect x="688" y="48" width="556" height="636" rx="18" fill="url(#panelGrad)" stroke="url(#frameGrad)" stroke-width="2"/>
    <rect x="692" y="50" width="548" height="5" rx="2" fill="white" opacity="0.08"/>
  </g>

  <!-- Photo with reveal -->
  <g clip-path="url(#photoReveal)">
    <g clip-path="url(#photoClip)">
      <image x="700" y="72" width="520" height="596" preserveAspectRatio="xMidYMid slice"
             href="data:image/jpeg;base64,{AVATAR_B64}" xlink:href="data:image/jpeg;base64,{AVATAR_B64}"/>
      <rect x="700" y="72" width="520" height="596" fill="url(#panelGrad)" opacity="0.15"/>
    </g>
  </g>

  <!-- Soft scanner (subtle) -->
  <g clip-path="url(#photoClip)">
    <rect x="700" y="72" width="520" height="6" fill="url(#scanGrad)" opacity="0.5">
      <animate attributeName="y" from="72" to="662" dur="4.5s" repeatCount="indefinite"/>
    </rect>
  </g>

  <!-- Floating particles -->
  <circle cx="600" cy="200" r="2" fill="{cyan}" opacity="0">
    <animate attributeName="opacity" values="0;0.8;0" dur="2.5s" begin="1s" repeatCount="indefinite"/>
  </circle>
  <circle cx="120" cy="450" r="1.5" fill="{pink}" opacity="0">
    <animate attributeName="opacity" values="0;0.7;0" dur="2s" begin="2s" repeatCount="indefinite"/>
  </circle>
</svg>'''


def lanyard_svg():
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 320 480" width="320" height="480">
  <defs>
    <linearGradient id="strapGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{C['cyan']}"/>
      <stop offset="100%" stop-color="{C['violet']}"/>
    </linearGradient>
    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{C['panel_hi']}"/>
      <stop offset="100%" stop-color="{C['panel_lo']}"/>
    </linearGradient>
    <linearGradient id="shine" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="white" stop-opacity="0"/>
      <stop offset="50%" stop-color="white" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="white" stop-opacity="0"/>
    </linearGradient>
    <filter id="card3d"><feDropShadow dx="0" dy="6" stdDeviation="8" flood-opacity="0.5"/></filter>
    <clipPath id="avatarClip"><circle cx="160" cy="280" r="52"/></clipPath>
  </defs>

  <g transform="rotate(0 160 0)">
    <animateTransform attributeName="transform" type="rotate"
      values="0 160 0; 8 160 0; -6 160 0; 4 160 0; -2 160 0; 0 160 0"
      dur="4s" begin="0.8s" repeatCount="indefinite"/>
    <animateTransform attributeName="transform" type="translate"
      values="0 -400; 0 0" dur="0.8s" begin="0s" fill="freeze" additive="sum"
      calcMode="spline" keySplines="0.2 0.8 0.2 1"/>

    <rect x="148" y="0" width="24" height="200" fill="url(#strapGrad)" rx="4"/>
    <text x="160" y="80" fill="white" font-family="monospace" font-size="8" text-anchor="middle" transform="rotate(90 160 80)">{PROFILE['username'].upper()}</text>
    <rect x="142" y="198" width="36" height="12" rx="3" fill="#888"/>
    <circle cx="160" cy="218" r="10" fill="#bbb" stroke="#666" stroke-width="2"/>

    <g filter="url(#card3d)">
      <rect x="70" y="228" width="180" height="230" rx="14" fill="url(#cardGrad)" stroke="{C['cyan']}" stroke-width="2"/>
    </g>
    <rect x="70" y="228" width="180" height="230" rx="14" fill="url(#shine)" opacity="0">
      <animate attributeName="opacity" values="0;0.5;0" dur="2.5s" repeatCount="indefinite"/>
      <animateTransform attributeName="transform" type="translate" from="-180 0" to="180 0" dur="2.5s" repeatCount="indefinite"/>
    </rect>

    <circle cx="160" cy="280" r="56" fill="none" stroke="{C['cyan']}" stroke-width="3" opacity="0.9">
      <animate attributeName="stroke-opacity" values="0.7;1;0.7" dur="2s" repeatCount="indefinite"/>
    </circle>
    <g clip-path="url(#avatarClip)">
      <image x="108" y="228" width="104" height="104" preserveAspectRatio="xMidYMid slice"
             href="data:image/jpeg;base64,{AVATAR_B64}" xlink:href="data:image/jpeg;base64,{AVATAR_B64}"/>
    </g>

    <text x="160" y="360" fill="{C['text']}" font-family="system-ui" font-size="16" font-weight="bold" text-anchor="middle">{PROFILE['name']}</text>
    <text x="160" y="380" fill="{C['cyan']}" font-family="system-ui" font-size="11" text-anchor="middle">{PROFILE['role']}</text>
    <text x="160" y="398" fill="{C['text_dim']}" font-family="monospace" font-size="10" text-anchor="middle">@{PROFILE['username']}</text>
    <g transform="translate(90, 410)">
      {"".join(f'<rect x="{i*4}" y="0" width="{2 if i%3 else 3}" height="28" fill="{C["violet"]}"/>' for i in range(22))}
    </g>
    <text x="160" y="455" fill="{C['text_dim']}" font-family="monospace" font-size="8" text-anchor="middle">DEV ID • 2026</text>
  </g>
</svg>'''


def stats_svg():
    s = PROFILE["stats"]
    rows = [
        ("Total Stars Earned", s["stars"]),
        ("Total Commits", s["commits"]),
        ("Public Repos", s["repos"]),
        ("Pull Requests", s["prs"]),
    ]
    rows_svg = ""
    for i, (label, val) in enumerate(rows):
        rows_svg += f'''
  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" begin="{0.3 + i*0.2}s" dur="0.4s" fill="freeze"/>
    <animateTransform attributeName="transform" type="translate" from="-30 0" to="0 0" begin="{0.3 + i*0.2}s" dur="0.4s" fill="freeze"/>
    <text x="24" y="{100 + i*36}" fill="{C['text_dim']}" font-family="system-ui" font-size="13">{label}</text>
    <text x="360" y="{100 + i*36}" fill="{C['cyan']}" font-family="monospace" font-size="14" font-weight="bold" text-anchor="end">{val}</text>
    <line x1="24" y1="{108 + i*36}" x2="360" y2="{108 + i*36}" stroke="{C['border']}" stroke-width="1" opacity="0.4"/>
  </g>'''

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 220" width="400" height="220">
  <defs>
    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{C['panel_hi']}"/>
      <stop offset="100%" stop-color="{C['panel_lo']}"/>
    </linearGradient>
    <filter id="s3d"><feDropShadow dx="0" dy="4" stdDeviation="6" flood-opacity="0.4"/></filter>
  </defs>
  <rect width="400" height="220" rx="12" fill="url(#cardGrad)" stroke="{C['cyan']}" stroke-width="1.5" filter="url(#s3d)"/>
  <text x="24" y="36" fill="{C['text']}" font-family="system-ui" font-size="16" font-weight="bold">{PROFILE['name']}'s GitHub Stats</text>
  <circle cx="360" cy="36" r="22" fill="none" stroke="{C['violet']}" stroke-width="3" stroke-dasharray="100" stroke-dashoffset="100">
    <animate attributeName="stroke-dashoffset" from="100" to="25" dur="1.5s" fill="freeze"/>
  </circle>
  <text x="360" y="41" fill="{C['gold']}" font-family="monospace" font-size="14" font-weight="bold" text-anchor="middle">{s['grade']}</text>
  {rows_svg}
</svg>'''


def langs_svg():
    bars = ""
    for i, (lang, pct) in enumerate(PROFILE["langs"]):
        y = 50 + i * 42
        bars += f'''
  <text x="20" y="{y}" fill="{C['text']}" font-family="system-ui" font-size="13">{lang}</text>
  <text x="380" y="{y}" fill="{C['cyan']}" font-family="monospace" font-size="12" text-anchor="end">{pct}%</text>
  <rect x="20" y="{y+6}" width="360" height="12" rx="6" fill="{C['glass']}"/>
  <rect x="20" y="{y+6}" width="0" height="12" rx="6" fill="url(#barGrad)">
    <animate attributeName="width" from="0" to="{pct*3.6}" dur="1.2s" begin="{0.2 + i*0.15}s" fill="freeze"/>
  </rect>'''

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 220" width="400" height="220">
  <defs>
    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{C['panel_hi']}"/>
      <stop offset="100%" stop-color="{C['panel_lo']}"/>
    </linearGradient>
    <linearGradient id="barGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{C['cyan']}"/>
      <stop offset="100%" stop-color="{C['violet']}"/>
    </linearGradient>
  </defs>
  <rect width="400" height="220" rx="12" fill="url(#cardGrad)" stroke="{C['violet']}" stroke-width="1.5"/>
  <text x="20" y="32" fill="{C['text']}" font-family="system-ui" font-size="16" font-weight="bold">Top Languages</text>
  {bars}
</svg>'''


def trophies_svg():
    cells = ""
    colors = [C["cyan"], C["violet"], C["pink"], C["gold"], C["border"], "#6366f1"]
    for i, (grade, label) in enumerate(PROFILE["trophies"]):
        col = i % 3
        row = i // 3
        x = 20 + col * 130
        y = 50 + row * 85
        cells += f'''
  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" begin="{0.2 + i*0.12}s" dur="0.35s" fill="freeze"/>
    <rect x="{x}" y="{y}" width="120" height="72" rx="10" fill="{C['glass']}" stroke="{colors[i]}" stroke-width="1.5"/>
    <text x="{x+60}" y="{y+38}" fill="{colors[i]}" font-family="monospace" font-size="28" font-weight="bold" text-anchor="middle">{grade}</text>
    <text x="{x+60}" y="{y+58}" fill="{C['text_dim']}" font-family="system-ui" font-size="10" text-anchor="middle">{label}</text>
  </g>'''

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 220" width="400" height="220">
  <defs>
    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{C['panel_hi']}"/>
      <stop offset="100%" stop-color="{C['panel_lo']}"/>
    </linearGradient>
    <linearGradient id="shine" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="white" stop-opacity="0"/>
      <stop offset="50%" stop-color="white" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="white" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <rect width="400" height="220" rx="12" fill="url(#cardGrad)" stroke="{C['pink']}" stroke-width="1.5"/>
  <text x="20" y="32" fill="{C['text']}" font-family="system-ui" font-size="16" font-weight="bold">GitHub Trophies</text>
  <rect x="0" y="0" width="400" height="220" fill="url(#shine)" opacity="0">
    <animate attributeName="opacity" values="0;1;0" dur="3s" repeatCount="indefinite"/>
    <animateTransform attributeName="transform" type="translate" from="-400 0" to="400 0" dur="3s" repeatCount="indefinite"/>
  </rect>
  {cells}
</svg>'''


def readme_md():
    v = PROFILE["cache_v"]
    u = PROFILE["username"]
    soc = PROFILE["social"]
    raw = f"https://raw.githubusercontent.com/{u}/{u}/main"

    proj_rows = "\n".join(
        f"| [{name}](https://github.com/{u}/{name}) | {tech} | ⭐ {stars} |"
        for name, tech, stars in PROFILE["projects"]
    )

    return f'''<div align="center">

<!-- Use full raw URLs + ?v= cache bust — GitHub profile caches relative paths aggressively -->
<img alt="Animated profile banner" src="{raw}/banner.svg?v={v}" width="100%"/>

<br/><br/>

<!-- ID Badge + Projects -->
<table>
<tr>
<td width="320" valign="top" align="center">
  <img alt="Swinging ID badge" src="{raw}/lanyard.svg?v={v}" width="280"/>
</td>
<td valign="top">

### ✨ My Projects

| Project | Tech | Stars |
|---------|------|-------|
{proj_rows}

*"I don't just write code — I craft experiences."*

</td>
</tr>
</table>

<br/>

<!-- Stats row -->
<table>
<tr>
<td><img alt="GitHub Stats" src="{raw}/stats.svg?v={v}" width="400"/></td>
<td><img alt="Top Languages" src="{raw}/langs.svg?v={v}" width="400"/></td>
</tr>
</table>

<br/>

<!-- Trophies -->
<img alt="GitHub Trophies" src="{raw}/trophies.svg?v={v}" width="820"/>

<br/><br/>

<!-- Activity Graph -->
<img alt="Contribution Graph" src="https://github-readme-activity-graph.vercel.app/graph?username={u}&bg_color=070b1a&color=00e5ff&line=a855f7&point=ec4899&area=true&hide_border=false&custom_title=Contribution%20Graph%20✨" width="100%"/>

<br/><br/>

<!-- Snake (run Actions workflow first) -->
<img alt="Snake eating contributions" src="https://raw.githubusercontent.com/{u}/{u}/output/snake.svg?v={v}" width="100%"/>

<p align="center"><i>🐍 Watch the snake eat my contributions!</i></p>

<br/>

<!-- Connect -->
### 🤝 Let's Connect

[![GitHub](https://img.shields.io/badge/GitHub-ayyappa3232-00e5ff?style=for-the-badge&logo=github&logoColor=white)](https://github.com/{u})
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-a855f7?style=for-the-badge&logo=linkedin&logoColor=white)]({soc['linkedin']})
[![Portfolio](https://img.shields.io/badge/Portfolio-Visit-ec4899?style=for-the-badge&logo=google-chrome&logoColor=white)]({soc['portfolio']})
[![Email](https://img.shields.io/badge/Email-Reach%20Out-6366f1?style=for-the-badge&logo=gmail&logoColor=white)]({soc['email']})

<br/>

<!-- Profile views -->
<img alt="Profile views" src="https://komarev.com/ghpvc/?username={u}&label=Profile%20Views&color=00e5ff&style=for-the-badge"/>

<br/><br/>

**Always learning, always building. ✨**

</div>
'''


def snake_yml():
    u = PROFILE["username"]
    return f'''name: Generate Snake

on:
  schedule:
    - cron: "0 0 * * *"
  workflow_dispatch:

jobs:
  generate:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4

      - uses: Platane/snk@v3
        id: snake
        with:
          github_user_name: {u}
          outputs: |
            dist/snake.svg
          snake_color: "00e5ff"
          snake_color2: "a855f7"
          snake_color3: "12103a"

      - name: Push snake.svg to output branch
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git checkout -B output
          mv dist/snake.svg snake.svg
          git add snake.svg
          git diff --staged --quiet || git commit -m "Update snake contribution graph"
          git push origin output --force
'''


def customization_md():
    return '''# Customization Guide

Your profile is live with **dummy/placeholder data**. When you have your real info, update these files and ask me to regenerate — or edit manually.

---

## Quick checklist

| What to change | Where |
|----------------|-------|
| Name, role, tagline, about, skills | `generate_profile.py` → `PROFILE` dict, then run `python3 generate_profile.py` |
| Stats numbers (stars, commits, etc.) | `generate_profile.py` → `PROFILE["stats"]` |
| Language percentages | `generate_profile.py` → `PROFILE["langs"]` |
| Trophy grades | `generate_profile.py` → `PROFILE["trophies"]` |
| Projects table | `generate_profile.py` → `PROFILE["projects"]` |
| Social links | `generate_profile.py` → `PROFILE["social"]` |
| Email | `generate_profile.py` → `PROFILE["email"]` |
| Character image | Replace `character-placeholder.png`, re-run avatar export (see below) |
| Cache bust after edits | Bump `PROFILE["cache_v"]` from `"1"` to `"2"`, etc. |

---

## Step 1 — Replace character image

1. Generate an anime-style image (white background) using the prompt in the PDF guide.
2. Save it as `character-placeholder.png` in this folder.
3. Run:
   ```bash
   python3 -c "
   import base64
   from pathlib import Path
   b64 = base64.b64encode(Path('character-placeholder.png').read_bytes()).decode()
   Path('avatar.b64.txt').write_text(b64)
   "
   python3 generate_profile.py
   ```

---

## Step 2 — Update profile text

Open `generate_profile.py` and edit the `PROFILE` dictionary at the top:

```python
PROFILE = {
    "name": "Your Name",
    "full_name": "Your Full Name",
    "role": "AI Native Engineer",
    "roles_cycle": ["AI Native Engineer", "Full Stack Developer"],
    "username": "ayyappa3232",
    "email": "you@email.com",
    ...
}
```

Then regenerate:
```bash
python3 generate_profile.py
```

---

## Step 3 — Create the GitHub profile repo

1. Go to https://github.com/new
2. Repository name: **`ayyappa3232`** (must match username exactly)
3. Public, tick **Add a README file**
4. Upload all generated files to the repo root:
   - `banner.svg`, `banner-light.svg`, `lanyard.svg`
   - `stats.svg`, `langs.svg`, `trophies.svg`
   - `README.md`
   - `.github/workflows/github-snake.yml`

---

## Step 4 — Activate the snake

1. Open repo → **Actions** tab → enable workflows
2. Run **Generate Snake** workflow manually
3. Snake appears on profile after ~1 minute

---

## Step 5 — Cache trick

GitHub caches README images. If you edit an SVG and nothing changes:

1. Bump `?v=1` to `?v=2` in `README.md` for that image
2. Commit SVG first, then README with bumped version

---

## Files in this package

| File | Purpose |
|------|---------|
| `banner.svg` | Dark mode animated hero banner |
| `banner-light.svg` | Light mode banner (auto-switches) |
| `lanyard.svg` | Swinging ID badge |
| `stats.svg` | Local GitHub stats card |
| `langs.svg` | Top languages bars |
| `trophies.svg` | Trophy grid |
| `README.md` | Profile README (paste into repo) |
| `.github/workflows/github-snake.yml` | Daily snake generator |
| `generate_profile.py` | Regenerator script — edit PROFILE dict and re-run |
| `character-placeholder.png` | Your character art (replace later) |
| `avatar.b64.txt` | Base64 of character (auto-generated) |

---

## When ready for a full update

Send me:
- Your anime character image
- Real name, email, LinkedIn, portfolio URL
- Updated skills, tagline, about me
- Real stats (or I can pull from GitHub API)
- Projects you want featured

Say **"update my profile"** and I will regenerate everything with your real data.
'''


def main():
    (ROOT / "banner.svg").write_text(banner_svg(light=False))
    (ROOT / "banner-light.svg").write_text(banner_svg(light=True))
    (ROOT / "lanyard.svg").write_text(lanyard_svg())
    (ROOT / "stats.svg").write_text(stats_svg())
    (ROOT / "langs.svg").write_text(langs_svg())
    (ROOT / "trophies.svg").write_text(trophies_svg())
    (ROOT / "README.md").write_text(readme_md())
    (ROOT / ".github/workflows/github-snake.yml").write_text(snake_yml())
    (ROOT / "CUSTOMIZATION.md").write_text(customization_md())
    print("Generated all profile assets in", ROOT)


if __name__ == "__main__":
    main()
