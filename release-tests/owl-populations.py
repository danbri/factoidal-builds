#!/usr/bin/env python3
"""owl-populations.py: the W3C OWL 2 Test Cases as discrete populations, run on the
built-in OWL engine (core's l4owl-probe).

The corpus is third_party/testing/owl/all.rdf in factoidal-core: the W3C OWL 2 Test
Cases export of 2009-11-18 (https://www.w3.org/2009/11/owl-test/, every test case whose
status is not Rejected: Approved, Proposed, Extracredit and cases with no status;
W3C Document Licence). A population is one kind of question the corpus asks:

  type x semantics   PositiveEntailmentTest, NegativeEntailmentTest, ConsistencyTest,
                     InconsistencyTest, each under the Direct Semantics (DIRECT) and under
                     the RDF-Based Semantics (RDF-BASED). A case typed with two types (or
                     annotated with both semantics) counts once in each population.
  profile            ProfileIdentificationTest, one population per profile EL, QL, RL: every
                     such case asks whether its ontology is in the profile (yes when
                     test:profile names it). The probe's `--profile-id` mode gives the verdict
                     (the OWL 2 DL species check, then the profile's grammar over the axioms
                     read back from the RDF graph); "undecided" (a graph the reader cannot
                     place) is counted as other. A probe without the mode prints no line, and
                     the population is then listed with its official size and none run.
  species            test:species DL / FULL (OWL 2 DL syntax membership): core's
                     lean-scoreboard l4owl-probe-species job, recorded by release-tests.

Every population's denominator is its full official count in all.rdf, whatever the
engine runs; "run" is the units the engine decided (pass + fail), so the share run shows.

  owl-populations.py official --catalog all.rdf [--out official.json]
  owl-populations.py run --probe BIN --catalog all.rdf --work DIR [--refute-ms 3000] [--timeout 2400]

`run` writes DIR/owl2-{direct,rdfbased}-{approved,proposed,extracredit,nostatus}.rdf (the
catalog's test cases with that semantics and status, every other element kept byte for
byte) and DIR/owl2-all-{status}.rdf (every case of that status), runs the probe once per
semantics (`--dl` for DIRECT, `--rdf-based` for RDF-BASED, two processes at once) and then
once with `--profile-id` over the owl2-all files, and writes DIR/populations.json: per population the official
count, pass, fail, other, run, and the same split by status.
"""
import argparse, collections, json, os, re, subprocess, sys, time
import xml.etree.ElementTree as ET

T = "http://www.w3.org/2007/OWL/testOntology#"
R = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
TYPES = ["PositiveEntailmentTest", "NegativeEntailmentTest", "ConsistencyTest", "InconsistencyTest"]
SEMANTICS = {"direct": "DIRECT", "rdfbased": "RDF-BASED"}
STATUSES = {"approved": "Approved", "proposed": "Proposed", "extracredit": "Extracredit", "nostatus": None}
PROFILES = ["EL", "QL", "RL"]
SOURCE = {"name": "W3C OWL 2 Test Cases", "url": "https://www.w3.org/2009/11/owl-test/",
          "published": "2009-11-18", "licence": "W3C Document Licence",
          "licence_url": "https://www.w3.org/Consortium/Legal/2015/doc-license",
          "file": "third_party/testing/owl/all.rdf", "selection": "every test case whose status is not Rejected"}


def cases(path):
    """(id, types, semantics, status, profiles, species) of every test:TestCase."""
    out = []
    for tc in ET.parse(path).getroot():
        if tc.tag != "{%s}TestCase" % T:
            continue
        res = lambda p: [e.get("{%s}resource" % R).split("#")[-1] for e in tc.findall("{%s}%s" % (T, p))
                         if e.get("{%s}resource" % R)]
        ident = (tc.findtext("{%s}identifier" % T) or tc.get("{%s}about" % R) or "").strip()
        types = [e.get("{%s}resource" % R).split("#")[-1] for e in tc.findall("{%s}type" % R)]
        st = res("status")
        out.append({"id": ident, "types": types, "semantics": res("semantics"), "status": st[0] if st else None,
                    "profiles": res("profile"), "species": res("species")})
    return out


def status_key(s):
    return next((k for k, v in STATUSES.items() if v == s), "nostatus")


