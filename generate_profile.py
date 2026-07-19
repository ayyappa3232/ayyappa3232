#!/usr/bin/env python3
"""Generate animated GitHub profile assets — Cosmic 3D theme."""

import base64
import html
import json
import subprocess
import urllib.parse
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).parent
AVATAR_B64 = (ROOT / "avatar.b64.txt").read_text().strip()

# ── Profile data — Ayyappa Kumar Penneti ──
PROFILE = {
    "name": "Ayyappa Kumar",
    "full_name": "Ayyappa Kumar Penneti",
    "role": "Senior React JS Developer",
    "roles_cycle": [
        "Senior React JS Developer",
        "AI Native Engineer",
        "Agentic AI Learner",
        "LangGraph Explorer",
        "MCP Enthusiast",
        "System Design Learner",
    ],
    "username": "ayyappa3232",
    "email": "ayyappakumar.penneti@gmail.com",
    "location": "India",
    "experience": "7+ years",
    "tagline": "From React to Agentic AI — one project at a time.",
    "about": [
        "7+ years building React applications",
        "Exploring AI Native Engineering & Agentic AI",
        "Learning LangGraph, MCP and LLM Architecture",
        "Passionate about clean architecture & developer experience",
        "Interested in System Design, AI Agents and Full Stack AI",
        "Building AI Playgrounds — 131 labs across LangGraph, RAG & MCP",
        "Always open to learning and collaborating",
    ],
    "skills_banner": [
        "React", "TypeScript", "Node.js", "LangGraph",
        "MCP", "Next.js", "OpenAI", "AWS",
    ],
    "tech_stack": {
        "Frontend": ["React", "React Native", "TypeScript", "JavaScript", "Redux", "Next.js", "HTML5", "CSS3", "Tailwind"],
        "Backend": ["Node.js", "Express", "REST APIs", "SQL"],
        "AI": ["OpenAI", "LLMs", "LangChain", "LangGraph", "MCP", "Prompt Engineering", "Vector Databases", "RAG"],
        "Tools": ["Cursor", "GitHub", "GitHub Copilot", "VS Code", "Docker", "Postman", "Git"],
        "Cloud": ["AWS", "Azure"],
    },
    "currently_learning": [
        "Agentic AI", "LangGraph", "MCP", "React 19", "AI Engineering", "System Design",
    ],
    "current_focus": [
        "Building AI Agents",
        "Mastering LangGraph",
        "Learning MCP",
        "Building Full Stack AI Apps",
        "Preparing for Senior Frontend Interviews",
    ],
    "goals_2026": [
        "Become AI Native Engineer",
        "Build production AI applications",
        "Master React ecosystem",
        "Master System Design",
        "Contribute to Open Source",
        "Publish AI Learning Projects",
    ],
    "learning_journey": [
        ("React", 100),
        ("TypeScript", 90),
        ("Node.js", 80),
        ("LangGraph", 70),
        ("MCP", 60),
        ("AI Agents", 60),
    ],
    "interests": [
        "React", "AI", "Agentic AI", "LLMs", "LangGraph",
        "System Design", "Prompt Engineering", "Developer Productivity", "Open Source",
    ],
    "fun_fact": "I enjoy turning complex AI concepts into simple explanations. Currently obsessed with AI Agents 🤖",
    "footer": "BUILD • LEARN • SHIP • REPEAT 🚀",
    "code_card": {
        "filename": "engineer.ts",
        "lines": [
            "const engineer = {",
            "  frontend: 'React', backend: 'Node.js',",
            "  ai: 'LangGraph', learning: 'MCP',",
            "  goal: 'AI Native Engineer'",
            "};",
        ],
    },
    "stats": {"stars": "0", "commits": "25", "repos": "6", "prs": "0", "followers": "0", "grade": "C"},
    "highlights": {"ai_projects": "131 labs", "open_source": "1"},
    "langs": [("JavaScript", 80), ("CSS", 6), ("C#", 5), ("TypeScript", 5)],
    "trophies": [("B+", "Commits"), ("D", "Stars"), ("C", "Repos"), ("D", "PRs"), ("D", "Issues"), ("D", "Followers")],
    # (repo_slug, display_title, tech, stars, description optional)
    "projects": [
        (
            "twc_ai_playgrounds",
            "AI Playgrounds",
            "Python, TypeScript, Next.js, LangGraph",
            "0",
            "9 playgrounds · 131 labs — LangChain, LangGraph, RAG, MCP & multi-agent",
        ),
        ("twc_familysync", "FamilySync", "React Native, TypeScript, Firebase", "—", "Private · family coordination app"),
        ("twc_pro_recorder", "Pro Recorder", "React Native, TypeScript", "—", "Private · professional recording app"),
    ],
    "featured_repo": {
        "slug": "twc_ai_playgrounds",
        "demo_url": "https://twc-playgrounds.vercel.app/",
        "demo_image": "ai-playgrounds-demo.png",
        "headline": "Master the full AI stack",
        "stats": "9 playgrounds · 131 hands-on labs",
        "tracks": "Prompts · LangChain · LangGraph · RAG · MCP · Multi-Agent · LangSmith · Evals",
        "deploy": "Free in browser · no signup · `make dev` for live Python validation",
    },
    "auto_projects": False,
    "social": {
        "linkedin": "https://www.linkedin.com/in/ayyappa-kumar-penneti-2604b2155",
        "portfolio": None,
        "email": "mailto:ayyappakumar.penneti@gmail.com",
        "medium": None,
    },
    "cache_v": "24",
}

# github-profile-trophy thresholds (ryo-ma) — highest tier first
TROPHY_THRESHOLDS = {
    "Commits": [(4000, "S"), (1000, "S"), (500, "A"), (200, "A"), (100, "A"), (10, "B+"), (1, "C")],
    "Stars": [(2000, "S"), (200, "S"), (100, "A"), (50, "A"), (30, "A"), (10, "B+"), (1, "C")],
    "Repos": [(50, "S"), (40, "S"), (35, "A"), (30, "A"), (20, "A"), (10, "B+"), (1, "C")],
    "PRs": [(1000, "S"), (200, "S"), (100, "A"), (50, "A"), (20, "A"), (10, "B+"), (1, "C")],
    "Issues": [(1000, "S"), (200, "S"), (100, "A"), (50, "A"), (20, "A"), (10, "B+"), (1, "C")],
    "Followers": [(1000, "S"), (200, "S"), (100, "A"), (50, "A"), (20, "A"), (10, "B+"), (1, "C")],
}

