#!/usr/bin/env bash
# Instalátor skillu web-legal-audit-cz pro AI editory a agenty (macOS, Linux, WSL).
#
# Použití:
#   ./install.sh                         # interaktivní výběr
#   ./install.sh --agent cursor          # do aktuálního projektu
#   ./install.sh --agent claude-code,codex --global
#   ./install.sh --agent all --global
#   ./install.sh --zip                   # ZIP pro nahrání do aplikace Claude
#   ./install.sh --agent cursor --uninstall
#
# Bez klonování:
#   curl -fsSL https://raw.githubusercontent.com/Kricula/web-legal-audit/main/install.sh | bash -s -- --agent cursor
set -euo pipefail

SKILL_NAME="web-legal-audit-cz"
REPO="Kricula/web-legal-audit"
BRANCH="main"

# agent | název | cesta v projektu | globální cesta
AGENTS=(
  "claude-code|Claude Code|.claude/skills|${HOME}/.claude/skills"
  "cursor|Cursor|.agents/skills|${HOME}/.cursor/skills"
  "codex|OpenAI Codex|.agents/skills|${HOME}/.agents/skills"
  "github-copilot|GitHub Copilot|.agents/skills|${HOME}/.copilot/skills"
  "gemini-cli|Gemini CLI|.agents/skills|${HOME}/.gemini/skills"
  "windsurf|Windsurf|.windsurf/skills|${HOME}/.codeium/windsurf/skills"
  "opencode|OpenCode|.agents/skills|${HOME}/.config/opencode/skills"
  "cline|Cline|.agents/skills|${HOME}/.agents/skills"
  "roo|Roo Code|.roo/skills|${HOME}/.roo/skills"
  "kiro-cli|Kiro CLI|.kiro/skills|${HOME}/.kiro/skills"
  "junie|JetBrains Junie|.junie/skills|${HOME}/.junie/skills"
  "universal|Amp / ostatní (.agents)|.agents/skills|${HOME}/.config/agents/skills"
)

AGENT_ARG=""
SCOPE="project"
PROJECT_DIR="${PWD}"
MODE="copy"
ACTION="install"
FORCE=0
DRY_RUN=0
SRC_DIR=""
TMP_DIR=""

tilde()  { case "$1" in "${HOME}"*) printf '~%s' "${1#"${HOME}"}" ;; *) printf '%s' "$1" ;; esac; }
c_ok()   { printf '\033[32m✔\033[0m %s\n' "$*"; }
c_info() { printf '\033[36m•\033[0m %s\n' "$*"; }
c_warn() { printf '\033[33m!\033[0m %s\n' "$*" >&2; }
die()    { printf '\033[31m✘\033[0m %s\n' "$*" >&2; exit 1; }

has_tty() { { : </dev/tty; } 2>/dev/null; }
cleanup() { if [ -n "${TMP_DIR}" ]; then rm -rf "${TMP_DIR}"; fi; }
trap cleanup EXIT

usage() {
  cat <<EOF
Instalátor skillu ${SKILL_NAME}

Volby:
  -a, --agent LIST     agenti oddělení čárkou nebo "all" (viz --list)
  -g, --global         instalovat globálně (pro všechny projekty)
  -p, --project DIR    instalovat do projektu DIR (výchozí: aktuální adresář)
      --symlink        místo kopie vytvořit symlink (jen při běhu z klonu repozitáře)
      --source DIR     cesta ke složce skillu (výchozí: skills/${SKILL_NAME} vedle skriptu, jinak stáhne z GitHubu)
  -f, --force          přepsat existující instalaci bez dotazu
  -u, --uninstall      odinstalovat
      --zip [SOUBOR]   vytvořit ZIP pro nahrání do aplikace Claude (web/desktop)
      --list           vypsat podporované agenty a cesty
  -n, --dry-run        jen vypsat, co by se stalo
  -h, --help           tato nápověda

Příklady:
  ./install.sh --agent cursor
  ./install.sh --agent claude-code,codex --global
  ./install.sh --zip
EOF
}

list_agents() {
  printf '%-16s %-26s %-22s %s\n' "AGENT" "NÁZEV" "PROJEKT" "GLOBÁLNĚ"
  for row in "${AGENTS[@]}"; do
    IFS='|' read -r id name proj glob <<<"${row}"
    printf '%-16s %-26s %-22s %s\n' "${id}" "${name}" "${proj}/" "$(tilde "${glob}")/"
  done
}

agent_row() {
  local want="$1" row id
  for row in "${AGENTS[@]}"; do
    id="${row%%|*}"
    [ "${id}" = "${want}" ] && { echo "${row}"; return 0; }
  done
  return 1
}

