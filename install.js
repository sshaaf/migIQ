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

/**
 * Parse YAML frontmatter from a SKILL.md file.
 * Returns { name, description, metadata: { source, target, language, build_tool, ... } }
 */
function parseFrontmatter(filePath) {
  const content = fs.readFileSync(filePath, 'utf-8');
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return null;

  const block = match[1];
  const result = { metadata: {} };
  let inMetadata = false;

  for (const line of block.split('\n')) {
    if (/^\s*$/.test(line)) continue;

    if (/^metadata:\s*$/.test(line)) {
      inMetadata = true;
      continue;
    }

    const nestedMatch = line.match(/^\s{2}(\w[\w_]*):\s*(.+)$/);
    if (inMetadata && nestedMatch) {
      let val = nestedMatch[2].trim();
      if ((val.startsWith('"') && val.endsWith('"')) || (val.startsWith("'") && val.endsWith("'"))) {
        val = val.slice(1, -1);
      }
      result.metadata[nestedMatch[1]] = val;
      continue;
    }

    const topMatch = line.match(/^(\w[\w_-]*):\s*(.+)$/);
    if (topMatch) {
      inMetadata = false;
      let val = topMatch[2].trim();
      if ((val.startsWith('"') && val.endsWith('"')) || (val.startsWith("'") && val.endsWith("'"))) {
        val = val.slice(1, -1);
      }
      result[topMatch[1]] = val;
    } else if (!nestedMatch) {
      inMetadata = false;
    }
  }

  return result.name ? result : null;
}

/**
 * Scan a directory for migration skills.
 * Looks for skills/<lang>/<name>/SKILL.md and <name>/SKILL.md patterns.
 * Skips the generator/ directory.
 */
function discoverSkills(sourceDir) {
  const found = [];
  const seen = new Set();

  function scanSkillDir(skillDir, skillMdPath) {
    const fm = parseFrontmatter(skillMdPath);
    if (!fm || !fm.name) return;
    if (seen.has(fm.name)) return;

    const coreSkills = ['migiq', 'mig-graphify', 'mig-plan', 'mig-prompt-builder',
      'mig-execute', 'mig-test-gen', 'mig-containerize', 'mig-deploy'];
    if (coreSkills.includes(fm.name)) {
      console.log(`  ⚠️  Skipping "${fm.name}" — name conflicts with core migIQ skill`);
      return;
    }

    seen.add(fm.name);

    const modules = [];
    const modulesDir = path.join(skillDir, 'modules');
    if (fs.existsSync(modulesDir)) {
      for (const f of fs.readdirSync(modulesDir)) {
        if (f.endsWith('.md')) modules.push(f.replace('.md', ''));
      }
    }

    const references = [];
    const refsDir = path.join(skillDir, 'references');
    if (fs.existsSync(refsDir)) {
      for (const f of fs.readdirSync(refsDir)) {
        if (f.endsWith('.md')) references.push(f.replace('.md', ''));
      }
    }

    found.push({
      name: fm.name,
      sourceTech: (fm.metadata && fm.metadata.source) || null,
      targetTech: (fm.metadata && fm.metadata.target) || null,
      language: (fm.metadata && fm.metadata.language) || null,
      buildTool: (fm.metadata && fm.metadata.build_tool) || null,
      sourcePath: skillDir,
      hasModules: modules.length > 0,
      hasReferences: references.length > 0,
      modules: modules,
      references: references
    });
  }

  // Pattern 1: skills/<lang>/<name>/SKILL.md (migration-skills repo layout)
  const skillsDir = path.join(sourceDir, 'skills');
  if (fs.existsSync(skillsDir)) {
    for (const lang of fs.readdirSync(skillsDir, { withFileTypes: true })) {
      if (!lang.isDirectory()) continue;
      const langDir = path.join(skillsDir, lang.name);
      for (const skill of fs.readdirSync(langDir, { withFileTypes: true })) {
        if (!skill.isDirectory()) continue;
        const skillMd = path.join(langDir, skill.name, 'SKILL.md');
        if (fs.existsSync(skillMd)) {
          scanSkillDir(path.join(langDir, skill.name), skillMd);
        }
      }
    }
  }

  // Pattern 2: <name>/SKILL.md (flat layout, skip generator/)
  for (const entry of fs.readdirSync(sourceDir, { withFileTypes: true })) {
    if (!entry.isDirectory()) continue;
    if (entry.name === 'generator' || entry.name === 'skills' || entry.name === 'node_modules' || entry.name === '.git') continue;
    const skillMd = path.join(sourceDir, entry.name, 'SKILL.md');
    if (fs.existsSync(skillMd)) {
      scanSkillDir(path.join(sourceDir, entry.name), skillMd);
    }
  }

  return found;
}

