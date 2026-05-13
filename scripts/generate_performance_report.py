#!/usr/bin/env python3
"""
Gera docs/performance/metrics.json e docs/performance/index.html
com métricas de produtividade por aluno extraídas do git log e da API do GitHub.

Uso:
    GITHUB_TOKEN=<token> python scripts/generate_performance_report.py \
        --repo owner/repo [--students .github/performance-students.json]
"""

import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from string import Template


DATE_ONLY_LENGTH = 10


# ---------------------------------------------------------------------------
# Helpers de configuração, datas e associação
# ---------------------------------------------------------------------------

def load_students(config_path: str) -> list:
    path = Path(config_path)
    if not path.exists():
        print(f"Erro: arquivo de configuração não encontrado: {config_path}", file=sys.stderr)
        sys.exit(1)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def init_students(raw_students: list) -> list:
    students = []
    for student in raw_students:
        students.append({
            "name": student["name"],
            "github": student["github"],
            "emails": student.get("emails", []),
            "commits_count": 0,
            "issues_count": 0,
            "pull_requests_count": 0,
            "pull_requests_merged_count": 0,
            "reviews_count": 0,
            "open_issues_count": 0,
            "open_pull_requests_count": 0,
            "issue_characters_total": 0,
            "issue_characters_average": 0,
            "recent_activity_count": 0,
            "commit_timeline": {},
            "issue_timeline": {},
            "pull_request_timeline": {},
            "review_timeline": {},
        })
    return students


def build_email_index(students: list) -> dict:
    index = {}
    for i, student in enumerate(students):
        for email in student.get("emails", []):
            index[email.lower()] = i
    return index


def build_login_index(students: list) -> dict:
    return {student["github"].lower(): i for i, student in enumerate(students)}


def parse_datetime(value: str) -> datetime | None:
    if not value:
        return None
    try:
        normalized = value.replace("Z", "+00:00")
        return datetime.fromisoformat(normalized)
    except ValueError:
        return None


def month_key(value: str) -> str:
    return value[:7] if value else "unknown"


def week_key(value: str) -> str:
    dt = parse_datetime(value)
    if dt is None:
        return "unknown"
    year, week, _ = dt.isocalendar()
    return f"{year}-W{week:02d}"


def increment(target: dict, key: str, amount: int = 1) -> None:
    target[key] = target.get(key, 0) + amount


def student_ref(students: list, idx: int | None) -> dict | None:
    if idx is None:
        return None
    return students[idx]


def student_key(student: dict | None) -> str:
    return student["github"] if student else "unassigned"


def student_name(student: dict | None) -> str:
    return student["name"] if student else "Não atribuído"


def is_recent(value: str, generated_at: datetime, days: int = 14) -> bool:
    dt = parse_datetime(value)
    if dt is None:
        return False
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt >= generated_at - timedelta(days=days)


def event_date(event: dict) -> str:
    return (
        event.get("date")
        or event.get("created_at")
        or event.get("submitted_at")
        or event.get("merged_at")
        or event.get("closed_at")
        or ""
    )


# ---------------------------------------------------------------------------
# API GitHub
# ---------------------------------------------------------------------------

def github_request(url: str, token: str) -> list:
    """Executa GET paginado e retorna todos os itens."""
    if not token:
        return []

    items = []
    page = 1
    separator = "&" if "?" in url else "?"
    while True:
        paged_url = f"{url}{separator}page={page}&per_page=100"
        req = urllib.request.Request(
            paged_url,
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "squad08-performance-report",
            },
        )
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode())
        except urllib.error.HTTPError as exc:
            print(f"Erro na API do GitHub ({exc.code}): {paged_url}", file=sys.stderr)
            break
        except urllib.error.URLError as exc:
            print(f"Erro de rede: {exc}", file=sys.stderr)
            break

        if not data:
            break
        items.extend(data)
        if len(data) < 100:
            break
        page += 1

    return items


# ---------------------------------------------------------------------------
# Coleta de commits, issues, PRs e reviews
# ---------------------------------------------------------------------------

