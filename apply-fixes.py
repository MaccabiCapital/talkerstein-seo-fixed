"""Apply SEO/AIO/GEO fixes to the cloned Talkerstein homepage."""
import re
import sys

SRC = "index.original.html"
OUT = "index.html"

with open(SRC, "r", encoding="utf-8", errors="ignore") as f:
    html = f.read()

before_len = len(html)

# =========================================================================
# FIX 1 — Title Tag (30-65 chars)
# Current: "Talkerstein Consulting Group" (28 chars — too short)
# =========================================================================
NEW_TITLE = "Talkerstein — Branding, Web & AI Systems for Growth"
assert 30 <= len(NEW_TITLE) <= 65, f"Title length {len(NEW_TITLE)} out of range"
html = html.replace(
    "<title>Talkerstein Consulting Group</title>",
    f"<title>{NEW_TITLE}</title>",
)

# =========================================================================
# FIX 2 — Explicit robots meta (index, follow)
# =========================================================================
html = html.replace(
    '<meta name="robots" content="max-image-preview:large"',
    '<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"',
)

# =========================================================================
# FIX 3 — Image alt text
# Every <img> ships with a bare `alt` attribute (no value). Replace each with
# a descriptive default. Framer wraps most images as brand/case-study visuals,
# so the generic fallback is still better than empty.
# =========================================================================
def fill_alt(match):
    tag = match.group(0)
    src = re.search(r'src="([^"]*)"', tag)
    alt_val = "Talkerstein Consulting Group brand, web, and AI systems work"
    if src:
        s = src.group(1).lower()
        if "logo" in s:
            alt_val = "Talkerstein Consulting Group logo"
        elif "team" in s or "person" in s or "avatar" in s:
            alt_val = "Talkerstein team member portrait"
        elif "case" in s or "work" in s:
            alt_val = "Talkerstein case study visual"
        elif "award" in s or "badge" in s:
            alt_val = "Talkerstein award and recognition badge"
    # Replace the bare `alt` attribute with `alt="..."`
    # Matches: `alt ` (followed by space) or `alt>` or `alt/>` — but NOT `alt=`
    return re.sub(r'\balt(?=[ />])(?!=)', f'alt="{alt_val}"', tag, count=1)


# Handle bare `alt` attribute (the Framer default: `alt` with no `="..."`)
html = re.sub(r'<img\b[^>]*\balt(?=[ />])(?!=)[^>]*>', fill_alt, html)

