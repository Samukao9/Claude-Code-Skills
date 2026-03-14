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
