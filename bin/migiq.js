#!/usr/bin/env node

const {
  installMigIQ,
  addExternalSkills,
  listExternalSkills,
  removeExternalSkill
} = require('../install.js');
const path = require('path');
const fs = require('fs');

// Parse arguments
const args = process.argv.slice(2);
const isGlobal = args.includes('-g') || args.includes('--global');
const showHelp = args.includes('-h') || args.includes('--help');
const showVersion = args.includes('-v') || args.includes('--version');

// Extract subcommand (first arg that isn't a flag)
const subcommand = args.find(a => !a.startsWith('-'));
const subcommandArgs = args.filter(a => !a.startsWith('-') && a !== subcommand);

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
  npx @sshaaf/migiq [options]           Install core migration skills
  npx @sshaaf/migiq add <source> [-g]   Add external migration skills
  npx @sshaaf/migiq list [-g]           List installed migration skills
  npx @sshaaf/migiq remove <name> [-g]  Remove a migration skill

SUBCOMMANDS:
  add <source>    Install migration skills from a git repo URL or local path
                  Examples:
                    npx @sshaaf/migiq add https://github.com/user/migration-skills
                    npx @sshaaf/migiq add ./path/to/migration-skills
                    npx @sshaaf/migiq add git@github.com:user/migration-skills.git

  list            List all installed external migration skills

  remove <name>   Remove an installed migration skill by name

OPTIONS:
  -g, --global    Target global ~/.claude directory
                  (default: local .claude directory)

  -h, --help      Show this help message
  -v, --version   Show version number

CORE SKILLS (installed with base command):
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

MIGRATION SKILLS (installed with 'add'):
  External migration skills provide authoritative mapping tables and
  phased instructions for specific migrations (e.g., Spring Boot to
  Quarkus, JBoss EAP 7 to 8). Once installed, the harness automatically
  detects and uses them during planning and execution.

AFTER INSTALLATION:
  In Claude Code, use:
    /migiq                  - Interactive migration

DOCUMENTATION:
  https://github.com/sshaaf/migIQ

  `);
  process.exit(0);
}

// Run the appropriate command
(async () => {
  try {
    switch (subcommand) {
      case 'add': {
        const source = subcommandArgs[0];
        if (!source) {
          console.error('\n❌ Missing source. Usage: npx migiq add <path-or-git-url>\n');
          process.exit(1);
        }
        await addExternalSkills(source, isGlobal);
        break;
      }
      case 'list':
        listExternalSkills(isGlobal);
        break;
      case 'remove': {
        const name = subcommandArgs[0];
        if (!name) {
          console.error('\n❌ Missing skill name. Usage: npx migiq remove <skill-name>\n');
          process.exit(1);
        }
        removeExternalSkill(name, isGlobal);
        break;
      }
      default:
        await installMigIQ(isGlobal);
        break;
    }
  } catch (error) {
    console.error('\n❌ Operation failed:', error.message);
    process.exit(1);
  }
})();