TROPHY_STYLE = {
    "Commits": ("📝", "cyan", True),
    "Stars": ("⭐", "violet", True),
    "Repos": ("📦", "pink", False),
    "PRs": ("🔀", "gold", True),
    "Issues": ("🐛", "a5b4fc", False),
    "Followers": ("👥", "5eead4", False),
}

GRADE_POINTS = {"S": 5, "A": 4, "B+": 3, "B": 3, "C": 2, "D": 1}


def _curl_json(url: str) -> object:
    raw = subprocess.check_output(["curl", "-sf", url], text=True)
    return json.loads(raw)


def trophy_grade(metric: str, score: int) -> str:
    if score <= 0:
        return "D"
    for threshold, grade in TROPHY_THRESHOLDS[metric]:
        if score >= threshold:
            return grade
    return "D"


def overall_grade(grades: list[str]) -> str:
    if not grades:
        return "D"
    avg = sum(GRADE_POINTS.get(g, 1) for g in grades) / len(grades)
    if avg >= 4.5:
        return "S"
    if avg >= 3.5:
        return "A"
    if avg >= 2.5:
        return "B+"
    if avg >= 1.5:
        return "C"
    return "D"


def fetch_github_stats(username: str) -> dict:
    user = _curl_json(f"https://api.github.com/users/{username}")
    repos = []
    page = 1
    while True:
        batch = _curl_json(
            f"https://api.github.com/users/{username}/repos?per_page=100&page={page}&sort=updated"
        )
        if not batch:
            break
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1

    total_stars = sum(r.get("stargazers_count", 0) for r in repos)
    total_commits = 0
    lang_bytes: dict[str, int] = {}

    for repo in repos:
        name = repo["name"]
        try:
            contribs = _curl_json(
                f"https://api.github.com/repos/{username}/{name}/contributors?per_page=100"
            )
            if isinstance(contribs, list):
                for c in contribs:
                    if c.get("login", "").lower() == username.lower():
                        total_commits += c.get("contributions", 0)
                        break
        except subprocess.CalledProcessError:
            pass
        try:
            langs = _curl_json(
                f"https://api.github.com/repos/{username}/{name}/languages"
            )
            if isinstance(langs, dict):
                for lang, size in langs.items():
                    lang_bytes[lang] = lang_bytes.get(lang, 0) + size
        except subprocess.CalledProcessError:
            pass

    prs = _curl_json(
        "https://api.github.com/search/issues?"
        + urllib.parse.urlencode({"q": f"author:{username} type:pr", "per_page": 1})
    )["total_count"]
    issues = _curl_json(
        "https://api.github.com/search/issues?"
        + urllib.parse.urlencode({"q": f"author:{username} type:issue -type:pr", "per_page": 1})
    )["total_count"]

    total_lang = sum(lang_bytes.values()) or 1
    top_langs = [
        (lang, round(100 * size / total_lang))
        for lang, size in sorted(lang_bytes.items(), key=lambda x: -x[1])[:4]
    ]

    metrics = {
        "Commits": total_commits,
        "Stars": total_stars,
        "Repos": user.get("public_repos", len(repos)),
        "PRs": prs,
        "Issues": issues,
        "Followers": user.get("followers", 0),
    }
    grades = {label: trophy_grade(label, score) for label, score in metrics.items()}

    return {
        "stats": {
            "stars": str(total_stars),
            "commits": str(total_commits),
            "repos": str(metrics["Repos"]),
            "prs": str(prs),
            "followers": str(metrics["Followers"]),
            "grade": overall_grade(list(grades.values())),
        },
        "trophies": [(grades[label], label) for label in metrics],
        "langs": top_langs or PROFILE["langs"],
        "projects": [
            (r["name"], r["name"], ", ".join(list(r.get("topics") or [])[:3]) or "—", str(r.get("stargazers_count", 0)))
            for r in sorted(repos, key=lambda x: x.get("stargazers_count", 0), reverse=True)[:5]
        ],
    }


def refresh_featured_projects(username: str) -> None:
    refreshed = []
    public_count = 0
    for row in PROFILE["projects"]:
        repo, title, tech, stars = row[:4]
        desc = row[4] if len(row) > 4 else ""
        try:
            data = _curl_json(f"https://api.github.com/repos/{username}/{repo}")
            if isinstance(data, dict) and data.get("name"):
                public_count += 1
                stars = str(data.get("stargazers_count", 0))
                if data.get("description"):
                    desc = data["description"]
                elif len(row) > 4 and row[4]:
                    desc = row[4]
                langs = _curl_json(
                    f"https://api.github.com/repos/{username}/{repo}/languages"
                )
                if isinstance(langs, dict) and langs:
                    tech = ", ".join(
                        k for k, _ in sorted(langs.items(), key=lambda x: -x[1])[:4]
                    )
        except subprocess.CalledProcessError:
            pass
        entry = (repo, title, tech, stars, desc) if desc else (repo, title, tech, stars)
        refreshed.append(entry)
    PROFILE["projects"] = refreshed
    if public_count:
        PROFILE["highlights"]["open_source"] = str(public_count)


