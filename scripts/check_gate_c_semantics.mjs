import fs from 'node:fs';
import path from 'node:path';

const modelPath = process.argv[2] || 'research/wave2/commentium-v2-candidate-v0.3.ontouml.json';
const outPath = process.argv[3] || 'validation-results/ontouml/gate-c-semantic-checks.json';
const project = JSON.parse(fs.readFileSync(modelPath, 'utf8'));
const elements = new Map(project.elements.map(e => [e.id, e]));
const classes = project.elements.filter(e => e.type === 'Class');
const relations = project.elements.filter(e => e.type === 'BinaryRelation');
const generalizations = project.elements.filter(e => e.type === 'Generalization');

const checks = [];
function check(id, condition, detail) {
  checks.push({ id, status: condition ? 'PASS' : 'FAIL', detail });
}
function C(id) { return elements.get(id); }
function R(id) { return elements.get(id); }
function relationEnds(id) {
  const r = R(id);
  return (r?.properties || []).map(pid => elements.get(pid));
}
function endpointTypes(id) {
  return relationEnds(id).map(p => p?.propertyType);
}
function cardinality(id, classId) {
  return relationEnds(id).find(p => p?.propertyType === classId)?.cardinality;
}

const expectedStereotypes = {
  Comment: 'event', Response: 'event', CommentThread: 'event',
  Commentable: 'historicalRoleMixin', Agent: 'category', Commenter: 'historicalRoleMixin',
  IntendedAudience: 'roleMixin', CommentSubject: 'roleMixin', ReferencedEntity: 'roleMixin',
  Interpretation: 'event', InterpretedMeaning: 'kind', InterpretiveAssumption: 'kind',
  AssertedRelation: 'kind', AssertedRelationKind: 'enumeration', InteractionNorm: 'kind',
  Situation: 'situation', Medium: 'category', CommentMessage: 'kind', Intent: 'mode',
  Stance: 'mode', ExpressionStyle: 'quality', Time: 'datatype'
};

check('core-count', classes.length === 22, `found ${classes.length} Core classes`);
for (const [id, stereotype] of Object.entries(expectedStereotypes)) {
  check(`stereotype:${id}`, C(id)?.stereotype === stereotype, `${id}=${C(id)?.stereotype}; expected ${stereotype}`);
}

check('response-specialization', generalizations.some(g => g.general === 'Comment' && g.specific === 'Response'), 'Response specializes Comment');
check('commenter-agent-specialization', generalizations.some(g => g.general === 'Agent' && g.specific === 'Commenter'), 'Commenter specializes Agent category');
check('no-relator-class-drift', !classes.some(c => c.stereotype === 'relator'), 'No v0.3 Core class is incorrectly retained as a relator');
check('thread-not-collective', C('CommentThread')?.stereotype === 'event', 'CommentThread is a complex event, not a collective');
check('time-not-quality', C('Time')?.stereotype === 'datatype', 'Time is a temporal value/qualification datatype');

const forbiddenRelations = ['playedBy', 'memberOf', 'isAboutOrDirectedTo'];
for (const name of forbiddenRelations) {
  check(`legacy-absent:${name}`, !relations.some(r => r.name?.en === name), `${name} absent`);
}

for (const id of ['rel_anchors','rel_mediumParticipatesIn','rel_authors','rel_performsInterpretation','rel_messageParticipatesInInterpretation','rel_assumptionUsedIn']) {
  const r = R(id); const [s,t] = endpointTypes(id);
  check(`participation-stereotype:${id}`, r?.stereotype === 'participation', `${id} uses participation`);
  check(`participation-orientation:${id}`, C(s)?.restrictedTo?.includes('functional-complex') && C(t)?.restrictedTo?.includes('event'), `${s} (endurant) -> ${t} (event)`);
}

for (const id of ['rel_hasMessage','rel_producesMeaning']) {
  const r = R(id); const [s,t] = endpointTypes(id);
  check(`creation-stereotype:${id}`, r?.stereotype === 'creation', `${id} uses creation`);
  check(`creation-orientation:${id}`, C(s)?.restrictedTo?.includes('event') && C(t)?.restrictedTo?.includes('functional-complex'), `${s} (event) -> ${t} (endurant)`);
}

