#!/usr/bin/env node
// Corre los checks declarados en .claude/flow.config.json, en orden.
// Lo usan dev-flow (por fase), pr-flow (tras actualizar con dev) y el CI del PR,
// así el PR nunca descubre un problema que no se pudo ver en local.
//
// Uso: node scripts/flow-checks.mjs [nombre ...]   (sin nombres = todos)
import { readFileSync } from 'node:fs';
import { spawnSync } from 'node:child_process';

const config = JSON.parse(readFileSync('.claude/flow.config.json', 'utf8'));
const only = process.argv.slice(2);
const checks = config.checks.filter((c) => only.length === 0 || only.includes(c.name));

if (checks.length === 0) {
  console.error(`No hay checks que coincidan con: ${only.join(', ')}`);
  process.exit(2);
}

const results = [];
for (const check of checks) {
  console.log(`\n▶ ${check.name}: ${check.cmd}`);
  const started = Date.now();
  const { status } = spawnSync(check.cmd, { shell: true, stdio: 'inherit' });
  results.push({ name: check.name, ok: status === 0, secs: (Date.now() - started) / 1000 });
  if (status !== 0) break; // el primero en rojo corta: arreglarlo antes de seguir
}

console.log('\nResumen');
for (const r of results) console.log(`  ${r.ok ? '✔' : '✘'} ${r.name} (${r.secs.toFixed(1)} s)`);
const skipped = checks.slice(results.length).map((c) => c.name);
if (skipped.length) console.log(`  · sin ejecutar: ${skipped.join(', ')}`);

process.exit(results.every((r) => r.ok) && skipped.length === 0 ? 0 : 1);