def apply_github_stats(username: Optional[str] = None) -> None:
    username = username or PROFILE["username"]
    try:
        live = fetch_github_stats(username)
    except (subprocess.CalledProcessError, json.JSONDecodeError, KeyError) as exc:
        print(f"Warning: could not fetch GitHub stats ({exc}); using PROFILE defaults")
        refresh_featured_projects(username)
        return
    PROFILE["stats"] = live["stats"]
    PROFILE["trophies"] = live["trophies"]
    PROFILE["langs"] = live["langs"]
    if PROFILE.get("auto_projects") and live["projects"]:
        PROFILE["projects"] = live["projects"]
    refresh_featured_projects(username)
    print(
        f"Live stats for @{username}: "
        f"{live['stats']['commits']} commits, {live['stats']['repos']} repos, "
        f"{live['stats']['stars']} stars"
    )


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
    role_dur = 3.5
    cycle_total = len(roles) * role_dur

    display_name = PROFILE["full_name"]
    name_parts = display_name.rsplit(" ", 1)
    name_line1 = name_parts[0] if len(name_parts) == 2 else display_name
    name_line2 = name_parts[1] if len(name_parts) == 2 else ""
    name_font = 36 if name_line2 else 42

    def _name_tspans(text: str, base_delay: float) -> str:
        out = ""
        for i, ch in enumerate(text):
            out += f'''
      <tspan opacity="0" fill="url(#nameGrad)">
        <animate attributeName="opacity" from="0" to="1" begin="{base_delay + i * 0.04}s" dur="0.35s" fill="freeze"/>
        <animate attributeName="dy" from="-12" to="0" begin="{base_delay + i * 0.04}s" dur="0.4s" fill="freeze"/>
        {xml_escape(ch)}
      </tspan>'''
        return out

    name_line1_svg = _name_tspans(name_line1, 0.6)
    name_line2_svg = _name_tspans(name_line2, 0.6 + len(name_line1) * 0.04 + 0.15) if name_line2 else ""

    # ── Roles — one visible at a time (no overlap) ──
    role_anims = ""
    n = len(roles)
    for i, role in enumerate(roles):
        t0 = i / n
        t_in = t0 + 0.015
        t_out = (i + 1) / n - 0.015
        t_end = (i + 1) / n
        role_anims += f'''
      <text x="52" y="210" fill="{cyan}" font-family="'SF Mono',monospace" font-size="13" opacity="0">
        <animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;{t0:.3f};{t_in:.3f};{t_out:.3f};{t_end:.3f};1" dur="{cycle_total}s" repeatCount="indefinite"/>
        &gt; {xml_escape(role)}<tspan fill="{violet}"><animate attributeName="opacity" values="1;0;1" dur="0.9s" repeatCount="indefinite"/>▌</tspan>
      </text>'''

    # ── About highlights in banner (3 lines, emoji — no bullets) ──
    about_banner = [
        ("🚀", PROFILE["about"][0]),
        ("🤖", PROFILE["about"][1]),
        ("🧠", PROFILE["about"][2]),
    ]
    about_lines = ""
    for i, (icon, line) in enumerate(about_banner):
        short = line if len(line) <= 46 else line[:43] + "..."
        about_lines += f'''
      <text x="44" y="{292 + i * 20}" fill="{text_dim}" font-family="system-ui,sans-serif" font-size="11" opacity="0">
        <animate attributeName="opacity" from="0" to="1" begin="{1.6 + i * 0.2}s" dur="0.4s" fill="freeze"/>
        <tspan fill="{cyan}">{icon}</tspan> {xml_escape(short)}
      </text>'''

    # ── Tech pills (2 rows, fixed grid) ──
    stats_y = 358
    tech_label_y = 408
    tech_pill_start = 420
    skills_pills = ""
    for i, sk in enumerate(PROFILE["skills_banner"][:8]):
        col = i % 4
        row = i // 4
        x = 44 + col * 148
        y = tech_pill_start + row * 34
        w = max(len(sk) * 8 + 22, 72)
        skills_pills += f'''
      <g opacity="0">
        <animate attributeName="opacity" from="0" to="1" begin="{2.2 + i * 0.1}s" dur="0.4s" fill="freeze"/>
        <rect x="{x}" y="{y}" width="{w}" height="24" rx="12" fill="url(#pillGrad)" stroke="{cyan}" stroke-width="0.8" opacity="0.9"/>
        <text x="{x + 11}" y="{y + 16}" fill="{text}" font-family="system-ui,sans-serif" font-size="11">{xml_escape(sk)}</text>
      </g>'''

    # ── Code card — full panel width ──
    code_y = 488
    code_w = 604
    code_h = 112
    line_count = len(PROFILE["code_card"]["lines"])
    footer_y = code_y + code_h + 18
    panel_h = footer_y + 28
    banner_h = panel_h + 44
    photo_y = 48
    photo_h = panel_h - 28
    code_card = PROFILE["code_card"]
    code_svg = ""
    for i, line in enumerate(code_card["lines"]):
        code_svg += f'''
    <text x="48" y="{code_y + 44 + i * 14}" fill="{code_text}" font-family="monospace" font-size="9.5" opacity="0">
      <animate attributeName="opacity" from="0" to="1" begin="{3.0 + i * 0.22}s" dur="0.3s" fill="freeze"/>
      {xml_escape(line)}
    </text>'''

    stats = PROFILE["stats"]

    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 1280 {banner_h}" width="1280" height="{banner_h}">
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
    <clipPath id="roleClip"><rect x="44" y="190" width="580" height="28"/></clipPath>
    <clipPath id="photoClip"><rect x="700" y="{photo_y + 24}" width="520" height="{photo_h - 24}" rx="14"/></clipPath>
    <clipPath id="photoReveal"><rect x="700" y="{photo_y + photo_h - 24}" width="520" height="0">
      <animate attributeName="y" from="{photo_y + photo_h - 24}" to="{photo_y + 24}" dur="1.6s" begin="0.4s" fill="freeze"/>
      <animate attributeName="height" from="0" to="{photo_h - 24}" dur="1.6s" begin="0.4s" fill="freeze"/>
    </rect></clipPath>
  </defs>

  <!-- Background -->
  <rect width="1280" height="{banner_h}" fill="url(#bgGrad)" rx="14"/>
  <circle cx="180" cy="120" r="120" fill="{violet}" opacity="0.07"/>
  <circle cx="1050" cy="620" r="140" fill="{cyan}" opacity="0.06"/>
  <circle cx="640" cy="370" r="200" fill="{pink}" opacity="0.03"/>

  <!-- ═══ LEFT PANEL (3D card) ═══ -->
  <g filter="url(#drop3d)">
    <rect x="22" y="22" width="636" height="{panel_h}" rx="18" fill="{panel_lo}" opacity="0.5"/>
    <rect x="20" y="20" width="636" height="{panel_h}" rx="18" fill="url(#panelGrad)" stroke="url(#frameGrad)" stroke-width="1.5"/>
    <rect x="24" y="22" width="628" height="4" rx="2" fill="white" opacity="0.07"/>
  </g>

  <!-- Terminal -->
  <rect x="36" y="36" width="604" height="34" rx="8" fill="{term_bg}" stroke="{cyan}" stroke-width="0.6" opacity="0.95"/>
  <circle cx="50" cy="53" r="5" fill="#ff5f57"/><circle cx="66" cy="53" r="5" fill="#febc2e"/><circle cx="82" cy="53" r="5" fill="#28c840"/>
  <text x="98" y="57" fill="{term_text}" font-family="monospace" font-size="13">
    user@dev:~$ cat README.md<tspan fill="{gold}"><animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/>█</tspan>
  </text>

  <!-- Greeting + Name (two lines) -->
  <text x="44" y="98" fill="{text_dim}" font-family="system-ui,sans-serif" font-size="14" opacity="0">
    <animate attributeName="opacity" from="0" to="1" begin="0.4s" dur="0.5s" fill="freeze"/>
    Hi, I'm 👋
  </text>
  <text x="44" y="132" font-family="Georgia,'Times New Roman',serif" font-size="{name_font}" font-weight="bold">{name_line1_svg}</text>
  <text x="44" y="164" font-family="Georgia,'Times New Roman',serif" font-size="{name_font}" font-weight="bold">{name_line2_svg}</text>

  <!-- Role (cycling, clipped) -->
  <rect x="36" y="182" width="604" height="34" rx="8" fill="{glass}" stroke="{violet}" stroke-width="0.6" opacity="0.85"/>
  <g clip-path="url(#roleClip)">{role_anims}</g>

  <!-- Tagline -->
  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" begin="1.2s" dur="0.5s" fill="freeze"/>
    <rect x="36" y="228" width="560" height="34" rx="8" fill="{glass2}" stroke="{pink}" stroke-width="0.6"/>
    <text x="50" y="250" fill="{text}" font-family="system-ui,sans-serif" font-size="12" font-style="italic">"{xml_escape(PROFILE['tagline'])}"</text>
  </g>

  <!-- About Me -->
  <text x="44" y="278" fill="{gold}" font-family="system-ui,sans-serif" font-size="12" font-weight="bold" opacity="0">
    <animate attributeName="opacity" from="0" to="1" begin="1.4s" dur="0.4s" fill="freeze"/>
    ✦ About Me
  </text>
  {about_lines}

  <!-- Stats bar -->
  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" begin="2.0s" dur="0.5s" fill="freeze"/>
    <rect x="36" y="{stats_y}" width="604" height="32" rx="8" fill="{glass}" stroke="{cyan}" stroke-width="0.5"/>
    <text x="50" y="{stats_y + 21}" fill="{text_dim}" font-family="monospace" font-size="10.5">
      💻 {stats.get('commits', '0')} commits   ·   📚 {stats.get('repos', '0')} repos   ·   ⭐ {stats.get('stars', '0')} stars   ·   👥 {stats.get('followers', '0')} followers
    </text>
  </g>

  <!-- Tech stack label + pills -->
  <text x="44" y="{tech_label_y}" fill="{violet}" font-family="system-ui,sans-serif" font-size="12" font-weight="bold" opacity="0">
    <animate attributeName="opacity" from="0" to="1" begin="2.1s" dur="0.4s" fill="freeze"/>
    ⚡ Tech Stack
  </text>
  {skills_pills}

  <!-- Code editor — full width -->
  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" begin="2.8s" dur="0.5s" fill="freeze"/>
    <rect x="36" y="{code_y}" width="{code_w}" height="{code_h}" rx="10" fill="{code_bg}" stroke="{cyan}" stroke-width="0.8"/>
    <rect x="36" y="{code_y}" width="{code_w}" height="22" rx="10" fill="{panel_hi}"/>
    <rect x="36" y="{code_y + 14}" width="{code_w}" height="8" fill="{panel_hi}"/>
    <circle cx="50" cy="{code_y + 11}" r="4" fill="#ff5f57"/><circle cx="64" cy="{code_y + 11}" r="4" fill="#febc2e"/><circle cx="78" cy="{code_y + 11}" r="4" fill="#28c840"/>
    <text x="92" y="{code_y + 15}" fill="{text_dim}" font-family="monospace" font-size="9">{xml_escape(code_card['filename'])}</text>
    {code_svg}
  </g>

  <!-- Neon sign -->
  <g filter="url(#glow3d)" opacity="0">
    <animate attributeName="opacity" from="0" to="1" begin="3.8s" dur="0.4s" fill="freeze"/>
    <text x="338" y="{footer_y}" fill="{cyan}" font-family="monospace" font-size="11" font-weight="bold" text-anchor="middle">
      <animate attributeName="opacity" values="1;0.55;1;0.75;1" dur="2.5s" repeatCount="indefinite"/>
      {xml_escape(PROFILE['footer'])}
    </text>
  </g>

  <!-- ═══ RIGHT PANEL — 3D photo frame ═══ -->
  <g filter="url(#drop3d)">
    <rect x="692" y="{photo_y + 4}" width="556" height="{photo_h}" rx="18" fill="{panel_lo}" opacity="0.4"/>
    <rect x="688" y="{photo_y}" width="556" height="{photo_h}" rx="18" fill="url(#panelGrad)" stroke="url(#frameGrad)" stroke-width="2"/>
    <rect x="692" y="{photo_y + 2}" width="548" height="5" rx="2" fill="white" opacity="0.08"/>
  </g>

  <!-- Photo with reveal -->
  <g clip-path="url(#photoReveal)">
    <g clip-path="url(#photoClip)">
      <image x="700" y="{photo_y + 24}" width="520" height="{photo_h - 24}" preserveAspectRatio="xMidYMid slice"
             href="data:image/png;base64,{AVATAR_B64}" xlink:href="data:image/png;base64,{AVATAR_B64}"/>
      <rect x="700" y="{photo_y + 24}" width="520" height="{photo_h - 24}" fill="url(#panelGrad)" opacity="0.15"/>
    </g>
  </g>

  <!-- Soft scanner (subtle) -->
  <g clip-path="url(#photoClip)">
    <rect x="700" y="{photo_y + 24}" width="520" height="6" fill="url(#scanGrad)" opacity="0.5">
      <animate attributeName="y" from="{photo_y + 24}" to="{photo_y + photo_h - 30}" dur="4.5s" repeatCount="indefinite"/>
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
    card_x, card_y, card_w, card_h = 70, 242, 180, 238
    avatar_cy = 302
    avatar_r = 48
    img_w = 100
    img_h = 130
    img_x = 160 - img_w // 2
    img_y = avatar_cy - 52  # anchor crop to face (top of full-body art)

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
      <stop offset="50%" stop-color="white" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="white" stop-opacity="0"/>
    </linearGradient>
    <filter id="card3d"><feDropShadow dx="0" dy="6" stdDeviation="8" flood-opacity="0.5"/></filter>
    <clipPath id="avatarClip"><circle cx="160" cy="{avatar_cy}" r="{avatar_r}"/></clipPath>
    <clipPath id="cardClip"><rect x="{card_x}" y="{card_y}" width="{card_w}" height="{card_h}" rx="14"/></clipPath>
  </defs>

  <g transform="rotate(0 160 0)">
    <animateTransform attributeName="transform" type="rotate"
      values="0 160 0; 8 160 0; -6 160 0; 4 160 0; -2 160 0; 0 160 0"
      dur="4s" begin="0.8s" repeatCount="indefinite"/>
    <animateTransform attributeName="transform" type="translate"
      values="0 -400; 0 0" dur="0.8s" begin="0s" fill="freeze" additive="sum"
      calcMode="spline" keySplines="0.2 0.8 0.2 1"/>

    <!-- Lanyard strap + hardware (drawn before card) -->
    <rect x="148" y="0" width="24" height="200" fill="url(#strapGrad)" rx="4"/>
    <text x="160" y="80" fill="white" font-family="monospace" font-size="8" text-anchor="middle" transform="rotate(90 160 80)">{PROFILE['username'].upper()}</text>
    <rect x="142" y="198" width="36" height="12" rx="3" fill="#888"/>
    <circle cx="160" cy="218" r="10" fill="#bbb" stroke="#666" stroke-width="2"/>

    <!-- ID card body -->
    <g filter="url(#card3d)">
      <rect x="{card_x}" y="{card_y}" width="{card_w}" height="{card_h}" rx="14" fill="url(#cardGrad)" stroke="{C['cyan']}" stroke-width="2"/>
    </g>

    <!-- Avatar -->
    <circle cx="160" cy="{avatar_cy}" r="{avatar_r + 4}" fill="none" stroke="{C['cyan']}" stroke-width="2.5" opacity="0.9">
      <animate attributeName="stroke-opacity" values="0.7;1;0.7" dur="2s" repeatCount="indefinite"/>
    </circle>
    <g clip-path="url(#avatarClip)">
      <image x="{img_x}" y="{img_y}" width="{img_w}" height="{img_h}" preserveAspectRatio="xMidYMin slice"
             href="data:image/png;base64,{AVATAR_B64}" xlink:href="data:image/png;base64,{AVATAR_B64}"/>
    </g>

    <!-- Text + barcode -->
    <text x="160" y="378" fill="{C['text']}" font-family="system-ui" font-size="14" font-weight="bold" text-anchor="middle">{PROFILE['name']}</text>
    <text x="160" y="394" fill="{C['cyan']}" font-family="system-ui" font-size="10" text-anchor="middle">{PROFILE['role']}</text>
    <text x="160" y="408" fill="{C['violet']}" font-family="system-ui" font-size="9" text-anchor="middle">AI Native Engineer</text>
    <text x="160" y="422" fill="{C['text_dim']}" font-family="monospace" font-size="10" text-anchor="middle">@{PROFILE['username']}</text>
    <g transform="translate(90, 434)">
      {"".join(f'<rect x="{i*4}" y="0" width="{2 if i%3 else 3}" height="24" fill="{C["violet"]}"/>' for i in range(22))}
    </g>
    <text x="160" y="468" fill="{C['text_dim']}" font-family="monospace" font-size="8" text-anchor="middle">DEV ID • 2026</text>

    <!-- Holographic shine — clipped to card only -->
    <g clip-path="url(#cardClip)">
      <rect x="{card_x}" y="{card_y}" width="{card_w}" height="{card_h}" fill="url(#shine)" opacity="0">
        <animate attributeName="opacity" values="0;0.45;0" dur="2.5s" repeatCount="indefinite"/>
        <animateTransform attributeName="transform" type="translate" from="-{card_w} 0" to="{card_w} 0" dur="2.5s" repeatCount="indefinite"/>
      </rect>
    </g>

    <!-- Hardware on top of card border -->
    <rect x="142" y="198" width="36" height="12" rx="3" fill="#888"/>
    <circle cx="160" cy="218" r="10" fill="#bbb" stroke="#666" stroke-width="2"/>
  </g>
