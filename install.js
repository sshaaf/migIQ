#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const os = require('os');

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
 * Get the installation target directory
 */
function getTargetDir(isGlobal) {
  if (isGlobal) {
    return path.join(os.homedir(), '.claude');
  } else {
    return path.join(process.cwd(), '.claude');
  }
}

/**
 * Main installation function
 */
async function installMigIQ(isGlobal = false) {
  const sourceDir = __dirname;
  const targetDir = getTargetDir(isGlobal);
  const scope = isGlobal ? 'global' : 'local';

  console.log(`
╔══════════════════════════════════════════════════════════════════════╗
║                     Installing MigIQ v0.2.0                          ║
╚══════════════════════════════════════════════════════════════════════╝
`);

  console.log(`📦 Installation mode: ${scope.toUpperCase()}`);
  console.log(`📂 Target directory: ${targetDir}\n`);

  try {
    // Create target directory if it doesn't exist
    fs.mkdirSync(targetDir, { recursive: true });

    // Skills to install
    const skills = [
      'migiq',
      'mig-graphify',
      'mig-plan',
      'mig-prompt-builder',
      'mig-execute',
      'mig-test-gen',
      'mig-containerize',
      'mig-deploy'
    ];

    // Install skills
    console.log('📚 Installing skills:');
    const skillsDir = path.join(targetDir, 'skills');
    fs.mkdirSync(skillsDir, { recursive: true });

    for (const skill of skills) {
      const srcSkillDir = path.join(sourceDir, skill);
      const destSkillDir = path.join(skillsDir, skill);

      if (fs.existsSync(srcSkillDir)) {
        copyDir(srcSkillDir, destSkillDir);
        console.log(`  ✅ ${skill}`);
      } else {
        console.log(`  ⚠️  ${skill} (not found, skipping)`);
      }
    }

    // Install agent
    console.log('\n🤖 Installing agent:');
    const agentsDir = path.join(targetDir, 'agents');
    fs.mkdirSync(agentsDir, { recursive: true });

    const agentFiles = [
      'AGENT.md'
    ];

    const migratorDir = path.join(agentsDir, 'migrator');
    fs.mkdirSync(migratorDir, { recursive: true });

    for (const file of agentFiles) {
      const srcFile = path.join(sourceDir, file);
      const destFile = path.join(migratorDir, file);

      if (fs.existsSync(srcFile)) {
        copyFile(srcFile, destFile);
        console.log(`  ✅ ${file}`);
      }
    }

    // Copy .env.example if it exists
    const envExample = path.join(sourceDir, '.env.example');
    if (fs.existsSync(envExample)) {
      copyFile(envExample, path.join(migratorDir, '.env.example'));
      console.log(`  ✅ .env.example`);
    }

    // Create a README in the installation directory
    const installReadme = `# MigIQ Installation

This directory contains the MigIQ migration platform for Claude Code.

## Installed Components

### Skills (use with /migiq in Claude Code)
- **migiq** - Main orchestration skill
- **mig-graphify** - Code analysis and knowledge graph generation
- **mig-prompt-builder** - Migration requirements builder
- **mig-plan** - Migration planning
- **mig-execute** - Migration execution
- **mig-test-gen** - Test generation
- **mig-containerize** - Container creation
- **mig-deploy** - OpenShift deployment

### Agent (use with Agent tool in Claude Code)
- **migrator** - Autonomous migration agent

## Usage

### Interactive Mode
In any Claude Code session:
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

    fs.writeFileSync(
      path.join(targetDir, 'README.migiq.md'),
      installReadme
    );

    // Success summary
    console.log(`
╔══════════════════════════════════════════════════════════════════════╗
║                   ✨ Installation Complete! ✨                        ║
╚══════════════════════════════════════════════════════════════════════╝

✅ Installed 8 skills to: ${skillsDir}
✅ Installed migrator agent to: ${agentsDir}/migrator

NEXT STEPS:

1. Open Claude Code in your project directory

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
  • Quick start: ${targetDir}/README.migiq.md
  • Full docs: https://github.com/sshaaf/migIQ

Happy migrating! 🚀
`);

  } catch (error) {
    console.error('\n❌ Installation failed:', error.message);
    throw error;
  }
}

// Export for use as module
module.exports = { installMigIQ };

// Run if called directly (for postinstall hook)
if (require.main === module) {
  const isGlobal = process.env.npm_config_global === 'true';
  installMigIQ(isGlobal).catch(error => {
    console.error('Installation failed:', error);
    process.exit(1);
  });
}
