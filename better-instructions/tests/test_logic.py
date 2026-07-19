"""Testes de ouro — lógica de render / qa_doc / qa_plan, SEM depender do Google Docs.

Rodar:
    scripts/.venv/bin/python tests/test_logic.py
Exit 0 = tudo passou, 1 = alguma falha.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(HERE, "..", "scripts")
FIX = os.path.join(HERE, "fixtures")
sys.path.insert(0, SCRIPTS)

from render import render                       # noqa: E402
from qa_doc import audit_ad                      # noqa: E402
from qa_plan import validate_plan                # noqa: E402
from _common import load_manifest, manifest_by_tag  # noqa: E402

PASS = FAIL = 0


def check(name, cond):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  ✅ {name}")
    else:
        FAIL += 1
        print(f"  ❌ {name}")


def fix(name):
    with open(os.path.join(FIX, name), encoding="utf-8") as f:
        return f.read()


def rowd(rows):
    return {r[0]: r[1] for r in rows}


print("RENDER")
check("legenda-minimalista renderiza", render("legenda-minimalista", {})["text"].startswith("📝"))
check("cenário default = ⚠️ CONFIRMAR (caso 5)", "CONFIRMAR cenário" in render("cenario", {})["text"])
check("ritmo carrega ref de velocidade", "🔗 Ref." in render("ritmo-tiktok-viral", {})["text"])
check("formato sem filler 'quando houver'", "quando houver" not in render("formato", {"tipo": "React"})["text"])
check("cenário casa NÃO vaza academia",
      "Em academia" not in render("cenario", {"status": "definido", "local": "casa (quarto/sala/garagem)"})["text"])
check("--with-img insere marcador",
      "[[img:legenda-min-branca]]" in render("legenda-minimalista", {}, with_img=True)["text"])
# formato Teleprompter (TP) — UGC do Murilo lendo no teleprompter, orgânico/dinâmico
_tp = render("formato", {"tipo": "Teleprompter (TP)"})["text"]
check("formato TP renderiza com teleprompter + orgânico",
      "Teleprompter" in _tp and "teleprompter" in _tp and "orgânico" in _tp)

print("AUDIT (qa_doc.audit_ad)")
# caso TP — Murilo grava (teleprompter ≠ b-roll forçado), detecta formato teleprompter
from qa_doc import detect_formato  # noqa: E402
check("TP: detect_formato = teleprompter", detect_formato(_tp) == "teleprompter")
_tp_body = ("AD 9\nInstruções para o editor de vídeo:\n" + _tp +
            "\n📝 Legenda minimalista — branca.\n⚡ Ritmo de TikTok viral — anda.\n🔗 Ref.: [v](http://x)\n"
            "Instruções para o Murilo:\n📍 Cenário: academia.\n🎤 microfone na mão.\n🎥 Takes vários aparelhos.\nROTEIRO")
_tp_rows, _tp_grava, _tp_fmt = audit_ad("AD 9", _tp_body)
_tpd = rowd(_tp_rows)
check("TP: Murilo grava", _tp_grava is True)
check("TP: NÃO força ressalva b-roll", "ressalva b-roll" not in _tpd)
check("TP: ritmo/legenda/formato/cenário/microfone/takes ✅",
      all(_tpd.get(k) is True for k in ("ritmo", "legenda", "formato", "cenário", "microfone/áudio", "takes")))
# caso 1 — CXP SP1 completo
rows, grava, fmt = audit_ad("AD 1", fix("ad_cxp_sp1_ok.txt"))
d = rowd(rows)
check("caso1 CXP ok: Murilo grava", grava is True)
check("caso1 CXP ok: formato cxp", fmt == "cxp")
check("caso1 CXP ok: ritmo/legenda/formato/cenário/microfone/takes ✅",
      all(d.get(k) is True for k in ("ritmo", "legenda", "formato", "cenário", "microfone/áudio", "takes")))
# caso 1b — fraco: exige e acusa o que falta
d = rowd(audit_ad("AD 1", fix("ad_cxp_sp1_weak.txt"))[0])
check("caso1 weak: ritmo faltando ❌", d.get("ritmo") is False)
check("caso1 weak: cenário/microfone/takes faltando ❌",
      d.get("cenário") is False and d.get("microfone/áudio") is False and d.get("takes") is False)

# caso 2 — CNM + voz feminina + b-roll
d = rowd(audit_ad("AD 2", fix("ad_cnm_broll_missing.txt"))[0])
check("caso2 CNM: exige b-roll-realista e está faltando ❌", d.get("ressalva b-roll") is False)
d = rowd(audit_ad("AD 2", fix("ad_cnm_broll_ok.txt"))[0])
check("caso2 CNM com b-roll ✅", d.get("ressalva b-roll") is True)

# caso 3 — React precisa de ref
d = rowd(audit_ad("AD 3", fix("ad_react_noref.txt"))[0])
check("caso3 React sem ref ❌", d.get("referência (🔗)") is False)

# caso 4 — Murilo Nenhuma
rows, grava, _ = audit_ad("AD 4", fix("ad_murilo_nenhuma.txt"))
d = rowd(rows)
check("caso4 Murilo Nenhuma: grava=False", grava is False)
check("caso4 Murilo Nenhuma: NÃO exige cenário/microfone/takes",
      "cenário" not in d and "microfone/áudio" not in d and "takes" not in d)

print("QA PLAN (qa_plan.validate_plan)")
by_tag = manifest_by_tag(load_manifest())
e, w = validate_plan(json.load(open(os.path.join(FIX, "plano_ok.json"), encoding="utf-8")), by_tag)
check("plano_ok: sem erros", len(e) == 0)
e, w = validate_plan(json.load(open(os.path.join(FIX, "plano_bad.json"), encoding="utf-8")), by_tag)
msgs = " ".join(m for _, m in e).lower()
check("plano_bad: tem erros", len(e) > 0)
check("plano_bad: pega anchor vazio", any("anchor" in m for _, m in e))
check("plano_bad: pega marcador proibido", "obrigat" in msgs)
check("plano_bad: pega [[img]] inexistente", "não existe no manifest" in msgs)
check("plano_bad: pega link sem http", "url inválida" in msgs)

print(f"\n{PASS} passaram, {FAIL} falharam")
sys.exit(1 if FAIL else 0)
