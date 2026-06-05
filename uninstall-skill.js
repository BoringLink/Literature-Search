#!/usr/bin/env node
/**
 * Uninstall script for literature-search skill
 * Removes skill from IDE directories
 */

const fs = require('fs');
const path = require('path');

const SKILL_NAME = 'literature-search';

// Target directories for different IDEs
const TARGET_DIRS = [
  path.join(process.env.HOME, '.claude', 'skills', SKILL_NAME),
  path.join(process.env.HOME, '.cursor', 'skills', SKILL_NAME),
  path.join(process.cwd(), '.agents', 'skills', SKILL_NAME),
];

function removeDir(dir) {
  if (fs.existsSync(dir)) {
    fs.rmSync(dir, { recursive: true, force: true });
  }
}

console.log(`Uninstalling ${SKILL_NAME} skill...`);

for (const targetDir of TARGET_DIRS) {
  try {
    if (fs.existsSync(targetDir)) {
      removeDir(targetDir);
      console.log(`✓ Removed from ${targetDir}`);
    }
  } catch (err) {
    console.log(`✗ Failed to remove ${targetDir}: ${err.message}`);
  }
}

console.log('Uninstallation complete!');