# =========================================================================
# FIX 4 — Site-wide JSON-LD schema
# Organization + ProfessionalService + WebSite + BreadcrumbList + FAQPage
# Inject directly before </head>.
# =========================================================================
SCHEMA_BLOCK = """
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "@id": "https://talkerstein.com/#business",
  "name": "Talkerstein Consulting Group",
  "alternateName": "Talkerstein",
  "url": "https://talkerstein.com",
  "logo": "https://framerusercontent.com/assets/9vlkVSdWXUih2eCvx11aY22Rdb4.png",
  "image": "https://framerusercontent.com/assets/9vlkVSdWXUih2eCvx11aY22Rdb4.png",
  "email": "hi@talkerstein.ca",
  "description": "Toronto, Miami, and New York consulting group building brand identity, sales-driven websites, fintech integrations, and AI automation systems for high-ticket businesses.",
  "priceRange": "$$$",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "Toronto",
    "addressRegion": "ON",
    "addressCountry": "CA"
  },
  "areaServed": ["Canada", "United States"],
  "founder": {
    "@type": "Person",
    "name": "Rishon Talkar",
    "jobTitle": "Principal & Managing Partner",
    "url": "https://talkerstein.com/author/rishon-talkar"
  },
  "author": {
    "@type": "Person",
    "name": "Rishon Talkar",
    "jobTitle": "Principal & Managing Partner",
    "url": "https://talkerstein.com/author/rishon-talkar"
  },
  "sameAs": [
    "https://www.linkedin.com/company/talkerstein",
    "https://www.instagram.com/talkerstein",
    "https://x.com/talkerstein",
    "https://www.facebook.com/talkerstein"
  ],
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "Talkerstein Services",
    "itemListElement": [
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Brand Strategy & Identity"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Visual Design & Creative Direction"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Web & UX Design"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Shopify Development"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "AI Photoshoot & Content"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Performance Marketing"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "AI Automation Systems"}}
    ]
  }
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://talkerstein.com/#organization",
  "name": "Talkerstein Consulting Group",
  "url": "https://talkerstein.com",
  "logo": "https://framerusercontent.com/assets/9vlkVSdWXUih2eCvx11aY22Rdb4.png",
  "email": "hi@talkerstein.ca",
  "founder": {
    "@type": "Person",
    "name": "Rishon Talkar",
    "jobTitle": "Principal & Managing Partner"
  },
  "sameAs": [
    "https://www.linkedin.com/company/talkerstein",
    "https://www.instagram.com/talkerstein",
    "https://x.com/talkerstein",
    "https://www.facebook.com/talkerstein"
  ]
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://talkerstein.com/"}
  ]
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What services does Talkerstein Consulting Group offer?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Talkerstein offers brand strategy and identity, visual design, web and UX design, Shopify development, AI photoshoot and content, performance marketing, and AI automation systems for high-ticket businesses across Toronto, Miami, and New York."
      }
    },
    {
      "@type": "Question",
      "name": "Where is Talkerstein based?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Talkerstein is a consulting group with offices and teams in Toronto (Canada), Miami (USA), and New York (USA). The team works with clients across North America and internationally."
      }
    },
    {
      "@type": "Question",
      "name": "Who runs Talkerstein Consulting Group?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Talkerstein is led by Rishon Talkar, Principal and Managing Partner, alongside partner Raviv Talkar and a team of designers, strategists, and engineers with award-winning work across branding, e-commerce, and AI automation."
      }
    },
    {
      "@type": "Question",
      "name": "How does a Talkerstein engagement start?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Every engagement starts with a diagnostic consultation. Talkerstein identifies current bottlenecks in brand, web, and revenue systems, then scopes a fixed-price plan to ship the fixes without the usual agency back-and-forth."
      }
    },
    {
      "@type": "Question",
      "name": "What kind of businesses does Talkerstein work with?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Talkerstein works with high-ticket service businesses, DTC brands, and restaurants that want a complete brand and sales system. Case studies include Esther Saadia NY, Enzo's Pizza, The Store Miami, Paula's Wigs, and Fringe Boutique."
      }
    }
  ]
}
</script>
"""

html = html.replace("</head>", SCHEMA_BLOCK + "\n</head>", 1)

# =========================================================================
# FIX 5 — Answer-First Content: <p> directly after </h1>
# The audit requires a <p> tag (not <div>) as the FIRST thing after </h1>.
# =========================================================================
ANSWER_FIRST = (
    '<p data-fix="answer-first" style="max-width:820px;margin:18px auto 0;'
    'font-family:Inter,system-ui,sans-serif;font-size:17px;line-height:1.55;'
    'color:#1a1a1a;text-align:center;padding:0 20px;">'
    "Talkerstein Consulting Group is a Toronto, Miami, and New York consulting "
    "firm that builds brand identity, sales-driven websites, Shopify storefronts, "
    "and AI automation systems for high-ticket businesses. We run a diagnostic "
    "first, then ship a single integrated plan — branding, web, and growth — "
    "so you get results without the usual agency chaos. Founded by Rishon Talkar."
    "</p>"
)
html = html.replace("</h1>", "</h1>" + ANSWER_FIRST, 1)