resolve_source() {
  if [ -n "${SRC_DIR}" ]; then
    [ -f "${SRC_DIR}/SKILL.md" ] || die "Ve složce ${SRC_DIR} chybí SKILL.md"
    return
  fi
  local here=""
  if [ -n "${BASH_SOURCE[0]:-}" ] && [ -f "${BASH_SOURCE[0]}" ]; then
    here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  fi
  if [ -n "${here}" ] && [ -f "${here}/skills/${SKILL_NAME}/SKILL.md" ]; then
    SRC_DIR="${here}/skills/${SKILL_NAME}"
    return
  fi
  [ "${MODE}" = "symlink" ] && die "--symlink funguje jen při spuštění z klonu repozitáře."
  command -v curl >/dev/null 2>&1 || die "Chybí curl."
  command -v tar  >/dev/null 2>&1 || die "Chybí tar."
  TMP_DIR="$(mktemp -d)"
  c_info "Stahuji ${REPO}@${BRANCH}..."
  curl -fsSL "https://codeload.github.com/${REPO}/tar.gz/refs/heads/${BRANCH}" | tar -xz -C "${TMP_DIR}" \
    || die "Stažení se nezdařilo."
  SRC_DIR="$(find "${TMP_DIR}" -type d -path "*/skills/${SKILL_NAME}" | head -n1)"
  [ -n "${SRC_DIR}" ] && [ -f "${SRC_DIR}/SKILL.md" ] || die "Ve staženém archivu chybí skills/${SKILL_NAME}/SKILL.md"
}

skill_version() {
  sed -n 's/^[[:space:]]*version:[[:space:]]*"\{0,1\}\([^"]*\)"\{0,1\}[[:space:]]*$/\1/p' "${SRC_DIR}/SKILL.md" | head -n1
}

run() {
  if [ "${DRY_RUN}" -eq 1 ]; then printf '  [dry-run] %s\n' "$*"; else "$@"; fi
}

copy_skill() {
  local dest="$1"
  run mkdir -p "${dest}"
  if command -v rsync >/dev/null 2>&1; then
    run rsync -a --exclude '__pycache__' --exclude '*.pyc' --exclude '.DS_Store' "${SRC_DIR}/" "${dest}/"
  else
    run cp -R "${SRC_DIR}/." "${dest}/"
    [ "${DRY_RUN}" -eq 1 ] || find "${dest}" -name '__pycache__' -type d -prune -exec rm -rf {} + 2>/dev/null || true
  fi
}

confirm() {
  local prompt="$1" ans
  [ "${FORCE}" -eq 1 ] && return 0
  if [ -t 0 ]; then read -r -p "${prompt} [a/N] " ans
  elif has_tty; then read -r -p "${prompt} [a/N] " ans </dev/tty || ans=""
  else c_warn "Neinteraktivní režim – pro přepsání použij --force."; return 1; fi
  [[ "${ans}" =~ ^[aAyY]$ ]]
}

install_to() {
  local base="$1" label="$2" dest="$1/${SKILL_NAME}"
  if [ -e "${dest}" ] || [ -L "${dest}" ]; then
    if ! confirm "${dest} už existuje. Přepsat?"; then
      c_warn "Přeskakuji ${label} (${dest})"; return 0
    fi
    run rm -rf "${dest}"
  fi
  run mkdir -p "${base}"
  if [ "${MODE}" = "symlink" ]; then
    run ln -s "${SRC_DIR}" "${dest}"
  else
    copy_skill "${dest}"
  fi
  c_ok "${label} → $(tilde "${dest}")"
}

uninstall_from() {
  local base="$1" label="$2" dest="$1/${SKILL_NAME}"
  if [ -e "${dest}" ] || [ -L "${dest}" ]; then
    run rm -rf "${dest}"
    c_ok "Odinstalováno: ${label} ($(tilde "${dest}"))"
  else
    c_info "${label}: nenainstalováno ($(tilde "${dest}"))"
  fi
}

make_zip() {
  local out="${1:-${PWD}/${SKILL_NAME}.zip}"
  command -v zip >/dev/null 2>&1 || die "Chybí příkaz zip."
  case "${out}" in /*) ;; *) out="${PWD}/${out}" ;; esac
  local parent; parent="$(dirname "${SRC_DIR}")"
  local stage="${SRC_DIR}"
  if [ "$(basename "${SRC_DIR}")" != "${SKILL_NAME}" ]; then
    stage="$(mktemp -d)/${SKILL_NAME}"; cp -R "${SRC_DIR}" "${stage}"; parent="$(dirname "${stage}")"
  fi
  rm -f "${out}"
  (cd "${parent}" && run zip -qr "${out}" "${SKILL_NAME}" -x '*/__pycache__/*' '*.pyc' '*/.DS_Store')
  c_ok "ZIP vytvořen: ${out}"
  echo "   Nahraj ho v aplikaci Claude: Nastavení → Capabilities → Skills → Upload skill."
}

