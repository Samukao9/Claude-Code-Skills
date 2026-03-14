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