/**
 * Get the manifest file path
 */
function getManifestPath(isGlobal) {
  return path.join(getTargetDir(isGlobal), 'skills', 'migration-skills.json');
}

/**
 * Read the manifest file, or return a default empty manifest
 */
function readManifest(isGlobal) {
  const manifestPath = getManifestPath(isGlobal);
  if (fs.existsSync(manifestPath)) {
    return JSON.parse(fs.readFileSync(manifestPath, 'utf-8'));
  }
  return { version: 1, source: null, installed_at: null, skills: [] };
}

/**
 * Write the manifest file
 */
function writeManifest(isGlobal, manifest) {
  const manifestPath = getManifestPath(isGlobal);
  fs.mkdirSync(path.dirname(manifestPath), { recursive: true });
  fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2) + '\n');
}

/**
 * Install external migration skills from a local path or git URL
 */
async function addExternalSkills(source, isGlobal = false) {
  const { execSync } = require('child_process');
  const targetDir = getTargetDir(isGlobal);
  const scope = isGlobal ? 'global' : 'local';
  let sourceDir = source;
  let tmpDir = null;

  console.log(`
╔══════════════════════════════════════════════════════════════════════╗
║                  Adding Migration Skills                             ║
╚══════════════════════════════════════════════════════════════════════╝
`);

  // Clone from git if source is a URL
  if (/^(https?:\/\/|git@|git:\/\/)/.test(source)) {
    tmpDir = path.join(os.tmpdir(), 'migiq-add-' + Date.now());
    console.log(`📥 Cloning from ${source}...`);
    try {
      execSync(`git clone --depth 1 "${source}" "${tmpDir}"`, { stdio: 'pipe' });
    } catch (err) {
      console.error(`\n❌ Failed to clone repository: ${err.message}`);
      throw err;
    }
    sourceDir = tmpDir;
  } else {
    sourceDir = path.resolve(sourceDir);
    if (!fs.existsSync(sourceDir)) {
      throw new Error(`Source directory not found: ${sourceDir}`);
    }
  }

  try {
    console.log(`🔍 Discovering migration skills in ${source}...\n`);

    const skills = discoverSkills(sourceDir);

    if (skills.length === 0) {
      console.log('  ⚠️  No migration skills found.');
      console.log('  Expected: skills/<lang>/<name>/SKILL.md or <name>/SKILL.md');
      return;
    }

    console.log(`📚 Installing ${skills.length} migration skill(s):\n`);

    const skillsDir = path.join(targetDir, 'skills');
    fs.mkdirSync(skillsDir, { recursive: true });

    for (const skill of skills) {
      const destDir = path.join(skillsDir, skill.name);
      copyDir(skill.sourcePath, destDir);

      const parts = [skill.name];
      if (skill.sourceTech && skill.targetTech) {
        parts.push(`(${skill.sourceTech} → ${skill.targetTech})`);
      }
      console.log(`  ✅ ${parts.join(' ')}`);
    }

    // Update manifest
    const manifest = readManifest(isGlobal);
    manifest.source = source;
    manifest.installed_at = new Date().toISOString();

    // Merge skills: update existing, add new
    for (const skill of skills) {
      const existing = manifest.skills.findIndex(s => s.name === skill.name);
      const entry = {
        name: skill.name,
        source_tech: skill.sourceTech,
        target_tech: skill.targetTech,
        language: skill.language,
        build_tool: skill.buildTool,
        has_modules: skill.hasModules,
        has_references: skill.hasReferences,
        modules: skill.modules,
        references: skill.references
      };
      if (existing >= 0) {
        manifest.skills[existing] = entry;
      } else {
        manifest.skills.push(entry);
      }
    }

    writeManifest(isGlobal, manifest);

    console.log(`
╔══════════════════════════════════════════════════════════════════════╗
║                  ✨ Skills Added Successfully! ✨                     ║
╚══════════════════════════════════════════════════════════════════════╝

✅ Installed ${skills.length} migration skill(s) to: ${skillsDir}
✅ Manifest saved to: ${getManifestPath(isGlobal)}

Installation type: ${scope}

These skills will be automatically detected during migration planning
and execution. Run /migiq to start a migration.
`);

  } finally {
    // Clean up temp directory
    if (tmpDir && fs.existsSync(tmpDir)) {
      fs.rmSync(tmpDir, { recursive: true, force: true });
    }
  }
}

