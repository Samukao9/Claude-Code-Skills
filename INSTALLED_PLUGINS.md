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
