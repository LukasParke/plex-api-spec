"use strict";

/**
 * Custom Redocly rules that resolve Arazzo step references against the
 * OpenAPI documents named in `sourceDescriptions`.
 *
 * Redocly's built-in Arazzo rules are structural only: nothing checks that
 * `operationId` / `operationPath` actually resolve to a real operation.
 * These rules close that gap.
 *
 * Parsing note: plex-api-spec.yaml is prettier-formatted (2-space indent),
 * so the `paths:` scanner below relies on stable indentation. If the
 * formatter config ever changes, revisit this parser.
 */

const fs = require("fs");
const path = require("path");

const HTTP_METHODS = new Set([
  "get",
  "put",
  "post",
  "delete",
  "options",
  "head",
  "patch",
  "trace",
]);

const specCache = new Map();

/**
 * Build an index of operationId -> {path, method} and "method path" ->
 * {path, method} by scanning the OpenAPI YAML file. Results are cached per
 * absolute file path for the lifetime of the lint process.
 */
function loadSpecIndex(absPath) {
  if (specCache.has(absPath)) return specCache.get(absPath);
  const index = { operations: new Map(), error: null };
  try {
    const text = fs.readFileSync(absPath, "utf8");
    let inPaths = false;
    let currentPath = null;
    let currentMethod = null;
    for (const line of text.split("\n")) {
      if (/^paths:/.test(line)) {
        inPaths = true;
        continue;
      }
      // Any other top-level key ends the paths section.
      if (inPaths && /^\S/.test(line)) break;
      if (!inPaths) continue;

      let m = line.match(/^ {2}("?)(\/[^"]*)\1:\s*$/);
      if (m) {
        currentPath = m[2];
        currentMethod = null;
        continue;
      }
      m = line.match(
        /^ {4}(get|put|post|delete|options|head|patch|trace):\s*$/,
      );
      if (m && currentPath) {
        currentMethod = m[1];
        continue;
      }
      m = line.match(/^ {6}operationId:\s*['"]?([A-Za-z0-9_.-]+)['"]?\s*$/);
      if (m && currentPath && currentMethod) {
        index.operations.set(m[1], {
          path: currentPath,
          method: currentMethod,
        });
        index.operations.set(`${currentMethod} ${currentPath}`, {
          path: currentPath,
          method: currentMethod,
        });
      }
    }
  } catch (e) {
    index.error = e.message;
  }
  specCache.set(absPath, index);
  return index;
}

function report(ctx, message) {
  ctx.report({ message, location: ctx.location });
}

module.exports = function arazzoRefRules() {
  return {
    id: "plex",
    rules: {
      arazzo1: {
        "operation-ref-resolves": () => {
          // Populated on Root enter; used by every Step visitor afterwards.
          let sources = null; // Map<name, absolute spec path>
          let docDir = null;

          const resolveSources = (ctx) => {
            if (sources !== null) return;
            sources = new Map();
            docDir = path.dirname(ctx.location.source.absoluteRef);
          };

          const checkOperationId = (step, ctx) => {
            const ref = step.operationId;
            const prefixed = ref.match(
              /^\$sourceDescriptions\.([A-Za-z0-9_-]+)\.(.+)$/,
            );
            let sourceName;
            let opId;
            if (prefixed) {
              [, sourceName, opId] = prefixed;
            } else if (sources.size === 1) {
              // Arazzo 1.0: a bare operationId is only unambiguous when
              // exactly one non-Arazzo sourceDescription exists.
              sourceName = [...sources.keys()][0];
              opId = ref;
            } else {
              report(
                ctx,
                `Step '${step.stepId}': bare operationId '${ref}' is ambiguous with ${sources.size} sourceDescriptions; use $sourceDescriptions.<name>.${ref}`,
              );
              return;
            }
            if (!sources.has(sourceName)) {
              report(
                ctx,
                `Step '${step.stepId}' references unknown sourceDescription '${sourceName}'. Defined: ${[...sources.keys()].join(", ") || "(none)"}`,
              );
              return;
            }
            const index = loadSpecIndex(sources.get(sourceName));
            if (index.error) {
              report(
                ctx,
                `Step '${step.stepId}': cannot read spec for '${sourceName}': ${index.error}`,
              );
              return;
            }
            const op = index.operations.get(opId);
            if (!op) {
              report(
                ctx,
                `Step '${step.stepId}' references operationId '${opId}' which does not exist in '${sourceName}' (${path.relative(docDir, sources.get(sourceName))})`,
              );
              return;
            }
            // Verify path parameters named by the step exist in the
            // operation's path template.
            const templateParams = new Set(
              [...op.path.matchAll(/\{([^}]+)\}/g)].map((m) => m[1]),
            );
            for (const p of step.parameters || []) {
              if (p && p.in === "path" && !templateParams.has(p.name)) {
                report(
                  ctx,
                  `Step '${step.stepId}' sets path parameter '${p.name}' but '${op.method.toUpperCase()} ${op.path}' only has: ${[...templateParams].join(", ") || "(none)"}`,
                );
              }
            }
          };

          const checkOperationPath = (step, ctx) => {
            const ref = step.operationPath;
            const m = ref.match(
              /^\{\$sourceDescriptions\.([A-Za-z0-9_-]+)\}#\/paths\/(.+)\/([a-z]+)$/,
            );
            if (!m) {
              report(
                ctx,
                `Step '${step.stepId}': operationPath '${ref}' does not match {$sourceDescriptions.<name>}#/paths/<pointer>/<method>`,
              );
              return;
            }
            const [, sourceName, pointer, method] = m;
            if (!sources.has(sourceName)) {
              report(
                ctx,
                `Step '${step.stepId}' references unknown sourceDescription '${sourceName}'`,
              );
              return;
            }
            if (!HTTP_METHODS.has(method)) {
              report(
                ctx,
                `Step '${step.stepId}': '${method}' is not an HTTP method in operationPath '${ref}'`,
              );
              return;
            }
            const apiPath = pointer.replace(/~1/g, "/").replace(/~0/g, "~");
            const index = loadSpecIndex(sources.get(sourceName));
            if (index.error) {
              report(
                ctx,
                `Step '${step.stepId}': cannot read spec for '${sourceName}': ${index.error}`,
              );
              return;
            }
            if (!index.operations.has(`${method} ${apiPath}`)) {
              report(
                ctx,
                `Step '${step.stepId}': no operation '${method.toUpperCase()} ${apiPath}' in '${sourceName}'`,
              );
            }
          };

          return {
            Root(node, ctx) {
              resolveSources(ctx);
              for (const sd of node.sourceDescriptions || []) {
                if (sd && sd.name && sd.url && sd.type === "openapi") {
                  sources.set(sd.name, path.resolve(docDir, sd.url));
                }
              }
            },
            Step(step, ctx) {
              if (sources === null) resolveSources(ctx);
              if (typeof step.operationId === "string")
                checkOperationId(step, ctx);
              else if (typeof step.operationPath === "string")
                checkOperationPath(step, ctx);
            },
          };
        },
      },
    },
  };
};