def collect_commits(repo: str, email_index: dict, students: list, unassigned: dict) -> list:
    sep = "||GIT_SEP||"
    fmt = f"%H{sep}%an{sep}%ae{sep}%aI{sep}%s"
    try:
        result = subprocess.run(
            ["git", "log", f"--format={fmt}", "--all"],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        print(f"Erro ao executar git log: {exc}", file=sys.stderr)
        return []

    commits = []
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        parts = line.split(sep, 4)
        if len(parts) < 5:
            continue

        hash_, author, email, date_str, message = parts
        idx = email_index.get(email.lower())
        student = student_ref(students, idx)
        event = {
            "hash": hash_,
            "short_hash": hash_[:7],
            "author": author,
            "email": email,
            "date": date_str,
            "message": message,
            "student": student_key(student),
            "student_name": student_name(student),
            "url": f"https://github.com/{repo}/commit/{hash_}",
            "month": month_key(date_str),
            "week": week_key(date_str),
        }
        commits.append(event)

        if student:
            student["commits_count"] += 1
            increment(student["commit_timeline"], event["month"])
        else:
            unassigned["commits_count"] += 1
            unassigned["commits"].append(event)

    return commits


def collect_issues(repo: str, token: str, login_index: dict, students: list, unassigned: dict) -> list:
    url = f"https://api.github.com/repos/{repo}/issues?state=all"
    raw_items = github_request(url, token)

    issues = []
    for item in raw_items:
        if item.get("pull_request") is not None:
            continue

        login = (item.get("user") or {}).get("login", "")
        idx = login_index.get(login.lower())
        student = student_ref(students, idx)
        title = item.get("title") or ""
        body = item.get("body") or ""
        created_at = item.get("created_at") or ""
        closed_at = item.get("closed_at") or ""
        characters = len(title) + len(body)

        event = {
            "number": item.get("number"),
            "title": title,
            "author": login,
            "state": item.get("state") or "",
            "created_at": created_at,
            "closed_at": closed_at,
            "url": item.get("html_url") or "",
            "characters": characters,
            "student": student_key(student),
            "student_name": student_name(student),
            "month": month_key(created_at),
            "week": week_key(created_at),
        }
        issues.append(event)

        if student:
            student["issues_count"] += 1
            student["issue_characters_total"] += characters
            if event["state"] == "open":
                student["open_issues_count"] += 1
            increment(student["issue_timeline"], event["month"])
        else:
            unassigned["issues_count"] += 1
            unassigned["issues"].append(event)

    for student in students:
        if student["issues_count"] > 0:
            student["issue_characters_average"] = round(
                student["issue_characters_total"] / student["issues_count"], 2
            )

    return issues


def collect_pull_requests(repo: str, token: str, login_index: dict, students: list, unassigned: dict) -> tuple[list, list]:
    url = f"https://api.github.com/repos/{repo}/pulls?state=all"
    raw_items = github_request(url, token)

    pull_requests = []
    reviews = []
    for item in raw_items:
        login = (item.get("user") or {}).get("login", "")
        idx = login_index.get(login.lower())
        student = student_ref(students, idx)
        created_at = item.get("created_at") or ""
        merged_at = item.get("merged_at") or ""
        closed_at = item.get("closed_at") or ""
        is_merged = bool(merged_at)

        pr = {
            "number": item.get("number"),
            "title": item.get("title") or "",
            "author": login,
            "state": item.get("state") or "",
            "created_at": created_at,
            "closed_at": closed_at,
            "merged_at": merged_at,
            "is_merged": is_merged,
            "url": item.get("html_url") or "",
            "student": student_key(student),
            "student_name": student_name(student),
            "review_count": 0,
            "month": month_key(created_at),
            "week": week_key(created_at),
        }
        pull_requests.append(pr)

        if student:
            student["pull_requests_count"] += 1
            if is_merged:
                student["pull_requests_merged_count"] += 1
            if pr["state"] == "open":
                student["open_pull_requests_count"] += 1
            increment(student["pull_request_timeline"], pr["month"])
        else:
            unassigned["pull_requests_count"] += 1
            unassigned["pull_requests"].append(pr)

        pr_reviews = collect_reviews_for_pr(repo, token, pr["number"], login_index, students, unassigned)
        pr["review_count"] = len(pr_reviews)
        reviews.extend(pr_reviews)

    return pull_requests, reviews


def collect_reviews_for_pr(repo: str, token: str, pr_number: int, login_index: dict, students: list, unassigned: dict) -> list:
    encoded_repo = urllib.parse.quote(repo, safe="/")
    url = f"https://api.github.com/repos/{encoded_repo}/pulls/{pr_number}/reviews"
    raw_reviews = github_request(url, token)

    reviews = []
    for item in raw_reviews:
        login = (item.get("user") or {}).get("login", "")
        idx = login_index.get(login.lower())
        student = student_ref(students, idx)
        submitted_at = item.get("submitted_at") or ""
        review = {
            "id": item.get("id"),
            "pull_request_number": pr_number,
            "author": login,
            "state": item.get("state") or "",
            "submitted_at": submitted_at,
            "url": item.get("html_url") or "",
            "student": student_key(student),
            "student_name": student_name(student),
            "month": month_key(submitted_at),
            "week": week_key(submitted_at),
        }
        reviews.append(review)

        if student:
            student["reviews_count"] += 1
            increment(student["review_timeline"], review["month"])
        else:
            unassigned["reviews_count"] += 1
            unassigned["reviews"].append(review)

    return reviews


# ---------------------------------------------------------------------------
# Agregação
# ---------------------------------------------------------------------------

def build_timeline(events: list, date_field: str, bucket: str) -> dict:
    timeline = {}
    for event in events:
        value = event.get(date_field) or event_date(event)
        key = month_key(value) if bucket == "month" else week_key(value)
        increment(timeline, key)
    return dict(sorted(timeline.items()))


def build_student_timelines(students: list, events: dict, bucket: str) -> dict:
    result = {student["github"]: {"commits": {}, "issues": {}, "pull_requests": {}, "reviews": {}} for student in students}
    result["unassigned"] = {"commits": {}, "issues": {}, "pull_requests": {}, "reviews": {}}

    field_by_type = {
        "commits": "date",
        "issues": "created_at",
        "pull_requests": "created_at",
        "reviews": "submitted_at",
    }
    for event_type, event_list in events.items():
        date_field = field_by_type[event_type]
        for event in event_list:
            key = event.get("student") or "unassigned"
            if key not in result:
                result[key] = {"commits": {}, "issues": {}, "pull_requests": {}, "reviews": {}}
            value = event.get(date_field) or ""
            period = month_key(value) if bucket == "month" else week_key(value)
            increment(result[key][event_type], period)

    return result


def build_summary(students: list, commits: list, issues: list, pull_requests: list, reviews: list, generated_dt: datetime, unassigned: dict) -> dict:
    open_issues = [issue for issue in issues if issue.get("state") == "open"]
    closed_issues = [issue for issue in issues if issue.get("state") == "closed"]
    open_prs = [pr for pr in pull_requests if pr.get("state") == "open"]
    merged_prs = [pr for pr in pull_requests if pr.get("is_merged")]
    closed_prs = [pr for pr in pull_requests if pr.get("state") == "closed" and not pr.get("is_merged")]

    all_events = commits + issues + pull_requests + reviews
    recent_events = [event for event in all_events if is_recent(event_date(event), generated_dt)]
    recent_by_student = {}
    for event in recent_events:
        increment(recent_by_student, event.get("student") or "unassigned")

    for student in students:
        student["recent_activity_count"] = recent_by_student.get(student["github"], 0)

    return {
        "students_count": len(students),
        "commits_count": len(commits),
        "issues_count": len(issues),
        "open_issues_count": len(open_issues),
        "closed_issues_count": len(closed_issues),
        "pull_requests_count": len(pull_requests),
        "open_pull_requests_count": len(open_prs),
        "merged_pull_requests_count": len(merged_prs),
        "closed_unmerged_pull_requests_count": len(closed_prs),
        "reviews_count": len(reviews),
        "recent_activity_count": len(recent_events),
        "unassigned": {
            "commits_count": unassigned["commits_count"],
            "issues_count": unassigned["issues_count"],
            "pull_requests_count": unassigned["pull_requests_count"],
            "reviews_count": unassigned["reviews_count"],
        },
    }


def build_timelines(commits: list, issues: list, pull_requests: list, reviews: list, students: list) -> dict:
    events = {
        "commits": commits,
        "issues": issues,
        "pull_requests": pull_requests,
        "reviews": reviews,
    }
    return {
        "month": {
            "repository": {
                "commits": build_timeline(commits, "date", "month"),
                "issues": build_timeline(issues, "created_at", "month"),
                "pull_requests": build_timeline(pull_requests, "created_at", "month"),
                "reviews": build_timeline(reviews, "submitted_at", "month"),
            },
            "students": build_student_timelines(students, events, "month"),
        },
        "week": {
            "repository": {
                "commits": build_timeline(commits, "date", "week"),
                "issues": build_timeline(issues, "created_at", "week"),
                "pull_requests": build_timeline(pull_requests, "created_at", "week"),
                "reviews": build_timeline(reviews, "submitted_at", "week"),
            },
            "students": build_student_timelines(students, events, "week"),
        },
    }


# ---------------------------------------------------------------------------
# Escrita de artefatos
# ---------------------------------------------------------------------------

def save_metrics(output_dir: Path, data: dict) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "metrics.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"metrics.json salvo em {path}")


def save_html(output_dir: Path, data: dict) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "index.html"
    html = render_html(data)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"index.html salvo em {path}")


