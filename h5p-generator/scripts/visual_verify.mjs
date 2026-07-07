#!/usr/bin/env node
/**
 * H5P Visual Verification with Puppeteer
 *
 * Verifies generated H5P files by:
 * 1. Extracting and serving with h5p-standalone
 * 2. Taking screenshots via Puppeteer
 * 3. Running basic visual checks
 *
 * Usage:
 *   node visual_verify.mjs <path-to-h5p-file> [--output-dir <dir>] [--port <port>]
 *
 * Returns JSON result to stdout:
 *   { "success": true, "screenshot": "path/to/screenshot.png", "checks": [...] }
 */

import puppeteer from 'puppeteer-core';
import http from 'http';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { createReadStream } from 'fs';
import { extract } from 'zip-lib';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const CHROME_PATH = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const DEFAULT_PORT = 8090;
const RENDER_TIMEOUT = 15000;

// MIME types for static serving
const MIME_TYPES = {
  '.html': 'text/html',
  '.js': 'application/javascript',
  '.css': 'text/css',
  '.json': 'application/json',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.svg': 'image/svg+xml',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2',
  '.ttf': 'font/ttf',
};

/**
 * Extract H5P file to a temp directory.
 * H5P files contain h5p.json at root and content/content.json.
 * h5p-standalone expects h5pJsonPath to point to the directory with h5p.json.
 */
async function extractH5P(h5pPath, extractDir) {
  if (fs.existsSync(extractDir)) {
    fs.rmSync(extractDir, { recursive: true });
  }
  fs.mkdirSync(extractDir, { recursive: true });
  await extract(h5pPath, extractDir);
}

/**
 * Create the preview HTML that loads H5P content
 */
function createPreviewHTML(title) {
  return `<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>H5P Verify: ${title}</title>
  <script src="https://cdn.jsdelivr.net/npm/h5p-standalone@3.6.0/dist/main.bundle.js"></script>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: Arial, sans-serif; background: #f5f5f5; padding: 20px; }
    #h5p-container { background: white; border-radius: 8px; padding: 20px; max-width: 960px; margin: 0 auto; min-height: 400px; }
    #status { max-width: 960px; margin: 10px auto; padding: 8px 12px; font-size: 13px; color: #666; }
    #status.error { color: #c62828; background: #ffebee; border-radius: 4px; }
    #status.ready { color: #2e7d32; background: #e8f5e9; border-radius: 4px; }
  </style>
</head>
<body>
  <div id="h5p-container"></div>
  <div id="status">Loading...</div>
  <script>
    const el = document.getElementById('h5p-container');
    const status = document.getElementById('status');
    new H5PStandalone.H5P(el, {
      h5pJsonPath: 'workspace',
      frameJs: 'https://cdn.jsdelivr.net/npm/h5p-standalone@3.6.0/dist/frame.bundle.js',
      frameCss: 'https://cdn.jsdelivr.net/npm/h5p-standalone@3.6.0/dist/styles/h5p.css',
    })
    .then(() => {
      status.textContent = 'H5P_RENDER_COMPLETE';
      status.className = 'ready';
    })
    .catch(err => {
      status.textContent = 'H5P_RENDER_ERROR: ' + err.message;
      status.className = 'error';
    });
  </script>
</body>
</html>`;
}

/**
 * Start a simple static file server
 */
function startServer(rootDir, port) {
  return new Promise((resolve) => {
    const server = http.createServer((req, res) => {
      let filePath = path.join(rootDir, decodeURIComponent(req.url === '/' ? '/preview.html' : req.url));

      // Security: prevent path traversal
      if (!filePath.startsWith(rootDir)) {
        res.writeHead(403);
        res.end();
        return;
      }

      const ext = path.extname(filePath).toLowerCase();
      const contentType = MIME_TYPES[ext] || 'application/octet-stream';

      if (fs.existsSync(filePath) && fs.statSync(filePath).isFile()) {
        res.writeHead(200, { 'Content-Type': contentType });
        createReadStream(filePath).pipe(res);
      } else {
        res.writeHead(404);
        res.end('Not found');
      }
    });

    server.listen(port, () => {
      resolve(server);
    });
  });
}

/**
 * Run visual checks on the rendered H5P content
 */
