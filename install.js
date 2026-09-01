#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const os = require('os');
const { execSync } = require('child_process');

/**
 * Check if a CLI command is on PATH
 */
function commandExists(cmd) {
  try {
    const check = process.platform === 'win32' ? `where ${cmd}` : `which ${cmd}`;
    execSync(check, { stdio: 'ignore' });
    return true;
  } catch {
    return false;
  }
}

const RGCTL_CANDIDATE_PATHS = [
  'rgctl',
  path.join(os.homedir(), '.local', 'bin', 'rgctl'),
  '/opt/homebrew/bin/rgctl',
  '/usr/local/bin/rgctl',
];

/**
 * Resolve rgctl executable (npm postinstall often omits ~/.local/bin from PATH).
 */
function resolveRgctlPath() {
  for (const candidate of RGCTL_CANDIDATE_PATHS) {
    if (candidate === 'rgctl') {
      if (commandExists('rgctl')) {
        return 'rgctl';
      }
      continue;
    }
    if (fs.existsSync(candidate) && fs.statSync(candidate).isFile()) {
      return candidate;
    }
  }
  return null;
}

/**
 * Install rgctl skill via `rgctl install --skill` (see https://github.com/sshaaf/rgctl/docs/installation.md).
 * Throws if rgctl is missing or install --skill fails.
 */
function installRgctlSkill(isGlobal) {
  const rgctl = resolveRgctlPath();
  if (!rgctl) {
    throw new Error(
      'rgctl CLI is required but not found on PATH.\n' +
      'Install from https://github.com/sshaaf/rgctl/releases\n' +
      'Typical location: ~/.local/bin/rgctl\n' +
      'Then re-run: npm install (or node install.js)'
    );
  }

  const cwd = isGlobal ? os.homedir() : process.cwd();

  try {
    execSync(`"${rgctl}" install --skill`, { cwd, stdio: 'pipe', encoding: 'utf8', shell: true });
  } catch (error) {
    const detail = error.stderr?.trim() || error.stdout?.trim() || error.message;
    throw new Error(
      `rgctl install --skill failed.\n` +
      (detail ? `${detail}\n` : '') +
      'Ensure rgctl is working, then re-run: npm install (or node install.js)'
    );
  }

  const skillPaths = [
    path.join(cwd, '.claude', 'skills', 'rgctl', 'SKILL.md'),
    path.join(cwd, '.cursor', 'skills', 'rgctl', 'SKILL.md'),
  ];

  if (!skillPaths.some((p) => fs.existsSync(p))) {
    throw new Error(
      'rgctl install --skill completed but rgctl skill was not found.\n' +
      `Expected one of:\n  ${skillPaths.join('\n  ')}\n` +
      'Re-run: rgctl install --skill'
    );
  }

  console.log('  ✅ rgctl (via rgctl install --skill)');
}

/**
 * Copy directory recursively
 */
