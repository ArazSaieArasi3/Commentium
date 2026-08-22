import fs from 'node:fs';
import path from 'node:path';
import Ajv2020 from 'ajv/dist/2020.js';
import addFormats from 'ajv-formats';
import schema from 'ontouml-schema';
import { serializationUtils } from 'ontouml-js';

const modelPath = process.argv[2] || 'research/wave2/commentium-v2-candidate-v0.3.ontouml.json';
const outDir = process.argv[3] || 'validation-results/ontouml';
fs.mkdirSync(outDir, { recursive: true });

const raw = fs.readFileSync(modelPath, 'utf8');
const project = JSON.parse(raw);

const summary = {
  model: modelPath,
  schemaId: schema.$id,
  schemaValidation: 'NOT_RUN',
  ontoumlJsValidation: 'NOT_RUN',
  roundTrip: 'NOT_RUN',
  server: { status: 'NOT_RUN', endpoint: 'https://api.ontouml.org/v1/verify', blockingErrors: null, issues: null }
};

let failed = false;

// 1) Direct official JSON Schema v1.0.2 validation.
const ajv = new Ajv2020({ allErrors: true, strict: false });
addFormats(ajv);
const validate = ajv.compile(schema);
if (!validate(project)) {
  summary.schemaValidation = 'FAIL';
  summary.schemaErrors = validate.errors;
  failed = true;
} else {
  summary.schemaValidation = 'PASS';
}

// 2) ontouml-js uses the same official exchange schema and provides parser checks.
const libValidation = serializationUtils.validate(raw);
if (libValidation !== true) {
  summary.ontoumlJsValidation = 'FAIL';
  summary.ontoumlJsErrors = libValidation;
  failed = true;
} else {
  summary.ontoumlJsValidation = 'PASS';
}
try {
  serializationUtils.parse(raw, true);
  summary.roundTrip = 'PASS';
} catch (error) {
  summary.roundTrip = 'FAIL';
  summary.roundTripError = String(error?.stack || error);
  failed = true;
}

// 3) Official OntoUML Server semantic/syntactical verification.
try {
  const response = await fetch(summary.server.endpoint, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ project, options: null }),
    signal: AbortSignal.timeout(60000)
  });
  const text = await response.text();
  let body;
  try { body = JSON.parse(text); } catch { body = { raw: text }; }
  fs.writeFileSync(path.join(outDir, 'ontouml-server-response.json'), JSON.stringify(body, null, 2) + '\n');
  summary.server.httpStatus = response.status;
  if (!response.ok) {
    summary.server.status = 'FAIL';
    summary.server.error = body;
    failed = true;
  } else {
    const issues = Array.isArray(body?.result) ? body.result : [];
    const blocking = issues.filter(i => String(i?.severity || '').toUpperCase() === 'ERROR');
    summary.server.status = blocking.length === 0 ? 'PASS' : 'FAIL';
    summary.server.blockingErrors = blocking.length;
    summary.server.issues = issues.length;
    summary.server.issueSeverities = issues.reduce((acc, i) => {
      const key = String(i?.severity || 'UNKNOWN').toUpperCase();
      acc[key] = (acc[key] || 0) + 1;
      return acc;
    }, {});
    if (blocking.length > 0) failed = true;
  }
} catch (error) {
  summary.server.status = 'UNAVAILABLE';
  summary.server.error = String(error?.stack || error);
  failed = true;
}

fs.writeFileSync(path.join(outDir, 'summary.json'), JSON.stringify(summary, null, 2) + '\n');
console.log(JSON.stringify(summary, null, 2));

if (failed) process.exit(2);
