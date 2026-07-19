#!/usr/bin/env python3
"""Generate animated GitHub profile assets — grass green theme."""

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
    "tagline": "Always learning, always building 🌿",
    "about": [
        "Building intelligent apps with AI & modern web tech",
        "Passionate about clean code & great UX",
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
    "cache_v": "2",
}

def xml_escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )

# Grass green palette
G = {
    "primary": "#22c55e",
    "light": "#4ade80",
    "dark": "#16a34a",
    "mint": "#86efac",
    "forest": "#15803d",
    "neon": "#39ff14",
    "bg_dark": "#0a120a",
    "bg_card": "#111a11",
    "bg_card2": "#161f16",
    "text": "#e6f5e6",
    "text_dim": "#94a894",
    "border": "#22c55e55",
}


def banner_svg(light=False):
    bg = "#f4fff4" if light else G["bg_dark"]
    card = "#ffffff" if light else G["bg_card"]
    card2 = "#eef8ee" if light else G["bg_card2"]
    text = "#0a1a0a" if light else G["text"]
    text_dim = "#4a6a4a" if light else G["text_dim"]
    accent = G["dark"] if light else G["primary"]
    accent2 = G["forest"] if light else G["light"]
    glow = G["forest"] if light else G["neon"]
    term_bg = "#e8f5e8" if light else "#0d1a0d"
    term_text = G["forest"] if light else G["mint"]

    roles = PROFILE["roles_cycle"]
    role_dur = 4
    role_total = len(roles) * role_dur

    skills_pills = ""
    for i, sk in enumerate(PROFILE["skills"][:8]):
        x = 40 + (i % 4) * 155
        y = 520 + (i // 4) * 36
        skills_pills += f'''
  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" begin="{2.5 + i * 0.15}s" dur="0.5s" fill="freeze"/>
    <rect x="{x}" y="{y}" width="{len(sk)*9+24}" height="26" rx="13" fill="{card2}" stroke="{accent}" stroke-width="1"/>
    <text x="{x+12}" y="{y+17}" fill="{accent2}" font-family="monospace" font-size="12">{xml_escape(sk)}</text>
  </g>'''

    about_lines = ""
    for i, line in enumerate(PROFILE["about"]):
        about_lines += f'''
    <text x="40" y="{430 + i*22}" fill="{text_dim}" font-family="system-ui,sans-serif" font-size="13" opacity="0">
      <animate attributeName="opacity" from="0" to="1" begin="{1.8 + i*0.3}s" dur="0.4s" fill="freeze"/>
      ▸ {xml_escape(line)}
    </text>'''

    name = PROFILE["name"]
    name_letters = ""
    for i, ch in enumerate(name):
        name_letters += f'''
    <tspan opacity="0" fill="url(#nameGrad)">
      <animate attributeName="opacity" from="0" to="1" begin="{0.8 + i*0.08}s" dur="0.3s" fill="freeze"/>
      <animate attributeName="dy" from="-20" to="0" begin="{0.8 + i*0.08}s" dur="0.4s" fill="freeze"/>
      {ch}
    </tspan>'''

    role_anims = ""
    for i, role in enumerate(roles):
        begin = i * role_dur
        role_anims += f'''
    <text x="40" y="175" fill="{accent2}" font-family="monospace" font-size="16" opacity="0">
      <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.05;0.9;1" begin="{begin}s" dur="{role_dur}s" repeatCount="indefinite"/>
      &gt; {xml_escape(role)}<tspan fill="{accent}" opacity="1"><animate attributeName="opacity" values="1;0;1" dur="0.8s" repeatCount="indefinite"/>_</tspan>
    </text>'''

    code_lines = [
        "const buildDreams = () => {",
        "  const stack = ['React','AI','Node'];",
        "  return stack.map(shipIt);",
        "};",
    ]
    code_svg = ""
    for i, line in enumerate(code_lines):
        code_svg += f'''
      <text x="16" y="{28 + i*18}" fill="{G['mint']}" font-family="monospace" font-size="11" opacity="0">
        <animate attributeName="opacity" from="0" to="1" begin="{3 + i*0.4}s" dur="0.3s" fill="freeze"/>
        {line}
      </text>'''

    stats = PROFILE["stats"]
    suffix = "-light" if light else ""

    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 1280 740" width="1280" height="740">
  <defs>
    <linearGradient id="nameGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{G['primary']}">
        <animate attributeName="stop-color" values="{G['primary']};{G['light']};{G['mint']};{G['primary']}" dur="4s" repeatCount="indefinite"/>
      </stop>
      <stop offset="100%" stop-color="{G['light']}">
        <animate attributeName="stop-color" values="{G['light']};{G['primary']};{G['light']}" dur="4s" repeatCount="indefinite"/>
      </stop>
    </linearGradient>
    <linearGradient id="scanGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{glow}" stop-opacity="0"/>
      <stop offset="50%" stop-color="{glow}" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="{glow}" stop-opacity="0"/>
    </linearGradient>
    <clipPath id="bannerClip"><rect x="680" y="60" width="560" height="620" rx="16"/></clipPath>
    <clipPath id="charReveal"><rect x="680" y="680" width="560" height="0">
      <animate attributeName="y" from="680" to="60" dur="1.8s" begin="0.5s" fill="freeze"/>
      <animate attributeName="height" from="0" to="620" dur="1.8s" begin="0.5s" fill="freeze"/>
    </rect></clipPath>
    <filter id="glow"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>

  <!-- Background -->
  <rect width="1280" height="740" fill="{bg}" rx="12"/>
  <!-- Ambient orbs -->
  <circle cx="200" cy="600" r="80" fill="{accent}" opacity="0.06">
    <animate attributeName="r" values="80;95;80" dur="5s" repeatCount="indefinite"/>
  </circle>
  <circle cx="1100" cy="150" r="60" fill="{G['light']}" opacity="0.05">
    <animate attributeName="opacity" values="0.05;0.12;0.05" dur="4s" repeatCount="indefinite"/>
  </circle>

  <!-- Left panel -->
  <rect x="20" y="20" width="640" height="700" rx="16" fill="{card}" stroke="{accent}" stroke-width="1" opacity="0.9"/>

  <!-- Terminal line -->
  <rect x="40" y="40" width="600" height="36" rx="8" fill="{term_bg}"/>
  <text x="52" y="63" fill="{term_text}" font-family="monospace" font-size="14">
    <tspan>user@dev:~$ cat README.md</tspan>
    <tspan fill="{accent}" opacity="1"><animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/>█</tspan>
  </text>

  <!-- Name -->
  <text x="40" y="130" font-family="Georgia,serif" font-size="52" font-weight="bold">{name_letters}</text>
  <text x="40" y="155" fill="{text_dim}" font-family="system-ui" font-size="14" opacity="0">
    <animate attributeName="opacity" from="0" to="1" begin="1.5s" dur="0.5s" fill="freeze"/>
    Hi, I'm 👋
  </text>

  <!-- Cycling roles -->
  {role_anims}

  <!-- Tagline box -->
  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" begin="1.6s" dur="0.5s" fill="freeze"/>
    <rect x="40" y="195" width="420" height="44" rx="8" fill="{card2}" stroke="{accent}" stroke-width="1"/>
    <text x="52" y="223" fill="{text}" font-family="system-ui" font-size="13" font-style="italic">"{xml_escape(PROFILE['tagline'])}"</text>
  </g>

  <!-- About -->
  <text x="40" y="400" fill="{accent}" font-family="system-ui" font-size="14" font-weight="bold" opacity="0">
    <animate attributeName="opacity" from="0" to="1" begin="1.7s" dur="0.4s" fill="freeze"/>
    About Me
  </text>
  {about_lines}

  <!-- Stats bar -->
  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" begin="2.2s" dur="0.5s" fill="freeze"/>
    <rect x="40" y="490" width="600" height="28" rx="6" fill="{card2}"/>
    <text x="52" y="509" fill="{text_dim}" font-family="monospace" font-size="11">⭐ {stats['stars']}  •  📝 {stats['commits']} commits  •  📦 {stats['repos']} repos  •  🔀 {stats['prs']} PRs</text>
  </g>

  <!-- Tech pills -->
  <text x="40" y="505" fill="{accent}" font-family="system-ui" font-size="13" font-weight="bold" opacity="0">
    <animate attributeName="opacity" from="0" to="1" begin="2.4s" dur="0.4s" fill="freeze"/>
  </text>
  {skills_pills}

  <!-- Code card -->
  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" begin="2.8s" dur="0.5s" fill="freeze"/>
    <rect x="40" y="600" width="300" height="100" rx="10" fill="#0d1a0d" stroke="{accent}" stroke-width="1"/>
    <rect x="40" y="600" width="300" height="22" rx="10" fill="{G['forest']}"/>
    <rect x="40" y="612" width="300" height="10" fill="{G['forest']}"/>
    <circle cx="54" cy="611" r="4" fill="#ff5f57"/><circle cx="68" cy="611" r="4" fill="#febc2e"/><circle cx="82" cy="611" r="4" fill="#28c840"/>
    <text x="100" y="615" fill="{G['mint']}" font-family="monospace" font-size="9">dreams.jsx</text>
    {code_svg}
  </g>

  <!-- Neon sign -->
  <g filter="url(#glow)" opacity="0">
    <animate attributeName="opacity" values="0;1;0.7;1;0.8;1" begin="4s" dur="0.3s" fill="freeze"/>
    <text x="360" y="680" fill="{glow}" font-family="monospace" font-size="13" font-weight="bold" text-anchor="middle">
      <animate attributeName="opacity" values="1;0.6;1;0.8;1" dur="2s" begin="4.3s" repeatCount="indefinite"/>
      KEEP CODING  •  KEEP GROWING
    </text>
  </g>

  <!-- Sparkles -->
  <circle cx="120" cy="80" r="2" fill="{G['light']}" opacity="0">
    <animate attributeName="opacity" values="0;1;0" dur="2s" begin="1s" repeatCount="indefinite"/>
  </circle>
  <circle cx="580" cy="200" r="1.5" fill="{G['mint']}" opacity="0">
    <animate attributeName="opacity" values="0;1;0" dur="1.5s" begin="2s" repeatCount="indefinite"/>
  </circle>
  <circle cx="300" cy="350" r="2" fill="{accent}" opacity="0">
    <animate attributeName="opacity" values="0;1;0" dur="2.5s" begin="0.5s" repeatCount="indefinite"/>
  </circle>

  <!-- Character panel -->
  <rect x="680" y="60" width="560" height="620" rx="16" fill="{card2}" stroke="{accent}" stroke-width="1"/>
  <g clip-path="url(#charReveal)">
    <image x="680" y="60" width="560" height="620" preserveAspectRatio="xMidYMid slice"
           href="data:image/jpeg;base64,{AVATAR_B64}" xlink:href="data:image/jpeg;base64,{AVATAR_B64}"/>
  </g>
  <g clip-path="url(#bannerClip)">
    <rect x="680" y="60" width="560" height="8" fill="url(#scanGrad)" opacity="0.8">
      <animate attributeName="y" from="60" to="672" dur="3.5s" repeatCount="indefinite"/>
    </rect>
  </g>
</svg>'''


def lanyard_svg():
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 320 480" width="320" height="480">
  <defs>
    <linearGradient id="strapGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{G['primary']}"/>
      <stop offset="100%" stop-color="{G['dark']}"/>
    </linearGradient>
    <linearGradient id="shine" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="white" stop-opacity="0"/>
      <stop offset="50%" stop-color="white" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="white" stop-opacity="0"/>
    </linearGradient>
    <clipPath id="avatarClip"><circle cx="160" cy="280" r="52"/></clipPath>
  </defs>

  <!-- Pendulum group -->
  <g transform="rotate(0 160 0)">
    <animateTransform attributeName="transform" type="rotate"
      values="0 160 0; 8 160 0; -6 160 0; 4 160 0; -2 160 0; 0 160 0"
      dur="4s" begin="0.8s" repeatCount="indefinite"/>
    <animateTransform attributeName="transform" type="translate"
      values="0 -400; 0 0" dur="0.8s" begin="0s" fill="freeze" additive="sum"
      calcMode="spline" keySplines="0.2 0.8 0.2 1"/>

    <!-- Strap -->
    <rect x="148" y="0" width="24" height="200" fill="url(#strapGrad)" rx="4"/>
    <text x="160" y="80" fill="white" font-family="monospace" font-size="8" text-anchor="middle" transform="rotate(90 160 80)">{PROFILE['username'].upper()}</text>

    <!-- Clasp -->
    <rect x="142" y="198" width="36" height="12" rx="3" fill="#888"/>
    <circle cx="160" cy="218" r="10" fill="#aaa" stroke="#666" stroke-width="2"/>

    <!-- Card -->
    <rect x="70" y="228" width="180" height="230" rx="14" fill="{G['bg_card']}" stroke="{G['primary']}" stroke-width="2"/>
    <rect x="70" y="228" width="180" height="230" rx="14" fill="url(#shine)" opacity="0">
      <animate attributeName="opacity" values="0;0.6;0" dur="2.5s" repeatCount="indefinite"/>
      <animateTransform attributeName="transform" type="translate" from="-180 0" to="180 0" dur="2.5s" repeatCount="indefinite"/>
    </rect>

    <!-- Avatar ring -->
    <circle cx="160" cy="280" r="56" fill="none" stroke="{G['primary']}" stroke-width="3" opacity="0.8">
      <animate attributeName="stroke-opacity" values="0.8;1;0.8" dur="2s" repeatCount="indefinite"/>
    </circle>
    <g clip-path="url(#avatarClip)">
      <image x="108" y="228" width="104" height="104" preserveAspectRatio="xMidYMid slice"
             href="data:image/jpeg;base64,{AVATAR_B64}" xlink:href="data:image/jpeg;base64,{AVATAR_B64}"/>
    </g>

    <text x="160" y="360" fill="{G['text']}" font-family="system-ui" font-size="16" font-weight="bold" text-anchor="middle">{PROFILE['name']}</text>
    <text x="160" y="380" fill="{G['light']}" font-family="system-ui" font-size="11" text-anchor="middle">{PROFILE['role']}</text>
    <text x="160" y="398" fill="{G['text_dim']}" font-family="monospace" font-size="10" text-anchor="middle">@{PROFILE['username']}</text>

    <!-- Barcode -->
    <g transform="translate(90, 410)">
      {"".join(f'<rect x="{i*4}" y="0" width="{2 if i%3 else 3}" height="28" fill="{G["mint"]}"/>' for i in range(22))}
    </g>
    <text x="160" y="455" fill="{G['text_dim']}" font-family="monospace" font-size="8" text-anchor="middle">DEV ID • 2026</text>
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
    <text x="24" y="{100 + i*36}" fill="{G['text_dim']}" font-family="system-ui" font-size="13">{label}</text>
    <text x="360" y="{100 + i*36}" fill="{G['light']}" font-family="monospace" font-size="14" font-weight="bold" text-anchor="end">{val}</text>
    <line x1="24" y1="{108 + i*36}" x2="360" y2="{108 + i*36}" stroke="{G['border']}" stroke-width="1"/>
  </g>'''

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 220" width="400" height="220">
  <rect width="400" height="220" rx="12" fill="{G['bg_card']}" stroke="{G['primary']}" stroke-width="1.5"/>
  <text x="24" y="36" fill="{G['text']}" font-family="system-ui" font-size="16" font-weight="bold">{PROFILE['name']}'s GitHub Stats</text>
  <circle cx="360" cy="36" r="22" fill="none" stroke="{G['primary']}" stroke-width="3" stroke-dasharray="100" stroke-dashoffset="100">
    <animate attributeName="stroke-dashoffset" from="100" to="25" dur="1.5s" fill="freeze"/>
  </circle>
  <text x="360" y="41" fill="{G['light']}" font-family="monospace" font-size="14" font-weight="bold" text-anchor="middle">{s['grade']}</text>
  {rows_svg}
</svg>'''


def langs_svg():
    bars = ""
    for i, (lang, pct) in enumerate(PROFILE["langs"]):
        y = 50 + i * 42
        bars += f'''
  <text x="20" y="{y}" fill="{G['text']}" font-family="system-ui" font-size="13">{lang}</text>
  <text x="380" y="{y}" fill="{G['light']}" font-family="monospace" font-size="12" text-anchor="end">{pct}%</text>
  <rect x="20" y="{y+6}" width="360" height="12" rx="6" fill="{G['bg_card2']}"/>
  <rect x="20" y="{y+6}" width="0" height="12" rx="6" fill="{G['primary']}">
    <animate attributeName="width" from="0" to="{pct*3.6}" dur="1.2s" begin="{0.2 + i*0.15}s" fill="freeze"/>
  </rect>'''

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 220" width="400" height="220">
  <rect width="400" height="220" rx="12" fill="{G['bg_card']}" stroke="{G['primary']}" stroke-width="1.5"/>
  <text x="20" y="32" fill="{G['text']}" font-family="system-ui" font-size="16" font-weight="bold">Top Languages</text>
  {bars}
</svg>'''


def trophies_svg():
    cells = ""
    colors = [G["primary"], G["light"], G["dark"], G["mint"], G["forest"], "#65a30d"]
    for i, (grade, label) in enumerate(PROFILE["trophies"]):
        col = i % 3
        row = i // 3
        x = 20 + col * 130
        y = 50 + row * 85
        cells += f'''
  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" begin="{0.2 + i*0.12}s" dur="0.35s" fill="freeze"/>
    <rect x="{x}" y="{y}" width="120" height="72" rx="10" fill="{G['bg_card2']}" stroke="{colors[i]}" stroke-width="1.5"/>
    <text x="{x+60}" y="{y+38}" fill="{colors[i]}" font-family="monospace" font-size="28" font-weight="bold" text-anchor="middle">{grade}</text>
    <text x="{x+60}" y="{y+58}" fill="{G['text_dim']}" font-family="system-ui" font-size="10" text-anchor="middle">{label}</text>
  </g>'''

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 220" width="400" height="220">
  <rect width="400" height="220" rx="12" fill="{G['bg_card']}" stroke="{G['primary']}" stroke-width="1.5"/>
  <text x="20" y="32" fill="{G['text']}" font-family="system-ui" font-size="16" font-weight="bold">GitHub Trophies</text>
  <rect x="0" y="0" width="400" height="220" fill="url(#shine)" opacity="0">
    <defs><linearGradient id="shine" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="white" stop-opacity="0"/><stop offset="50%" stop-color="white" stop-opacity="0.08"/><stop offset="100%" stop-color="white" stop-opacity="0"/></linearGradient></defs>
    <animate attributeName="opacity" values="0;1;0" dur="3s" repeatCount="indefinite"/>
    <animateTransform attributeName="transform" type="translate" from="-400 0" to="400 0" dur="3s" repeatCount="indefinite"/>
  </rect>
  {cells}
</svg>'''


def readme_md():
    v = PROFILE["cache_v"]
    u = PROFILE["username"]
    soc = PROFILE["social"]

    proj_rows = "\n".join(
        f"| [{name}](https://github.com/{u}/{name}) | {tech} | ⭐ {stars} |"
        for name, tech, stars in PROFILE["projects"]
    )

    return f'''<div align="center">

<!-- Banner (dark) — GitHub renders SVG reliably via img tag -->
<img alt="Animated profile banner" src="banner.svg?v={v}" width="100%"/>

<br/><br/>

<!-- ID Badge + Projects -->
<table>
<tr>
<td width="320" valign="top" align="center">
  <img alt="Swinging ID badge" src="lanyard.svg?v={v}" width="280"/>
</td>
<td valign="top">

### 🌿 My Projects

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
<td><img alt="GitHub Stats" src="stats.svg?v={v}" width="400"/></td>
<td><img alt="Top Languages" src="langs.svg?v={v}" width="400"/></td>
</tr>
</table>

<br/>

<!-- Trophies -->
<img alt="GitHub Trophies" src="trophies.svg?v={v}" width="820"/>

<br/><br/>

<!-- Activity Graph -->
<img alt="Contribution Graph" src="https://github-readme-activity-graph.vercel.app/graph?username={u}&bg_color=0a120a&color=22c55e&line=4ade80&point=86efac&area=true&hide_border=false&custom_title=Contribution%20Graph%20🌿" width="100%"/>

<br/><br/>

<!-- Snake -->
<img alt="Snake eating contributions" src="https://raw.githubusercontent.com/{u}/{u}/output/snake.svg" width="100%"/>

<p align="center"><i>🐍 Watch the snake eat my contributions!</i></p>

<br/>

<!-- Connect -->
### 🤝 Let's Connect

[![GitHub](https://img.shields.io/badge/GitHub-ayyappa3232-22c55e?style=for-the-badge&logo=github&logoColor=white)](https://github.com/{u})
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-16a34a?style=for-the-badge&logo=linkedin&logoColor=white)]({soc['linkedin']})
[![Portfolio](https://img.shields.io/badge/Portfolio-Visit-15803d?style=for-the-badge&logo=google-chrome&logoColor=white)]({soc['portfolio']})
[![Email](https://img.shields.io/badge/Email-Reach%20Out-4ade80?style=for-the-badge&logo=gmail&logoColor=white)]({soc['email']})

<br/>

<!-- Profile views -->
<img alt="Profile views" src="https://komarev.com/ghpvc/?username={u}&label=Profile%20Views&color=22c55e&style=for-the-badge"/>

<br/><br/>

**Always learning, always building. 🌿**

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
          snake_color: "22c55e"
          snake_color2: "4ade80"
          snake_color3: "15803d"

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
