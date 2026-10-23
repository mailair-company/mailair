"""
Daily social post content — a 7-day rotation of themes, each backed by
real product copy or real data (never a fabricated stat, never an
invented testimonial). Edit the lists below as the product changes;
nothing here calls an LLM, so output is predictable and won't drift or
hallucinate.

No testimonial theme yet — there are no real customer quotes to use,
and made-up ones aren't going up. social_image.py still has the
pull-quote template ready to switch on the day there's real ones.

Each theme also maps to a distinct visual template (see social_image.py)
so the feed doesn't look like the same card recolored every day.
"""
from datetime import date

# Each feature carries a `problem` line (what it's like without Mailair)
# and a `fix` line (what Mailair does) — used as a 3-slide carousel:
# problem -> feature -> "how it looks" mockup. Deliberately NOT all
# phrased the same way — some are blunt, some are a question, some
# just state the fact — so twelve in a row don't read like a template.
FEATURES = [
    # Email marketing + team hub first — that's the positioning. The AI
    # inbox features follow as the reason the hub is smarter than a bundle.
    {
        "problem": "Your customer list lives in a spreadsheet, and the last newsletter went out in March.",
        "headline": "Email campaigns, built in",
        "body": "Paste in your contacts, write the campaign, hit send. Opens, clicks, bounces, and unsubscribes are tracked for you.",
    },
    {
        "problem": "A lead says \"interested\" — and then nobody follows up for a week.",
        "headline": "Follow-up sequences that keep going",
        "body": "Set the steps once. Mailair sends the follow-ups on schedule, so no lead quietly goes cold.",
    },
    {
        "problem": "One tool for marketing, one for email, one for chat, one for calls. Four logins, zero shared context.",
        "headline": "One hub instead of five tools",
        "body": "Campaigns, a shared inbox, docs, files, chat, and calls — in one place, built for small teams.",
    },
    {
        "problem": "The latest proposal is in someone's Downloads folder. Again.",
        "headline": "Docs, files, and chat your whole team can see",
        "body": "A shared workspace for the things your team keeps asking each other for.",
    },
    {
        "problem": "Opening a separate app just to call a client you were emailing a minute ago.",
        "headline": "Voice and video calls, built in",
        "body": "Start a call from the same place you work with the client. No extra subscription.",
    },
    {
        "problem": "Half the team is on Gmail. The other half is on Outlook.",
        "headline": "Gmail and Outlook in one inbox",
        "body": "Connect both and work from a single inbox — sorted by AI, so the urgent ones come first.",
    },
    {
        "problem": "Your CRM says one thing. Your inbox says another.",
        "headline": "Works with HubSpot, Salesforce, and Slack",
        "body": "Mailair plugs into the tools you already use, so the hub doesn't become another island.",
    },
    {
        "problem": "The important email is buried under eleven newsletters.",
        "headline": "Priority inbox, sorted before you open it",
        "body": "Urgent, needs-response, follow-up, FYI. Sorted before you've had coffee.",
    },
    {
        "problem": "Every AI reply tool writes like it's from customer support.",
        "headline": "AI drafts that sound like you",
        "body": "Mailair scores how close each draft is to what you actually sent — a real number, not a vibe, and it climbs the more you use it.",
    },
    {
        "problem": "A great client goes quiet, and the invoice quietly dies with the relationship.",
        "headline": "See revenue before it walks out the door",
        "body": "Open quotes and invoices, crossed with which relationships are fading. The deal to chase first is usually the coldest one, not the biggest.",
    },
    {
        "problem": "A client who used to email weekly has gone quiet for a month. Nobody noticed until now.",
        "headline": "A health score for every client relationship",
        "body": "Recency, frequency, response patterns — tracked so the quiet ones get flagged before they're gone for good.",
    },
    {
        "problem": "Re-reading a whole thread just to remember what you promised — again.",
        "headline": "Action items, pulled out automatically",
        "body": "Task and deadline, lifted straight out of the email. Check it off when it's done.",
    },
]

PAIN_POINTS = [
    # Deliberately mixed lengths — a one-liner next to a real paragraph,
    # so the rotation doesn't settle into one rhythm.
    "Small businesses don't need an enterprise suite. They need one place that does the five things they actually use.",
    "Your customer list is the most valuable thing you own. Most small businesses email it twice a year.",
    "Five tools, five logins, five bills — and still nobody knows where the latest proposal is.",
    "A lead that waits a week for a follow-up usually stops waiting.",
    "Switching between your marketing tool and your inbox isn't a workflow. It's a tax.",
    "\"I'll reply later\" is how a $15k contract quietly disappears.",
    "Big companies get a connected suite and an IT department to run it. Small teams get a pile of free trials and a spreadsheet holding it all together.",
    "Silence from a client isn't the same as satisfaction. It's usually the opposite, and it's the easiest signal in the world to miss.",
]

FOUNDER_VOICE = [
    "We started Mailair to sort an inbox. Customers kept asking for one place to market and work as a team. So that's what it's becoming.",
    "Small teams deserve the connected tools big companies get from enterprise suites — without the price tag or the IT department.",
    "No growth hacks this week — just fixed a bug where the plan-limit banner showed the wrong count. Small things matter.",
    "Shipping something most weeks. Not because it's a rule — because a hub that stops improving stops being useful.",
    "We don't want Mailair to feel clever. We want it to feel like it noticed the thing you were about to miss.",
    "Spent today's build time on something nobody will ever screenshot: making the sync job stop double-counting emails. It had been wrong for weeks until a support email pointed it out.",
    "If you've emailed and we were slow, that's on us, not a policy.",
    "Every feature in here exists because we hit the problem ourselves first, usually while annoyed.",
    "Wrote three versions of the pricing page before one didn't sound like every other SaaS pricing page. Still not sure we nailed it.",
]

