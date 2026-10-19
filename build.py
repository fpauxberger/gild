#!/usr/bin/env python3
"""Generates style.css, one detail page per product (in products/), and the product cards on index.html.
Run:  python3 build.py   (safe to re-run; edit PRODUCTS below to change content)"""
import os, re, html
from urllib.parse import quote

ROOT = os.path.dirname(os.path.abspath(__file__))

PRODUCTS = [
 ("terminal", "📈", "GIT Terminal", "Real-time market intelligence for professional traders",
  "Live market data, news and analytics in one workspace.",
  "GIT Terminal brings streaming prices, breaking news, research and charting into a single customisable workspace. Traders and analysts monitor global markets, build watchlists and share ideas securely with colleagues.",
  ["Real-time and historical data across equities, FX, rates and commodities", "Advanced charting with 100+ technical indicators", "Integrated news feed with sentiment scoring", "Secure messaging and idea sharing", "Excel and Python add-ins for custom models"],
  ["Faster decisions with one source of truth", "Lower data costs through consolidated feeds", "Works on desktop, web and mobile"]),
 ("corebank", "🏦", "GIT CoreBank", "Cloud-native core banking for modern institutions",
  "Accounts, deposits and transactions on a flexible core.",
  "GIT CoreBank is a modular, API-first banking core that runs accounts, deposits, payments and general ledger in the cloud. Launch new products in days instead of months and scale from a challenger bank to a full retail operation.",
  ["Multi-currency accounts and deposit products", "Real-time general ledger and reconciliation", "Configurable product engine with no-code rules", "Open banking APIs and event streaming", "Built-in audit trail and regulatory reporting hooks"],
  ["Cut time-to-market for new products", "Reduce legacy maintenance costs", "Elastic scaling during peak loads"]),
 ("portfolio-manager", "🧭", "GIT Portfolio Manager", "Portfolio construction, orders and performance in one place",
  "Portfolio construction, order management and reporting.",
  "GIT Portfolio Manager helps asset managers design portfolios, check compliance before trading, route orders and measure performance. Front, middle and back office work from the same live positions.",
  ["Model portfolios and what-if rebalancing", "Pre- and post-trade compliance checks", "Order management with broker connectivity", "Performance attribution and client reporting", "Cash, position and exposure monitoring"],
  ["One consistent view of positions", "Fewer manual spreadsheets and errors", "Faster, richer client reports"]),
 ("riskguard", "🛡️", "GIT RiskGuard", "Enterprise risk analytics you can trust",
  "Market, credit and liquidity risk with stress testing.",
  "GIT RiskGuard measures and monitors market, credit and liquidity risk across the whole firm. Run VaR, scenario and stress tests on demand and give risk officers and regulators clear, explainable numbers.",
  ["Value-at-Risk and expected shortfall", "Custom and regulatory stress-test scenarios", "Counterparty credit exposure and limits", "Liquidity coverage and funding analysis", "Interactive dashboards with drill-down"],
  ["Spot concentrations before they hurt", "Meet regulatory expectations with confidence", "Overnight batches shrink to minutes"]),
 ("tradehub", "⚡", "GIT TradeHub", "Multi-asset trading, execution and post-trade processing",
  "Trading, execution and post-trade in one platform.",
  "GIT TradeHub covers the full trade lifecycle: pricing, execution, confirmation, clearing and settlement. Connect to exchanges, brokers and liquidity venues through a single, low-latency platform.",
  ["Equities, fixed income, FX and derivatives", "Smart order routing and algorithmic execution", "Straight-through processing to clearing", "Real-time position and P&L", "FIX and REST connectivity"],
  ["Lower execution costs", "Fewer failed settlements", "Single platform replaces siloed systems"]),
 ("wealthadvisor", "💼", "GIT WealthAdvisor", "Digital tools for advisers and their clients",
  "Onboarding, planning and advice tools for wealth managers.",
  "GIT WealthAdvisor gives advisers a complete client workspace: digital onboarding, goal-based planning, suitability checks and a branded client portal. Spend less time on paperwork and more time advising.",
  ["Digital onboarding with e-signature", "Goal-based financial planning and cash-flow modelling", "Suitability and risk-profile questionnaires", "Branded client portal and mobile app", "Fee billing and household reporting"],
  ["Onboard clients in minutes", "Consistent, documented advice", "Higher client engagement"]),
 ("comply", "📋", "GIT Comply", "Compliance and regulatory technology made simple",
  "KYC, AML screening and regulatory reporting automation.",
  "GIT Comply automates know-your-customer checks, sanctions and AML screening, transaction monitoring and regulatory reporting. Smart case management reduces false positives and gives compliance teams a full audit trail.",
  ["Identity verification and KYC workflows", "Sanctions, PEP and adverse-media screening", "Rule- and model-based transaction monitoring", "Case management with audit history", "Prebuilt regulatory report templates"],
  ["Reduce false-positive alerts", "Faster customer onboarding", "Stay ahead of changing regulations"]),
 ("payflow", "💳", "GIT PayFlow", "Fast, secure payments worldwide",
  "Instant payments, cards and cross-border settlement.",
  "GIT PayFlow processes instant payments, card transactions and cross-border transfers on one secure platform. Support domestic schemes and international networks with built-in fraud detection and reconciliation.",
  ["Instant and batch payment schemes", "Card issuing and acquiring", "Cross-border payments with FX", "Real-time fraud scoring", "Automated reconciliation and dispute handling"],
  ["Settle in seconds, not days", "Fewer fraud losses", "One integration for many schemes"]),
 ("loansuite", "🏠", "GIT LoanSuite", "End-to-end lending from application to servicing",
  "Origination, credit scoring and servicing in one suite.",
  "GIT LoanSuite digitises the lending journey: application, credit decisioning, documentation, disbursement and servicing. Configure products for mortgages, consumer loans or SME lending and decide in real time.",
  ["Online application and document upload", "Automated credit scoring and decision rules", "Collateral and covenant management", "Repayment schedules and collections", "Portfolio analytics and early-warning signals"],
  ["Decisions in minutes", "Consistent credit policy", "Lower cost per loan"]),
 ("fundledger", "🧮", "GIT FundLedger", "Fund accounting and investor administration",
  "Fund accounting, NAV calculation and investor administration.",
  "GIT FundLedger automates fund accounting for mutual funds, ETFs and alternatives. Calculate NAV, manage investor registers and fees, and produce accurate statements on schedule.",
  ["Daily NAV calculation and pricing controls", "Subscriptions, redemptions and transfer agency", "Fee, accrual and waterfall calculations", "Investor statements and tax reporting", "Audit-ready ledger with full lineage"],
  ["Shorter close cycles", "Fewer NAV breaks", "Scales across funds and share classes"]),
]

