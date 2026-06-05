#!/usr/bin/env node
/**
 * Install script for literature-search skill
 * Copies Python package to appropriate location based on IDE
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const SKILL_NAME = 'literature-search';
const SOURCE_DIR = path.join(__dirname, 'python', 'literature_search');

// Target directories for different IDEs
const TARGET_DIRS = [
  path.join(process.env.HOME, '.claude', 'skills', SKILL_NAME),
  path.join(process.env.HOME, '.cursor', 'skills', SKILL_NAME),
  path.join(process.cwd(), '.agents', 'skills', SKILL_NAME),
];

function copyDir(src, dest) {
  if (!fs.existsSync(dest)) {
    fs.mkdirSync(dest, { recursive: true });
  }
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

console.log(`Installing ${SKILL_NAME} skill...`);

let installed = false;
for (const targetDir of TARGET_DIRS) {
  try {
    // Check if parent directory exists
    const parentDir = path.dirname(targetDir);
    if (fs.existsSync(parentDir)) {
      copyDir(SOURCE_DIR, targetDir);
      console.log(`✓ Installed to ${targetDir}`);
      installed = true;
    }
  } catch (err) {
    console.log(`✗ Failed to install to ${targetDir}: ${err.message}`);
  }
}

if (!installed) {
  console.error('Error: Could not find a suitable target directory');
  process.exit(1);
}

console.log('Installation complete!');
