import fs from 'node:fs';
import path from 'node:path';
import { Project, serializationUtils } from 'ontouml-js';

const outPath = process.argv[2] || 'research/wave2/commentium-v2-candidate-v0.3.ontouml.json';

const project = new Project();
project.id = 'commentium-v2-candidate-v0.3';
project.name.add('Commentium v2 Candidate Model v0.3');
project.namespace = 'https://w3id.org/commentium/model/v2/';
project.languages = ['en'];
project.acronyms = ['Commentium'];

const model = project.packageBuilder().root().id('core').name('Commentium Core').build();

function cls(id, stereotype, opts = {}) {
  let b = model.classBuilder().id(id).name(opts.name || id).stereotype(stereotype);
  if (opts.derived) b = b.derived();
  return b.build();
}

const C = {
  Comment: cls('Comment', 'event'),
  Response: cls('Response', 'event'),
  CommentThread: cls('CommentThread', 'event'),
  Commentable: cls('Commentable', 'historicalRoleMixin', { derived: true }),
  Agent: cls('Agent', 'category'),
  Commenter: cls('Commenter', 'historicalRoleMixin', { derived: true }),
  IntendedAudience: cls('IntendedAudience', 'roleMixin', { derived: true }),
  CommentSubject: cls('CommentSubject', 'roleMixin', { derived: true }),
  ReferencedEntity: cls('ReferencedEntity', 'roleMixin', { derived: true }),
  Interpretation: cls('Interpretation', 'event'),
  InterpretedMeaning: cls('InterpretedMeaning', 'kind'),
  InterpretiveAssumption: cls('InterpretiveAssumption', 'kind'),
  AssertedRelation: cls('AssertedRelation', 'kind'),
  AssertedRelationKind: cls('AssertedRelationKind', 'enumeration'),
  InteractionNorm: cls('InteractionNorm', 'kind'),
  Situation: cls('Situation', 'situation'),
  Medium: cls('Medium', 'category'),
  CommentMessage: cls('CommentMessage', 'kind'),
  Intent: cls('Intent', 'mode'),
  Stance: cls('Stance', 'mode'),
  ExpressionStyle: cls('ExpressionStyle', 'quality'),
  Time: cls('Time', 'datatype')
};

model.generalizationBuilder().id('gen_Response_Comment').general(C.Comment).specific(C.Response).name('Response specializes Comment').build();
model.generalizationBuilder().id('gen_Commenter_Agent').general(C.Agent).specific(C.Commenter).name('Commenter specializes Agent').build();

for (const lit of ['praises','criticizes','supports','disagreesWith','questions','clarifies','cites','mentions','requests','reports']) {
  C.AssertedRelationKind.literalBuilder().id(`ark_${lit}`).name(lit).build();
}

function relation(id, name, source, target, opts = {}) {
  let b = model.binaryRelationBuilder().id(id).name(name).source(source).target(target);
  if (opts.stereotype) b = b.stereotype(opts.stereotype);
  if (opts.derived) b = b.derived();
  if (opts.sourceCardinality) b = b.sourceCardinality(opts.sourceCardinality);
  if (opts.targetCardinality) b = b.targetCardinality(opts.targetCardinality);
  return b.build();
}

relation('rel_hasMessage', 'hasMessage', C.Comment, C.CommentMessage, {
  stereotype: 'creation', sourceCardinality: '0..1', targetCardinality: '1'
});

// OntoUML participation is formally oriented Endurant -> Event.
// OWL v2 will expose user-facing inverses: anchoredTo, via, hasCommenter, performedBy.
relation('rel_anchors', 'anchors', C.Commentable, C.Comment, {
  stereotype: 'participation', sourceCardinality: '1..*', targetCardinality: '0..*'
});
relation('rel_mediumParticipatesIn', 'mediumParticipatesIn', C.Medium, C.Comment, {
  stereotype: 'participation', sourceCardinality: '1..*', targetCardinality: '0..*'
});
relation('rel_authors', 'authors', C.Commenter, C.Comment, {
  stereotype: 'participation', sourceCardinality: '1..*', targetCardinality: '0..*'
});