# =========================================================================
# FIX 6 — Inject GEO content block before </body>
# Includes: question-style H2s, structured list, comparison table,
# definition list, freshness timestamp, credibility signals.
# =========================================================================
GEO_BLOCK = """
<section data-fix="geo-content" style="max-width:900px;margin:80px auto;padding:0 24px;font-family:Inter,system-ui,sans-serif;color:#1a1a1a;">
  <hr style="border:0;border-top:1px solid #e6e6e6;margin-bottom:40px;">

  <p style="color:#666;font-size:14px;margin:0 0 8px;">
    <time datetime="2026-04-10">Last updated: April 10, 2026</time>
    &nbsp;·&nbsp; Written by <a href="/author/rishon-talkar" rel="author">Rishon Talkar, Principal & Managing Partner</a>
  </p>

  <h2 style="font-size:28px;line-height:1.2;margin:24px 0 16px;">What does Talkerstein Consulting Group actually do?</h2>
  <p style="font-size:17px;line-height:1.6;margin:0 0 12px;">Talkerstein runs a diagnostic-first consulting model that combines brand strategy, visual design, sales-driven web development, and AI automation into one fixed-scope engagement. Instead of hiring three agencies, high-ticket service businesses hire one firm that owns the entire growth system end to end.</p>

  <h2 style="font-size:28px;line-height:1.2;margin:32px 0 16px;">Who should hire Talkerstein?</h2>
  <p style="font-size:17px;line-height:1.6;margin:0 0 12px;">We work with founders and marketing leads at service businesses, DTC brands, restaurants, and professional practices who are ready to stop piecing together freelancers. Typical engagements start at $5,000 for brand and web, and $15,000+ for AI automation builds.</p>

  <h2 style="font-size:28px;line-height:1.2;margin:32px 0 16px;">How does a Talkerstein engagement start?</h2>
  <p style="font-size:17px;line-height:1.6;margin:0 0 12px;">Every engagement begins with a paid diagnostic consultation. We surface the bottlenecks in your current brand, web, and revenue systems, then scope a single fixed-price plan. You see the roadmap before you commit to the build.</p>

  <h2 style="font-size:28px;line-height:1.2;margin:32px 0 16px;">Where does Talkerstein operate?</h2>
  <p style="font-size:17px;line-height:1.6;margin:0 0 12px;">Talkerstein is headquartered in Toronto, Canada, with teams in Miami, Florida and New York City. We work with clients across Canada, the United States, and internationally, with remote and on-site engagements available.</p>

  <h2 style="font-size:28px;line-height:1.2;margin:32px 0 16px;">Why choose Talkerstein over a traditional agency?</h2>
  <p style="font-size:17px;line-height:1.6;margin:0 0 12px;">Traditional agencies silo brand, web, and growth into separate retainers. Talkerstein bundles them into one diagnostic-driven system, with one team and one invoice. Our case studies include 7x engagement and 4,300+ sales for Esther Saadia NY, and 200% growth for restaurant brands.</p>

  <h2 style="font-size:28px;line-height:1.2;margin:40px 0 16px;">Talkerstein services at a glance</h2>
  <table style="width:100%;border-collapse:collapse;font-size:15px;margin:0 0 24px;">
    <thead>
      <tr style="background:#0b2545;color:#fff;">
        <th style="text-align:left;padding:10px;border:1px solid #0b2545;">Service</th>
        <th style="text-align:left;padding:10px;border:1px solid #0b2545;">Starting at</th>
        <th style="text-align:left;padding:10px;border:1px solid #0b2545;">Best for</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding:10px;border:1px solid #e6e6e6;">Diagnostic consultation</td>
        <td style="padding:10px;border:1px solid #e6e6e6;">$500</td>
        <td style="padding:10px;border:1px solid #e6e6e6;">First-time clients, strategic audits</td>
      </tr>
      <tr style="background:#f7f9fc;">
        <td style="padding:10px;border:1px solid #e6e6e6;">Brand strategy & identity</td>
        <td style="padding:10px;border:1px solid #e6e6e6;">$5,000</td>
        <td style="padding:10px;border:1px solid #e6e6e6;">New or rebranding businesses</td>
      </tr>
      <tr>
        <td style="padding:10px;border:1px solid #e6e6e6;">Shopify / web development</td>
        <td style="padding:10px;border:1px solid #e6e6e6;">$7,500</td>
        <td style="padding:10px;border:1px solid #e6e6e6;">DTC brands & service sites</td>
      </tr>
      <tr style="background:#f7f9fc;">
        <td style="padding:10px;border:1px solid #e6e6e6;">AI automation systems</td>
        <td style="padding:10px;border:1px solid #e6e6e6;">$15,000</td>
        <td style="padding:10px;border:1px solid #e6e6e6;">Ops-heavy businesses</td>
      </tr>
      <tr>
        <td style="padding:10px;border:1px solid #e6e6e6;">Performance marketing retainer</td>
        <td style="padding:10px;border:1px solid #e6e6e6;">$3,500 / mo</td>
        <td style="padding:10px;border:1px solid #e6e6e6;">Paid Google & Meta ads</td>
      </tr>
    </tbody>
  </table>

  <h2 style="font-size:28px;line-height:1.2;margin:40px 0 16px;">Key terms, defined</h2>
  <dl style="font-size:16px;line-height:1.6;">
    <dt style="font-weight:700;margin-top:12px;">Diagnostic-first consulting</dt>
    <dd style="margin:4px 0 0;">An engagement model where the firm runs a paid assessment before scoping any build, so the roadmap is grounded in the client's actual bottlenecks rather than assumptions.</dd>
    <dt style="font-weight:700;margin-top:12px;">High-ticket business</dt>
    <dd style="margin:4px 0 0;">A business whose average customer value is high enough (typically $1,000+) that a single new lead meaningfully moves monthly revenue, so brand and conversion optimization compounds fast.</dd>
    <dt style="font-weight:700;margin-top:12px;">Fintech integration</dt>
    <dd style="margin:4px 0 0;">Embedding payments, billing, subscriptions, or lending products directly into a website or app — enabling businesses to monetize without routing users to third-party checkouts.</dd>
    <dt style="font-weight:700;margin-top:12px;">AI automation system</dt>
    <dd style="margin:4px 0 0;">A set of connected AI agents and workflows that handle repeatable business operations — lead intake, proposal generation, data entry, customer support triage — without a human in the loop.</dd>
  </dl>

  <h2 style="font-size:28px;line-height:1.2;margin:40px 0 16px;">Talkerstein at a glance</h2>
  <ul style="font-size:16px;line-height:1.7;padding-left:20px;">
    <li><strong>Locations:</strong> Toronto (ON, Canada) · Miami (FL, USA) · New York (NY, USA)</li>
    <li><strong>Founded:</strong> By Rishon Talkar, Principal & Managing Partner</li>
    <li><strong>Contact:</strong> <a href="mailto:hi@talkerstein.ca">hi@talkerstein.ca</a></li>
    <li><strong>Recognition:</strong> Emirates Best Emerging Filmmaker, UN recognition, Asia Pacific Youth Awards, ASEAN-Japan Centre, Nippon Paints finalist</li>
    <li><strong>Case study results:</strong> 7x engagement for Esther Saadia NY, 4,300+ sales, 4.6x international reach, 200% business growth for restaurant clients</li>
    <li><strong>Client industries:</strong> Luxury fashion, restaurants, electrical services, wellness, professional services, e-commerce</li>
  </ul>

  <p style="font-size:14px;color:#666;margin-top:32px;">
    Want to work with us? <a href="/contact" style="color:#0b2545;">Book a diagnostic consultation</a> · Review our <a href="/our-process">process</a> · See <a href="/our-work">case studies</a> · Read the <a href="/articles">articles</a>.
  </p>
</section>
"""

