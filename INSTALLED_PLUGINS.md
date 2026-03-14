# Installed Claude Code Plugins

## claude-mem (thedotmack)

- **Source:** https://github.com/thedotmack/claude-mem.git
- **Version:** 10.5.5
- **Location:** `~/.claude/plugins/marketplaces/thedotmack/`
- **Description:** Persistent memory system for Claude Code. Automatically captures and compresses coding session context, then injects relevant information into future sessions.

### Features

- **Lifecycle Hooks:** SessionStart, UserPromptSubmit, PostToolUse, Stop, SessionEnd
- **Skills:** `/mem-search`, `/do`, `/make-plan`, `/smart-explore`
- **Modes:** Multiple language modes + specialized modes (code, law-study, email-investigation)
- **Worker Service:** HTTP API on port 37777 with web UI
- **Storage:** SQLite database + Chroma vector DB for hybrid semantic + keyword search
- **MCP Tools:** search, timeline, get_observations (3-layer workflow)

## n8n-mcp (czlonkowski)

- **Source:** https://github.com/czlonkowski/n8n-mcp.git
- **Version:** 2.37.1
- **Location:** MCP server via `npx n8n-mcp` (configured in `~/.mcp.json`)
- **Description:** MCP server that bridges AI assistants with n8n's workflow automation platform. Provides access to 1,239+ workflow automation nodes documentation, templates, and workflow management.

### Features

- **Node Discovery:** Search and explore 809 core + 430 community n8n nodes
- **Configuration Tools:** Get node details, examples, and task templates
- **Validation Tools:** Validate configurations and workflows before deployment
- **Workflow Management:** Create and update n8n workflows (requires API config)
- **Template Library:** Access 2,709+ workflow templates and real-world examples
- **Modes:** stdio (Claude Desktop/Code) and HTTP server

## obsidian-skills (kepano)

- **Source:** https://github.com/kepano/obsidian-skills.git
- **Location:** `.claude/skills/` (project-level skills)
- **Description:** Collection of agent skills for working with Obsidian note-taking app file formats and tools.

### Skills

- **obsidian-markdown** — Create/edit Obsidian Flavored Markdown with wikilinks, callouts, properties
- **obsidian-bases** — Work with Obsidian Bases (`.base` files) including views and filters
- **json-canvas** — Manage JSON Canvas files (`.canvas`) with nodes and connections
- **obsidian-cli** — CLI interaction for vault operations
- **defuddle** — Extract clean markdown from web pages to reduce token usage

## get-shit-done (gsd-build)

- **Source:** https://github.com/gsd-build/get-shit-done.git
- **Version:** 1.22.4
- **Location:** `~/.claude/` (global install — commands, agents, hooks)
- **Description:** Meta-prompting, context engineering and spec-driven development system for Claude Code. Provides structured project planning, milestone management, and phased execution workflows.

### Commands (`/gsd:*`)

- `new-project`, `new-milestone`, `complete-milestone`
- `plan-phase`, `execute-phase`, `research-phase`, `validate-phase`, `discuss-phase`
- `add-phase`, `insert-phase`, `remove-phase`
- `debug`, `quick`, `progress`, `health`, `cleanup`
- `add-todo`, `check-todos`, `add-tests`, `verify-work`
- `map-codebase`, `pause-work`, `resume-work`, `settings`, `update`

### Agents

- gsd-planner, gsd-executor, gsd-verifier, gsd-debugger
- gsd-phase-researcher, gsd-project-researcher, gsd-research-synthesizer
- gsd-codebase-mapper, gsd-roadmapper, gsd-plan-checker
- gsd-integration-checker, gsd-nyquist-auditor

### Hooks

- Update checker, context window monitor, statusline

## superpowers (obra)

- **Source:** https://github.com/obra/superpowers.git
- **Version:** 5.0.2
- **Location:** `~/.claude/plugins/marketplaces/obra/`
- **Description:** Core skills library for Claude Code with TDD, debugging, collaboration patterns, and proven development techniques.

### Skills

- using-superpowers, subagent-driven-development, dispatching-parallel-agents
- test-driven-development, systematic-debugging, verification-before-completion
- writing-plans, executing-plans, brainstorming
- writing-skills, requesting-code-review, receiving-code-review
- finishing-a-development-branch, using-git-worktrees

### Commands

- `/brainstorm`, `/write-plan`, `/execute-plan`

### Agents

- code-reviewer

### Hooks

- SessionStart (injects superpowers context)

## awesome-claude-code (hesreallyhim)

- **Source:** https://github.com/hesreallyhim/awesome-claude-code.git
- **Location:** `~/.claude/commands/awesome/` (global slash commands)
- **Description:** Curated collection of community slash commands for Claude Code covering commits, PRs, reviews, testing, documentation, and more.

### Commands (`/awesome:*`)

- `act`, `clean`, `commit`, `optimize`, `release`, `todo`
- `create-pr`, `create-pull-request`, `pr-review`, `fix-github-issue`
- `create-prd`, `create-prp`, `create-jtbd`, `create-hook`
- `context-prime`, `initref`, `load-llms-txt`
- `add-to-changelog`, `update-docs`, `update-branch-name`
- `create-worktrees`, `husky`, `testing_plan_integration`

## ui-ux-pro-max-skill (nextlevelbuilder)

- **Source:** https://github.com/nextlevelbuilder/ui-ux-pro-max-skill.git
- **Version:** 2.2.1
- **Location:** `~/.claude/plugins/marketplaces/nextlevelbuilder/` + `.claude/skills/`
- **Description:** Professional UI/UX design intelligence with 67 styles, 96 palettes, 57 font pairings, 25 charts, and 13 stack guidelines for React, Next.js, Vue, Svelte, SwiftUI, React Native, Flutter, Tailwind, shadcn/ui, and more.

### Skills

- **ui-ux-pro-max** — Core design intelligence (styles, palettes, typography, charts)
- **ui-styling** — Tailwind, shadcn/ui theming, canvas fonts, responsive design
- **design** — Logo, icon, CIP design with prompt engineering and generation scripts
- **design-system** — Design tokens, component specs, slide generation
- **brand** — Brand guidelines, visual identity, color management, messaging
- **slides** — Presentation creation with layout patterns and copywriting formulas
- **banner-design** — Banner sizes and styles reference

## notebooklm-py (teng-lin)

- **Source:** https://github.com/teng-lin/notebooklm-py.git
- **Version:** 0.3.4
- **Location:** Python CLI (`notebooklm`) + `.claude/skills/notebooklm/`
- **Description:** Complete programmatic access to Google NotebookLM — create notebooks, add sources, generate podcasts/videos/reports/quizzes, download in multiple formats. Includes features not available in the web UI.

### Capabilities

- **Notebooks:** Create, list, delete, rename
- **Sources:** Add URLs, YouTube, PDFs, audio, video, images, web research
- **Chat:** Ask questions with citations, conversation history, save as notes
- **Generation:** Audio (podcast), video, slide decks, reports, mind maps, quizzes, flashcards, infographics, data tables
- **Downloads:** MP3, MP4, PDF, PPTX, Markdown, JSON, CSV, HTML
- **Languages:** 80+ supported languages for artifact generation
- **Auth:** Google OAuth via `notebooklm login`
