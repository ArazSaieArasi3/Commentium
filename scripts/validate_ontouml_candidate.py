#!/usr/bin/env python3
from pathlib import Path
from rdflib import Graph, Namespace, RDF, Literal

ONTOUML = Namespace("https://w3id.org/ontouml#")
C = Namespace("https://w3id.org/commentium/model/v2#")

def local(u):
    return str(u).split("#")[-1]

def relation_info(g, name):
    r = C[f"rel_{name}"]
    se = next(g.objects(r, ONTOUML.sourceEnd), None)
    te = next(g.objects(r, ONTOUML.targetEnd), None)
    def typ(e):
        x = next(g.objects(e, ONTOUML.propertyType), None)
        return local(x) if x else None
    def card(e):
        ca = next(g.objects(e, ONTOUML.cardinality), None)
        v = next(g.objects(ca, ONTOUML.cardinalityValue), None) if ca else None
        return str(v) if v else None
    st = next(g.objects(r, ONTOUML.stereotype), None)
    return typ(se), typ(te), card(se), card(te), local(st) if st else None

def main(path):
    g = Graph()
    g.parse(path, format="turtle")
    checks = []
    def check(label, cond, detail=""):
        checks.append((label, bool(cond), detail))

    classes = list(g.subjects(RDF.type, ONTOUML.Class))
    check("exactly 22 core classes", len(classes) == 22, f"found={len(classes)}")
    allowed = {"event", "historicalRoleMixin", "category", "roleMixin", "kind", "enumeration", "situation", "mode", "quality"}
    bad = []
    for c in classes:
        sts = list(g.objects(c, ONTOUML.stereotype))
        if len(sts) != 1 or local(sts[0]) not in allowed:
            bad.append((local(c), [local(x) for x in sts]))
    check("class stereotypes are in approved candidate set", not bad, str(bad))

    expected = {
        "Comment": "event", "Response": "event", "CommentThread": "event",
        "Commentable": "historicalRoleMixin", "Agent": "category",
        "Commenter": "historicalRoleMixin", "IntendedAudience": "roleMixin",
        "CommentSubject": "roleMixin", "ReferencedEntity": "roleMixin",
        "Interpretation": "event", "AssertedRelation": "kind",
        "AssertedRelationKind": "enumeration", "Medium": "category"
    }
    for n, st in expected.items():
        vals = list(g.objects(C[n], ONTOUML.stereotype))
        actual = local(vals[0]) if vals else None
        check(f"{n} stereotype", actual == st, actual or "missing")

    gens = {(local(s), local(o)) for gu in g.subjects(RDF.type, ONTOUML.Generalization)
            for s in g.objects(gu, ONTOUML.specific)
            for o in g.objects(gu, ONTOUML.general)}
    check("Response specializes Comment", ("Response", "Comment") in gens, str(gens))
    check("Commenter specializes Agent", ("Commenter", "Agent") in gens, str(gens))

    required_rel = {
        "anchoredTo": ("Comment", "Commentable", "participation"),
        "via": ("Comment", "Medium", "participation"),
        "partOfThread": ("Comment", "CommentThread", "participational"),
        "hasCommenter": ("Comment", "Commenter", "participation"),
        "performedBy": ("Interpretation", "Agent", "participation"),
        "styleInheresIn": ("ExpressionStyle", "CommentMessage", "characterization"),
        "intentInheresIn": ("Intent", "Agent", "characterization"),
        "stanceInheresIn": ("Stance", "Agent", "characterization"),
        "refersTo": ("CommentMessage", "ReferencedEntity", None),
        "governedBy": ("Situation", "InteractionNorm", None),
        "assertedIn": ("AssertedRelation", "CommentMessage", None),
    }
    for n, (s, t, st) in required_rel.items():
        inf = relation_info(g, n)
        ok = (inf[0], inf[1]) == (s, t) and (st is None or inf[4] == st)
        check(f"relation {n} endpoints/stereotype", ok, str(inf))

    names = {str(next(g.objects(r, ONTOUML.name), Literal(""))) for r in g.subjects(RDF.type, ONTOUML.Relation)}
    for forbidden in ["playedBy", "memberOf", "isAboutOrDirectedTo"]:
        check(f"forbidden relation absent: {forbidden}", forbidden not in names)
    check("five target semantics present", all(x in names for x in ["anchoredTo", "respondsTo", "isAbout", "refersTo", "addresses"]))

    for role, rel in [("Commentable", "anchoredTo"), ("Commenter", "hasCommenter"),
                      ("IntendedAudience", "addresses"), ("CommentSubject", "isAbout"),
                      ("ReferencedEntity", "refersTo")]:
        check(f"{role} has an explicit defining/grounding relation", relation_info(g, rel)[1] == role)

    relators = [c for c in classes if next(g.objects(c, ONTOUML.stereotype), None) == ONTOUML.relator]
    check("no relator-typed class remains", not relators, str([local(x) for x in relators]))
    check("AssertedRelationKind has 10 literals", len(list(g.objects(C.AssertedRelationKind, ONTOUML.literal))) == 10)

    cards = {
        "hasMessage": "1", "anchoredTo": "1..*", "occursIn": "1..*", "via": "1..*", "hasTime": "1",
        "respondsTo": "1..*", "partOfThread": "0..*", "hasCommenter": "1..*", "addresses": "0..*",
        "isAbout": "0..*", "refersTo": "0..*", "performedBy": "1..*", "interpretsMessage": "1",
        "producesMeaning": "1..*", "assertedIn": "1", "typedAs": "1"
    }
    for n, c in cards.items():
        check(f"{n} target cardinality", relation_info(g, n)[3] == c, relation_info(g, n)[3])

    failed = [x for x in checks if not x[1]]
    print(f"MODEL={path}")
    print(f"TRIPLES={len(g)}")
    print(f"CHECKS={len(checks)} PASS={len(checks)-len(failed)} FAIL={len(failed)}")
    for label, ok, detail in checks:
        print(("PASS" if ok else "FAIL") + f" | {label}" + (f" | {detail}" if detail else ""))
    return 1 if failed else 0

if __name__ == "__main__":
    import sys
    raise SystemExit(main(Path(sys.argv[1] if len(sys.argv) > 1 else "research/wave2/commentium-v2-candidate-v0.2.ontouml.ttl")))