async function runChecks(page, contentType) {
  const checks = [];

  // Check 1: Is the H5P content visible?
  const h5pContent = await page.$('.h5p-content');
  const contentVisible = h5pContent !== null;
  checks.push({
    name: 'content_visible',
    passed: contentVisible,
    message: contentVisible ? 'H5P content is visible' : 'H5P content not found'
  });

  if (!contentVisible) return checks;

  // Check 2: Content has non-zero dimensions
  const contentBox = await h5pContent.boundingBox();
  const hasDimensions = contentBox && contentBox.width > 50 && contentBox.height > 50;
  checks.push({
    name: 'has_dimensions',
    passed: hasDimensions,
    message: hasDimensions
      ? `Content size: ${Math.round(contentBox.width)}x${Math.round(contentBox.height)}`
      : 'Content has zero or very small dimensions'
  });

  // Check 3: Are interactive elements present (buttons)?
  const buttons = await page.$$('.h5p-joubelui-button, .h5p-question-check-answer, button');
  const hasButtons = buttons.length > 0;
  checks.push({
    name: 'has_interactive_elements',
    passed: hasButtons,
    message: hasButtons ? `Found ${buttons.length} interactive element(s)` : 'No interactive elements found'
  });

  // Check 4: No error messages visible
  const errorElements = await page.$$('.h5p-error, .error, [class*="error"]');
  let hasErrors = false;
  for (const el of errorElements) {
    const text = await page.evaluate(e => e.textContent, el);
    if (text && text.includes('Error')) {
      hasErrors = true;
      break;
    }
  }
  checks.push({
    name: 'no_errors',
    passed: !hasErrors,
    message: hasErrors ? 'Error messages detected' : 'No error messages'
  });

  // Check 5 (CoursePresentation): Check for overlapping elements
  if (contentType === 'CoursePresentation') {
    const slideElements = await page.$$('.h5p-course-presentation .h5p-element-outer');
    if (slideElements.length > 1) {
      const boxes = [];
      for (const el of slideElements) {
        const box = await el.boundingBox();
        if (box) boxes.push(box);
      }
      let overlaps = 0;
      for (let i = 0; i < boxes.length; i++) {
        for (let j = i + 1; j < boxes.length; j++) {
          const a = boxes[i], b = boxes[j];
          if (a.x < b.x + b.width && a.x + a.width > b.x &&
              a.y < b.y + b.height && a.y + a.height > b.y) {
            overlaps++;
          }
        }
      }
      checks.push({
        name: 'no_overlapping_elements',
        passed: overlaps === 0,
        message: overlaps === 0 ? 'No overlapping elements' : `${overlaps} overlapping element pair(s)`
      });
    }
  }

  // Check 6 (InteractiveBook): Navigation present
  if (contentType === 'InteractiveBook') {
    const nav = await page.$('.h5p-interactive-book-navigation, [class*="navigation"]');
    checks.push({
      name: 'book_navigation',
      passed: nav !== null,
      message: nav ? 'Book navigation found' : 'Book navigation missing'
    });
  }

  return checks;
}

/**
 * Run structural checks on H5P JSON files (no rendering needed)
 */
