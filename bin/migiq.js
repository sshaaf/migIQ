#!/usr/bin/env node

const { installMigIQ } = require('../install.js');
const path = require('path');
const fs = require('fs');

// Parse arguments
const args = process.argv.slice(2);
const isGlobal = args.includes('-g') || args.includes('--global');
const showHelp = args.includes('-h') || args.includes('--help');
const showVersion = args.includes('-v') || args.includes('--version');

// Package info
const packageJson = require('../package.json');

if (showVersion) {
  console.log(`MigIQ v${packageJson.version}`);
  process.exit(0);
}

if (showHelp) {
  console.log(`
╔══════════════════════════════════════════════════════════════════════╗
║                        MigIQ Installer v${packageJson.version}                       ║
╚══════════════════════════════════════════════════════════════════════╝

AI-powered application migration orchestrator for Claude Code

USAGE:
  npx @sshaaf/migiq [options]

OPTIONS:
  -g, --global    Install to global ~/.claude and ~/.cursor directories
                  (default: install to local .claude and .cursor)

  -h, --help      Show this help message
  -v, --version   Show version number

EXAMPLES:
  # Install to local project (.claude and .cursor)
  npx @sshaaf/migiq

  # Install globally (~/.claude and ~/.cursor)
  npx @sshaaf/migiq -g

WHAT GETS INSTALLED:
  • Migrator Agent (autonomous mode)
  • /migiq skill (interactive mode)
  • 7 core migration skills:
    - rgctl (code knowledge graph, via rgctl install --skill)
    - mig-prompt-builder (requirements)
    - mig-plan (planning)
    - mig-execute (execution)
    - mig-test-gen (testing)
    - mig-containerize (containers)
    - mig-deploy (deployment)

PREREQUISITES:
  • rgctl CLI — https://github.com/sshaaf/rgctl/releases
  • Cursor or Claude Code with skills
  • Node.js 14+

  Install fails if rgctl is not on PATH.

AFTER INSTALLATION:
  Restart Cursor, then use:
    /migiq                  - Interactive migration (lowercase)

DOCUMENTATION:
  https://github.com/sshaaf/migIQ

  `);
  process.exit(0);
}

// Run installer
(async () => {
  try {
    await installMigIQ(isGlobal);
  } catch (error) {
    console.error('\n❌ Installation failed:', error.message);
    process.exit(1);
  }
})();
