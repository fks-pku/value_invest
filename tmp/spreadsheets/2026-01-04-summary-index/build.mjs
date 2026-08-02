import fs from "node:fs/promises";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const repoRoot = "D:/codex/value_invest";
const inputPath = `${repoRoot}/tmp/pdfs/2026-01-04/summaries.json`;
const outputDir = `${repoRoot}/outputs/2026-01-04-pdf-summary-index`;
const previewPath = `${repoRoot}/tmp/spreadsheets/2026-01-04-summary-index/preview.png`;

const rows = JSON.parse(await fs.readFile(inputPath, "utf8"));
if (!Array.isArray(rows) || rows.length !== 21) {
  throw new Error(`Expected 21 summary rows, got ${rows?.length}`);
}

const workbook = Workbook.create();
const sheet = workbook.worksheets.add("INDEX");
sheet.showGridLines = false;
sheet.freezePanes.freezeRows(1);

const matrix = [
  ["PDF_NAME", "SUMMARY"],
  ...rows.map((row) => [row.PDF_NAME, row.SUMMARY]),
];
sheet.getRange(`A1:B${matrix.length}`).values = matrix;

const header = sheet.getRange("A1:B1");
header.format = {
  fill: "#17365D",
  font: { bold: true, color: "#FFFFFF", size: 11 },
  horizontalAlignment: "left",
  verticalAlignment: "center",
  borders: { bottom: { style: "medium", color: "#17365D" } },
};
header.format.rowHeight = 28;

const body = sheet.getRange(`A2:B${matrix.length}`);
body.format = {
  font: { color: "#1F2937", size: 10 },
  verticalAlignment: "top",
  wrapText: true,
  borders: {
    insideHorizontal: { style: "thin", color: "#D9E2F3" },
    bottom: { style: "thin", color: "#D9E2F3" },
  },
};
body.format.rowHeight = 96;

sheet.getRange(`A2:A${matrix.length}`).format.fill = "#F4F7FB";
sheet.getRange(`A1:A${matrix.length}`).format.columnWidth = 68;
sheet.getRange(`B1:B${matrix.length}`).format.columnWidth = 108;

const table = sheet.tables.add(`A1:B${matrix.length}`, true, "PdfSummaryIndex");
table.style = "TableStyleMedium2";
table.showFilterButton = true;
table.showBandedRows = false;

await fs.mkdir(outputDir, { recursive: true });

const inspect = await workbook.inspect({
  kind: "table",
  range: `INDEX!A1:B${matrix.length}`,
  include: "values,formulas",
  tableMaxRows: 6,
  tableMaxCols: 2,
  tableMaxCellChars: 100,
  maxChars: 3500,
});
console.log(inspect.ndjson);

const formulaErrors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 50 },
  summary: "final formula error scan",
});
console.log(formulaErrors.ndjson);

const preview = await workbook.render({
  sheetName: "INDEX",
  range: `A1:B${matrix.length}`,
  scale: 1,
  format: "png",
});
await fs.writeFile(previewPath, new Uint8Array(await preview.arrayBuffer()));

const output = await SpreadsheetFile.exportXlsx(workbook);
const outputPath = `${outputDir}/PDF信息索引_2026-01-04.xlsx`;
await output.save(outputPath);
console.log(JSON.stringify({ outputPath, previewPath, rowCount: rows.length }));
