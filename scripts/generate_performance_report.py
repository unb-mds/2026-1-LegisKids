#!/usr/bin/env python3
"""
Gera docs/performance/metrics.json e docs/performance/index.html
com métricas de desempenho por aluno extraídas do git log e da API do GitHub.

Uso:
    GITHUB_TOKEN=<token> python scripts/generate_performance_report.py \
        --repo owner/repo [--students .github/performance-students.json]
"""

import json
import os
import subprocess
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path


# ---------------------------------------------------------------------------
# Carregamento de configuração
# ---------------------------------------------------------------------------

def load_students(config_path: str) -> list:
    path = Path(config_path)
    if not path.exists():
        print(f"Erro: arquivo de configuração não encontrado: {config_path}", file=sys.stderr)
        sys.exit(1)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def build_email_index(students: list) -> dict:
    """Mapeia e-mail → índice do aluno na lista."""
    index = {}
    for i, student in enumerate(students):
        for email in student.get("emails", []):
            index[email.lower()] = i
    return index


def build_login_index(students: list) -> dict:
    """Mapeia login GitHub (lower) → índice do aluno na lista."""
    return {s["github"].lower(): i for i, s in enumerate(students)}


# ---------------------------------------------------------------------------
# Coleta de commits via git log
# ---------------------------------------------------------------------------

def collect_commits(email_index: dict, students: list) -> tuple[list, list]:
    """
    Retorna (all_commits, student_data_updates).
    all_commits: lista de dicts com hash, author, email, date, message.
    Atualiza commits_count e commit_timeline em cada aluno.
    """
    sep = "||GIT_SEP||"
    fmt = f"%H{sep}%an{sep}%ae{sep}%aI{sep}%s"
    try:
        result = subprocess.run(
            ["git", "log", f"--format={fmt}", "--all"],
            capture_output=True, text=True, check=True,
        )
    except subprocess.CalledProcessError as exc:
        print(f"Erro ao executar git log: {exc}", file=sys.stderr)
        return [], []

    commits = []
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        parts = line.split(sep, 4)
        if len(parts) < 5:
            continue
        hash_, author, email, date_str, message = parts
        commits.append({
            "hash": hash_,
            "author": author,
            "email": email,
            "date": date_str,
            "message": message,
        })

        month_key = date_str[:7]  # YYYY-MM
        idx = email_index.get(email.lower())
        if idx is not None:
            s = students[idx]
            s["commits_count"] += 1
            s["commit_timeline"][month_key] = s["commit_timeline"].get(month_key, 0) + 1

    return commits


# ---------------------------------------------------------------------------
# Coleta de issues via API do GitHub
# ---------------------------------------------------------------------------