relation('rel_occursIn', 'occursIn', C.Comment, C.Situation, {
  sourceCardinality: '0..*', targetCardinality: '1..*'
});
relation('rel_hasTime', 'hasTime', C.Comment, C.Time, {
  sourceCardinality: '0..*', targetCardinality: '1'
});
relation('rel_styleInheresIn', 'styleInheresIn', C.ExpressionStyle, C.CommentMessage, {
  stereotype: 'characterization', sourceCardinality: '0..*', targetCardinality: '1'
});
relation('rel_respondsTo', 'respondsTo', C.Response, C.Comment, {
  stereotype: 'historicalDependence', sourceCardinality: '0..*', targetCardinality: '1..*'
});
relation('rel_partOfThread', 'partOfThread', C.Comment, C.CommentThread, {
  stereotype: 'participational', sourceCardinality: '1..*', targetCardinality: '0..1'
});

relation('rel_addresses', 'addresses', C.Comment, C.IntendedAudience, {
  derived: true, sourceCardinality: '0..*', targetCardinality: '0..*'
});
relation('rel_isAbout', 'isAbout', C.Comment, C.CommentSubject, {
  derived: true, sourceCardinality: '0..*', targetCardinality: '0..*'
});
relation('rel_refersTo', 'refersTo', C.CommentMessage, C.ReferencedEntity, {
  derived: true, sourceCardinality: '0..*', targetCardinality: '0..*'
});

relation('rel_intentInheresIn', 'intentInheresIn', C.Intent, C.Agent, {
  stereotype: 'characterization', sourceCardinality: '0..*', targetCardinality: '1'
});
relation('rel_stanceInheresIn', 'stanceInheresIn', C.Stance, C.Agent, {
  stereotype: 'characterization', sourceCardinality: '0..*', targetCardinality: '1'
});
relation('rel_motivatedBy', 'motivatedBy', C.Comment, C.Intent, {
  sourceCardinality: '0..*', targetCardinality: '0..*'
});
relation('rel_reflects', 'reflects', C.Comment, C.Stance, {
  stereotype: 'manifestation', sourceCardinality: '0..*', targetCardinality: '0..*'
});
relation('rel_governedBy', 'governedBy', C.Situation, C.InteractionNorm, {
  sourceCardinality: '0..*', targetCardinality: '0..*'
});

relation('rel_performsInterpretation', 'performsInterpretation', C.Agent, C.Interpretation, {
  stereotype: 'participation', sourceCardinality: '1..*', targetCardinality: '0..*'
});
relation('rel_messageParticipatesInInterpretation', 'messageParticipatesInInterpretation', C.CommentMessage, C.Interpretation, {
  stereotype: 'participation', sourceCardinality: '1', targetCardinality: '0..*'
});
relation('rel_producesMeaning', 'producesMeaning', C.Interpretation, C.InterpretedMeaning, {
  stereotype: 'creation', sourceCardinality: '0..1', targetCardinality: '1..*'
});
relation('rel_assumptionUsedIn', 'assumptionUsedIn', C.InterpretiveAssumption, C.Interpretation, {
  stereotype: 'participation', sourceCardinality: '0..*', targetCardinality: '0..*'
});
relation('rel_groundedIn', 'groundedIn', C.InterpretedMeaning, C.InterpretiveAssumption, {
  sourceCardinality: '0..*', targetCardinality: '0..*'
});

relation('rel_assertedIn', 'assertedIn', C.AssertedRelation, C.CommentMessage, {
  sourceCardinality: '0..*', targetCardinality: '1'
});
relation('rel_involvesSubject', 'involvesSubject', C.AssertedRelation, C.CommentSubject, {
  sourceCardinality: '0..*', targetCardinality: '0..*'
});
relation('rel_involvesReference', 'involvesReference', C.AssertedRelation, C.ReferencedEntity, {
  sourceCardinality: '0..*', targetCardinality: '0..*'
});
relation('rel_typedAs', 'typedAs', C.AssertedRelation, C.AssertedRelationKind, {
  sourceCardinality: '0..*', targetCardinality: '1'
});

// serialize() validates against the official OntoUML JSON Schema before returning.
const json = serializationUtils.serialize(project, 2);
serializationUtils.parse(json);
fs.mkdirSync(path.dirname(outPath), { recursive: true });
fs.writeFileSync(outPath, `${json}\n`, 'utf8');
console.log(`Generated ${outPath}`);
console.log(`Core concepts: ${Object.keys(C).length}`);
console.log('ontouml-js schema validation: PASS');
console.log('ontouml-js parse round-trip: PASS');
