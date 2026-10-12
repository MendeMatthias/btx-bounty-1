#!/usr/bin/env python3
"""The BTX Explainer grader (bounty/evaluation-spec.md).

    grade.py QUESTIONS.json [QUESTIONS2.json ...] --server http://127.0.0.1:8080 [--report out.json]

Asks a llama.cpp server every question once (temperature 0, max 200 tokens,
no system prompt, the question text alone) and applies the rule: a question
passes when every required fact appears in the answer, case-insensitively,
numbers with or without separators, and no forbidden fact appears. Writes a
report with every answer so anyone can re-run and compare. Standard library.
"""
import argparse
import json
import re
import sys
import time
import urllib.request


def norm(s):
    s = s.lower()
    s = re.sub(r"(?<=\d)[,\s](?=\d{3}\b)", "", s)   # 21,000,000 and 21 000 000 -> 21000000
    return s


def contains(answer, fact):
    return norm(fact) in norm(answer)


def ask(server, question, max_tokens=200, timeout=600):
    body = json.dumps({
        "messages": [{"role": "user", "content": question}],
        "temperature": 0, "top_p": 1, "max_tokens": max_tokens, "stream": False,
    }).encode()
    req = urllib.request.Request(server.rstrip("/") + "/v1/chat/completions", data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        d = json.load(r)
    return (d.get("choices") or [{}])[0].get("message", {}).get("content", "") or ""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+")
    ap.add_argument("--server", default="http://127.0.0.1:8080")
    ap.add_argument("--report", default="")
    ap.add_argument("--pass-mark", type=int, default=48, help="questions needed out of the whole set (spec: 48 of 60)")
    a = ap.parse_args()
    questions = []
    for f in a.files:
        questions += json.load(open(f, encoding="utf-8"))["questions"]
    results = []
    passed = 0
    t0 = time.time()
    for q in questions:
        answer = ask(a.server, q["q"])
        missing = [x for x in q.get("required", []) if not contains(answer, x)]
        hit = [x for x in q.get("forbidden", []) if contains(answer, x)]
        ok = not missing and not hit
        passed += ok
        results.append({"id": q["id"], "q": q["q"], "answer": answer, "pass": ok, "missing": missing, "forbidden_hit": hit})
        print("%s %-4s %s" % ("PASS" if ok else "FAIL", q["id"], q["q"][:70]), flush=True)
        if not ok:
            print("      missing %s forbidden %s | %s" % (missing, hit, answer[:120].replace("\n", " ")))
    total = len(questions)
    verdict = "PASS" if passed >= a.pass_mark and total >= a.pass_mark else "FAIL"
    summary = {"total": total, "passed": passed, "pass_mark": a.pass_mark, "verdict": verdict,
               "server": a.server, "seconds": round(time.time() - t0, 1), "results": results}
    print("\n%d of %d passed (pass mark %d): %s" % (passed, total, a.pass_mark, verdict))
    if a.report:
        json.dump(summary, open(a.report, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print("report:", a.report)
    sys.exit(0 if verdict == "PASS" else 1)


if __name__ == "__main__":
    main()