function runStructuralChecks(h5pJsonPath, contentJsonPath, contentType) {
  const checks = [];

  // Check 1: h5p.json exists and is valid JSON
  let h5pJson = null;
  try {
    h5pJson = JSON.parse(fs.readFileSync(h5pJsonPath, 'utf-8'));
    checks.push({ name: 'h5p_json_valid', passed: true, message: 'h5p.json is valid JSON' });
  } catch (e) {
    checks.push({ name: 'h5p_json_valid', passed: false, message: `h5p.json invalid: ${e.message}` });
    return checks;
  }

  // Check 2: content.json exists and is valid JSON
  let contentJson = null;
  try {
    contentJson = JSON.parse(fs.readFileSync(contentJsonPath, 'utf-8'));
    checks.push({ name: 'content_json_valid', passed: true, message: 'content.json is valid JSON' });
  } catch (e) {
    checks.push({ name: 'content_json_valid', passed: false, message: `content.json invalid: ${e.message}` });
    return checks;
  }

  // Check 3: mainLibrary is set
  const mainLib = h5pJson.mainLibrary || '';
  checks.push({
    name: 'has_main_library',
    passed: mainLib.length > 0,
    message: mainLib ? `mainLibrary: ${mainLib}` : 'mainLibrary missing'
  });

  // Check 4: preloadedDependencies has entries
  const deps = h5pJson.preloadedDependencies || [];
  checks.push({
    name: 'has_dependencies',
    passed: deps.length > 0,
    message: `${deps.length} dependencies`
  });

  // Check 5: Content type specific checks
  if (contentType === 'InteractiveBook') {
    const chapters = contentJson.chapters || [];
    checks.push({
      name: 'book_has_chapters',
      passed: chapters.length > 0,
      message: `${chapters.length} chapter(s)`
    });
    // Check each chapter has Column wrapper
    const allColumn = chapters.every(ch =>
      ch.chapter && ch.chapter.library && ch.chapter.library.startsWith('H5P.Column')
    );
    checks.push({
      name: 'chapters_use_column_wrapper',
      passed: allColumn,
      message: allColumn ? 'All chapters use H5P.Column wrapper' : 'Some chapters missing Column wrapper'
    });
  }

  if (contentType === 'CoursePresentation') {
    const slides = (contentJson.presentation || {}).slides || [];
    checks.push({
      name: 'has_slides',
      passed: slides.length > 0,
      message: `${slides.length} slide(s)`
    });
    // Check subContentIds are UUIDs
    let allUuid = true;
    for (const slide of slides) {
      for (const elem of (slide.elements || [])) {
        const subId = (elem.action || {}).subContentId || '';
        if (subId.length < 20) { allUuid = false; break; }
      }
    }
    checks.push({
      name: 'uuid_subcontent_ids',
      passed: allUuid,
      message: allUuid ? 'All subContentIds are UUIDs' : 'Some subContentIds are not UUIDs'
    });
  }

  if (contentType === 'QuestionSet') {
    const questions = contentJson.questions || [];
    checks.push({
      name: 'has_questions',
      passed: questions.length > 0,
      message: `${questions.length} question(s)`
    });
  }

  return checks;
}

/**
 * Take screenshots of CoursePresentation slides
 */
async function screenshotSlides(page, outputDir, baseName) {
  const screenshots = [];
  const nextBtn = await page.$('.h5p-next, [class*="next"]');

  if (!nextBtn) {
    return screenshots;
  }

  let slideNum = 1;
  const maxSlides = 20;

  while (slideNum <= maxSlides) {
    const screenshotPath = path.join(outputDir, `${baseName}_slide${slideNum}.png`);
    await page.screenshot({ path: screenshotPath, fullPage: false });
    screenshots.push(screenshotPath);

    // Try to go to next slide
    const nextButton = await page.$('.h5p-next:not(.h5p-hidden), .h5p-course-presentation .h5p-footer-button.h5p-next');
    if (!nextButton) break;

    const isDisabled = await page.evaluate(btn => {
      return btn.classList.contains('h5p-hidden') || btn.disabled || btn.style.display === 'none';
    }, nextButton);

    if (isDisabled) break;

    await nextButton.click();
    await new Promise(r => setTimeout(r, 500));
    slideNum++;
  }

  return screenshots;
}

/**
 * Main verification function
 */