def github_request(url: str, token: str) -> list:
    """Executa GET paginado e retorna todos os itens."""
    items = []
    page = 1
    while True:
        paged_url = f"{url}&page={page}&per_page=100"
        req = urllib.request.Request(
            paged_url,
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "performance-report-script",
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


def collect_issues(repo: str, token: str, login_index: dict, students: list) -> list:
    """Coleta issues reais (ignora PRs) e atualiza métricas dos alunos."""
    url = f"https://api.github.com/repos/{repo}/issues?state=all"
    raw_items = github_request(url, token)

    issues = []
    for item in raw_items:
        if item.get("pull_request") is not None:
            continue  # ignora pull requests

        login = (item.get("user") or {}).get("login", "")
        body = item.get("body") or ""
        title = item.get("title") or ""
        chars = len(body) + len(title)
        created_at = item.get("created_at", "")
        month_key = created_at[:7] if created_at else "unknown"

        issues.append({
            "number": item.get("number"),
            "title": title,
            "login": login,
            "created_at": created_at,
            "characters": chars,
        })

        idx = login_index.get(login.lower())
        if idx is not None:
            s = students[idx]
            s["issues_count"] += 1
            s["issue_characters_total"] += chars
            s["issue_timeline"][month_key] = s["issue_timeline"].get(month_key, 0) + 1

    # Calcular médias após processar todas as issues
    for s in students:
        if s["issues_count"] > 0:
            s["issue_characters_average"] = round(
                s["issue_characters_total"] / s["issues_count"], 2
            )

    return issues


# ---------------------------------------------------------------------------
# Geração do metrics.json
# ---------------------------------------------------------------------------

def save_metrics(output_dir: Path, data: dict) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "metrics.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"metrics.json salvo em {path}")


# ---------------------------------------------------------------------------
# Geração do index.html
# ---------------------------------------------------------------------------

def save_html(output_dir: Path, data: dict) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    students = data["students"]
    generated_at = data.get("generated_at", "")
    repository = data.get("repository", "")

    student_names = json.dumps([s["name"] for s in students], ensure_ascii=False)
    commits_data = json.dumps([s["commits_count"] for s in students])
    issues_data = json.dumps([s["issues_count"] for s in students])
    chars_total_data = json.dumps([s["issue_characters_total"] for s in students])
    chars_avg_data = json.dumps([s["issue_characters_average"] for s in students])

    rows = ""
    for s in students:
        rows += (
            f"<tr>"
            f"<td>{s['name']}</td>"
            f"<td><a href='https://github.com/{s['github']}' target='_blank'>@{s['github']}</a></td>"
            f"<td>{s['commits_count']}</td>"
            f"<td>{s['issues_count']}</td>"
            f"<td>{s['issue_characters_total']}</td>"
            f"<td>{s['issue_characters_average']}</td>"
            f"</tr>\n"
        )

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Relatório de Desempenho — {repository}</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: system-ui, sans-serif; background: #f5f5f5; color: #222; padding: 2rem; }}
    h1 {{ font-size: 1.6rem; margin-bottom: 0.25rem; }}
    .meta {{ color: #666; font-size: 0.85rem; margin-bottom: 2rem; }}
    .meta a {{ color: #0969da; }}
    .section {{ background: #fff; border-radius: 8px; padding: 1.5rem; margin-bottom: 2rem; box-shadow: 0 1px 3px rgba(0,0,0,.1); }}
    h2 {{ font-size: 1.1rem; margin-bottom: 1rem; color: #333; }}
    .charts {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }}
    @media (max-width: 700px) {{ .charts {{ grid-template-columns: 1fr; }} }}
    table {{ width: 100%; border-collapse: collapse; font-size: 0.9rem; }}
    th {{ background: #f0f0f0; text-align: left; padding: 0.5rem 0.75rem; border-bottom: 2px solid #ddd; }}
    td {{ padding: 0.5rem 0.75rem; border-bottom: 1px solid #eee; }}
    tr:hover td {{ background: #fafafa; }}
    .no-data {{ color: #888; font-style: italic; text-align: center; padding: 1rem; }}
    footer {{ text-align: center; font-size: 0.78rem; color: #999; margin-top: 2rem; }}
  </style>
</head>
<body>
  <h1>Relatório de Desempenho — {repository}</h1>
  <p class="meta">
    Gerado em: <strong>{generated_at}</strong> &nbsp;|&nbsp;
    <a href="metrics.json">metrics.json</a>
  </p>

  <div class="section">
    <h2>Resumo por Aluno</h2>
    <table>
      <thead>
        <tr>
          <th>Aluno</th>
          <th>GitHub</th>
          <th>Commits</th>
          <th>Issues</th>
          <th>Caracteres (total)</th>
          <th>Caracteres (média)</th>
        </tr>
      </thead>
      <tbody>
        {rows}
      </tbody>
    </table>
  </div>

  <div class="section">
    <h2>Gráficos</h2>
    <div class="charts">
      <div>
        <h2>Commits por Aluno</h2>
        <canvas id="commitsChart"></canvas>
        <p class="no-data" id="commitsNoData" style="display:none">Nenhum commit registrado.</p>
      </div>
      <div>
        <h2>Issues por Aluno</h2>
        <canvas id="issuesChart"></canvas>
        <p class="no-data" id="issuesNoData" style="display:none">Nenhuma issue registrada.</p>
      </div>
      <div>
        <h2>Total de Caracteres em Issues</h2>
        <canvas id="charsTotalChart"></canvas>
        <p class="no-data" id="charsTotalNoData" style="display:none">Nenhuma issue registrada.</p>
      </div>
      <div>
        <h2>Média de Caracteres por Issue</h2>
        <canvas id="charsAvgChart"></canvas>
        <p class="no-data" id="charsAvgNoData" style="display:none">Nenhuma issue registrada.</p>
      </div>
    </div>
  </div>

  <footer>
    Dados extraídos do repositório <strong>{repository}</strong> via GitHub Actions.
    Este relatório é um indicador auxiliar de participação, não uma avaliação oficial.
  </footer>

  <script>
    const NAMES = {student_names};
    const COMMITS = {commits_data};
    const ISSUES = {issues_data};
    const CHARS_TOTAL = {chars_total_data};
    const CHARS_AVG = {chars_avg_data};

    const PALETTE = [
      '#4e79a7','#f28e2b','#e15759','#76b7b2',
      '#59a14f','#edc948','#b07aa1','#ff9da7',
    ];

    function makeChart(id, noDataId, labels, values, label, color) {{
      const allZero = values.every(v => v === 0);
      if (allZero) {{
        document.getElementById(id).style.display = 'none';
        document.getElementById(noDataId).style.display = '';
        return;
      }}
      new Chart(document.getElementById(id), {{
        type: 'bar',
        data: {{
          labels,
          datasets: [{{ label, data: values, backgroundColor: PALETTE.slice(0, labels.length) }}],
        }},
        options: {{
          responsive: true,
          plugins: {{ legend: {{ display: false }} }},
          scales: {{ y: {{ beginAtZero: true, ticks: {{ precision: 0 }} }} }},
        }},
      }});
    }}

    makeChart('commitsChart', 'commitsNoData', NAMES, COMMITS, 'Commits', '#4e79a7');
    makeChart('issuesChart', 'issuesNoData', NAMES, ISSUES, 'Issues', '#f28e2b');
    makeChart('charsTotalChart', 'charsTotalNoData', NAMES, CHARS_TOTAL, 'Caracteres totais', '#e15759');
    makeChart('charsAvgChart', 'charsAvgNoData', NAMES, CHARS_AVG, 'Média de caracteres', '#76b7b2');
  </script>
</body>
</html>
"""

    path = output_dir / "index.html"
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"index.html salvo em {path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def parse_args() -> tuple[str, str, str]:
    import argparse
    parser = argparse.ArgumentParser(description="Gera relatório de desempenho por aluno.")
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
        print("Aviso: GITHUB_TOKEN não definido. Coleta de issues será ignorada.", file=sys.stderr)

    raw_students = load_students(students_path)

    # Inicializa estrutura de dados por aluno
    students = []
    for s in raw_students:
        students.append({
            "name": s["name"],
            "github": s["github"],
            "emails": s.get("emails", []),
            "commits_count": 0,
            "issues_count": 0,
            "issue_characters_total": 0,
            "issue_characters_average": 0,
            "commit_timeline": {},
            "issue_timeline": {},
        })

    email_index = build_email_index(students)
    login_index = build_login_index(students)

    commits = collect_commits(email_index, students)
    issues = collect_issues(repo, token, login_index, students) if token else []

    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    metrics = {
        "generated_at": generated_at,
        "repository": repo,
        "students": students,
        "commits": commits,
        "issues": issues,
    }

    output_dir = Path(output_dir_str)
    save_metrics(output_dir, metrics)
    save_html(output_dir, metrics)

    print(f"\nRelatório gerado com sucesso em {output_dir}/")
    print(f"  Alunos: {len(students)}")
    print(f"  Commits: {len(commits)}")
    print(f"  Issues: {len(issues)}")


if __name__ == "__main__":
    main()