/**
 * List installed external migration skills
 */
function listExternalSkills(isGlobal = false) {
  const manifest = readManifest(isGlobal);

  if (manifest.skills.length === 0) {
    console.log('\nNo migration skills installed.');
    console.log('Install with: npx migiq add <path-or-git-url>\n');
    return;
  }

  console.log(`
Migration Skills (${isGlobal ? 'global' : 'local'}):
`);

  // Calculate column widths
  const nameWidth = Math.max(4, ...manifest.skills.map(s => s.name.length));
  const migWidth = Math.max(9, ...manifest.skills.map(s =>
    ((s.source_tech || '?') + ' → ' + (s.target_tech || '?')).length
  ));

  console.log(
    '  ' + 'Name'.padEnd(nameWidth + 2) +
    'Migration'.padEnd(migWidth + 2) +
    'Language'
  );
  console.log('  ' + '─'.repeat(nameWidth + migWidth + 12));

  for (const skill of manifest.skills) {
    const migration = (skill.source_tech || '?') + ' → ' + (skill.target_tech || '?');
    console.log(
      '  ' + skill.name.padEnd(nameWidth + 2) +
      migration.padEnd(migWidth + 2) +
      (skill.language || '?')
    );
  }

  if (manifest.source) {
    console.log(`\nSource: ${manifest.source}`);
  }
  if (manifest.installed_at) {
    console.log(`Installed: ${manifest.installed_at}`);
  }
  console.log('');
}

/**
 * Remove an installed external migration skill
 */
function removeExternalSkill(name, isGlobal = false) {
  const manifest = readManifest(isGlobal);
  const idx = manifest.skills.findIndex(s => s.name === name);

  if (idx < 0) {
    console.error(`\n❌ Migration skill "${name}" not found.`);
    console.log('Run "npx migiq list" to see installed skills.\n');
    return;
  }

  const targetDir = getTargetDir(isGlobal);
  const skillDir = path.join(targetDir, 'skills', name);

  if (fs.existsSync(skillDir)) {
    fs.rmSync(skillDir, { recursive: true, force: true });
  }

  manifest.skills.splice(idx, 1);
  writeManifest(isGlobal, manifest);

  console.log(`\n✅ Removed migration skill "${name}".`);
  console.log(`  Deleted: ${skillDir}\n`);
}

// Export for use as module
module.exports = {
  installMigIQ,
  addExternalSkills,
  listExternalSkills,
  removeExternalSkill
};

// Run if called directly (for postinstall hook)
if (require.main === module) {
  const isGlobal = process.env.npm_config_global === 'true';
  installMigIQ(isGlobal).catch(error => {
    console.error('Installation failed:', error);
    process.exit(1);
  });
}