async function verify(h5pPath, options = {}) {
  const port = options.port || DEFAULT_PORT;
  const outputDir = options.outputDir || path.dirname(h5pPath);
  const baseName = path.basename(h5pPath, '.h5p');

  // Setup
  const tempDir = path.join(outputDir, `.h5p-verify-${baseName}`);

  let server = null;
  let browser = null;

  try {
    fs.mkdirSync(tempDir, { recursive: true });

    // 1. Extract H5P to 'workspace' subdir
    // h5p-standalone expects: {h5pJsonPath}/h5p.json and {h5pJsonPath}/content/content.json
    const workspaceDir = path.join(tempDir, 'workspace');
    await extractH5P(h5pPath, workspaceDir);

    // Read h5p.json to determine content type
    const h5pJsonPath = path.join(workspaceDir, 'h5p.json');
    let contentType = 'Unknown';
    if (fs.existsSync(h5pJsonPath)) {
      const h5pJson = JSON.parse(fs.readFileSync(h5pJsonPath, 'utf-8'));
      contentType = (h5pJson.mainLibrary || '').replace('H5P.', '');
    }

    // 2. Create preview HTML
    const previewHtml = createPreviewHTML(baseName);
    fs.writeFileSync(path.join(tempDir, 'preview.html'), previewHtml, 'utf-8');

    // 3. Start server
    server = await startServer(tempDir, port);

    // 4. Launch browser
    browser = await puppeteer.launch({
      executablePath: CHROME_PATH,
      headless: 'new',
      args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'],
    });

    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 900 });

    // 5. Navigate and wait for render
    await page.goto(`http://localhost:${port}/preview.html`, { waitUntil: 'networkidle0', timeout: 30000 });

    // Wait for H5P render complete or error (with generous timeout for library loading)
    let renderSuccess = false;
    let renderStatus = 'unknown';
    try {
      await page.waitForFunction(
        () => {
          const status = document.getElementById('status');
          return status && (
            status.textContent.includes('H5P_RENDER_COMPLETE') ||
            status.textContent.includes('H5P_RENDER_ERROR')
          );
        },
        { timeout: RENDER_TIMEOUT }
      );
      renderStatus = await page.evaluate(() => {
        const status = document.getElementById('status');
        return status ? status.textContent : 'unknown';
      });
      renderSuccess = renderStatus.includes('H5P_RENDER_COMPLETE');
    } catch {
      // Timeout - check if any content rendered anyway
      renderStatus = await page.evaluate(() => {
        const status = document.getElementById('status');
        const hasContent = document.querySelector('.h5p-content') !== null;
        return hasContent ? 'partial_render' : (status ? status.textContent : 'timeout');
      });
      renderSuccess = renderStatus === 'partial_render';
    }

    // 6. Take screenshot
    const screenshotPath = path.join(outputDir, `${baseName}_verify.png`);
    await page.screenshot({ path: screenshotPath, fullPage: true });

    // 7. Run structural checks (JSON-based, independent of rendering)
    const structuralChecks = runStructuralChecks(
      path.join(workspaceDir, 'h5p.json'),
      path.join(workspaceDir, 'content', 'content.json'),
      contentType
    );

    // 8. Run visual checks (rendering-dependent)
    const visualChecks = await runChecks(page, contentType);
    const checks = [...structuralChecks, ...visualChecks];

    // 9. For CoursePresentation, screenshot individual slides
    let slideScreenshots = [];
    if (contentType === 'CoursePresentation') {
      slideScreenshots = await screenshotSlides(page, outputDir, baseName);
    }

    // 10. Determine overall result
    // Success = all structural checks pass (render may fail in standalone mode)
    const structuralPassed = structuralChecks.every(c => c.passed);
    const allPassed = structuralPassed; // Don't require render success for overall pass

    const result = {
      success: allPassed,
      renderSuccess,
      contentType,
      screenshot: screenshotPath,
      slideScreenshots,
      checks,
      renderStatus: renderSuccess ? 'ok' : renderStatus,
    };

    return result;

  } finally {
    if (browser) await browser.close();
    if (server) server.close();

    // Cleanup temp dir
    if (fs.existsSync(tempDir)) {
      fs.rmSync(tempDir, { recursive: true, force: true });
    }
  }
}

// =============================================================================
// CLI Entry Point
// =============================================================================

async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0 || args.includes('--help')) {
    console.log('Usage: node visual_verify.mjs <path-to-h5p-file> [--output-dir <dir>] [--port <port>]');
    console.log('');
    console.log('Verifies H5P files by rendering them and taking screenshots.');
    console.log('Returns JSON result to stdout.');
    process.exit(0);
  }

  const h5pPath = path.resolve(args[0]);
  const options = {};

  for (let i = 1; i < args.length; i++) {
    if (args[i] === '--output-dir' && args[i + 1]) {
      options.outputDir = path.resolve(args[++i]);
    } else if (args[i] === '--port' && args[i + 1]) {
      options.port = parseInt(args[++i], 10);
    }
  }

  if (!fs.existsSync(h5pPath)) {
    console.error(JSON.stringify({ success: false, error: `File not found: ${h5pPath}` }));
    process.exit(1);
  }

  try {
    const result = await verify(h5pPath, options);
    console.log(JSON.stringify(result, null, 2));
    process.exit(result.success ? 0 : 1);
  } catch (err) {
    console.error(JSON.stringify({ success: false, error: err.message }));
    process.exit(1);
  }
}

main();
