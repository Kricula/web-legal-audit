<#
.SYNOPSIS
  Instalátor skillu web-legal-audit-cz pro AI editory a agenty (Windows PowerShell 5.1+ / PowerShell 7).

.EXAMPLE
  .\install.ps1 -Agent cursor
  .\install.ps1 -Agent claude-code,codex -Global
  .\install.ps1 -Agent all -Global
  .\install.ps1 -Zip
  .\install.ps1 -Agent cursor -Uninstall
  .\install.ps1 -Agent cursor -Ref v2.2.0

.EXAMPLE
  # Bez klonování:
  & ([scriptblock]::Create((irm https://raw.githubusercontent.com/Kricula/web-legal-audit/main/install.ps1))) -Agent cursor
#>
[CmdletBinding()]
param(
  [string[]]$Agent,
  [switch]$Global,
  [string]$Project = (Get-Location).Path,
  [string]$Source,
  [string]$Ref,
  [switch]$Force,
  [switch]$Uninstall,
  [switch]$Zip,
  [string]$ZipPath,
  [switch]$List,
  [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
$SkillName = 'web-legal-audit-cz'
$Repo = 'Kricula/web-legal-audit'
$DefaultRef = 'main'
$H = $HOME

$Agents = [ordered]@{
  'claude-code'    = @{ Name = 'Claude Code';             Project = '.claude/skills';   Global = "$H/.claude/skills" }
  'cursor'         = @{ Name = 'Cursor';                  Project = '.agents/skills';   Global = "$H/.cursor/skills" }
  'codex'          = @{ Name = 'OpenAI Codex';            Project = '.agents/skills';   Global = "$H/.agents/skills" }
  'github-copilot' = @{ Name = 'GitHub Copilot';          Project = '.agents/skills';   Global = "$H/.copilot/skills" }
  'gemini-cli'     = @{ Name = 'Gemini CLI';              Project = '.agents/skills';   Global = "$H/.gemini/skills" }
  'windsurf'       = @{ Name = 'Windsurf';                Project = '.windsurf/skills'; Global = "$H/.codeium/windsurf/skills" }
  'opencode'       = @{ Name = 'OpenCode';                Project = '.agents/skills';   Global = "$H/.config/opencode/skills" }
  'cline'          = @{ Name = 'Cline';                   Project = '.agents/skills';   Global = "$H/.agents/skills" }
  'roo'            = @{ Name = 'Roo Code';                Project = '.roo/skills';      Global = "$H/.roo/skills" }
  'kiro-cli'       = @{ Name = 'Kiro CLI';                Project = '.kiro/skills';     Global = "$H/.kiro/skills" }
  'junie'          = @{ Name = 'JetBrains Junie';         Project = '.junie/skills';    Global = "$H/.junie/skills" }
  'universal'      = @{ Name = 'Amp / ostatní (.agents)'; Project = '.agents/skills';   Global = "$H/.config/agents/skills" }
}

function Ok($m)   { Write-Host "✔ $m" -ForegroundColor Green }
function Info($m) { Write-Host "• $m" -ForegroundColor Cyan }
function Warn($m) { Write-Warning $m }

if ($List) {
  '{0,-16} {1,-26} {2,-22} {3}' -f 'AGENT', 'NÁZEV', 'PROJEKT', 'GLOBÁLNĚ'
  foreach ($k in $Agents.Keys) { '{0,-16} {1,-26} {2,-22} {3}' -f $k, $Agents[$k].Name, "$($Agents[$k].Project)/", "$($Agents[$k].Global)/" }
  return
}

$tmp = $null
function Resolve-Source {
  if ($Source) {
    if (-not (Test-Path (Join-Path $Source 'SKILL.md'))) { throw "Ve složce $Source chybí SKILL.md" }
    return (Resolve-Path $Source).Path
  }
  if (-not $Ref -and $PSScriptRoot) {
    $local = Join-Path $PSScriptRoot "skills/$SkillName"
    if (Test-Path (Join-Path $local 'SKILL.md')) { return $local }
  }
  $script:tmp = Join-Path ([IO.Path]::GetTempPath()) ("wla-" + [guid]::NewGuid())
  New-Item -ItemType Directory -Path $script:tmp | Out-Null
  $zipFile = Join-Path $script:tmp 'repo.zip'
  $r = if ($Ref) { $Ref } else { $DefaultRef }
  if ($r -notmatch '^[A-Za-z0-9._/-]+$') { throw "Neplatná hodnota -Ref: $r" }
  Info "Stahuji ${Repo}@${r}..."
  try {
    Invoke-WebRequest -UseBasicParsing -Uri "https://codeload.github.com/$Repo/zip/$r" -OutFile $zipFile
  } catch { throw "Stažení se nezdařilo – existuje verze '$r'? Seznam: https://github.com/$Repo/releases" }
  Expand-Archive -Path $zipFile -DestinationPath $script:tmp -Force
  $dir = Get-ChildItem -Path $script:tmp -Recurse -Directory -Filter $SkillName |
    Where-Object { Test-Path (Join-Path $_.FullName 'SKILL.md') } | Select-Object -First 1
  if (-not $dir) { throw "Ve staženém archivu chybí skills/$SkillName/SKILL.md" }
  return $dir.FullName
}

try {
  if (-not $Agent -and -not $Zip) {
    Write-Host "Kam chceš skill $SkillName nainstalovat?"
    $keys = @($Agents.Keys); $i = 1
    foreach ($k in $keys) { Write-Host ('  {0,2}) {1}' -f $i, $Agents[$k].Name); $i++ }
    Write-Host ('  {0,2}) Všichni výše' -f $i)
    Write-Host ('  {0,2}) ZIP pro aplikaci Claude (web/desktop)' -f ($i + 1))
    $ans = Read-Host 'Čísla oddělená čárkou'
    $sel = @()
    foreach ($n in ($ans -replace '\s', '' -split ',')) {
      $n = [int]$n
      if ($n -eq $i) { $sel = @('all'); break }
      elseif ($n -eq $i + 1) { $Zip = $true; break }
      elseif ($n -ge 1 -and $n -lt $i) { $sel += $keys[$n - 1] }
      else { throw "Neplatná volba: $n" }
    }
    $Agent = $sel
    if (-not $Zip -and (Read-Host 'Instalovat globálně pro všechny projekty? [a/N]') -match '^[aAyY]$') { $Global = $true }
  }

  if (-not $Uninstall) {
    $src = Resolve-Source
    Info "Skill: $SkillName ze složky $src"
  }

  if ($Zip) {
    if (-not $ZipPath) { $ZipPath = Join-Path (Get-Location) "$SkillName.zip" }
    $stage = Join-Path ([IO.Path]::GetTempPath()) ("wla-zip-" + [guid]::NewGuid())
    $stageSkill = Join-Path $stage $SkillName
    New-Item -ItemType Directory -Path $stageSkill -Force | Out-Null
    Copy-Item -Path (Join-Path $src '*') -Destination $stageSkill -Recurse -Force
    Get-ChildItem $stageSkill -Recurse -Directory -Filter '__pycache__' | Remove-Item -Recurse -Force
    foreach ($x in 'tests', 'README.md', 'CHANGELOG.md') {
      $xp = Join-Path $stageSkill $x
      if (Test-Path $xp) { Remove-Item $xp -Recurse -Force }
    }
    if (Test-Path $ZipPath) { Remove-Item $ZipPath -Force }
    if ($DryRun) { Info "[dry-run] ZIP → $ZipPath" } else { Compress-Archive -Path $stageSkill -DestinationPath $ZipPath }
    Remove-Item $stage -Recurse -Force
    Ok "ZIP vytvořen: $ZipPath"
    Write-Host '   Nahraj ho v aplikaci Claude: Nastavení → Capabilities → Skills → Upload skill.'
    return
  }

  if ($Agent -contains 'all') { $ids = @($Agents.Keys) } else { $ids = @($Agent | ForEach-Object { $_ -split ',' } | ForEach-Object { $_.Trim() } | Where-Object { $_ }) }

  if (-not $Global) {
    if (-not (Test-Path $Project)) { throw "Projektová složka neexistuje: $Project" }
    $Project = (Resolve-Path $Project).Path
    Info "Projekt: $Project"
  } else { Info 'Režim: globální instalace' }

  $done = @{}
  foreach ($id in $ids) {
    if (-not $Agents.Contains($id)) { throw "Neznámý agent: $id (seznam: .\install.ps1 -List)" }
    $a = $Agents[$id]
    $base = if ($Global) { $a.Global } else { Join-Path $Project $a.Project }
    $base = [IO.Path]::GetFullPath($base)
    if ($done.ContainsKey($base)) { Info "$($a.Name) sdílí $base – už zpracováno"; continue }
    $done[$base] = $true
    $dest = Join-Path $base $SkillName

    if ($Uninstall) {
      if (Test-Path $dest) {
        if ($DryRun) { Info "[dry-run] smazat $dest" } else { Remove-Item $dest -Recurse -Force }
        Ok "Odinstalováno: $($a.Name) ($dest)"
      } else { Info "$($a.Name): nenainstalováno ($dest)" }
      continue
    }

    if (Test-Path $dest) {
      if (-not $Force -and (Read-Host "$dest už existuje. Přepsat? [a/N]") -notmatch '^[aAyY]$') { Warn "Přeskakuji $($a.Name)"; continue }
      if (-not $DryRun) { Remove-Item $dest -Recurse -Force }
    }
    if ($DryRun) { Info "[dry-run] kopírovat $src → $dest" }
    else {
      New-Item -ItemType Directory -Path $dest -Force | Out-Null
      Copy-Item -Path (Join-Path $src '*') -Destination $dest -Recurse -Force
      Get-ChildItem $dest -Recurse -Directory -Filter '__pycache__' | Remove-Item -Recurse -Force
    }
    Ok "$($a.Name) → $dest"
  }

  if (-not $Uninstall -and -not $DryRun) {
    Write-Host ''
    Write-Host 'Hotovo. Restartuj editor/agenta a požádej ho třeba: „Proveď právní audit tohoto webu.“'
  }
}
finally {
  if ($tmp -and (Test-Path $tmp)) { Remove-Item $tmp -Recurse -Force }
}
