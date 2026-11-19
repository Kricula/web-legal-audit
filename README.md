# Web Legal Audit CZ

[![CI](https://github.com/Kricula/web-legal-audit/actions/workflows/ci.yml/badge.svg)](https://github.com/Kricula/web-legal-audit/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/Kricula/web-legal-audit)](https://github.com/Kricula/web-legal-audit/releases/latest)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**An Agent Skill for technical and legal audits of Czech websites under Czech and EU law.**

Web Legal Audit CZ helps you systematically review a website, identify the third-party services it uses, check selected legal and technical areas and prepare concrete remediation proposals. The skill works in Czech: its reports, findings and generated documents are written in Czech and reflect the Czech legal environment as well as relevant European Union law.

> **Note:** The skill provides an indicative technical and legal analysis. It does not replace the services of a lawyer, an individual legal assessment or a professional security audit. Results depend on the available materials, access to the website and how current the verified sources are.

## What the skill checks

| Area | Focus |
|---|---|
| Operator identification | Mandatory information about the business and the website operator |
| Cookies and tracking | Cookie banner, consents, analytics and marketing technologies, Google Consent Mode |
| GDPR | Personal data, purposes and legal bases of processing, information obligations, recipients and retention periods |
| Newsletters | Commercial communications, consents, the existing-customer exemption and unsubscribing |
| E-shops and consumer contracts | Pre-contractual information, the order process, terms and conditions, withdrawal from contract |
| Accessibility | Relevant accessibility requirements for websites and digital services |
| AI Act | Obligations depending on the entity's role and the specific use of AI |
| DSA and other areas | Obligations depending on the type of service, user-generated content and related security issues |

The audit adapts to the type of website. A presentation website, an e-shop, a booking system, a SaaS application and a website with user-generated content do not automatically have the same obligations.

## Key features

- **Source code analysis** – static inventory of known third-party services and technologies.
- **Live website check** – when a browser is available, checks cookies, network requests, cookie banner behaviour and selected parts of the website.
- **Modular legal review** – loads only the areas relevant to the specific website.
- **Primary sources first** – legislation and official guidance from the competent authorities take precedence.
- **Finding classification** – distinguishes proven non-compliance, likely non-compliance, unverifiable state, recommendations and future obligations.
- **Concrete fixes** – recommendations tied to a specific file, place on the website or observed behaviour.
- **Working templates** – templates and drafts for cookie information, privacy policies, forms and other documents.

## Project structure

```
.claude-plugin/         # Claude Code marketplace and plugin manifest
.agents/plugins/        # marketplace for Codex and other agents
.github/workflows/      # CI and automated releases (GitHub Release with a ZIP)
install.sh              # installer for macOS / Linux / WSL
install.ps1             # installer for Windows PowerShell
tools/set_version.py    # set and check the version in one place
tests/                  # repository tests (versions, manifests, installer)
skills/web-legal-audit-cz/
├── SKILL.md            # main instructions and workflow (Agent Skills format)
├── references/         # legal modules A–H, methodology, sources, live website check
├── assets/             # templates: cookie banner, privacy policy, footer, forms, T&C, report…
├── scripts/
│   └── detect_services.py   # static inventory of third-party services
├── tests/              # automated tests (unittest)
├── CHANGELOG.md
├── LICENSE
└── README.md
```

The skill follows the [Agent Skills](https://agentskills.io/specification) specification and passes the `skills-ref` reference validator.

## Installation

The skill is meant for AI agents and editors that support the **Agent Skills** format. After installation, the whole `web-legal-audit-cz` directory must be available, including `SKILL.md`, references, scripts and templates. Pick one option:

| Option | When to use it |
|---|---|
| [Claude Code plugin](#claude-code--plugin-marketplace) | you use Claude Code and want automatic updates via `/plugin` |
| [Codex plugin](#codex--plugin-marketplace) | you use Codex and want the skill in the plugin directory |
| [Install script](#install-script-macos-linux-windows) | one command for Claude Code, Cursor, Codex, Copilot, Windsurf and more, no Node.js needed |
| [skills.sh CLI](#skillssh-cli) | you have Node.js and want updates via `npx skills update` |
| [Claude app](#claude-web-and-desktop-app) | Claude on the web or in the desktop app – just download the ZIP |
| [Manual](#manual-installation) | a custom path or an agent the script does not know |

### Supported editors and agents

| Editor / agent | `--agent` | Project | Global |
|---|---|---|---|
| Claude Code | `claude-code` | `.claude/skills/` | `~/.claude/skills/` |
| Cursor | `cursor` | `.agents/skills/` | `~/.cursor/skills/` |
| OpenAI Codex | `codex` | `.agents/skills/` | `~/.agents/skills/` |
| GitHub Copilot | `github-copilot` | `.agents/skills/` | `~/.copilot/skills/` |
| Gemini CLI | `gemini-cli` | `.agents/skills/` | `~/.gemini/skills/` |
| Windsurf | `windsurf` | `.windsurf/skills/` | `~/.codeium/windsurf/skills/` |
| OpenCode | `opencode` | `.agents/skills/` | `~/.config/opencode/skills/` |
| Cline | `cline` | `.agents/skills/` | `~/.agents/skills/` |
| Roo Code | `roo` | `.roo/skills/` | `~/.roo/skills/` |
| Kiro CLI | `kiro-cli` | `.kiro/skills/` | `~/.kiro/skills/` |
| JetBrains Junie | `junie` | `.junie/skills/` | `~/.junie/skills/` |
| Amp and others | `universal` | `.agents/skills/` | `~/.config/agents/skills/` |

The paths follow the [skills.sh](https://github.com/vercel-labs/skills/blob/main/docs/agents.md) reference table. A "project" install applies only to that repository; a "global" install applies to all of the user's projects.

### Claude Code – plugin marketplace

This repository is also a Claude Code marketplace. In Claude Code, run:

```
/plugin marketplace add Kricula/web-legal-audit
/plugin install web-legal-audit-cz@web-legal-audit
```

In Claude Code 2.1.275 or later, a single command is enough:

```
/plugin install web-legal-audit-cz --marketplace Kricula/web-legal-audit
```

The same from a terminal: `claude plugin marketplace add Kricula/web-legal-audit` and `claude plugin install web-legal-audit-cz@web-legal-audit`. Claude Code then handles updates itself (`/plugin` → Marketplaces → Update), no scripts needed. Inside the plugin, the skill is named `web-legal-audit-cz:web-legal-audit-cz`.

### Codex – plugin marketplace

Codex loads the marketplace from `.agents/plugins/marketplace.json` when you work inside this repository, or you can add it with:

```bash
codex plugin marketplace add Kricula/web-legal-audit
```

Then open `/plugins` in Codex and install **Web Legal Audit CZ**. To install straight into the skills folder, use the [install script](#install-script-macos-linux-windows) with `--agent codex`.

### Install script (macOS, Linux, Windows)

**macOS / Linux / WSL** – without cloning:

```bash
# interactive editor picker
curl -fsSL https://raw.githubusercontent.com/Kricula/web-legal-audit/main/install.sh | bash

# Cursor, into the current project
curl -fsSL https://raw.githubusercontent.com/Kricula/web-legal-audit/main/install.sh | bash -s -- --agent cursor

# Claude Code and Codex, globally
curl -fsSL https://raw.githubusercontent.com/Kricula/web-legal-audit/main/install.sh | bash -s -- --agent claude-code,codex --global
```

A specific version (recommended, especially with `curl | bash` – installs exactly the released tag, not the current `main`):

```bash
curl -fsSL https://raw.githubusercontent.com/Kricula/web-legal-audit/v2.2.0/install.sh | bash -s -- --agent cursor --ref v2.2.0
```

From a clone of the repository:

```bash
git clone https://github.com/Kricula/web-legal-audit.git
cd web-legal-audit
./install.sh --agent cursor --project ~/projects/my-site   # into a specific project
./install.sh --agent all --global                         # everywhere
./install.sh --agent claude-code --global --symlink       # symlink – changes in the clone apply immediately
```

**Windows (PowerShell)** – without cloning:

```powershell
& ([scriptblock]::Create((irm https://raw.githubusercontent.com/Kricula/web-legal-audit/main/install.ps1))) -Agent cursor
& ([scriptblock]::Create((irm https://raw.githubusercontent.com/Kricula/web-legal-audit/main/install.ps1))) -Agent claude-code,codex -Global
& ([scriptblock]::Create((irm https://raw.githubusercontent.com/Kricula/web-legal-audit/v2.2.0/install.ps1))) -Agent cursor -Ref v2.2.0
```

From a clone: `.\install.ps1 -Agent cursor` (or `powershell -ExecutionPolicy Bypass -File .\install.ps1 -Agent cursor`).

**Script options**

| `install.sh` | `install.ps1` | Meaning |
|---|---|---|
| `--agent LIST` | `-Agent LIST` | comma-separated editors or `all`; without it, an interactive picker is shown |
| `--global` | `-Global` | install for all projects |
| `--project DIR` | `-Project DIR` | target project (default: current directory) |
| `--ref REF` | `-Ref REF` | download a specific version from GitHub – a tag (`v2.2.0`), branch or commit; default `main` |
| `--symlink` | – | symlink instead of a copy (only from a clone, without `--ref`) |
| `--force` | `-Force` | overwrite an existing installation without asking |
| `--uninstall` | `-Uninstall` | uninstall |
| `--zip [FILE]` | `-Zip [-ZipPath FILE]` | build a ZIP for the Claude app (without tests, README and CHANGELOG) |
| `--list` | `-List` | list editors and paths |
| `--dry-run` | `-DryRun` | only show what would happen |

Running the script again updates the installation (after confirmation or with `--force`). Editors that share the same folder (e.g. Cursor and Codex in `.agents/skills/`) are installed only once.

> The installer's messages are in Czech.

### skills.sh CLI

Requires Node.js 22.20 or later:

```bash
npx skills add Kricula/web-legal-audit                                        # interactive agent picker
npx skills add Kricula/web-legal-audit --skill web-legal-audit-cz -a cursor   # a specific agent
npx skills add Kricula/web-legal-audit -g                                     # globally
npx skills update                                                             # update
```

### Claude (web and desktop app)

1. Download **[web-legal-audit-cz.zip](https://github.com/Kricula/web-legal-audit/releases/latest/download/web-legal-audit-cz.zip)** from the latest release (no terminal needed).
   You can also build the ZIP yourself: `./install.sh --zip` (Windows: `.\install.ps1 -Zip`).
2. In Claude, open **Settings → Capabilities → Skills** and upload `web-legal-audit-cz.zip`.
3. If you already have an older version with the same name, remove it first.

### Manual installation

Copy the `skills/web-legal-audit-cz` directory into your editor's skills folder according to the table above, for example:

```bash
git clone https://github.com/Kricula/web-legal-audit.git
cp -r web-legal-audit/skills/web-legal-audit-cz ~/.claude/skills/
```

Restart the editor or agent after installation.

### Verifying the installation

```bash
cd skills/web-legal-audit-cz            # or the directory where the skill was installed
python3 -m unittest discover -s tests -v
```

## Usage

Activate the skill with a request such as (the skill expects Czech; English translations in brackets):

- „Proveď právní audit tohoto webu.“ *(Run a legal audit of this website.)*
- „Zkontroluj cookie lištu a načítání analytických skriptů.“ *(Check the cookie banner and how analytics scripts load.)*
- „Prověř GDPR a formuláře na tomto webu.“ *(Review GDPR compliance and the forms on this website.)*
- „Zkontroluj obchodní podmínky a objednávkový proces e-shopu.“ *(Check the e-shop's terms and conditions and order process.)*
- „Prověř, jaké služby třetích stran používá tento repozitář.“ *(Find out which third-party services this repository uses.)*

For a partial check, name the area explicitly, for example „zkontroluj pouze cookies“ *(check cookies only)*.

### Requirements

- Python **3.8 or later** for the detection script and the automated tests.
- Access to the website's source code for the static inventory.
- For the live website check, a browser that can inspect network requests, cookies and storage.
- Access to primary legal sources to verify current legislation.

### Static service inventory

From the skill directory (`skills/web-legal-audit-cz/`), run:

```bash
python3 scripts/detect_services.py /path/to/website --format md > inventory.md
```

JSON output:

```bash
python3 scripts/detect_services.py /path/to/website --format json > inventory.json
```

The script scans selected text source files for known service patterns. It deliberately skips files with sensitive configuration, such as `.env*`, keys, certificates, databases and dependency directories.

**Important limitation:** A static occurrence in the code does not prove that the service actually loads in the browser, that it sets cookies or that the website breaks the law. Findings must be verified in the context of the code and, where possible, with a runtime check.

### Running the tests

From the skill directory (`skills/web-legal-audit-cz/`):

```bash
python3 -m unittest discover -s tests -v
```

Run the repository tests (version sync, plugin manifests, installer) from the repository root:

```bash
python3 -m unittest discover -s tests -v
python3 tools/set_version.py --check
```

The tests use only the Python standard library and need no extra packages. [CI](.github/workflows/ci.yml) runs the same checks on every push, plus skill validation (`skills-ref`), plugin validation (`claude plugin validate`), ShellCheck and a dry run of both installers.

## How the skill evaluates findings

Each finding is first assigned to one of these categories (the labels appear in Czech in the reports):

- **PROKÁZANÝ NESOULAD** *(proven non-compliance)* – the available evidence confirms a conflict with a specific obligation.
- **PRAVDĚPODOBNÝ NESOULAD** *(likely non-compliance)* – the facts found point to a problem, but part of the evidence is missing.
- **NELZE OVĚŘIT** *(cannot be verified)* – the available materials are not enough to reach a conclusion.
- **DOPORUČENÍ** *(recommendation)* – an improvement beyond a proven legal obligation.
- **BUDOUCÍ POVINNOST** *(future obligation)* – a requirement that will apply from a future date or under set conditions.

Severity is then assigned according to the methodology in `references/pravni-metodika.md`.

Every legal conclusion should rest on a specific provision and, where possible, a primary source. The skill must distinguish a statutory obligation, an official interpretation by an authority and recommended practice. If factual information is missing, it must not assume it.

## Security and data protection

- Preferably run the analysis on a copy of the repository or source files.
- Do not put passwords, API keys, access tokens, private keys or production configuration files into the inputs or reports.
- Before sharing the output, check that it contains no personal data, trade secrets or other sensitive information.
- The detection script is meant for local static analysis; it does not modify the scanned files or make network requests.
- Never submit forms, orders or other production transactions without explicit instruction.
- Do not treat the script's output as proof that the website is secure or legally compliant.

## Legal notice and disclaimer

**This skill was not created, reviewed or approved by an attorney or any other lawyer. Its content is neither a legal opinion nor a legal service.**

The skill draws only on available legislation, publicly available guidance, interpretive materials and the other sources it lists. The accuracy and completeness of its output therefore depend on the availability, currency and correct interpretation of those sources. Citing a statute or an official methodology does not by itself guarantee that a legal conclusion is complete or correct for a particular situation.

The outputs serve only as an indicative technical and legal aid. They are not legal advice, do not create an attorney–client relationship and do not guarantee that a website complies with the law. Neither the author nor the project warrants the correctness, completeness or currency of the outputs, and they accept no liability for decisions made solely on their basis.

Laws, their interpretation and official guidance change. Each audit must therefore verify the current wording of the relevant legislation, its effective dates and its applicability to the specific case. Borderline cases, exemptions, regulated services and processing of sensitive data need particular attention. Before making legally significant decisions or publishing legal documents, we recommend an independent review by a qualified lawyer.

## Versions and changes

Current version: **2.2.0**

See [`CHANGELOG.md`](skills/web-legal-audit-cz/CHANGELOG.md) (in Czech) for details of the changes, and [Releases](https://github.com/Kricula/web-legal-audit/releases) for ready-made packages.

### Releasing a new version

```bash
python3 tools/set_version.py 2.3.0     # updates the version in SKILL.md, plugin.json, marketplace.json and README
# add a "## 2.3.0 – date" entry to skills/web-legal-audit-cz/CHANGELOG.md
git commit -am "Release 2.3.0" && git tag v2.3.0 && git push --follow-tags
```

After the tag is pushed, the [Release](.github/workflows/release.yml) workflow checks that the tag matches the version, runs the tests, builds `web-legal-audit-cz.zip` and creates a GitHub Release with notes from the CHANGELOG.

## License

The project is distributed under the MIT license. See [`LICENSE`](LICENSE) for details.

---

**Skill language:** Czech  
**Legal environment:** Czech Republic and European Union