def official(path):
    cs = cases(path)
    pops = {}

    def add(key, label, c):
        p = pops.setdefault(key, {"label": label, "total": 0, "by_status": collections.Counter()})
        p["total"] += 1
        p["by_status"][status_key(c["status"])] += 1

    for c in cs:
        for t in TYPES:
            if t in c["types"]:
                for k, s in SEMANTICS.items():
                    if s in c["semantics"]:
                        add(f"{t}/{k}", f"{t}, {s} semantics", c)
        if "ProfileIdentificationTest" in c["types"]:
            for p in PROFILES:
                add(f"ProfileIdentificationTest/{p}", f"ProfileIdentificationTest, profile {p}", c)
                if p in c["profiles"]:
                    pops[f"ProfileIdentificationTest/{p}"].setdefault("in_profile", 0)
                    pops[f"ProfileIdentificationTest/{p}"]["in_profile"] += 1
        if "DL" in c["species"]:
            add("species/DL", "species DL (the engine must say OWL 2 DL)", c)
        elif "FULL" in c["species"]:
            add("species/FULL-only", "species FULL only (the engine must say not OWL 2 DL)", c)
        add("species/all", "species verdict, all cases", c)
    for p in pops.values():
        p["by_status"] = dict(p["by_status"])
    return {"source": SOURCE, "cases": len(cs),
            "cases_by_status": dict(collections.Counter(status_key(c["status"]) for c in cs)),
            "no_semantics": [c["id"] for c in cs if not c["semantics"] and any(t in c["types"] for t in TYPES)],
            "populations": pops}


CASE_RE = re.compile(r"<test:TestCase\b.*?</test:TestCase>", re.S)


def split(path, work):
    """One catalog per (semantics, status): the TestCase blocks that match, the rest kept."""
    text = open(path, encoding="utf-8").read()
    blocks = CASE_RE.findall(text)
    meta = cases(path)
    if len(blocks) != len(meta):
        sys.exit(f"{path}: {len(blocks)} TestCase blocks in the text, {len(meta)} parsed; the split would be wrong")
    files = {}
    for sk, sv in SEMANTICS.items():
        for tk, tv in STATUSES.items():
            keep = {i for i, c in enumerate(meta) if sv in c["semantics"] and c["status"] == tv}
            it = iter(range(len(blocks)))
            body = CASE_RE.sub(lambda m, it=it: m.group(0) if next(it) in keep else "", text)
            name = f"owl2-{sk}-{tk}.rdf"
            with open(os.path.join(work, name), "w", encoding="utf-8") as f:
                f.write(body)
            n = len(cases(os.path.join(work, name)))
            if n != len(keep):
                sys.exit(f"{name}: {n} cases written, {len(keep)} wanted")
            files[(sk, tk)] = (name, n)
    for tk, tv in STATUSES.items():
        keep = {i for i, c in enumerate(meta) if c["status"] == tv}
        it = iter(range(len(blocks)))
        body = CASE_RE.sub(lambda m, it=it: m.group(0) if next(it) in keep else "", text)
        name = f"owl2-all-{tk}.rdf"
        with open(os.path.join(work, name), "w", encoding="utf-8") as f:
            f.write(body)
        files[("all", tk)] = (name, len(keep))
    return files


LINE = re.compile(r"^(owl2-(direct|rdfbased)-([a-z]+)\.rdf) (\w+Test)(?: \[rdf-based\])?: (.*)\(out of (\d+)\)\s*$")


PROFILE_LINE = re.compile(r"^(owl2-all-([a-z]+)\.rdf) ProfileIdentificationTest (EL|QL|RL): (.*)\(out of (\d+)\)\s*$")


def parse_counts(text):
    return {k: int(v) for v, k in re.findall(r"(\d+) ([a-z][a-z-]*)", text)}


