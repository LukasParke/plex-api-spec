#!/usr/bin/env node
import SwaggerParser from '@apidevtools/swagger-parser';
import { writeFileSync } from 'node:fs';
import { resolve } from 'node:path';

const SCHEMA_PATH = process.argv[2] ? resolve(process.cwd(), process.argv[2]) : resolve(process.cwd(), 'plex-api-spec.yaml');
const OUTPUT_PATH = resolve(process.cwd(), 'docs/endpoints.md');

function escapeTableCell(text) {
  return String(text).replace(/\|/g, '\\|').replace(/\n/g, '<br>');
}

async function main() {
  const api = await SwaggerParser.parse(SCHEMA_PATH);

  const lines = [];
  lines.push('---');
  lines.push('title: API Endpoints');
  lines.push('---');
  lines.push('');
  lines.push('# API Endpoints');
  lines.push('');
  lines.push('This page is generated from [`plex-api-spec.yaml`](./plex-api-spec.yaml).');
  lines.push('Do not edit it by hand; run `pnpm run spec:generate-reference` to regenerate it.');
  lines.push('');
  lines.push('## Overview');
  lines.push('');
  lines.push(`| Method | Path | Summary | Operation ID |`);
  lines.push(`| ------ | ---- | ------- | ------------ |`);

  const paths = Object.entries(api.paths || {}).sort(([a], [b]) => a.localeCompare(b));
  for (const [path, methods] of paths) {
    for (const [method, operation] of Object.entries(methods)) {
      if (typeof operation !== 'object' || !operation.summary) continue;
      lines.push(
        `| ${method.toUpperCase()} | \`${escapeTableCell(path)}\` | ${escapeTableCell(operation.summary)} | \`${escapeTableCell(operation.operationId || '')}\` |`
      );
    }
  }

  lines.push('');
  lines.push('## Authentication');
  lines.push('');
  lines.push('Most endpoints require an `X-Plex-Token` header or `X-Plex-Token` query parameter.');
  lines.push('');
  lines.push('## Response format');
  lines.push('');
  lines.push('Responses default to XML. Request JSON by sending `Accept: application/json`.');
  lines.push('');

  writeFileSync(OUTPUT_PATH, lines.join('\n'), 'utf-8');
  console.log(`✅ Generated ${OUTPUT_PATH}`);
}

main().catch((err) => {
  console.error('❌ Reference generation failed:', err.message);
  process.exit(1);
});
