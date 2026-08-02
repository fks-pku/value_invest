import fs from "node:fs/promises";
import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const repoRoot = "D:/codex/value_invest";
const inputPath = `${repoRoot}/tmp/pdfs/2026-01-04/summaries.json`;
const workbookPath = `${repoRoot}/outputs/2026-01-04-pdf-summary-index/PDF信息索引_2026-01-04.xlsx`;
const previewPath = `${repoRoot}/tmp/spreadsheets/2026-01-04-summary-index/final_preview.png`;

const expectedRows = JSON.parse(await fs.readFile(inputPath, "utf8"));
const blob = await FileBlob.load(workbookPath);
const workbook = await SpreadsheetFile.importXlsx(blob);
const sheet = workbook.worksheets.getItem("INDEX");
const values = sheet.getRange("A1:B22").values;

if (values.length !== 22 || values[0][0] !== "PDF_NAME" || values[0][1] !== "SUMMARY") {
  throw new Error("Workbook dimensions or headers are incorrect");
}
for (let index = 0; index < expectedRows.length; index += 1) {
  const actual = values[index + 1];
  const expected = expectedRows[index];
  if (actual[0] !== expected.PDF_NAME || actual[1] !== expected.SUMMARY) {
    throw new Error(`Workbook value mismatch at row ${index + 2}`);
  }
}

const preview = await workbook.render({
  sheetName: "INDEX",
  range: "A1:B22",
  scale: 1,
  format: "png",
});
await fs.writeFile(previewPath, new Uint8Array(await preview.arrayBuffer()));
console.log(JSON.stringify({ verifiedRows: expectedRows.length, previewPath }));