esc = html.escape

def extract_css():
    p = os.path.join(ROOT, "style.css")
    if os.path.exists(p):
        return
    src = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    css = re.search(r"<style>(.*?)</style>", src, re.S).group(1).strip()
    css += """
.crumb{padding:24px 0 0;color:var(--muted);font-size:.9rem}.crumb a:hover{color:var(--gold)}
.phero{padding:32px 0 48px}.phero .ic{font-size:2.4rem;width:72px;height:72px;display:grid;place-items:center;border-radius:18px;background:rgba(74,168,173,.15);margin-bottom:16px}
.phero p{color:var(--muted);font-size:1.15rem;max-width:720px}
.two{display:grid;grid-template-columns:1.4fr 1fr;gap:32px}
.panel{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:26px}
.panel h3{margin-top:0}.panel ul{padding-left:20px;margin:0;color:var(--muted)}.panel li{margin:8px 0}
.more{display:inline-block;margin-top:12px;color:var(--gold);font-size:.9rem;font-weight:600}
.others{display:flex;flex-wrap:wrap;gap:10px}.others a{padding:8px 16px;border:1px solid var(--line);border-radius:999px;color:var(--muted);font-size:.9rem}.others a:hover{border-color:var(--teal);color:var(--text)}
@media(max-width:800px){.two{grid-template-columns:1fr}}
"""
    open(p, "w", encoding="utf-8").write(css)

