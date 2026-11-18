// Render art/poster.html to ../entry.png at exactly 1024x1024.
// Uses the Puppeteer + Chrome installed under ~/workspace/makefun/tools.
// Run: node art/render.mjs
import { createRequire } from "node:module";
import { createServer } from "node:http";
import { readFile } from "node:fs/promises";
import { statSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const require = createRequire("/home/hatch/workspace/makefun/tools/package.json");
const puppeteer = require("puppeteer");

const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const outFile = path.join(repoRoot, "entry.png");

const server = createServer(async (req, res) => {
  try {
    const file = path.join(repoRoot, decodeURIComponent(req.url.split("?")[0]));
    const body = await readFile(file);
    res.writeHead(200, { "content-type": "text/html; charset=utf-8" });
    res.end(body);
  } catch {
    res.writeHead(404);
    res.end("not found");
  }
});

await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
const port = server.address().port;

const browser = await puppeteer.launch({
  headless: true,
  args: ["--no-sandbox", "--disable-dev-shm-usage", "--force-color-profile=srgb"],
});
try {
  const page = await browser.newPage();
  await page.setViewport({ width: 1024, height: 1024, deviceScaleFactor: 1 });
  await page.goto(`http://127.0.0.1:${port}/art/poster.html`, {
    waitUntil: "networkidle0",
  });
  await page.screenshot({ path: outFile, type: "png" });
} finally {
  await browser.close();
  server.close();
}

const { size } = statSync(outFile);
console.log(`wrote ${outFile}: ${size} bytes (cap 1048576)`);
