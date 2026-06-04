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
  -g, --global    Install to global ~/.claude directory
                  (default: install to local .claude directory)

  -h, --help      Show this help message
  -v, --version   Show version number

EXAMPLES:
  # Install to local project .claude directory
  npx @sshaaf/migiq

  # Install to global ~/.claude directory
  npx @sshaaf/migiq -g

WHAT GETS INSTALLED:
  • Migrator Agent (autonomous mode)
  • /migiq skill (interactive mode)
  • 7 core migration skills:
    - mig-graphify (code analysis)
    - mig-prompt-builder (requirements)
    - mig-plan (planning)
    - mig-execute (execution)
    - mig-test-gen (testing)
    - mig-containerize (containers)
    - mig-deploy (deployment)

AFTER INSTALLATION:
  In Claude Code, use:
    /migiq                  - Interactive migration
    Agent({ ... })          - Autonomous migration (see AGENT_EXAMPLES.md)

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