function copyDir(src, dest) {
  // Create destination directory
  fs.mkdirSync(dest, { recursive: true });

  // Read source directory
  const entries = fs.readdirSync(src, { withFileTypes: true });

  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);

    if (entry.isDirectory()) {
      copyDir(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

/**
 * Copy file with directory creation
 */
function copyFile(src, dest) {
  const destDir = path.dirname(dest);
  fs.mkdirSync(destDir, { recursive: true });
  fs.copyFileSync(src, dest);
}

/**
 * Installation roots for Claude Code (.claude) and Cursor (.cursor).
 */
function getTargetDirs(isGlobal) {
  const base = isGlobal ? os.homedir() : process.cwd();
  return [
    path.join(base, '.claude'),
    path.join(base, '.cursor'),
  ];
}

/**
 * Main installation function
 */
async function installMigIQ(isGlobal = false) {
  const sourceDir = __dirname;
  const targetDirs = getTargetDirs(isGlobal);
  const scope = isGlobal ? 'global' : 'local';

  console.log(`
╔══════════════════════════════════════════════════════════════════════╗
║                     Installing MigIQ v0.2.0                          ║
╚══════════════════════════════════════════════════════════════════════╝
`);

  console.log(`📦 Installation mode: ${scope.toUpperCase()}`);
  console.log('📂 Target directories:');
  for (const dir of targetDirs) {
    console.log(`   ${dir}`);
  }
  console.log();

  try {
    // rgctl is required — fail before copying anything else
    console.log('📚 Installing skills:');
    installRgctlSkill(isGlobal);

    // Skills to install
    const skills = [
      'mig-rgctl',
      'migiq',
      'mig-plan',
      'mig-prompt-builder',
      'mig-execute',
      'mig-test-gen',
      'mig-containerize',
      'mig-deploy'
    ];

    for (const targetDir of targetDirs) {
      fs.mkdirSync(targetDir, { recursive: true });
      const skillsDir = path.join(targetDir, 'skills');
      fs.mkdirSync(skillsDir, { recursive: true });

      for (const skill of skills) {
        const srcSkillDir = path.join(sourceDir, skill);
        const destSkillDir = path.join(skillsDir, skill);

        if (fs.existsSync(srcSkillDir)) {
          copyDir(srcSkillDir, destSkillDir);
        }
      }
    }

    for (const skill of skills) {
      const srcSkillDir = path.join(sourceDir, skill);
      if (fs.existsSync(srcSkillDir)) {
        console.log(`  ✅ ${skill}`);
      } else {
        console.log(`  ⚠️  ${skill} (not found, skipping)`);
      }
    }

    // Install agent (Claude Code; copied to both roots for consistency)
    console.log('\n🤖 Installing agent:');
    const agentFiles = ['AGENT.md'];
    const envExample = path.join(sourceDir, '.env.example');

    for (const targetDir of targetDirs) {
      const agentsDir = path.join(targetDir, 'agents');
      fs.mkdirSync(agentsDir, { recursive: true });
      const migratorDir = path.join(agentsDir, 'migrator');
      fs.mkdirSync(migratorDir, { recursive: true });

      for (const file of agentFiles) {
        const srcFile = path.join(sourceDir, file);
        if (fs.existsSync(srcFile)) {
          copyFile(srcFile, path.join(migratorDir, file));
        }
      }

      if (fs.existsSync(envExample)) {
        copyFile(envExample, path.join(migratorDir, '.env.example'));
      }
    }

    console.log('  ✅ AGENT.md');
    if (fs.existsSync(envExample)) {
      console.log('  ✅ .env.example');
    }

    // Create a README in each installation directory
    const installReadme = `# MigIQ Installation

This directory contains the MigIQ migration platform for Cursor and Claude Code.

## Installed Components

### Skills (use with /migiq in Cursor or Claude Code)
- **migiq** - Main orchestration skill
- **mig-rgctl** - MigIQ-specific rgctl analysis (phase commands, artifact checks)
- **rgctl** - Upstream code knowledge graph ([rgctl](https://github.com/sshaaf/rgctl) CLI, via \`rgctl install --skill\`)
- **mig-prompt-builder** - Migration requirements builder
- **mig-plan** - Migration planning
- **mig-execute** - Migration execution
- **mig-test-gen** - Test generation
- **mig-containerize** - Container creation
- **mig-deploy** - OpenShift deployment

### Agent (use with Agent tool in Claude Code)
- **migrator** - Autonomous migration agent

### Prerequisites
- **rgctl** CLI from [rgctl](https://github.com/sshaaf/rgctl) (required at install; runs \`rgctl install --skill\`)
- **Cursor** or **Claude Code** with skills
- **Node.js** 14+

## Usage

### Interactive Mode
In Cursor or Claude Code (restart the IDE after install):
\`\`\`
/migiq
"Migrate this Spring Boot app to Quarkus"
\`\`\`

### Autonomous Mode
\`\`\`
Agent({
  description: "Migrate Spring Boot to Quarkus",
  prompt: "Follow AGENT.md. Migrate this Spring Boot application to Quarkus...",
  subagent_type: "general-purpose"
})
\`\`\`

## Documentation
- Main README: https://github.com/sshaaf/migIQ
- Skill Docs: skills/migiq/SKILL.md

## Version
MigIQ v0.2.0

Installation type: ${scope}
Installed on: ${new Date().toISOString()}
`;

    for (const targetDir of targetDirs) {
      fs.writeFileSync(path.join(targetDir, 'README.migiq.md'), installReadme);
    }

    const skillDirs = targetDirs.map((dir) => path.join(dir, 'skills'));
    const agentDirs = targetDirs.map((dir) => path.join(dir, 'agents', 'migrator'));

    // Success summary
    console.log(`
╔══════════════════════════════════════════════════════════════════════╗
║                   ✨ Installation Complete! ✨                        ║
╚══════════════════════════════════════════════════════════════════════╝

✅ Installed ${skills.length} MigIQ skills to:
${skillDirs.map((dir) => `   ${dir}`).join('\n')}
✅ rgctl skill installed via rgctl CLI
✅ Installed migrator agent to:
${agentDirs.map((dir) => `   ${dir}`).join('\n')}

NEXT STEPS:

1. Restart your editor session (Claude Code: /exit then claude again; Cursor: restart the app)

2. For interactive migration:
   /migiq
   "Migrate to [target technology]"

3. For autonomous migration:
   Agent({
     description: "Migration task",
     prompt: "Follow AGENT.md. Migrate from [source] to [target]...",
     subagent_type: "general-purpose"
   })

DOCUMENTATION:
  • Quick start: ${targetDirs[0]}/README.migiq.md
  • Full docs: https://github.com/sshaaf/migIQ

Happy migrating! 🚀
`);

  } catch (error) {
    console.error('\n❌ Installation failed:', error.message);
    process.exit(1);
  }
}

// Export for use as module
module.exports = { installMigIQ, installRgctlSkill, resolveRgctlPath };

function parseIsGlobal(argv) {
  if (process.env.npm_config_global === 'true') {
    return true;
  }
  return argv.includes('-g') || argv.includes('--global');
}

// Run if called directly (for postinstall hook)
if (require.main === module) {
  const isGlobal = parseIsGlobal(process.argv.slice(2));
  installMigIQ(isGlobal).catch(error => {
    console.error('Installation failed:', error);
    process.exit(1);
  });
}
