#!/usr/bin/env node
/**
 * Patch clawdbot's ERROR_PATTERNS.billing so Anthropic "API usage limits"
 * and similar messages trigger model fallback (billing/rate_limit).
 *
 * Target: node_modules/clawdbot/dist/agents/pi-embedded-helpers/errors.js
 * Adds: "usage limits", "api usage limits", "regain access", "insufficient_quota", "insufficient quota"
 */
const fs = require("fs");
const path = require("path");

const globalPath = "/usr/local/lib/node_modules/clawdbot/dist/agents/pi-embedded-helpers/errors.js";
const defaultPath = path.join(__dirname, "../node_modules/clawdbot/dist/agents/pi-embedded-helpers/errors.js");
const candidates = [process.env.CLAWDBOT_ERRORS_PATH, globalPath, defaultPath].filter(Boolean);
let target = null;
for (const p of candidates) {
  const resolved = path.isAbsolute(p) ? p : path.resolve(p);
  if (fs.existsSync(resolved)) {
    target = resolved;
    break;
  }
}
if (!target) {
  console.error("patch-failover-errors: errors.js not found. Tried:", candidates.join(", "));
  process.exit(1);
}

const marker = '"plans & billing",';
const addition = [
  '        "usage limits",',
  '        "api usage limits",',
  '        "regain access",',
  '        "insufficient_quota",',
  '        "insufficient quota",',
].join("\n");

let content = fs.readFileSync(target, "utf8");
if (content.includes('"usage limits",')) {
  console.log("patch-failover-errors: already patched");
  process.exit(0);
}
if (!content.includes(marker)) {
  console.error("patch-failover-errors: marker not found:", marker);
  process.exit(1);
}

// Insert new lines after "plans & billing",
content = content.replace(
  marker + "\n",
  marker + "\n" + addition + "\n"
);
fs.writeFileSync(target, content);
console.log("patch-failover-errors: patched", target);