</svg>'''


def stats_svg():
    s = PROFILE["stats"]
    h = PROFILE["highlights"]
    rows = [
        ("💻 Contributions", s.get("commits", "0")),
        ("📚 Repositories", s.get("repos", "0")),
        ("⭐ Total Stars", s.get("stars", "0")),
        ("🔀 Pull Requests", s.get("prs", "0")),
        ("👥 Followers", s.get("followers", "0")),
        ("🏆 AI Projects", h.get("ai_projects", "—")),
    ]
    rows_svg = ""
    for i, (label, val) in enumerate(rows):
        rows_svg += f'''
  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" begin="{0.3 + i*0.15}s" dur="0.4s" fill="freeze"/>
    <animateTransform attributeName="transform" type="translate" from="-30 0" to="0 0" begin="{0.3 + i*0.15}s" dur="0.4s" fill="freeze"/>
    <text x="24" y="{88 + i*30}" fill="{C['text_dim']}" font-family="system-ui" font-size="12">{label}</text>
    <text x="360" y="{88 + i*30}" fill="{C['cyan']}" font-family="monospace" font-size="13" font-weight="bold" text-anchor="end">{val}</text>
    <line x1="24" y1="{96 + i*30}" x2="360" y2="{96 + i*30}" stroke="{C['border']}" stroke-width="1" opacity="0.35"/>
  </g>'''

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 280" width="400" height="280">
  <defs>
    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{C['panel_hi']}"/>
      <stop offset="100%" stop-color="{C['panel_lo']}"/>
    </linearGradient>
    <filter id="s3d"><feDropShadow dx="0" dy="4" stdDeviation="6" flood-opacity="0.4"/></filter>
  </defs>
  <rect width="400" height="280" rx="12" fill="url(#cardGrad)" stroke="{C['cyan']}" stroke-width="1.5" filter="url(#s3d)"/>
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


def learning_journey_svg():
    bars = ""
    items = PROFILE["learning_journey"]
    for i, (skill, pct) in enumerate(items):
        y = 50 + i * 38
        filled = int(pct * 3.2)
        bars += f'''
  <text x="20" y="{y}" fill="{C['text']}" font-family="system-ui" font-size="13">{skill}</text>
  <text x="380" y="{y}" fill="{C['pink']}" font-family="monospace" font-size="11" text-anchor="end">{pct}%</text>
  <rect x="20" y="{y+6}" width="320" height="10" rx="5" fill="{C['glass']}"/>
  <rect x="20" y="{y+6}" width="0" height="10" rx="5" fill="url(#journeyGrad)">
    <animate attributeName="width" from="0" to="{filled}" dur="1.4s" begin="{0.15 + i*0.12}s" fill="freeze"/>
  </rect>'''

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 280" width="400" height="280">
  <defs>
    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{C['panel_hi']}"/>
      <stop offset="100%" stop-color="{C['panel_lo']}"/>
    </linearGradient>
    <linearGradient id="journeyGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{C['cyan']}"/>
      <stop offset="50%" stop-color="{C['violet']}"/>
      <stop offset="100%" stop-color="{C['pink']}"/>
    </linearGradient>
  </defs>
  <rect width="400" height="280" rx="12" fill="url(#cardGrad)" stroke="{C['pink']}" stroke-width="1.5"/>
  <text x="20" y="32" fill="{C['text']}" font-family="system-ui" font-size="16" font-weight="bold">📊 Learning Journey</text>
  {bars}
</svg>'''