def header():
    return """<header><div class="wrap nav">
  <a class="brand" href="../index.html"><img src="../git-logo-circle.png" alt="GIT logo"><span>Gild Investment Trust</span></a>
  <nav><a href="../index.html#products">Products</a><a href="../index.html#about">Why GIT</a><a class="btn" href="../contact.html">Contact us</a></nav>
</div></header>"""

def page(p):
    slug, ic, name, tag, _short, overview, feats, bens = p
    contact = f"../contact.html?product={quote(name)}#contact"
    others = "".join(f'<a href="product-{s}.html">{esc(n)}</a>' for s, _, n, *_ in PRODUCTS if s != slug)
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(name)} – Gild Investment Trust</title><link rel="icon" href="../git-logo-circle.png"><link rel="stylesheet" href="../style.css"></head>
<body>
{header()}
<main><div class="wrap">
  <div class="crumb"><a href="../index.html">Home</a> / <a href="../index.html#products">Products</a> / {esc(name)}</div>
  <div class="phero"><div class="ic">{ic}</div><h1>{esc(name)}</h1><p>{esc(tag)}. {esc(overview)}</p>
    <div class="cta" style="display:flex;gap:12px;flex-wrap:wrap;margin-top:20px"><a class="btn" href="{contact}">Contact us about {esc(name)}</a><a class="btn ghost" href="../index.html#products">All products</a></div></div>
  <div class="two">
    <div class="panel"><h3>Key features</h3><ul>{"".join(f"<li>{esc(f)}</li>" for f in feats)}</ul></div>
    <div class="panel"><h3>Benefits</h3><ul>{"".join(f"<li>{esc(b)}</li>" for b in bens)}</ul></div>
  </div>
  <div class="ad" style="margin-top:32px"><div><h4>Nordhaven Cloud: bank-grade hosting for financial apps</h4><p>ISO 27001 certified. Free migration for GIT customers.</p></div><a class="btn" href="#">Learn more</a></div>
  <section style="padding:40px 0 56px"><h2>Other GIT products</h2><div class="others" style="margin-top:16px">{others}</div>
    <p style="margin-top:32px"><a class="btn" href="{contact}">Request a demo of {esc(name)}</a></p></section>
</div></main>
<footer><div class="wrap"><span>© 2026 Gild Investment Trust (GIT). Fictional company for demonstration.</span><span>Privacy · Terms · Imprint</span></div></footer>
</body></html>"""

def update_index():
    p = os.path.join(ROOT, "index.html")
    s = open(p, encoding="utf-8").read()
    cards = "\n".join(
        f'    <a class="card" href="products/product-{slug}.html"><div class="ic">{ic}</div><h3>{esc(name)}</h3><p>{esc(short)}</p><span class="more">Learn more →</span></a>'
        for slug, ic, name, _t, short, *_ in PRODUCTS)
    s = re.sub(r'(<section id="products">.*?<div class="grid">\n).*?(\n  </div>\n</div></section>)',
               lambda m: m.group(1) + cards + m.group(2), s, count=1, flags=re.S)
    if ".more{" not in s:
        s = s.replace("</style>", ".more{display:inline-block;margin-top:12px;color:var(--gold);font-size:.9rem;font-weight:600}\n</style>", 1)
    open(p, "w", encoding="utf-8").write(s)

if __name__ == "__main__":
    extract_css()
    os.makedirs(os.path.join(ROOT, "products"), exist_ok=True)
    for p in PRODUCTS:
        open(os.path.join(ROOT, "products", f"product-{p[0]}.html"), "w", encoding="utf-8").write(page(p))
    update_index()
    print(f"Generated {len(PRODUCTS)} product pages, style.css and updated index.html")
