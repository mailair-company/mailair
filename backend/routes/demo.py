"""
"Book a demo" requests from the landing page.

Saved to demo_requests, then emailed to ADMIN_EMAIL with Reply-To set to
the requester, so the founders can answer straight from their inbox
(mailair.company can't receive mail yet, see issue #3). The requester
gets a short confirmation. Email failures never fail the request — the
row is already saved.
"""
import html
import logging

import httpx
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, EmailStr, Field

from config import settings
from database import get_supabase
from limiter import limiter

logger = logging.getLogger(__name__)
router = APIRouter()

RESEND_API = "https://api.resend.com/emails"
INTEREST_LABELS = {
    "campaigns": "Email campaigns",
    "inbox": "AI-sorted inbox",
    "workspace": "Team workspace & calls",
    "integrations": "CRM & integrations",
}


class DemoRequest(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    email: EmailStr
    company: str = Field(default="", max_length=160)
    team_size: str = Field(default="", max_length=20)
    interests: list[str] = Field(default_factory=list, max_length=4)
    message: str = Field(default="", max_length=2000)


def _row(label: str, value: str) -> str:
    return (
        f'<tr><td style="padding:8px 12px;color:#635646;font-size:13px;width:120px;vertical-align:top;">{label}</td>'
        f'<td style="padding:8px 12px;color:#221c16;font-size:14px;">{value or "—"}</td></tr>'
    )


async def _send_emails(req: DemoRequest, interests: list[str]) -> None:
    if not settings.RESEND_API_KEY:
        return

    e = html.escape
    interest_text = ", ".join(INTEREST_LABELS[i] for i in interests)
    first = e(req.name.split()[0])
    headers = {"Authorization": f"Bearer {settings.RESEND_API_KEY}"}

    async with httpx.AsyncClient(timeout=10) as client:
        if settings.ADMIN_EMAIL:
            await client.post(RESEND_API, headers=headers, json={
                "from": "Mailair Demos <hello@mailair.company>",
                "to": [settings.ADMIN_EMAIL],
                "reply_to": req.email,
                "subject": f"Demo request: {req.name}" + (f" ({req.company})" if req.company else ""),
                "html": (
                    '<div style="font-family:sans-serif;max-width:520px;margin:24px auto;">'
                    '<h2 style="color:#221c16;font-size:18px;margin:0 0 4px;">New demo request</h2>'
                    '<p style="color:#635646;font-size:13px;margin:0 0 16px;">Reply to this email to answer them directly.</p>'
                    '<table style="width:100%;border-collapse:collapse;background:#faf3ec;border-radius:8px;">'
                    + _row("Name", e(req.name))
                    + _row("Email", e(req.email))
                    + _row("Company", e(req.company))
                    + _row("Team size", e(req.team_size))
                    + _row("Interested in", e(interest_text))
                    + _row("Message", e(req.message).replace("\n", "<br>"))
                    + "</table></div>"
                ),
            })

        await client.post(RESEND_API, headers=headers, json={
            "from": "Mailair <hello@mailair.company>",
            "to": [req.email],
            "subject": "We got your Mailair demo request",
            "html": (
                '<div style="font-family:sans-serif;max-width:520px;margin:24px auto;color:#221c16;font-size:15px;line-height:1.6;">'
                f"<p>Hi {first},</p>"
                "<p>Thanks for asking for a demo of Mailair. We'll reply within one business day "
                "to find a time that works — usually a 20-minute call where we show campaigns, "
                "the shared inbox, and the team workspace using your own use case.</p>"
                "<p>— The Mailair team<br>"
                '<a href="https://mailair.company" style="color:#b04723;">mailair.company</a></p>'
                "</div>"
            ),
        })


@router.post("/api/public/demo-request")
@limiter.limit("5/minute")
async def request_demo(request: Request, body: DemoRequest):
    interests = [i for i in body.interests if i in INTEREST_LABELS]
    try:
        get_supabase().table("demo_requests").insert({
            "name": body.name.strip(),
            "email": body.email,
            "company": body.company.strip(),
            "team_size": body.team_size,
            "interests": interests,
            "message": body.message.strip(),
        }).execute()
    except Exception as exc:
        logger.error("Saving demo request failed: %s", exc)
        raise HTTPException(status_code=500, detail="Couldn't save your request. Please try again.")

    try:
        await _send_emails(body, interests)
    except Exception as exc:
        logger.error("Demo request emails failed (request saved): %s", exc)

    return {"ok": True}