TIPS = [
    "Email your customers on a rhythm they can predict. Monthly beats \"whenever we remember.\"",
    "Remove addresses that bounce. Sending to dead emails hurts delivery for the live ones.",
    "One campaign, one call to action. Two buttons usually means neither gets clicked.",
    "Write the follow-up before you send the first email. If there's no second step, there's no sequence.",
    "Keep subject lines short — most phones cut them off long before you think.",
    "Shared files belong where the whole team can find them, not buried in one person's inbox.",
    "Reply to the oldest urgent email first, not the newest one. Recency bias is why things sit for weeks.",
    "The client who emails the least is often the one closest to leaving.",
]

# Real shipped changelog entries — mirrors frontend/pages/changelog.tsx.
# Update this list when that page's `releases` array changes.
CHANGELOG = [
    "Email marketing campaigns: build an audience, send a campaign, and track opens, clicks, bounces, and unsubscribes.",
    "Built-in voice and video calls, right inside Mailair.",
    "A team workspace with shared docs, files, and chat.",
    "The mobile app now matches the web: campaigns, calls, and workspace on iOS and Android.",
    "Outlook support — Gmail and Outlook in one inbox.",
    "Manual AI processing per email — click \"Process with AI\" to control your own usage.",
    "Email body renders as HTML inside a sandboxed iframe, like Gmail.",
    "Razorpay integration — accept subscription payments from India.",
    "HMAC-SHA256 signed OAuth state on the Gmail connect flow, closing a CSRF gap.",
    "Fernet encryption for stored CRM credentials (HubSpot, Salesforce).",
    "AI email categorization shipped: Urgent, Needs Response, Follow Up, FYI, Newsletter, Spam.",
    "Smart reply drafts using Claude, tuned to your tone preference.",
    "Google Calendar integration that detects meeting requests inside emails.",
]

TAGLINE = "Email Marketing & Team Hub for Small Businesses"

# The first HUB_FEATURE_COUNT entries in FEATURES are the marketing/hub
# ones; two of the three weekly feature slots draw only from those.
HUB_FEATURE_COUNT = 7
AI_FEATURE_DAY = 2  # Wednesday

THEMES = ["feature", "pain_point", "feature", "tip", "founder", "changelog", "feature"]  # Mon..Sun


def get_todays_post(today: date | None = None) -> dict:
    """
    Deterministic pick — same day always yields the same content, so a
    retry after a failed post doesn't produce something different.

    Returns either a single-image post ({"slides": [one dict]}) or a
    carousel ({"slides": [2-3 dicts]}) — feature days are carousels.
    """
    d = today or date.today()
    weekday = d.weekday()  # 0=Mon .. 6=Sun
    theme = THEMES[weekday]
    ordinal = d.toordinal()

    if theme == "feature":
        week = (ordinal - weekday) // 7  # Monday-aligned week number
        if weekday == AI_FEATURE_DAY:
            item = FEATURES[HUB_FEATURE_COUNT:][week % (len(FEATURES) - HUB_FEATURE_COUNT)]
        else:
            # Mon and Sun each get a different hub feature every week.
            slot = week * 2 + (1 if weekday == 6 else 0)
            item = FEATURES[slot % HUB_FEATURE_COUNT]
        # Alternate whether the CTA line shows up — not every post needs one.
        caption = f"{item['headline']}\n\n{item['body']}"
        if ordinal % 2 == 0:
            caption += f"\n\nMailair — {TAGLINE}.\nmailair.company"
        slides = [
            {"template": "statement", "text": item["problem"], "tagline": None},
            {"template": "card", "headline": item["headline"], "subtext": item["body"]},
            {"template": "mockup", "headline": None, "subtext": None},
        ]
    elif theme == "pain_point":
        line = PAIN_POINTS[ordinal % len(PAIN_POINTS)]
        caption = line
        slides = [{"template": "statement", "text": line, "tagline": TAGLINE}]
    elif theme == "tip":
        line = TIPS[ordinal % len(TIPS)]
        # Only prefix "Small business tip:" about half the time — a bare line reads
        # less like a recurring content slot and more like a thought.
        caption = f"Small business tip:\n\n{line}" if ordinal % 3 != 0 else line
        slides = [{"template": "card", "headline": "Small business tip", "subtext": line}]
    elif theme == "founder":
        line = FOUNDER_VOICE[ordinal % len(FOUNDER_VOICE)]
        caption = line
        slides = [{"template": "statement", "text": line, "tagline": "from the founders"}]
    else:  # changelog
        line = CHANGELOG[ordinal % len(CHANGELOG)]
        # Same: the "every update documented" line doesn't need to run every week.
        caption = f"Shipped: {line}"
        if ordinal % 2 == 0:
            caption += "\n\nEvery update, documented at mailair.company/changelog."
        slides = [{"template": "badge", "text": line}]

    return {"theme": theme, "caption": caption, "slides": slides}
