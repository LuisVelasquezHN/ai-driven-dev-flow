#!/usr/bin/env node
// Costo de IA de una rama, calculado desde los transcripts locales de Claude Code.
//
// Claude Code guarda cada sesión en ~/.claude/projects/<cwd-sanitizado>/*.jsonl, y cada
// respuesta del modelo trae `gitBranch`, `message.model` y `message.usage`. Sumamos las
// de la rama pedida en el repo actual y sus worktrees (incluye subagentes).
//
// Uso: node ai-cost.mjs --branch <rama> [--repo <ruta>] [--pricing <json>] [--json]
//
// Es costo equivalente a precio de API: con un plan de suscripción no es lo facturado,
// pero sirve igual para comparar tareas entre sí.
import { readFileSync, readdirSync, statSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { homedir } from 'node:os';
import { fileURLToPath } from 'node:url';
import { execSync } from 'node:child_process';

const args = process.argv.slice(2);
const opt = (name, fallback) => {
  const i = args.indexOf(`--${name}`);
  return i >= 0 ? args[i + 1] : fallback;
};

const branch = opt('branch');
if (!branch) {
  console.error('Falta --branch <rama>');
  process.exit(2);
}
const repoRoot = opt('repo') ?? execSync('git rev-parse --show-toplevel', { encoding: 'utf8' }).trim();
const here = dirname(fileURLToPath(import.meta.url));
const pricing = JSON.parse(readFileSync(opt('pricing', join(here, 'pricing.json')), 'utf8')).models;
const projectsDir = join(process.env.CLAUDE_CONFIG_DIR ?? join(homedir(), '.claude'), 'projects');

// Claude Code nombra la carpeta del proyecto reemplazando todo lo no alfanumérico por '-'.
// Los worktrees viven bajo <repo>/.claude/worktrees/…, así que comparten el prefijo.
const prefix = repoRoot.replace(/[^a-zA-Z0-9]/g, '-');

function* jsonlFiles(dir) {
  for (const name of readdirSync(dir)) {
    const p = join(dir, name);
    if (statSync(p).isDirectory()) yield* jsonlFiles(p);
    else if (name.endsWith('.jsonl')) yield p;
  }
}

function priceFor(model) {
  // El prefijo más largo gana: "claude-opus-5-5" antes que "claude-opus-5".
  const key = Object.keys(pricing)
    .filter((k) => model.startsWith(k))
    .sort((a, b) => b.length - a.length)[0];
  return key ? pricing[key] : null;
}

function cost(usage, p) {
  const M = 1_000_000;
  const write1h = usage.cache_creation?.ephemeral_1h_input_tokens ?? 0;
  const write5m = usage.cache_creation
    ? usage.cache_creation.ephemeral_5m_input_tokens ?? 0
    : usage.cache_creation_input_tokens ?? 0;
  const read = p.cache_read ?? p.input * 0.1;
  const usd =
    ((usage.input_tokens ?? 0) * p.input +
      (usage.output_tokens ?? 0) * p.output +
      write5m * p.input * 1.25 +
      write1h * p.input * 2 +
      (usage.cache_read_input_tokens ?? 0) * read) / M;
  return usage.speed === 'fast' ? usd * 2 : usd;
}

const seen = new Set();
const byModel = {};
const sessions = new Set();
const unknownModels = new Set();

if (existsSync(projectsDir)) {
  for (const dir of readdirSync(projectsDir)) {
    if (!dir.startsWith(prefix)) continue;
    for (const file of jsonlFiles(join(projectsDir, dir))) {
      for (const line of readFileSync(file, 'utf8').split('\n')) {
        if (!line.includes('"usage"')) continue;
        let e;
        try {
          e = JSON.parse(line);
        } catch {
          continue;
        }
        const m = e.message;
        if (e.type !== 'assistant' || e.gitBranch !== branch || !m?.usage || !m.model) continue;
        // Una respuesta puede aparecer en varias líneas (un bloque por línea): contar una vez.
        const id = `${m.id}:${e.requestId ?? ''}`;
        if (seen.has(id)) continue;
        seen.add(id);
        const p = priceFor(m.model);
        if (!p) {
          unknownModels.add(m.model);
          continue;
        }
        sessions.add(e.sessionId);
        const acc = (byModel[m.model] ??= { requests: 0, input: 0, output: 0, cache_read: 0, cache_write: 0, usd: 0 });
        acc.requests += 1;
        acc.input += m.usage.input_tokens ?? 0;
        acc.output += m.usage.output_tokens ?? 0;
        acc.cache_read += m.usage.cache_read_input_tokens ?? 0;
        acc.cache_write += m.usage.cache_creation_input_tokens ?? 0;
        acc.usd += cost(m.usage, p);
      }
    }
  }
}

const total = Object.values(byModel).reduce((s, x) => s + x.usd, 0);
const result = {
  branch,
  repo: repoRoot,
  sessions: sessions.size,
  total_usd: Math.round(total * 100) / 100,
  by_model: byModel,
  unknown_models: [...unknownModels],
};

if (args.includes('--json')) {
  console.log(JSON.stringify(result, null, 2));
} else {
  console.log(`Rama ${branch}: ${sessions.size} sesión(es), US$ ${result.total_usd.toFixed(2)}`);
  for (const [model, x] of Object.entries(byModel)) {
    console.log(`  ${model}: ${x.requests} respuestas, US$ ${x.usd.toFixed(2)}`);
  }
  if (unknownModels.size) console.log(`  Sin precio (no sumados): ${[...unknownModels].join(', ')}`);
}