def run(a):
    os.makedirs(a.work, exist_ok=True)
    off = official(a.catalog)
    files = split(a.catalog, a.work)
    procs, logs, t0 = {}, {}, time.time()
    for sk, flag in (("direct", ["--dl"]), ("rdfbased", ["--rdf-based"])):
        names = [files[(sk, tk)][0] for tk in STATUSES if files[(sk, tk)][1]]
        cmd = [a.probe] + flag + ["--refute-ms", str(a.refute_ms), "--dir", a.work] + names
        logs[sk] = os.path.join(a.work, f"owl2-{sk}.log")
        procs[sk] = (subprocess.Popen(cmd, stdout=open(logs[sk], "wb"), stderr=subprocess.STDOUT), cmd, time.time())
    status = {}
    for sk, (p, cmd, ts) in procs.items():
        try:
            rc = p.wait(timeout=max(1, a.timeout - (time.time() - t0)))
            err = None
        except subprocess.TimeoutExpired:
            p.kill()
            p.wait()
            rc, err = 124, f"no end in {a.timeout} s"
        status[sk] = {"command": cmd, "exit": rc, "error": err, "seconds": round(time.time() - ts)}
    # Profile identification: one more run of the probe, after the two semantics runs.
    names = [files[("all", tk)][0] for tk in STATUSES if files[("all", tk)][1]]
    cmd = [a.probe, "--profile-id", "--dir", a.work] + names
    logs["profile"] = os.path.join(a.work, "owl2-profile.log")
    ts = time.time()
    try:
        rc = subprocess.run(cmd, stdout=open(logs["profile"], "wb"), stderr=subprocess.STDOUT,
                            timeout=max(1, a.timeout - (time.time() - t0))).returncode
        err = None
    except subprocess.TimeoutExpired:
        rc, err = 124, f"no end in {a.timeout} s"
    status["profile"] = {"command": cmd, "exit": rc, "error": err, "seconds": round(time.time() - ts)}
    pops = {k: dict(v, pass_=0, fail=0, other=0, measured=False, status_counts={}) for k, v in off["populations"].items()}
    seen = collections.defaultdict(dict)
    for sk, lp in logs.items():
        for line in open(lp, errors="replace"):
            m = PROFILE_LINE.match(line.rstrip("\n")) if sk == "profile" else None
            if m:
                _, st, prof, rest, out_of = m.groups()
                c = parse_counts(rest)
                seen[("ProfileIdentificationTest", prof)][st] = {
                    "pass": c.get("pass", 0), "fail": c.get("fail", 0), "total": int(out_of), "counts": c}
                continue
            m = LINE.match(line.rstrip("\n"))
            if not m or sk == "profile":
                continue
            _, sem, st, ty, rest, out_of = m.groups()
            c = parse_counts(rest)
            seen[(ty, sem)][st] = {"pass": c.get("pass", 0), "fail": c.get("fail", 0), "total": int(out_of),
                                   "counts": c}
    for (ty, sem), by in seen.items():
        key = f"{ty}/{sem}"
        if key not in pops:
            continue
        p = pops[key]
        p["measured"] = not status["profile" if ty == "ProfileIdentificationTest" else sem]["error"]
        p["pass_"] = sum(v["pass"] for v in by.values())
        p["fail"] = sum(v["fail"] for v in by.values())
        p["reported"] = sum(v["total"] for v in by.values())
        p["other"] = p["reported"] - p["pass_"] - p["fail"]
        p["status_counts"] = by
    for p in pops.values():
        p["pass"] = p.pop("pass_")
        p["run"] = p["pass"] + p["fail"]
    res = {"format": "owl2-populations-v1", "source": off["source"], "cases": off["cases"],
           "cases_by_status": off["cases_by_status"], "no_semantics": off["no_semantics"],
           "regimes": {"direct": "--dl: RL closure, class-expression materialisation and the tableau refuter",
                       "rdfbased": "--rdf-based: RL closure and the proved RDF-Based rules",
                       "profile": "--profile-id: the OWL 2 DL species check, then the EL, QL or RL grammar "
                                  "(OWL 2 Profiles sections 2.2, 3.2, 4.2) over the axioms read back from the "
                                  "RDF graph"},
           "refute_ms": a.refute_ms, "status": status, "populations": pops}
    json.dump(res, open(os.path.join(a.work, "populations.json"), "w"), indent=1)
    for k, p in sorted(pops.items()):
        print(f"{k}: {p['pass']} pass, {p['fail']} fail, {p['other']} other, of {p['total']} "
              f"({'measured' if p['measured'] else 'not run'})")
    return 0 if all(not s["error"] and s["exit"] in (0, 1) for k, s in status.items() if k != "profile") else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    o = sub.add_parser("official")
    o.add_argument("--catalog", required=True)
    o.add_argument("--out")
    r = sub.add_parser("run")
    r.add_argument("--probe", required=True)
    r.add_argument("--catalog", required=True)
    r.add_argument("--work", required=True)
    r.add_argument("--refute-ms", type=int, default=3000)
    r.add_argument("--timeout", type=int, default=2400)
    a = ap.parse_args()
    if a.cmd == "official":
        d = official(a.catalog)
        s = json.dumps(d, indent=1)
        open(a.out, "w").write(s) if a.out else print(s)
        return 0
    return run(a)


if __name__ == "__main__":
    sys.exit(main())
