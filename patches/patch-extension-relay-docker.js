#!/usr/bin/env node
/**
 * WebSocket upgrade en extension-relay solo acepta remoteAddress "loopback".
 * Con Docker Desktop, Chrome en el Mac llega por port-forward con IP de bridge (172.x), no 127.0.0.1 → 403 Forbidden → icono rojo.
 *
 * Target: dist/browser/extension-relay.js — amplía isLoopbackAddress para RFC1918 / Docker bridge.
 */
const fs = require("fs");
const path = require("path");

const globalPath = "/usr/local/lib/node_modules/clawdbot/dist/browser/extension-relay.js";
const defaultPath = path.join(__dirname, "../node_modules/clawdbot/dist/browser/extension-relay.js");
const candidates = [process.env.CLAWDBOT_EXTENSION_RELAY_PATH, globalPath, defaultPath].filter(Boolean);
let target = null;
for (const p of candidates) {
  const resolved = path.isAbsolute(p) ? p : path.resolve(p);
  if (fs.existsSync(resolved)) {
    target = resolved;
    break;
  }
}
if (!target) {
  console.error("patch-extension-relay-docker: extension-relay.js not found");
  process.exit(1);
}

const marker = "Docker Desktop port-forward";
let content = fs.readFileSync(target, "utf8");
if (content.includes(marker)) {
  console.log("patch-extension-relay-docker: already patched");
  process.exit(0);
}

const oldFn = `function isLoopbackAddress(ip) {
    if (!ip)
        return false;
    if (ip === "127.0.0.1")
        return true;
    if (ip.startsWith("127."))
        return true;
    if (ip === "::1")
        return true;
    if (ip.startsWith("::ffff:127."))
        return true;
    return false;
}`;

const newFn = `function isLoopbackAddress(ip) {
    if (!ip)
        return false;
    if (ip === "127.0.0.1")
        return true;
    if (ip.startsWith("127."))
        return true;
    if (ip === "::1")
        return true;
    if (ip.startsWith("::ffff:127."))
        return true;
    // ${marker}: el host Mac llega como 172.x/10.x vía NAT de Docker, no como loopback.
    if (ip.startsWith("172.") || ip.startsWith("10.") || ip.startsWith("192.168."))
        return true;
    if (ip.startsWith("::ffff:172.") || ip.startsWith("::ffff:10.") || ip.startsWith("::ffff:192.168."))
        return true;
    return false;
}`;

if (!content.includes(oldFn)) {
  console.error("patch-extension-relay-docker: expected isLoopbackAddress block not found (clawdbot version mismatch?)");
  process.exit(1);
}

content = content.replace(oldFn, newFn);
fs.writeFileSync(target, content, "utf8");
console.log("patch-extension-relay-docker: patched", target);