def trophies_svg():
    w, h = 820, 240
    cell_w, cell_h, gap = 248, 82, 14
    ox, row1, row2 = 24, 52, 146

    trophy_meta = []
    for grade, label in PROFILE["trophies"]:
        icon, color_key, glow_default = TROPHY_STYLE[label]
        color = C[color_key] if color_key in C else f"#{color_key}"
        glow = glow_default and grade in ("S", "A")
        trophy_meta.append((grade, label, icon, color, glow))

    cells = ""
    for i, (grade, label, icon, color, glow) in enumerate(trophy_meta):
        col = i % 3
        row = i // 3
        x = ox + col * (cell_w + gap)
        y = row1 if row == 0 else row2
        cid = f"cell{i}"

        ring = ""
        if grade == "S":
            ring = f'''
    <circle cx="{x + cell_w // 2}" cy="{y + 38}" r="34" fill="none" stroke="{color}" stroke-width="2" opacity="0.5">
      <animate attributeName="stroke-opacity" values="0.4;0.9;0.4" dur="2s" repeatCount="indefinite"/>
      <animate attributeName="r" values="32;36;32" dur="2s" repeatCount="indefinite"/>
    </circle>'''

        glow_filter = ' filter="url(#gradeGlow)"' if glow else ""
        grade_color = C["text_dim"] if grade == "D" else color

        cells += f'''
  <clipPath id="{cid}"><rect x="{x}" y="{y}" width="{cell_w}" height="{cell_h}" rx="12"/></clipPath>
  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" begin="{0.15 + i * 0.1}s" dur="0.4s" fill="freeze"/>
    <animateTransform attributeName="transform" type="translate" from="0 12" to="0 0" begin="{0.15 + i * 0.1}s" dur="0.4s" fill="freeze"/>
    <rect x="{x}" y="{y}" width="{cell_w}" height="{cell_h}" rx="12" fill="{C['glass']}" stroke="{color}" stroke-width="1.5"/>
    {ring}
    <text x="{x + cell_w // 2}" y="{y + 22}" font-size="14" text-anchor="middle">{icon}</text>
    <text x="{x + cell_w // 2}" y="{y + 50}" fill="{grade_color}" font-family="monospace" font-size="26" font-weight="bold" text-anchor="middle"{glow_filter}>{grade}</text>
    <text x="{x + cell_w // 2}" y="{y + 68}" fill="{C['text_dim']}" font-family="system-ui" font-size="11" text-anchor="middle">{label}</text>
    <g clip-path="url(#{cid})">
      <rect x="{x}" y="{y}" width="{cell_w}" height="{cell_h}" fill="url(#cellShine)" opacity="0">
        <animate attributeName="opacity" values="0;0.5;0" dur="2.8s" begin="{i * 0.4}s" repeatCount="indefinite"/>
        <animateTransform attributeName="transform" type="translate" from="-{cell_w} 0" to="{cell_w} 0" dur="2.8s" begin="{i * 0.4}s" repeatCount="indefinite"/>
      </rect>
    </g>
  </g>'''

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <defs>
    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{C['panel_hi']}"/>
      <stop offset="100%" stop-color="{C['panel_lo']}"/>
    </linearGradient>
    <linearGradient id="frameGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{C['pink']}"/>
      <stop offset="50%" stop-color="{C['violet']}"/>
      <stop offset="100%" stop-color="{C['cyan']}"/>
    </linearGradient>
    <linearGradient id="cellShine" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="white" stop-opacity="0"/>
      <stop offset="50%" stop-color="white" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="white" stop-opacity="0"/>
    </linearGradient>
    <filter id="gradeGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="2" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="cardShadow" x="-5%" y="-5%" width="110%" height="115%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-opacity="0.35"/>
    </filter>
  </defs>
  <rect width="{w}" height="{h}" rx="14" fill="url(#cardGrad)" stroke="url(#frameGrad)" stroke-width="1.5" filter="url(#cardShadow)"/>
  <text x="28" y="36" fill="{C['text']}" font-family="system-ui" font-size="17" font-weight="bold">🏆 GitHub Trophies</text>
  <text x="{w - 28}" y="36" fill="{C['text_dim']}" font-family="monospace" font-size="10" text-anchor="end">rank snapshot</text>
  {cells}
