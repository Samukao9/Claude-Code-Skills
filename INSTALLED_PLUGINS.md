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

## skills (anthropics) — Official Anthropic Skills

- **Source:** https://github.com/anthropics/skills.git
- **Location:** `.claude/skills/` (project-level skills)
- **Description:** Official collection of Claude Code skills by Anthropic covering document generation, design, development, and productivity.

### Skills

- **pdf** — Generate and manipulate PDF documents with forms support
- **docx** — Create and edit Word documents
- **xlsx** — Create and edit Excel spreadsheets
- **pptx** — Create and edit PowerPoint presentations
- **claude-api** — Build apps with Claude API (Python, TypeScript, Go, Java, PHP, Ruby, C#, curl)
- **mcp-builder** — Build MCP servers with reference docs and scripts
- **skill-creator** — Create new skills with agents, eval viewer, and templates
- **web-artifacts-builder** — Build interactive web artifacts
- **webapp-testing** — Test web applications with examples and scripts
- **frontend-design** — Frontend UI/UX design patterns
- **canvas-design** — Canvas-based design with bundled fonts
- **brand-guidelines** — Create and apply brand guidelines
- **theme-factory** — Generate themes with showcase PDF and templates
- **algorithmic-art** — Create algorithmic art with templates
- **doc-coauthoring** — Collaborative document co-authoring
- **internal-comms** — Internal communications with examples
- **slack-gif-creator** — Create Slack GIFs with Python

## context7 (upstash)

- **Source:** https://github.com/upstash/context7.git
- **Version:** CLI 0.3.5 / MCP 2.0.2
- **Location:** CLI (`ctx7`), MCP server (`~/.mcp.json`), skills (`.claude/skills/`), command (`.claude/commands/docs.md`), agent (`.claude/agents/docs-researcher.md`)
- **Description:** Up-to-date documentation lookup for any library/framework. Fetches current docs, API references, and code examples instead of relying on training data.

### Components

- **CLI `ctx7`** — `ctx7 library <name> <query>` + `ctx7 docs <libraryId> <query>`
- **MCP Server** — `resolve-library-id` and `query-docs` tools via `@upstash/context7-mcp`
- **Skills:** `find-docs` (CLI-based), `context7-mcp` (MCP-based), `context7-cli` (setup/reference)
- **Command:** `/docs` — quick documentation lookup
- **Agent:** `docs-researcher` — deep documentation research

## ralph (snarktank)

- **Source:** https://github.com/snarktank/ralph.git
- **Version:** 1.0.0
- **Location:** `~/.claude/plugins/marketplaces/snarktank/` + `.claude/skills/`
- **Description:** Autonomous agent system for spec-driven development. Generates PRDs and converts them to prd.json format for autonomous execution.

### Skills

- **prd** — Generate Product Requirements Documents from feature descriptions (triggers on `/prd`)
- **ralph** — Convert existing PRDs to prd.json format for Ralph's autonomous loop (triggers on `/ralph`)

## ruflo / claude-flow (ruvnet)

- **Source:** https://github.com/ruvnet/ruflo.git
- **Version:** 2.5.0
- **Location:** `~/.claude/plugins/marketplaces/ruvnet/` + MCP server (`~/.mcp.json`)
- **Description:** Enterprise AI agent orchestration with 150+ commands, 74+ agents, SPARC methodology, swarm coordination, GitHub automation, and neural training.

### Components

- **38 skills** — swarm orchestration, GitHub automation, SPARC methodology, pair programming, performance analysis, hive-mind, neural training, and more
- **23 command categories** — agents, analysis, automation, coordination, GitHub, memory, monitoring, optimization, SPARC, swarm, training, verification, workflows
- **21 agent categories** — architecture, core, data, development, DevOps, documentation, GitHub, neural, optimization, reasoning, SPARC, swarm, testing
- **MCP Server** — `claude-flow` for swarm coordination (40+ tools)
- **Hooks** — SessionStart integration
