$ErrorActionPreference = "Stop"

$expected = @(
  ".gitignore",
  ".pre-commit-config.yaml",
  "README.md",
  ".secrets.baseline",
  "screenshots",
  "ai_governance\policy.md",
  "ai_governance\prompt_catalog.json",
  "ai_governance\evaluations\sample_eval.json",
  "api\.env.example",
  "api\.flake8",
  "api\gunicorn_conf.py",
  "api\manage.py",
  "api\requirements.txt",
  "api\ecoroute_api\__init__.py",
  "api\ecoroute_api\asgi.py",
  "api\ecoroute_api\middleware.py",
  "api\ecoroute_api\settings.py",
  "api\ecoroute_api\urls.py",
  "api\ecoroute_api\wsgi.py",
  "api\core\__init__.py",
  "api\core\admin.py",
  "api\core\apps.py",
  "api\core\models.py",
  "api\core\serializers.py",
  "api\core\tests.py",
  "api\core\urls.py",
  "api\core\views.py",
  "client\.editorconfig",
  "client\.eslintignore",
  "client\.eslintrc.json",
  "client\angular.json",
  "client\package.json",
  "client\tsconfig.json",
  "client\tsconfig.app.json",
  "client\tsconfig.spec.json",
  "client\src\index.html",
  "client\src\main.ts",
  "client\src\styles.css",
  "client\src\environments\environment.ts",
  "client\src\environments\environment.development.ts",
  "client\src\app\app.ts",
  "client\src\app\app.config.ts",
  "client\src\app\app.routes.ts",
  "client\src\app\models\route-audit.model.ts",
  "client\src\app\services\api.ts",
  "docs\adr\0001-security-by-design-and-openapi-first.md",
  "infra\Dockerfile",
  "infra\docker-compose.yml",
  "scripts\mock_gitleaks.py",
  "scripts\verify_tree.ps1"
)

$repoRoot = Join-Path $PSScriptRoot ".."

$missing = @()
foreach ($p in $expected) {
  $full = Join-Path $repoRoot $p
  if (-not (Test-Path -LiteralPath $full)) {
    $missing += $p
  }
}

if ($missing.Count -gt 0) {
  Write-Host "MISSING:" -ForegroundColor Red
  $missing | ForEach-Object { Write-Host "  $_" -ForegroundColor Red }
  exit 1
}

Write-Host "OK: Structure matches expected blueprint." -ForegroundColor Green