</svg>'''


def get_git_sha() -> str:
    """Return current git commit SHA (used to pin CDN URLs and bust cache)."""
    import subprocess
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, stderr=subprocess.DEVNULL
        ).strip()
    except Exception:
        return PROFILE["cache_v"]


def _readme_html_list(items: list[str]) -> str:
    rows = "\n".join(f"  <li>{html.escape(item)}</li>" for item in items)
    return f"<ul align=\"left\">\n{rows}\n</ul>"


def _readme_chip_list(items: list[str]) -> str:
    return " ".join(
        f"![{item}](https://img.shields.io/badge/{urllib.parse.quote(item.replace(' ', '_'))}-1c1c4a?style=for-the-badge&color=00e5ff)"
        for item in items
    )


def _readme_tech_stack() -> str:
    blocks = []
    icons = {"Frontend": "🎨", "Backend": "⚙️", "AI": "🤖", "Tools": "🛠", "Cloud": "☁️"}
    for category, items in PROFILE["tech_stack"].items():
        pills = " ".join(
            f"![{item}](https://img.shields.io/badge/"
            f"{urllib.parse.quote(item.replace(' ', '_'))}-12103a?style=flat-square&color=00e5ff)"
            for item in items
        )
        blocks.append(f"**{icons.get(category, '•')} {category}**  \n{pills}")
    return "\n\n".join(blocks)


def _readme_list(items: list[str], prefix: str) -> str:
    return "\n".join(f"{prefix} {item}" for item in items)


def _project_row(username: str, row: tuple) -> str:
    repo, title, tech, stars = row[:4]
    desc = row[4] if len(row) > 4 else ""
    label = f"{title} 🌐" if repo == "twc_ai_playgrounds" else title
    if desc:
        return (
            f"| [{label}](https://github.com/{username}/{repo}) "
            f"| {desc} | {tech} | ⭐ {stars} |"
        )
    return f"| [{label}](https://github.com/{username}/{repo}) | {tech} | ⭐ {stars} |"


def _readme_featured_repo(username: str, cdn: str) -> str:
    feat = PROFILE.get("featured_repo")
    if not feat:
        return ""
    slug = feat["slug"]
    repo_url = f"https://github.com/{username}/{slug}"
    demo_url = feat.get("demo_url", "")
    demo_img = feat.get("demo_image")
    demo_block = ""
    if demo_url and demo_img:
        demo_block = f'''
