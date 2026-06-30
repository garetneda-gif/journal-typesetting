#!/usr/bin/env node
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);

function parseArgs(argv) {
  const args = { html: null, out: null, url: null };
  for (let i = 2; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--out") args.out = argv[++i];
    else if (arg === "--url") args.url = argv[++i];
    else if (arg === "--help" || arg === "-h") args.help = true;
    else if (!args.html) args.html = arg;
    else throw new Error(`Unexpected argument: ${arg}`);
  }
  return args;
}

function usage() {
  return [
    "Usage:",
    "  node scripts/validate_two_column_layout.mjs /path/to/two-column.html --out /path/to/screenshot",
    "  NODE_PATH=/path/to/node_modules CHROME_EXECUTABLE_PATH=/Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome node ...",
  ].join("\n");
}

function loadPlaywright() {
  const candidates = [];
  if (process.env.PLAYWRIGHT_NODE_PATH) candidates.push(process.env.PLAYWRIGHT_NODE_PATH);
  if (process.env.NODE_PATH) candidates.push(...process.env.NODE_PATH.split(path.delimiter));
  candidates.push(path.join(os.homedir(), ".cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules"));

  try {
    return require("playwright");
  } catch {
    for (const base of candidates.filter(Boolean)) {
      try {
        return require(path.join(base, "playwright"));
      } catch {
        // Try the next configured module root.
      }
    }
  }
  throw new Error("Cannot load playwright. Set NODE_PATH or PLAYWRIGHT_NODE_PATH to a node_modules directory containing playwright.");
}

function defaultChromePath() {
  const macChrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
  return fs.existsSync(macChrome) ? macChrome : undefined;
}

function round(value) {
  return Number.isFinite(value) ? Math.round(value * 10) / 10 : null;
}

function statusFromIssues(issues) {
  return issues.length === 0 ? "PASS" : "FAIL";
}