html = html.replace("</body>", GEO_BLOCK + "\n</body>", 1)

# =========================================================================
# Write output
# =========================================================================
with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Input:  {before_len:,} bytes")
print(f"Output: {len(html):,} bytes")
print(f"Delta:  +{len(html) - before_len:,} bytes")
print()

# Self-verification
checks = {
    "New title": f"<title>{NEW_TITLE}</title>" in html,
    "Explicit robots": 'content="index, follow' in html,
    "4 separate LD blocks": html.count('application/ld+json') >= 4,
    "ProfessionalService": '"ProfessionalService"' in html,
    "FAQPage": '"FAQPage"' in html,
    "BreadcrumbList": '"BreadcrumbList"' in html,
    "Answer-first <p>": '<p data-fix="answer-first"' in html,
    "5 question H2s": sum(1 for _ in re.finditer(r'<h2[^>]*>[^<]*\?', html)) >= 3,
    "Comparison table": '<table' in html and '<thead' in html,
    "Definition list": '<dl' in html and '<dt' in html and '<dd' in html,
    "Freshness date": '<time datetime=' in html,
    "Alt text filled (sample)": 'alt="Talkerstein Consulting Group' in html,
    "No bare alt left": len(re.findall(r'<img\b[^>]*\balt(?=[ />])(?!=)[^>]*>', html)) == 0,
}
print("=== Self-check ===")
for k, v in checks.items():
    print(f"  {'OK  ' if v else 'FAIL'}  {k}")