<a href="{demo_url}">
  <img alt="AI Playgrounds live demo — LangGraph learning hub" src="{cdn}/{demo_img}" width="1024"/>
</a>

<br/>

[![Live Demo](https://img.shields.io/badge/Live_Demo-tw--playgrounds.vercel.app-ec4899?style=for-the-badge&logo=vercel&logoColor=white)]({demo_url})
[![Source Code](https://img.shields.io/badge/Source_Code-GitHub-00e5ff?style=for-the-badge&logo=github&logoColor=white)]({repo_url})

<br/><br/>
'''
    elif demo_url:
        demo_block = f'''
[![Live Demo](https://img.shields.io/badge/Live_Demo-tw--playgrounds.vercel.app-ec4899?style=for-the-badge&logo=vercel&logoColor=white)]({demo_url})

<br/><br/>
'''
    return f'''
<br/>

### 🚀 Featured Open Source

<a href="{repo_url}">
  <img src="https://img.shields.io/badge/AI_Playgrounds-9_playgrounds_·_131_labs-00e5ff?style=for-the-badge&logo=github&logoColor=white" alt="AI Playgrounds"/>
</a>

<br/><br/>

{demo_block}

<table>
<tr>
<td align="left" valign="top">

**{feat["headline"]}** — {feat["stats"]}

{feat["tracks"]}

<br/>

🌐 {feat["deploy"]}

<br/><br/>

👉 **[Try the live demo]({demo_url})** · **[Explore the repo]({repo_url})**

</td>
</tr>
</table>
'''


def _readme_connect_badges(soc: dict, username: str) -> str:
    badges = [
        f"[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-a855f7?style=for-the-badge&logo=linkedin&logoColor=white)]({soc['linkedin']})",
        f"[![GitHub](https://img.shields.io/badge/GitHub-{username}-00e5ff?style=for-the-badge&logo=github&logoColor=white)](https://github.com/{username})",
        f"[![Email](https://img.shields.io/badge/Email-Reach%20Out-6366f1?style=for-the-badge&logo=gmail&logoColor=white)]({soc['email']})",
    ]
    if soc.get("portfolio"):
        badges.insert(
            0,
            f"[![Portfolio](https://img.shields.io/badge/Portfolio-Visit-ec4899?style=for-the-badge&logo=google-chrome&logoColor=white)]({soc['portfolio']})",
        )
    else:
        badges.append(
            "![Portfolio](https://img.shields.io/badge/Portfolio-Coming%20Soon-475569?style=for-the-badge&logo=google-chrome&logoColor=white)"
        )
    if soc.get("medium"):
        badges.append(
            f"[![Medium](https://img.shields.io/badge/Medium-Blog-fbbf24?style=for-the-badge&logo=medium&logoColor=white)]({soc['medium']})"
        )
    return "\n".join(badges)


def readme_md(sha: Optional[str] = None):
    v = PROFILE["cache_v"]
    u = PROFILE["username"]
    soc = PROFILE["social"]
    pin = sha or get_git_sha()
    # Pin to exact commit — new SHA = entirely new URL (beats GitHub profile cache)
    cdn = f"https://cdn.jsdelivr.net/gh/{u}/{u}@{pin}"
    snake = f"https://cdn.jsdelivr.net/gh/{u}/{u}@output/snake.gif?v={v}"
    streak = (
        f"https://streak-stats.demolab.com/?user={u}"
        f"&theme=dark&background=070B1A&border=6366F1&stroke=00E5FF"
        f"&ring=00E5FF&fire=A855F7&currStreakNum=00E5FF&sideNums=00E5FF"
        f"&currStreakLabel=EC4899&sideLabels=E2E8F0&dates=94A3B8"
    )

    proj_rows = "\n".join(
        _project_row(u, row) for row in PROFILE["projects"]
    )

    about_md = _readme_html_list(PROFILE["about"])
    learning_md = _readme_chip_list(PROFILE["currently_learning"])
    focus_md = _readme_html_list([f"✓ {x}" for x in PROFILE["current_focus"]])
    goals_md = _readme_html_list([f"□ {x}" for x in PROFILE["goals_2026"]])
    interests_md = " · ".join(f"`{i}`" for i in PROFILE["interests"])
    tech_md = _readme_tech_stack()
    st = PROFILE["stats"]
    hl = PROFILE["highlights"]
    connect_md = _readme_connect_badges(soc, u)
    featured_md = _readme_featured_repo(u, cdn)

    return f'''<div align="center">

<!-- Pinned to commit {pin[:12]} — changes every push, bypasses GitHub profile cache -->
<img alt="Animated profile banner" src="{cdn}/banner.svg" width="100%"/>

<br/><br/>

<!-- ID Badge + About -->
<table>
<tr>
<td width="320" valign="top" align="center">
  <img alt="Swinging ID badge" src="{cdn}/lanyard.svg" width="280"/>
</td>
<td valign="top" align="left">

### 👋 About Me

{about_md}

<br/>

### ✨ My Projects

| Project | About | Tech | Stars |
|:--------|:--------|:------|-----:|
{proj_rows}

*"Building AI that works, not just demos. 🚀"*

</td>
</tr>
</table>
{featured_md}

<br/>

<!-- Tech Stack -->
### 🛠 Tech Stack

{tech_md}

<br/>

<!-- Learning + Focus -->
<table>
<tr>
<td width="50%" valign="top" align="left">

### 📚 Currently Learning

{learning_md}

</td>
<td width="50%" valign="top" align="left">

### 🚀 Current Focus

{focus_md}

</td>
</tr>
</table>

<br/>

### 🎯 Goals 2026

{goals_md}

<br/>

<!-- Stats + Journey -->
<table>
<tr>
<td><img alt="GitHub Stats" src="{cdn}/stats.svg" width="400"/></td>
<td><img alt="Learning Journey" src="{cdn}/learning.svg" width="400"/></td>
</tr>
<tr>
<td><img alt="Top Languages" src="{cdn}/langs.svg" width="400"/></td>
<td align="center" valign="middle">

**📈 Highlights**

🏆 AI Projects · **{hl.get('ai_projects', '—')}**  
📦 Open Source · **{hl.get('open_source', '—')} public**  
🔥 Streak · see below  
💻 Contributions · **{st.get('commits', '0')}**  
📚 Repos · **{st.get('repos', '0')}**  
👥 Followers · **{st.get('followers', '0')}**

</td>
</tr>
</table>

<br/>

<!-- Trophies -->
<img alt="GitHub Trophies" src="{cdn}/trophies.svg" width="820"/>

<br/><br/>

<!-- Activity Graph -->
<img alt="Contribution Graph" src="https://github-readme-activity-graph.vercel.app/graph?username={u}&bg_color=070b1a&color=00e5ff&line=a855f7&point=ec4899&area=true&hide_border=false&custom_title=Contribution%20Graph%20✨" width="100%"/>

<br/><br/>

<!-- Streak + Snake -->
<img alt="GitHub streak stats" src="{streak}" width="100%"/>

<br/><br/>

<div align="center">

### 🐍 Contribution Snake

<table>
<tr>
<td align="center" bgcolor="#12103a">

<img alt="Snake eating my GitHub contributions" src="{snake}" width="820"/>

</td>
</tr>
</table>

<sub>✨ Classic green grid · cyan snake · updates daily</sub>

</div>

<br/>

<!-- Interests + Fun Fact -->
<table>
<tr>
<td width="50%" valign="top" align="left">

### 🏅 Interests

{interests_md}

</td>
<td width="50%" valign="top" align="left">

### 🧠 Fun Fact

{PROFILE['fun_fact']}

</td>
</tr>
</table>

<br/>

<!-- Connect -->
### 🌐 Let's Connect

{connect_md}

<br/>

<!-- Profile views -->
<img alt="Profile views" src="https://komarev.com/ghpvc/?username={u}&label=Profile%20Views&color=00e5ff&style=for-the-badge"/>

<br/><br/>

**{PROFILE['footer']}**

</div>
'''


def snake_yml():
    u = PROFILE["username"]
    return f'''name: Generate Snake

on:
  schedule:
    - cron: "0 0 * * *"
  workflow_dispatch:
  push:
    branches: [main]
    paths:
      - .github/workflows/github-snake.yml

jobs:
  generate:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    permissions:
      contents: write
    steps:
      - name: Generate snake.gif
        uses: Platane/snk@v3
        with:
          github_user_name: {u}
          outputs: |
            dist/snake.gif?color_snake=00e5ff&color_dots=#3d4460,#0e4429,#006d32,#26a641,#39d353&color_background=12103a

      - name: Push snake.gif to output branch
        uses: crazy-max/ghaction-github-pages@v4
        with:
          target_branch: output
          build_dir: dist
        env:
          GITHUB_TOKEN: ${{{{ secrets.GITHUB_TOKEN }}}}
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
    apply_github_stats()
    (ROOT / "banner.svg").write_text(banner_svg(light=False))
    (ROOT / "banner-light.svg").write_text(banner_svg(light=True))
    (ROOT / "lanyard.svg").write_text(lanyard_svg())
    (ROOT / "stats.svg").write_text(stats_svg())
    (ROOT / "langs.svg").write_text(langs_svg())
    (ROOT / "learning.svg").write_text(learning_journey_svg())
    (ROOT / "trophies.svg").write_text(trophies_svg())
    (ROOT / "README.md").write_text(readme_md())
    (ROOT / ".github/workflows/github-snake.yml").write_text(snake_yml())
    (ROOT / "CUSTOMIZATION.md").write_text(customization_md())
    print("Generated all profile assets in", ROOT)


if __name__ == "__main__":
    main()