def render_html(data: dict) -> str:
    data_json = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    generated_at = data.get("generated_at", "")
    repository = data.get("repository", "")

    template = Template("""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Produtividade GitHub - $repository</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    :root {
      color-scheme: light;
      --bg: #f7f8fa;
      --panel: #ffffff;
      --panel-soft: #f1f5f9;
      --text: #1f2937;
      --muted: #64748b;
      --border: #d9e2ec;
      --accent: #2563eb;
      --accent-2: #0f766e;
      --warn: #b45309;
      --danger: #b91c1c;
      --shadow: 0 1px 2px rgba(15, 23, 42, 0.08);
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.45;
    }
    a { color: var(--accent); text-decoration: none; }
    a:hover { text-decoration: underline; }
    header {
      background: #0f172a;
      color: #fff;
      padding: 24px clamp(16px, 4vw, 40px);
      border-bottom: 4px solid var(--accent-2);
    }
    header h1 { margin: 0 0 8px; font-size: clamp(1.45rem, 2vw, 2.2rem); letter-spacing: 0; }
    header p { margin: 0; color: #cbd5e1; }
    main { padding: 20px clamp(12px, 3vw, 36px) 36px; }
    .toolbar {
      display: grid;
      grid-template-columns: minmax(220px, 1.4fr) repeat(4, minmax(150px, 1fr)) auto;
      gap: 12px;
      align-items: end;
      margin-bottom: 18px;
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 14px;
      box-shadow: var(--shadow);
    }
    label { display: grid; gap: 5px; font-size: 0.78rem; color: var(--muted); font-weight: 650; }
    select, input, button {
      min-height: 38px;
      border: 1px solid var(--border);
      border-radius: 6px;
      background: #fff;
      color: var(--text);
      padding: 8px 10px;
      font: inherit;
      width: 100%;
    }
    button {
      cursor: pointer;
      background: var(--accent);
      color: #fff;
      border-color: var(--accent);
      font-weight: 700;
      white-space: nowrap;
    }
    button.secondary { background: #fff; color: var(--text); border-color: var(--border); }
    .kpis {
      display: grid;
      grid-template-columns: repeat(8, minmax(130px, 1fr));
      gap: 12px;
      margin-bottom: 18px;
    }
    .kpi {
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 14px;
      box-shadow: var(--shadow);
      min-height: 94px;
    }
    .kpi span { display: block; color: var(--muted); font-size: 0.78rem; font-weight: 700; }
    .kpi strong { display: block; font-size: 1.75rem; margin-top: 6px; }
    .grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 14px;
      margin-bottom: 18px;
    }
    section {
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 14px;
      box-shadow: var(--shadow);
      min-width: 0;
    }
    section h2 { font-size: 1rem; margin: 0 0 12px; }
    .chart-box { min-height: 320px; position: relative; }
    canvas { max-height: 280px; }
    .empty { display: none; color: var(--muted); background: var(--panel-soft); border-radius: 6px; padding: 16px; text-align: center; }
    .table-tools { display: flex; gap: 10px; align-items: center; justify-content: space-between; margin-bottom: 10px; }
    .table-wrap { overflow-x: auto; border: 1px solid var(--border); border-radius: 8px; }
    table { width: 100%; border-collapse: collapse; font-size: 0.86rem; min-width: 760px; }
    th, td { padding: 9px 10px; border-bottom: 1px solid var(--border); text-align: left; vertical-align: top; }
    th { background: var(--panel-soft); color: #334155; cursor: pointer; user-select: none; white-space: nowrap; }
    tr:hover td { background: #f8fafc; }
    .pill { display: inline-block; border-radius: 999px; padding: 2px 8px; font-size: 0.74rem; font-weight: 700; background: #e0f2fe; color: #075985; }
    .pill.open { background: #fef3c7; color: var(--warn); }
    .pill.closed { background: #dcfce7; color: #166534; }
    .pill.merged { background: #ede9fe; color: #6d28d9; }
    footer { color: var(--muted); text-align: center; padding: 0 16px 28px; font-size: 0.8rem; }
    @media (max-width: 1200px) {
      .kpis { grid-template-columns: repeat(4, minmax(130px, 1fr)); }
      .toolbar { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    }
    @media (max-width: 760px) {
      main { padding: 12px; }
      .grid, .toolbar, .kpis { grid-template-columns: 1fr; }
      .kpi strong { font-size: 1.45rem; }
    }
  </style>
</head>
<body>
  <header>
    <h1>Produtividade GitHub - $repository</h1>
    <p>Gerado em <strong>$generated_at</strong>. Indicadores auxiliares para acompanhamento do squad.</p>
  </header>

  <main>
    <div class="toolbar">
      <label>Busca
        <input id="searchInput" type="search" placeholder="Aluno, titulo, autor, hash...">
      </label>
      <label>Aluno
        <select id="studentFilter"></select>
      </label>
      <label>Metrica
        <select id="metricFilter">
          <option value="all">Todas</option>
          <option value="commits">Commits</option>
          <option value="issues">Issues</option>
          <option value="pull_requests">Pull requests</option>
          <option value="reviews">Reviews</option>
        </select>
      </label>
      <label>Inicio
        <input id="startDate" type="date">
      </label>
      <label>Fim
        <input id="endDate" type="date">
      </label>
      <label>Periodo
        <select id="timelineMode">
          <option value="month">Mensal</option>
          <option value="week">Semanal</option>
        </select>
      </label>
      <button id="clearFilters" class="secondary" type="button">Limpar filtros</button>
    </div>

    <div class="kpis" id="kpis"></div>

    <div class="grid">
      <section>
        <h2>Comparativo por aluno</h2>
        <div class="chart-box"><canvas id="studentChart"></canvas><p id="studentChartEmpty" class="empty">Sem dados para os filtros selecionados.</p></div>
      </section>
      <section>
        <h2>Evolucao temporal</h2>
        <div class="chart-box"><canvas id="timelineChart"></canvas><p id="timelineChartEmpty" class="empty">Sem dados temporais para os filtros selecionados.</p></div>
      </section>
      <section>
        <h2>Distribuicao de atividade</h2>
        <div class="chart-box"><canvas id="activityChart"></canvas><p id="activityChartEmpty" class="empty">Sem atividade para os filtros selecionados.</p></div>
      </section>
      <section>
        <h2>Pendencias por aluno</h2>
        <div class="chart-box"><canvas id="pendingChart"></canvas><p id="pendingChartEmpty" class="empty">Sem pendencias para os filtros selecionados.</p></div>
      </section>
    </div>

    <section>
      <div class="table-tools"><h2>Resumo por aluno</h2><span id="studentCount" class="pill"></span></div>
      <div class="table-wrap"><table id="studentsTable"></table></div>
    </section>

    <div class="grid">
      <section>
        <div class="table-tools"><h2>Commits</h2><span id="commitCount" class="pill"></span></div>
        <div class="table-wrap"><table id="commitsTable"></table></div>
      </section>
      <section>
        <div class="table-tools"><h2>Issues</h2><span id="issueCount" class="pill"></span></div>
        <div class="table-wrap"><table id="issuesTable"></table></div>
      </section>
      <section>
        <div class="table-tools"><h2>Pull requests</h2><span id="prCount" class="pill"></span></div>
        <div class="table-wrap"><table id="pullRequestsTable"></table></div>
      </section>
      <section>
        <div class="table-tools"><h2>Reviews</h2><span id="reviewCount" class="pill"></span></div>
        <div class="table-wrap"><table id="reviewsTable"></table></div>
      </section>
    </div>
  </main>

  <footer>
    Dados gerados por GitHub Actions. O relatorio nao inclui tokens ou credenciais.
    <a href="metrics.json">Abrir metrics.json</a>
  </footer>

  <script id="metrics-data" type="application/json">$data_json</script>
  <script>
    const DATA = JSON.parse(document.getElementById('metrics-data').textContent);
    const PALETTE = ['#2563eb', '#0f766e', '#b45309', '#7c3aed', '#dc2626', '#0891b2', '#4d7c0f', '#be185d'];
    const charts = {};
    const sortState = {};

    const filters = {
      search: '',
      student: 'all',
      metric: 'all',
      start: '',
      end: '',
      timeline: 'month',
    };

    function byId(id) { return document.getElementById(id); }
    function number(value) { return new Intl.NumberFormat('pt-BR').format(value || 0); }
    function dateOnly(value) { return value ? String(value).slice(0, 10) : ''; }
    function recentCutoff() {
      const generated = dateOnly(DATA.generated_at);
      if (!generated) return '';
      const date = new Date(`${generated}T00:00:00Z`);
      date.setUTCDate(date.getUTCDate() - 14);
      return date.toISOString().slice(0, 10);
    }
    function isRecent(value) {
      const cutoff = recentCutoff();
      const date = dateOnly(value);
      return Boolean(cutoff && date && date >= cutoff);
    }
    function escapeHtml(value) {
      return String(value ?? '').replace(/[&<>"']/g, char => ({
        '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
      })[char]);
    }
    function inDateRange(value) {
      const date = dateOnly(value);
      if (!date) return true;
      if (filters.start && date < filters.start) return false;
      if (filters.end && date > filters.end) return false;
      return true;
    }
    function matchesSearch(row) {
      if (!filters.search) return true;
      return JSON.stringify(row).toLowerCase().includes(filters.search);
    }
    function matchesStudent(row) {
      return filters.student === 'all' || row.student === filters.student || row.github === filters.student;
    }
    function metricEnabled(metric) {
      return filters.metric === 'all' || filters.metric === metric;
    }
    function filterEvents(events, metric) {
      if (!metricEnabled(metric)) return [];
      return events.filter(event => matchesStudent(event) && inDateRange(event.date || event.created_at || event.submitted_at) && matchesSearch(event));
    }
    function filteredStudents() {
      return DATA.students.filter(student => matchesStudent(student) && matchesSearch(student));
    }
    function uniqueSorted(values) {
      return [...new Set(values.filter(Boolean))].sort();
    }
    function addSeriesValue(series, key, metric, amount = 1) {
      if (!series[key]) series[key] = { commits: 0, issues: 0, pull_requests: 0, reviews: 0 };
      series[key][metric] += amount;
    }
    function eventBucket(event) {
      return filters.timeline === 'week' ? event.week : event.month;
    }
    function destroyChart(id) {
      if (charts[id]) charts[id].destroy();
      charts[id] = null;
    }
    function renderChart(id, emptyId, config, hasData) {
      const canvas = byId(id);
      const empty = byId(emptyId);
      destroyChart(id);
      if (!hasData || typeof Chart === 'undefined') {
        canvas.style.display = 'none';
        empty.style.display = 'block';
        return;
      }
      canvas.style.display = '';
      empty.style.display = 'none';
      charts[id] = new Chart(canvas, config);
    }
    function link(url, text) {
      if (!url) return escapeHtml(text);
      return `<a href="${escapeHtml(url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(text)}</a>`;
    }
    function setupFilters() {
      const studentFilter = byId('studentFilter');
      studentFilter.innerHTML = '<option value="all">Todos</option>' + DATA.students
        .map(student => `<option value="${escapeHtml(student.github)}">${escapeHtml(student.name)}</option>`)
        .join('');

      const dates = [
        ...DATA.commits.map(item => dateOnly(item.date)),
        ...DATA.issues.map(item => dateOnly(item.created_at)),
        ...DATA.pull_requests.map(item => dateOnly(item.created_at)),
        ...DATA.reviews.map(item => dateOnly(item.submitted_at)),
      ].filter(Boolean).sort();
      if (dates.length) {
        byId('startDate').value = dates[0];
        byId('endDate').value = dates[dates.length - 1];
        filters.start = dates[0];
        filters.end = dates[dates.length - 1];
      }

      byId('searchInput').addEventListener('input', event => { filters.search = event.target.value.trim().toLowerCase(); render(); });
      byId('studentFilter').addEventListener('change', event => { filters.student = event.target.value; render(); });
      byId('metricFilter').addEventListener('change', event => { filters.metric = event.target.value; render(); });
      byId('startDate').addEventListener('change', event => { filters.start = event.target.value; render(); });
      byId('endDate').addEventListener('change', event => { filters.end = event.target.value; render(); });
      byId('timelineMode').addEventListener('change', event => { filters.timeline = event.target.value; render(); });
      byId('clearFilters').addEventListener('click', () => {
        filters.search = '';
        filters.student = 'all';
        filters.metric = 'all';
        filters.start = dates[0] || '';
        filters.end = dates[dates.length - 1] || '';
        filters.timeline = 'month';
        byId('searchInput').value = '';
        byId('studentFilter').value = 'all';
        byId('metricFilter').value = 'all';
        byId('startDate').value = filters.start;
        byId('endDate').value = filters.end;
        byId('timelineMode').value = 'month';
        render();
      });
    }
    function calculate() {
      const commits = filterEvents(DATA.commits, 'commits');
      const issues = filterEvents(DATA.issues, 'issues');
      const prs = filterEvents(DATA.pull_requests, 'pull_requests');
      const reviews = filterEvents(DATA.reviews, 'reviews');
      const students = filteredStudents();
      const byStudent = {};
      for (const student of DATA.students) {
        if (filters.student !== 'all' && student.github !== filters.student) continue;
        byStudent[student.github] = {
          github: student.github,
          name: student.name,
          commits: 0,
          issues: 0,
          prs: 0,
          merged: 0,
          reviews: 0,
          openIssues: 0,
          openPrs: 0,
          recent: 0,
          chars: 0,
        };
      }
      function ensure(key, name) {
        if (!byStudent[key]) byStudent[key] = { github: key, name, commits: 0, issues: 0, prs: 0, merged: 0, reviews: 0, openIssues: 0, openPrs: 0, recent: 0, chars: 0 };
        return byStudent[key];
      }
      for (const commit of commits) {
        const row = ensure(commit.student, commit.student_name);
        row.commits += 1;
        if (isRecent(commit.date)) row.recent += 1;
      }
      for (const issue of issues) {
        const row = ensure(issue.student, issue.student_name);
        row.issues += 1;
        row.chars += issue.characters || 0;
        if (isRecent(issue.created_at)) row.recent += 1;
        if (issue.state === 'open') row.openIssues += 1;
      }
      for (const pr of prs) {
        const row = ensure(pr.student, pr.student_name);
        row.prs += 1;
        if (pr.is_merged) row.merged += 1;
        if (isRecent(pr.created_at)) row.recent += 1;
        if (pr.state === 'open') row.openPrs += 1;
      }
      for (const review of reviews) {
        const row = ensure(review.student, review.student_name);
        row.reviews += 1;
        if (isRecent(review.submitted_at)) row.recent += 1;
      }
      return { commits, issues, prs, reviews, students, byStudent: Object.values(byStudent).filter(item => matchesSearch(item)) };
    }
    function renderKpis(model) {
      const openIssues = model.issues.filter(item => item.state === 'open').length;
      const mergedPrs = model.prs.filter(item => item.is_merged).length;
      const openPrs = model.prs.filter(item => item.state === 'open').length;
      const recent = model.byStudent.reduce((total, item) => total + item.recent, 0);
      const cards = [
        ['Commits', model.commits.length],
        ['Issues', model.issues.length],
        ['Issues abertas', openIssues],
        ['Pull requests', model.prs.length],
        ['PRs mergeados', mergedPrs],
        ['PRs abertos', openPrs],
        ['Reviews', model.reviews.length],
        ['Atividade recente', recent],
      ];
      byId('kpis').innerHTML = cards.map(([label, value]) => `<div class="kpi"><span>${escapeHtml(label)}</span><strong>${number(value)}</strong></div>`).join('');
    }
    function renderCharts(model) {
      const labels = model.byStudent.map(item => item.name);
      const datasets = [
        { label: 'Commits', data: model.byStudent.map(item => item.commits), backgroundColor: PALETTE[0] },
        { label: 'Issues', data: model.byStudent.map(item => item.issues), backgroundColor: PALETTE[1] },
        { label: 'PRs', data: model.byStudent.map(item => item.prs), backgroundColor: PALETTE[2] },
        { label: 'Reviews', data: model.byStudent.map(item => item.reviews), backgroundColor: PALETTE[3] },
        { label: 'Recentes', data: model.byStudent.map(item => item.recent), backgroundColor: PALETTE[4] },
      ];
      renderChart('studentChart', 'studentChartEmpty', {
        type: 'bar',
        data: { labels, datasets },
        options: { responsive: true, maintainAspectRatio: false, scales: { y: { beginAtZero: true, ticks: { precision: 0 } } } }
      }, datasets.some(ds => ds.data.some(Boolean)));

      const series = {};
      for (const commit of model.commits) addSeriesValue(series, eventBucket(commit), 'commits');
      for (const issue of model.issues) addSeriesValue(series, eventBucket(issue), 'issues');
      for (const pr of model.prs) addSeriesValue(series, eventBucket(pr), 'pull_requests');
      const periods = Object.keys(series).sort();
      renderChart('timelineChart', 'timelineChartEmpty', {
        type: 'line',
        data: {
          labels: periods,
          datasets: [
            { label: 'Commits', data: periods.map(p => series[p].commits), borderColor: PALETTE[0], backgroundColor: PALETTE[0], tension: 0.25 },
            { label: 'Issues', data: periods.map(p => series[p].issues), borderColor: PALETTE[1], backgroundColor: PALETTE[1], tension: 0.25 },
            { label: 'PRs', data: periods.map(p => series[p].pull_requests), borderColor: PALETTE[2], backgroundColor: PALETTE[2], tension: 0.25 },
          ]
        },
        options: { responsive: true, maintainAspectRatio: false, scales: { y: { beginAtZero: true, ticks: { precision: 0 } } } }
      }, periods.length > 0);

      const activityValues = [model.commits.length, model.issues.length, model.prs.length, model.reviews.length];
      renderChart('activityChart', 'activityChartEmpty', {
        type: 'doughnut',
        data: { labels: ['Commits', 'Issues', 'PRs', 'Reviews'], datasets: [{ data: activityValues, backgroundColor: PALETTE.slice(0, 4) }] },
        options: { responsive: true, maintainAspectRatio: false }
      }, activityValues.some(Boolean));

      const pendingValues = model.byStudent.map(item => item.openIssues + item.openPrs);
      renderChart('pendingChart', 'pendingChartEmpty', {
        type: 'bar',
        data: { labels, datasets: [{ label: 'Issues + PRs abertos', data: pendingValues, backgroundColor: PALETTE[4] }] },
        options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, ticks: { precision: 0 } } } }
      }, pendingValues.some(Boolean));
    }
    function sortRows(tableId, rows, key) {
      const state = sortState[tableId] || { key, dir: 1 };
      state.dir = state.key === key ? -state.dir : 1;
      state.key = key;
      sortState[tableId] = state;
      rows.sort((a, b) => {
        const av = a[key] ?? '';
        const bv = b[key] ?? '';
        if (typeof av === 'number' && typeof bv === 'number') return (av - bv) * state.dir;
        return String(av).localeCompare(String(bv), 'pt-BR') * state.dir;
      });
    }
    function renderTable(tableId, columns, rows) {
      const table = byId(tableId);
      table.innerHTML = `<thead><tr>${columns.map(col => `<th data-key="${col.key}">${escapeHtml(col.label)}</th>`).join('')}</tr></thead><tbody>${rows.map(row => `<tr>${columns.map(col => `<td>${col.render ? col.render(row) : escapeHtml(row[col.key])}</td>`).join('')}</tr>`).join('')}</tbody>`;
      table.querySelectorAll('th').forEach(th => th.addEventListener('click', () => {
        sortRows(tableId, rows, th.dataset.key);
        renderTable(tableId, columns, rows);
      }));
    }
    function renderTables(model) {
      byId('studentCount').textContent = `${model.byStudent.length} alunos`;
      byId('commitCount').textContent = `${model.commits.length} commits`;
      byId('issueCount').textContent = `${model.issues.length} issues`;
      byId('prCount').textContent = `${model.prs.length} PRs`;
      byId('reviewCount').textContent = `${model.reviews.length} reviews`;

      renderTable('studentsTable', [
        { key: 'name', label: 'Aluno', render: row => row.github === 'unassigned' ? escapeHtml(row.name) : link(`https://github.com/${row.github}`, row.name) },
        { key: 'commits', label: 'Commits' },
        { key: 'issues', label: 'Issues' },
        { key: 'prs', label: 'PRs' },
        { key: 'merged', label: 'PRs mergeados' },
        { key: 'reviews', label: 'Reviews' },
        { key: 'recent', label: 'Atividade recente' },
        { key: 'openIssues', label: 'Issues abertas' },
        { key: 'openPrs', label: 'PRs abertos' },
        { key: 'chars', label: 'Caracteres issues' },
      ], [...model.byStudent]);

      renderTable('commitsTable', [
        { key: 'date', label: 'Data', render: row => escapeHtml(dateOnly(row.date)) },
        { key: 'student_name', label: 'Aluno' },
        { key: 'short_hash', label: 'Hash', render: row => link(row.url, row.short_hash) },
        { key: 'message', label: 'Mensagem' },
      ], [...model.commits]);

      renderTable('issuesTable', [
        { key: 'created_at', label: 'Criada', render: row => escapeHtml(dateOnly(row.created_at)) },
        { key: 'student_name', label: 'Aluno' },
        { key: 'number', label: '#', render: row => link(row.url, `#${row.number}`) },
        { key: 'title', label: 'Titulo' },
        { key: 'state', label: 'Estado', render: row => `<span class="pill ${escapeHtml(row.state)}">${escapeHtml(row.state)}</span>` },
        { key: 'characters', label: 'Caracteres' },
      ], [...model.issues]);

      renderTable('pullRequestsTable', [
        { key: 'created_at', label: 'Criado', render: row => escapeHtml(dateOnly(row.created_at)) },
        { key: 'student_name', label: 'Aluno' },
        { key: 'number', label: '#', render: row => link(row.url, `#${row.number}`) },
        { key: 'title', label: 'Titulo' },
        { key: 'state', label: 'Estado', render: row => `<span class="pill ${row.is_merged ? 'merged' : escapeHtml(row.state)}">${row.is_merged ? 'merged' : escapeHtml(row.state)}</span>` },
        { key: 'review_count', label: 'Reviews' },
      ], [...model.prs]);

      renderTable('reviewsTable', [
        { key: 'submitted_at', label: 'Data', render: row => escapeHtml(dateOnly(row.submitted_at)) },
        { key: 'student_name', label: 'Aluno' },
        { key: 'pull_request_number', label: 'PR', render: row => link(row.url, `#${row.pull_request_number}`) },
        { key: 'state', label: 'Estado' },
        { key: 'author', label: 'Autor' },
      ], [...model.reviews]);
    }
    function render() {
      const model = calculate();
      renderKpis(model);
      renderCharts(model);
      renderTables(model);
    }
    setupFilters();
    render();
  </script>
</body>
</html>
""")
    return template.safe_substitute(
        repository=repository,
        generated_at=generated_at,
        data_json=data_json,
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def parse_args() -> tuple[str, str, str]:
    parser = argparse.ArgumentParser(description="Gera relatório de produtividade por aluno.")
    parser.add_argument("--repo", required=True, help="owner/repo (ex: unb-mds/2026-1-Squad08)")
    parser.add_argument(
        "--students",
        default=".github/performance-students.json",
        help="Caminho para o arquivo de configuração de alunos",
    )
    parser.add_argument(
        "--output-dir",
        default="docs/performance",
        help="Diretório de saída para os artefatos gerados",
    )
    args = parser.parse_args()
    return args.repo, args.students, args.output_dir


def main() -> None:
    repo, students_path, output_dir_str = parse_args()
    token = os.environ.get("GITHUB_TOKEN", "")
    if not token:
        print("Aviso: GITHUB_TOKEN não definido. Coleta de issues, PRs e reviews será ignorada.", file=sys.stderr)

    raw_students = load_students(students_path)
    students = init_students(raw_students)
    email_index = build_email_index(students)
    login_index = build_login_index(students)
    unassigned = {
        "commits_count": 0,
        "issues_count": 0,
        "pull_requests_count": 0,
        "reviews_count": 0,
        "commits": [],
        "issues": [],
        "pull_requests": [],
        "reviews": [],
    }

    generated_dt = datetime.now(timezone.utc)
    generated_at = generated_dt.strftime("%Y-%m-%dT%H:%M:%SZ")

    commits = collect_commits(repo, email_index, students, unassigned)
    issues = collect_issues(repo, token, login_index, students, unassigned) if token else []
    pull_requests, reviews = collect_pull_requests(repo, token, login_index, students, unassigned) if token else ([], [])

    summary = build_summary(students, commits, issues, pull_requests, reviews, generated_dt, unassigned)
    timelines = build_timelines(commits, issues, pull_requests, reviews, students)

    metrics = {
        "generated_at": generated_at,
        "repository": repo,
        "students": students,
        "summary": summary,
        "timelines": timelines,
        "unassigned": unassigned,
        "commits": commits,
        "issues": issues,
        "pull_requests": pull_requests,
        "reviews": reviews,
    }

    output_dir = Path(output_dir_str)
    save_metrics(output_dir, metrics)
    save_html(output_dir, metrics)

    print(f"\nRelatório gerado com sucesso em {output_dir}/")
    print(f"  Alunos: {len(students)}")
    print(f"  Commits: {len(commits)}")
    print(f"  Issues: {len(issues)}")
    print(f"  Pull requests: {len(pull_requests)}")
    print(f"  Reviews: {len(reviews)}")


if __name__ == "__main__":
    main()
