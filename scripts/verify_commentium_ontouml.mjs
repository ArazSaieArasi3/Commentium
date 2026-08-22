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
const endpoints = [
  'https://api.ontouml.org/v1/verify',
  'http://api.ontouml.org/v1/verify',
  'http://api.ontouml.org:3001/v1/verify'
];

const summary = {
  model: modelPath,
  schemaId: schema.$id,
  schemaValidation: 'NOT_RUN',
  ontoumlJsValidation: 'NOT_RUN',
  roundTrip: 'NOT_RUN',
  server: { status: 'NOT_RUN', endpoint: null, attempts: [], blockingErrors: null, issues: null }
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

// 2) Current ontouml-js validation and round trip.
try {
  serializationUtils.validate(raw);
  summary.ontoumlJsValidation = 'PASS';
} catch (error) {
  summary.ontoumlJsValidation = 'FAIL';
  summary.ontoumlJsErrors = String(error?.stack || error);
  failed = true;
}
try {
  serializationUtils.parse(raw);
  summary.roundTrip = 'PASS';
} catch (error) {
  summary.roundTrip = 'FAIL';
  summary.roundTripError = String(error?.stack || error);
  failed = true;
}

// 3) Probe documented OntoUML Server endpoints. The deployed server is an
// advisory/legacy service; current schema/toolchain validation above is normative
// for this workflow. Server unavailability is recorded but is not reclassified
// as a model defect.
let serverSucceeded = false;
for (const endpoint of endpoints) {
  const attempt = { endpoint, status: 'NOT_RUN' };
  try {
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ project, options: null }),
      signal: AbortSignal.timeout(30000),
      redirect: 'follow'
    });
    const text = await response.text();
    let body;
    try { body = JSON.parse(text); } catch { body = { raw: text }; }
    attempt.httpStatus = response.status;
    attempt.status = response.ok ? 'REACHABLE' : 'HTTP_ERROR';
    attempt.response = body;
    summary.server.attempts.push(attempt);
    if (!response.ok) continue;

    const issues = Array.isArray(body?.result)
      ? body.result
      : (Array.isArray(body?.issues) ? body.issues : []);
    const blocking = issues.filter(i => String(i?.severity || '').toUpperCase() === 'ERROR');
    summary.server.endpoint = endpoint;
    summary.server.status = blocking.length === 0 ? 'PASS' : 'FAIL';
    summary.server.blockingErrors = blocking.length;
    summary.server.issues = issues.length;
    summary.server.issueSeverities = issues.reduce((acc, i) => {
      const key = String(i?.severity || 'UNKNOWN').toUpperCase();
      acc[key] = (acc[key] || 0) + 1;
      return acc;
    }, {});
    fs.writeFileSync(path.join(outDir, 'ontouml-server-response.json'), JSON.stringify(body, null, 2) + '\n');
    serverSucceeded = true;
    if (blocking.length > 0) failed = true;
    break;
  } catch (error) {
    attempt.status = 'UNAVAILABLE';
    attempt.error = String(error?.message || error);
    summary.server.attempts.push(attempt);
  }
}

if (!serverSucceeded) {
  summary.server.status = 'UNAVAILABLE_OR_INCOMPATIBLE';
  summary.server.note = 'All documented current/legacy server endpoints were unavailable or returned HTTP errors. Current OntoUML Schema 1.0.2 + ontouml-js 1.0.0 validation remains independently recorded.';
}

fs.writeFileSync(path.join(outDir, 'summary.json'), JSON.stringify(summary, null, 2) + '\n');
console.log(JSON.stringify(summary, null, 2));

if (failed) process.exit(2);