async function main() {
  const args = parseArgs(process.argv);
  if (args.help || (!args.html && !args.url)) {
    console.log(usage());
    process.exit(args.help ? 0 : 2);
  }

  const htmlPath = args.html ? path.resolve(args.html) : null;
  if (htmlPath && !fs.existsSync(htmlPath)) throw new Error(`HTML file not found: ${htmlPath}`);

  const outDir = path.resolve(args.out || path.join(path.dirname(htmlPath || process.cwd()), "screenshot"));
  fs.mkdirSync(outDir, { recursive: true });

  const { chromium } = loadPlaywright();
  const executablePath = process.env.CHROME_EXECUTABLE_PATH || defaultChromePath();
  const browser = await chromium.launch({
    headless: true,
    executablePath,
  });

  const page = await browser.newPage({
    viewport: { width: 1600, height: 2400 },
    deviceScaleFactor: 1,
  });

  const targetUrl = args.url || pathToFileURL(htmlPath).href;
  await page.goto(targetUrl, { waitUntil: "networkidle" });
  await page.evaluate(() => document.fonts && document.fonts.ready);

  const pageHandles = await page.$$(".page");
  if (pageHandles.length === 0) throw new Error("No .page elements found.");

  for (let i = 0; i < pageHandles.length; i += 1) {
    await pageHandles[i].screenshot({ path: path.join(outDir, `two-column-strict-page-${String(i + 1).padStart(2, "0")}.png`) });
  }

  const metrics = await page.evaluate(() => {
    const px = (value) => Math.round(value * 10) / 10;
    const rectObj = (r) => ({ left: r.left, right: r.right, top: r.top, bottom: r.bottom, width: r.width, height: r.height });
    const pages = Array.from(document.querySelectorAll(".page"));

    function textRects(root) {
      const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
        acceptNode(node) {
          return node.nodeValue && node.nodeValue.trim() ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT;
        },
      });
      const rects = [];
      while (walker.nextNode()) {
        const range = document.createRange();
        range.selectNodeContents(walker.currentNode);
        for (const rect of Array.from(range.getClientRects())) {
          if (rect.width > 0.5 && rect.height > 0.5) rects.push(rectObj(rect));
        }
        range.detach();
      }
      return rects;
    }

    function elementRects(root) {
      return Array.from(root.querySelectorAll("img, table, figure, .table-wrapper, .side-by-side-figures"))
        .map((el) => rectObj(el.getBoundingClientRect()))
        .filter((r) => r.width > 0.5 && r.height > 0.5);
    }

    function pageRects(pageEl) {
      const content = pageEl.querySelector(".page-content");
      const footer = pageEl.querySelector(".page-footer");
      const header = pageEl.querySelector(".page-header");
      const pRect = rectObj(pageEl.getBoundingClientRect());
      const cRect = content ? rectObj(content.getBoundingClientRect()) : pRect;
      const fRect = footer ? rectObj(footer.getBoundingClientRect()) : { top: pRect.bottom, bottom: pRect.bottom, left: pRect.left, right: pRect.right, width: pRect.width, height: 0 };
      const hRect = header ? rectObj(header.getBoundingClientRect()) : null;
      const blocks = content ? elementRects(content) : [];
      const rawRects = content ? [...textRects(content), ...blocks] : [];
      const rects = rawRects.filter((r) => r.bottom > cRect.top - 2 && r.top < fRect.top + 20);
      return { pRect, cRect, fRect, hRect, rects, blocks, textOnly: content ? textRects(content) : [] };
    }

    function columnMetrics(cRect, fRect, rects) {
      const center = cRect.left + cRect.width / 2;
      const narrow = rects.filter((r) => r.width < cRect.width * 0.62 && r.height < cRect.height * 0.35);
      const leftRects = narrow.filter((r) => (r.left + r.right) / 2 < center - 2);
      const rightRects = narrow.filter((r) => (r.left + r.right) / 2 > center + 2);
      const leftBottom = leftRects.length ? Math.max(...leftRects.map((r) => r.bottom)) : null;
      const rightBottom = rightRects.length ? Math.max(...rightRects.map((r) => r.bottom)) : null;
      const leftTop = leftRects.length ? Math.min(...leftRects.map((r) => r.top)) : null;
      const rightTop = rightRects.length ? Math.min(...rightRects.map((r) => r.top)) : null;
      return {
        left_bottom_gap_px: leftBottom === null ? null : px(fRect.top - leftBottom),
        right_bottom_gap_px: rightBottom === null ? null : px(fRect.top - rightBottom),
        bottom_delta_px: leftBottom === null || rightBottom === null ? null : px(Math.abs(leftBottom - rightBottom)),
        top_delta_px: leftTop === null || rightTop === null ? null : px(Math.abs(leftTop - rightTop)),
        left_line_count: leftRects.length,
        right_line_count: rightRects.length,
      };
    }

    function sFlowStatus(pageEl, cRect, rects) {
      const hasExplicitColumns = Boolean(pageEl.querySelector(".intro-explicit, .first-page-introduction, .column-left, .column-right, .left-column, .right-column"));
      const hasFullWidthBlocks = Boolean(pageEl.querySelector(".figure-wide, .wide-table, .table-wrapper, .side-by-side-figures"));
      if (hasExplicitColumns || hasFullWidthBlocks) {
        return { status: "SKIPPED", violations: 0, reason: hasExplicitColumns ? "explicit column control" : "full-width structured block" };
      }
      const center = cRect.left + cRect.width / 2;
      const lineRects = rects
        .filter((r) => r.width < cRect.width * 0.62 && r.height < 40)
        .map((r) => ({ zone: (r.left + r.right) / 2 < center ? "left" : "right", top: r.top, bottom: r.bottom }))
        .filter((r) => r.zone === "left" || r.zone === "right");
      let sawRight = false;
      let violations = 0;
      for (const r of lineRects) {
        if (r.zone === "right") sawRight = true;
        if (sawRight && r.zone === "left") violations += 1;
      }
      return { status: violations === 0 ? "PASS" : "FAIL", violations };
    }

    function firstIntroMetrics(pageEl, fRect) {
      const intro = pageEl.querySelector(".first-page-introduction, .intro-explicit, [data-first-page-introduction]");
      if (!intro) return null;
      const iRect = rectObj(intro.getBoundingClientRect());
      const rects = textRects(intro);
      const columns = columnMetrics(iRect, fRect, rects);
      const minGap = Math.min(
        columns.left_bottom_gap_px ?? Number.POSITIVE_INFINITY,
        columns.right_bottom_gap_px ?? Number.POSITIVE_INFINITY,
      );
      return {
        ...columns,
        footer_safety_px: Number.isFinite(minGap) ? px(minGap) : null,
        visual_safe: Number.isFinite(minGap) && minGap >= 24 && (columns.bottom_delta_px ?? 999) <= 2,
      };
    }

    function footerMetrics(pageEl) {
      const footer = pageEl.querySelector(".page-footer");
      const pageNum = pageEl.querySelector(".page-footer .page-num");
      if (!footer) return { footer_present: false };
      const fRect = rectObj(footer.getBoundingClientRect());
      const nRect = pageNum ? rectObj(pageNum.getBoundingClientRect()) : null;
      const text = footer.innerText || footer.textContent || "";
      return {
        footer_present: true,
        footer_text: text.trim(),
        page_num_present: Boolean(pageNum),
        page_num_right_delta_px: nRect ? px(Math.abs(fRect.right - nRect.right)) : null,
        footer_page_number_right_aligned: Boolean(nRect && Math.abs(fRect.right - nRect.right) <= 1.5),
        footer_page_number_appended_to_url: !pageNum || (nRect ? nRect.left < fRect.right - 80 : true),
      };
    }

    function finalReferenceStretch(pageEl) {
      const refs = pageEl.querySelector(".references");
      if (!refs) return false;
      const style = getComputedStyle(refs);
      const fontSize = parseFloat(style.fontSize) || 1;
      const lineHeight = style.lineHeight === "normal" ? fontSize * 1.2 : parseFloat(style.lineHeight);
      return lineHeight / fontSize > 1.75;
    }

    const pageMetrics = pages.map((pageEl, index) => {
      const { pRect, cRect, fRect, rects, blocks } = pageRects(pageEl);
      const maxBottom = rects.length ? Math.max(...rects.map((r) => r.bottom)) : cRect.top;
      const xRects = blocks;
      const maxRight = xRects.length ? Math.max(...xRects.map((r) => r.right)) : cRect.right;
      const minLeft = xRects.length ? Math.min(...xRects.map((r) => r.left)) : cRect.left;
      const footer = footerMetrics(pageEl);
      const columns = columnMetrics(cRect, fRect, rects);
      const firstIntro = index === 0 ? firstIntroMetrics(pageEl, fRect) : null;
      const hasFullWidthBlocks = Boolean(pageEl.querySelector(".figure-wide, .wide-table, .table-wrapper, .side-by-side-figures"));
      const columnAlignmentApplicable = !hasFullWidthBlocks && index !== pages.length - 1;
      const sFlow = sFlowStatus(pageEl, cRect, rects);
      return {
        page: index + 1,
        is_final_page: index === pages.length - 1,
        overflow_px: px(Math.max(0, maxBottom - fRect.top)),
        overflow_x_px: px(Math.max(0, maxRight - pRect.right, pRect.left - minLeft)),
        whitespace_px: px(Math.max(0, fRect.top - maxBottom)),
        ...columns,
        column_alignment_applicable: columnAlignmentApplicable,
        has_full_width_blocks: hasFullWidthBlocks,
        ...footer,
        s_flow: sFlow,
        first_page_intro_flow: firstIntro,
        final_reference_inline_stretch: index === pages.length - 1 ? finalReferenceStretch(pageEl) : false,
      };
    });

    const bodySupCitations = Array.from(document.querySelectorAll(".page-content.two-column sup, .two-column.flow-strict sup"))
      .filter((sup) => /^\s*\d+(?:\s*[,;-]\s*\d+)*\s*$/.test(sup.textContent || "")).length;
    const referencesWithJMarker = Array.from(document.querySelectorAll(".references div"))
      .filter((ref) => /\[J\]/.test(ref.textContent || "")).length;

    return {
      generated_at: new Date().toISOString(),
      page_count: pages.length,
      pages: pageMetrics,
      format_issues: {
        footer_page_number_right_aligned: pageMetrics.every((p) => p.footer_page_number_right_aligned),
        footer_page_number_appended_to_url: pageMetrics.some((p) => p.footer_page_number_appended_to_url),
        first_page_intro_visual_safe: pageMetrics[0]?.first_page_intro_flow ? pageMetrics[0].first_page_intro_flow.visual_safe : null,
        first_page_intro_outside_footer: pageMetrics[0]?.first_page_intro_flow ? Math.max(0, 24 - pageMetrics[0].first_page_intro_flow.footer_safety_px) : null,
        body_paragraph_sup_citations: bodySupCitations,
        references_with_J_marker: referencesWithJMarker,
        final_reference_inline_stretch: pageMetrics.some((p) => p.final_reference_inline_stretch),
      },
    };
  });

  const failures = [];
  for (const p of metrics.pages) {
    if (p.overflow_px > 0) failures.push(`P${p.page}: overflow_px=${p.overflow_px}`);
    if (p.overflow_x_px > 0) failures.push(`P${p.page}: overflow_x_px=${p.overflow_x_px}`);
    if (!p.is_final_page && p.whitespace_px >= 57) failures.push(`P${p.page}: whitespace_px=${p.whitespace_px}`);
    if (p.column_alignment_applicable && p.bottom_delta_px !== null && p.bottom_delta_px > 13) failures.push(`P${p.page}: bottom_delta_px=${p.bottom_delta_px}`);
    if (p.page === 1 && p.first_page_intro_flow && !p.first_page_intro_flow.visual_safe) failures.push(`P1: first_page_intro visual safety failed`);
    if (!p.footer_page_number_right_aligned) failures.push(`P${p.page}: footer page number is not right aligned`);
    if (p.footer_page_number_appended_to_url) failures.push(`P${p.page}: footer page number appears appended to URL`);
    if (p.s_flow?.status === "FAIL") failures.push(`P${p.page}: S-flow violations=${p.s_flow.violations}`);
    if (p.is_final_page && p.final_reference_inline_stretch) failures.push(`P${p.page}: final references line-height appears stretched`);
  }
  if (metrics.format_issues.body_paragraph_sup_citations > 0) failures.push(`body sup citation count=${metrics.format_issues.body_paragraph_sup_citations}`);
  if (metrics.format_issues.references_with_J_marker > 0) failures.push(`references [J] marker count=${metrics.format_issues.references_with_J_marker}`);

  metrics.strict_column_result = statusFromIssues(failures);
  metrics.failures = failures;

  const metricsPath = path.join(outDir, "two-column-strict-metrics.json");
  fs.writeFileSync(metricsPath, `${JSON.stringify(metrics, null, 2)}\n`);

  await browser.close();

  console.log(`CP3 metrics: ${metrics.strict_column_result}`);
  console.log(`Metrics JSON: ${metricsPath}`);
  if (failures.length) {
    for (const failure of failures) console.error(`FAIL: ${failure}`);
    process.exit(1);
  }
}

main().catch((error) => {
  console.error(error.stack || error.message);
  process.exit(1);
});
