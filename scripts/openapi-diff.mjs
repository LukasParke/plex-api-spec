#!/usr/bin/env node
import SwaggerParser from "@apidevtools/swagger-parser";
import { execSync } from "node:child_process";
import { mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";

const SPEC_PATH = resolve(process.cwd(), "plex-api-spec.yaml");
const BASE_REF = process.argv[2] || "origin/main";

function getBaseSpec(ref) {
  try {
    return execSync(`git show ${ref}:plex-api-spec.yaml`, {
      encoding: "utf-8",
      stdio: ["pipe", "pipe", "pipe"],
    });
  } catch (err) {
    const stderr = String(err.stderr || err);
    if (
      stderr.includes("Path 'plex-api-spec.yaml' does not exist") ||
      stderr.includes("Invalid object name")
    ) {
      console.log("ℹ️  No baseline spec found in git history; skipping breaking-change check.");
      process.exit(0);
    }
    throw err;
  }
}

function getMethods(pathItem) {
  const methods = new Set();
  for (const [method, op] of Object.entries(pathItem || {})) {
    if (typeof op === "object" && op !== null && op.operationId) {
      methods.add(method.toLowerCase());
    }
  }
  return methods;
}

function normalizeParam(param) {
  return `${param.in}:${param.name}`;
}

async function diffSpecs(basePath, headPath) {
  const base = await SwaggerParser.parse(basePath);
  const head = await SwaggerParser.parse(headPath);

  const basePaths = Object.keys(base.paths || {});
  const headPaths = Object.keys(head.paths || {});

  const breaking = [];
  const nonBreaking = [];

  // Removed paths are breaking
  for (const path of basePaths) {
    if (!headPaths.includes(path)) {
      breaking.push(`Removed path: ${path}`);
      continue;
    }

    const baseMethods = getMethods(base.paths[path]);
    const headMethods = getMethods(head.paths[path]);

    for (const method of baseMethods) {
      if (!headMethods.has(method)) {
        breaking.push(`Removed operation: ${method.toUpperCase()} ${path}`);
      }
    }

    // Added methods are non-breaking
    for (const method of headMethods) {
      if (!baseMethods.has(method)) {
        nonBreaking.push(`Added operation: ${method.toUpperCase()} ${path}`);
      }
    }

    // Added required parameters are breaking
    const baseParams = new Map(
      (base.paths[path].parameters || [])
        .filter((p) => p.required)
        .map((p) => [normalizeParam(p), p]),
    );
    const headParams = new Map(
      (head.paths[path].parameters || [])
        .filter((p) => p.required)
        .map((p) => [normalizeParam(p), p]),
    );
    for (const [key, param] of headParams) {
      if (!baseParams.has(key)) {
        breaking.push(`Added required parameter: ${key} on ${path}`);
      }
    }
  }

  // Added paths are non-breaking
  for (const path of headPaths) {
    if (!basePaths.includes(path)) {
      nonBreaking.push(`Added path: ${path}`);
    }
  }

  return { breaking, nonBreaking };
}

async function main() {
  const baseSpec = getBaseSpec(BASE_REF);
  const tmpDir = mkdtempSync(join(tmpdir(), "openapi-diff-"));
  const basePath = join(tmpDir, "base.openapi.yaml");
  writeFileSync(basePath, baseSpec, "utf-8");

  const { breaking, nonBreaking } = await diffSpecs(basePath, SPEC_PATH);

  console.log(`Breaking changes: ${breaking.length}`);
  for (const item of breaking) {
    console.log(`  - ${item}`);
  }

  console.log(`Non-breaking changes: ${nonBreaking.length}`);
  for (const item of nonBreaking.slice(0, 10)) {
    console.log(`  - ${item}`);
  }
  if (nonBreaking.length > 10) {
    console.log(`  ... and ${nonBreaking.length - 10} more`);
  }

  if (breaking.length > 0) {
    console.error("❌ Breaking changes detected in OpenAPI spec.");
    process.exit(1);
  }

  console.log("✅ No breaking changes detected.");
}

main().catch((err) => {
  console.error("❌ OpenAPI diff failed:", err.message);
  process.exit(1);
});