for (const id of ['rel_styleInheresIn','rel_intentInheresIn','rel_stanceInheresIn']) {
  const r = R(id); const [s,t] = endpointTypes(id);
  const aspect = C(s)?.restrictedTo || [];
  check(`characterization-stereotype:${id}`, r?.stereotype === 'characterization', `${id} uses characterization`);
  check(`characterization-orientation:${id}`, (aspect.includes('quality') || aspect.includes('intrinsic-mode')) && C(t)?.restrictedTo?.includes('functional-complex'), `${s} (intrinsic aspect) -> ${t} (bearer)`);
}

check('participational-thread', R('rel_partOfThread')?.stereotype === 'participational' && endpointTypes('rel_partOfThread').every(x => C(x)?.restrictedTo?.includes('event')), 'Comment and CommentThread are events in event decomposition');
check('manifestation-stance', R('rel_reflects')?.stereotype === 'manifestation' && endpointTypes('rel_reflects')[0] === 'Comment' && endpointTypes('rel_reflects')[1] === 'Stance', 'Comment event manifests Stance');

const fiveSemantics = ['rel_anchors','rel_respondsTo','rel_isAbout','rel_refersTo','rel_addresses'];
check('five-target-semantics-present', fiveSemantics.every(id => R(id)), 'anchor, reply, aboutness, reference, audience all present');
check('five-target-semantics-distinct', new Set(fiveSemantics.map(id => R(id)?.id)).size === 5, 'five semantics are distinct relations');

check('commentable-grounded', endpointTypes('rel_anchors')[0] === 'Commentable' && R('rel_anchors')?.stereotype === 'participation', 'Commentable historical role is grounded by participation in Comment event');
check('commenter-grounded', endpointTypes('rel_authors')[0] === 'Commenter' && R('rel_authors')?.stereotype === 'participation', 'Commenter historical role is grounded by participation in Comment event');
check('audience-derived-view', C('IntendedAudience')?.isDerived === true && R('rel_addresses')?.isDerived === true, 'IntendedAudience is explicitly treated as a derived semantic view');
check('subject-derived-view', C('CommentSubject')?.isDerived === true && R('rel_isAbout')?.isDerived === true, 'CommentSubject is explicitly treated as a derived semantic view');
check('reference-derived-view', C('ReferencedEntity')?.isDerived === true && R('rel_refersTo')?.isDerived === true, 'ReferencedEntity is explicitly treated as a derived semantic view');
check('no-artificial-relator-for-derived-views', !classes.some(c => ['AudienceRelator','SubjectRelator','ReferenceRelator'].includes(c.id)), 'No artificial relator introduced to silence FreeRole-like warnings');

const cardinalities = [
  ['rel_anchors','Commentable','1..*'], ['rel_authors','Commenter','1..*'],
  ['rel_hasMessage','CommentMessage','1'], ['rel_hasTime','Time','1'],
  ['rel_partOfThread','CommentThread','0..1'], ['rel_producesMeaning','InterpretedMeaning','1..*'],
  ['rel_assertedIn','CommentMessage','1'], ['rel_typedAs','AssertedRelationKind','1']
];
for (const [rel, end, expected] of cardinalities) {
  check(`cardinality:${rel}:${end}`, cardinality(rel,end) === expected, `${rel} ${end} end=${cardinality(rel,end)}; expected ${expected}`);
}

const failed = checks.filter(c => c.status === 'FAIL');
const report = {
  model: modelPath,
  methodology: 'Deterministic Gate C checks derived from Commentium decisions and current OntoUML stereotype semantics; targeted anti-pattern guardrails, not a substitute for unavailable legacy server anti-pattern tooling.',
  total: checks.length,
  passed: checks.length - failed.length,
  failed: failed.length,
  checks
};
fs.mkdirSync(path.dirname(outPath), { recursive: true });
fs.writeFileSync(outPath, JSON.stringify(report, null, 2) + '\n');
console.log(`Gate C semantic checks: ${report.passed}/${report.total} PASS; ${report.failed} FAIL`);
if (failed.length) {
  console.error(JSON.stringify(failed, null, 2));
  process.exit(2);
}