interactive_pick() {
  echo "Kam chceš skill ${SKILL_NAME} nainstalovat?"
  local i=1 row id name
  for row in "${AGENTS[@]}"; do
    IFS='|' read -r id name _ _ <<<"${row}"
    printf '  %2d) %s\n' "${i}" "${name}"; i=$((i + 1))
  done
  printf '  %2d) Všichni výše\n' "${i}"
  printf '  %2d) ZIP pro aplikaci Claude (web/desktop)\n' "$((i + 1))"
  local ans
  read -r -p "Čísla oddělená čárkou: " ans </dev/tty
  local picked=() n
  ans="${ans// /}"
  [ -n "${ans}" ] || die "Nic nevybráno."
  IFS=',' read -ra nums <<<"${ans}"
  for n in "${nums[@]}"; do
    [[ "${n}" =~ ^[0-9]+$ ]] || die "Neplatná volba: ${n}"
    if [ "${n}" -eq "${i}" ]; then AGENT_ARG="all"; break
    elif [ "${n}" -eq $((i + 1)) ]; then ACTION="zip"; return
    elif [ "${n}" -ge 1 ] && [ "${n}" -lt "${i}" ]; then
      row="${AGENTS[$((n - 1))]}"; picked+=("${row%%|*}")
    else die "Neplatná volba: ${n}"; fi
  done
  [ -z "${AGENT_ARG}" ] && AGENT_ARG="$(IFS=,; echo "${picked[*]}")"
  read -r -p "Instalovat globálně pro všechny projekty? [a/N] " ans </dev/tty
  [[ "${ans}" =~ ^[aAyY]$ ]] && SCOPE="global"
  return 0
}

ZIP_OUT=""
while [ $# -gt 0 ]; do
  case "$1" in
    -a|--agent)    AGENT_ARG="${2:-}"; shift 2 ;;
    --agent=*)     AGENT_ARG="${1#*=}"; shift ;;
    -g|--global)   SCOPE="global"; shift ;;
    -p|--project)  SCOPE="project"; PROJECT_DIR="${2:-}"; shift 2 ;;
    --symlink)     MODE="symlink"; shift ;;
    --source)      SRC_DIR="${2:-}"; shift 2 ;;
    -f|--force)    FORCE=1; shift ;;
    -u|--uninstall) ACTION="uninstall"; shift ;;
    --zip)         ACTION="zip"; if [ -n "${2:-}" ] && [ "${2#-}" = "$2" ]; then ZIP_OUT="$2"; shift; fi; shift ;;
    --list)        list_agents; exit 0 ;;
    -n|--dry-run)  DRY_RUN=1; shift ;;
    -h|--help)     usage; exit 0 ;;
    *) die "Neznámá volba: $1 (viz --help)" ;;
  esac
done

if [ -z "${AGENT_ARG}" ] && [ "${ACTION}" != "zip" ]; then
  if [ -t 0 ] || has_tty; then interactive_pick; else usage; exit 1; fi
fi

if [ "${ACTION}" != "uninstall" ]; then
  resolve_source
  c_info "Skill: ${SKILL_NAME} ${SKILL_VER:-$(skill_version)} ze složky $(tilde "${SRC_DIR}")"
fi

if [ "${ACTION}" = "zip" ]; then make_zip "${ZIP_OUT}"; exit 0; fi

if [ "${SCOPE}" = "project" ]; then
  [ -d "${PROJECT_DIR}" ] || die "Projektová složka neexistuje: ${PROJECT_DIR}"
  PROJECT_DIR="$(cd "${PROJECT_DIR}" && pwd)"
  c_info "Projekt: $(tilde "${PROJECT_DIR}")"
else
  c_info "Režim: globální instalace"
fi

[ -n "${AGENT_ARG//[ ,]/}" ] || die "Nezadán žádný agent (viz --list)."
if [ "${AGENT_ARG}" = "all" ]; then
  ids=(); for row in "${AGENTS[@]}"; do ids+=("${row%%|*}"); done
else
  IFS=',' read -ra ids <<<"${AGENT_ARG// /}"
fi

done_paths="|"
for id in "${ids[@]}"; do
  row="$(agent_row "${id}")" || die "Neznámý agent: ${id} (seznam: ./install.sh --list)"
  IFS='|' read -r _ name proj glob <<<"${row}"
  if [ "${SCOPE}" = "global" ]; then base="${glob}"; else base="${PROJECT_DIR}/${proj}"; fi
  case "${done_paths}" in *"|${base}|"*) c_info "${name} sdílí $(tilde "${base}") – už zpracováno"; continue ;; esac
  done_paths="${done_paths}${base}|"
  if [ "${ACTION}" = "uninstall" ]; then uninstall_from "${base}" "${name}"; else install_to "${base}" "${name}"; fi
done

if [ "${ACTION}" = "install" ] && [ "${DRY_RUN}" -eq 0 ]; then
  echo
  echo "Hotovo. Restartuj editor/agenta a požádej ho třeba: \"Proveď právní audit tohoto webu.\""
fi
