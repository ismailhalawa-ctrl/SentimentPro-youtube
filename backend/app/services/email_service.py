import html
import logging
import smtplib
import ssl
from datetime import UTC, datetime
from email.message import EmailMessage

from app.core.config import settings

logger = logging.getLogger(__name__)


class EmailNotConfiguredError(Exception):
    pass


class EmailSendError(Exception):
    pass


def is_configured() -> bool:
    return bool(settings.smtp_host and settings.smtp_from_email)


def send_email(to: str, subject: str, html_body: str, reply_to: str | None = None) -> None:
    if not is_configured():
        raise EmailNotConfiguredError("SMTP is not configured.")

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = settings.smtp_from_email
    message["To"] = to
    if reply_to:
        message["Reply-To"] = reply_to
    message.set_content(html_body, subtype="html")

    try:
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=10) as server:
            if settings.smtp_use_tls:
                server.starttls(context=ssl.create_default_context())
            if settings.smtp_username and settings.smtp_password:
                server.login(settings.smtp_username, settings.smtp_password)
            server.send_message(message)
    except smtplib.SMTPAuthenticationError as e:
        logger.error("SMTP authentication rejected by %s: %s", settings.smtp_host, e)
        raise EmailSendError("SMTP authentication failed.") from e
    except (smtplib.SMTPConnectError, smtplib.SMTPServerDisconnected, TimeoutError, OSError) as e:
        logger.error("Could not connect to SMTP server %s:%s: %s", settings.smtp_host, settings.smtp_port, e)
        raise EmailSendError("Could not connect to the SMTP server.") from e
    except ssl.SSLError as e:
        logger.error("TLS handshake with %s failed: %s", settings.smtp_host, e)
        raise EmailSendError("SMTP TLS handshake failed.") from e
    except smtplib.SMTPException as e:
        logger.error("SMTP error sending to %s: %s", to, e)
        raise EmailSendError("SMTP error while sending the email.") from e


_FONT_STACK = "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"

_SPARKLES_GLYPH = (
    '<span style="color: #FAFAFA; font-size: 16px; line-height: 32px; '
    'font-family: Arial, sans-serif;">&#10022;</span>'
)


def _render_email_shell(title: str, preheader: str, heading: str, body_html: str) -> str:
    year = datetime.now(UTC).year
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="color-scheme" content="dark">
        <title>{title}</title>
        <style>
            @media (max-width: 600px) {{
                .container {{ width: 100% !important; }}
                .content-padding {{ padding-left: 20px !important; padding-right: 20px !important; }}
                .cta-link {{ display: block !important; width: 100% !important; box-sizing: border-box; }}
            }}
        </style>
    </head>
    <body style="margin: 0; padding: 0; background-color: #0A0A0B; font-family: {_FONT_STACK}; -webkit-font-smoothing: antialiased;">
        <div style="display: none; max-height: 0; overflow: hidden; opacity: 0;">
            {preheader}
        </div>
        <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #0A0A0B; padding: 40px 20px;">
            <tr>
                <td align="center">
                    <table role="presentation" class="container" border="0" cellpadding="0" cellspacing="0" width="600" style="max-width: 600px; background-color: #141416; border-radius: 16px; overflow: hidden; border: 1px solid #27272A;">
                        <tr>
                            <td align="center" style="background-color: #0A0A0B; padding: 32px 20px; border-bottom: 1px solid #1F1F22;">
                                <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                                    <tr>
                                        <td style="padding-right: 10px; vertical-align: middle;">
                                            <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="32" height="32" style="width: 32px; height: 32px; border-radius: 8px; background-color: #6366F1; background-image: linear-gradient(135deg, #6366F1 0%, #818CF8 100%);">
                                                <tr>
                                                    <td align="center" valign="middle">{_SPARKLES_GLYPH}</td>
                                                </tr>
                                            </table>
                                        </td>
                                        <td style="vertical-align: middle;">
                                            <span style="color: #FAFAFA; font-size: 18px; font-weight: 600; letter-spacing: -0.2px;">
                                                Sentiment<span style="color: #818CF8;">PRO</span>
                                            </span>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>

                        <tr>
                            <td class="content-padding" style="padding: 40px 32px; text-align: left;">
                                <h1 style="color: #FAFAFA; font-size: 20px; margin: 0 0 16px; font-weight: 600;">
                                    {heading}
                                </h1>
                                {body_html}
                            </td>
                        </tr>

                        <tr>
                            <td align="center" style="background-color: #0A0A0B; padding: 20px; border-top: 1px solid #1F1F22; color: #71717A; font-size: 12px;">
                                &copy; {year} SentimentPRO. All rights reserved.
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """


def send_password_reset_email(to: str, reset_link: str) -> None:
    body_html = f"""
    <p style="color: #A1A1AA; font-size: 15px; line-height: 1.6; margin: 0 0 28px;">
        I received a request to reset the password for your <strong style="color: #FAFAFA;">SentimentPRO</strong> account. Click the button below to choose a new one.
    </p>

    <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" style="margin-bottom: 32px;">
        <tr>
            <td align="center">
                <a href="{reset_link}" target="_blank" class="cta-link" style="display: inline-block; background-color: #6366F1; color: #FAFAFA; font-size: 15px; font-weight: 600; text-decoration: none; padding: 14px 36px; border-radius: 8px; box-shadow: 0 0 20px rgba(99, 102, 241, 0.35);">
                    Reset Password
                </a>
            </td>
        </tr>
    </table>

    <p style="color: #A1A1AA; font-size: 13px; line-height: 1.5; margin: 0 0 24px; background-color: #0A0A0B; padding: 14px 18px; border-radius: 8px; border-left: 3px solid #818CF8;">
        <strong style="color: #818CF8;">Note:</strong> This link expires in <strong>60 minutes</strong>. If you didn't request this, you can safely ignore this email.
    </p>

    <hr style="border: none; border-top: 1px solid #1F1F22; margin: 28px 0;" />

    <p style="color: #71717A; font-size: 12px; line-height: 1.5; margin: 0; word-break: break-all;">
        If the button doesn't work, copy and paste this link into your browser:<br>
        <a href="{reset_link}" style="color: #818CF8; text-decoration: underline;">{reset_link}</a>
    </p>
    """
    html_body = _render_email_shell(
        "Reset your SentimentPRO password",
        "Reset your SentimentPRO password. This link expires in 60 minutes.",
        "Reset your password",
        body_html,
    )
    send_email(to, "Reset your SentimentPRO password", html_body)


def send_contact_notification_email(name: str, email: str, message: str) -> None:
    safe_name = html.escape(name)
    safe_email = html.escape(email)
    safe_message = html.escape(message).replace("\n", "<br>")

    body_html = f"""
    <p style="color: #A1A1AA; font-size: 15px; line-height: 1.6; margin: 0 0 24px;">
        Someone just submitted the Contact form on SentimentPRO.
    </p>

    <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" style="margin: 0 0 20px; background-color: #0A0A0B; border-radius: 8px; border: 1px solid #1F1F22;">
        <tr>
            <td style="padding: 14px 18px; border-bottom: 1px solid #1F1F22;">
                <span style="color: #71717A; font-size: 12px; text-transform: uppercase; letter-spacing: 0.4px;">From</span><br>
                <span style="color: #FAFAFA; font-size: 15px; font-weight: 600;">{safe_name}</span>
            </td>
        </tr>
        <tr>
            <td style="padding: 14px 18px;">
                <span style="color: #71717A; font-size: 12px; text-transform: uppercase; letter-spacing: 0.4px;">Email</span><br>
                <a href="mailto:{safe_email}" style="color: #818CF8; font-size: 15px; text-decoration: none;">{safe_email}</a>
            </td>
        </tr>
    </table>

    <p style="color: #71717A; font-size: 12px; margin: 0 0 8px; text-transform: uppercase; letter-spacing: 0.4px;">
        Message
    </p>
    <p style="color: #FAFAFA; font-size: 15px; line-height: 1.6; margin: 0 0 28px; background-color: #0A0A0B; padding: 16px 18px; border-radius: 8px; border-left: 3px solid #818CF8;">
        {safe_message}
    </p>

    <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">
        <tr>
            <td align="center">
                <a href="mailto:{safe_email}" class="cta-link" style="display: inline-block; background-color: #6366F1; color: #FAFAFA; font-size: 15px; font-weight: 600; text-decoration: none; padding: 14px 36px; border-radius: 8px; box-shadow: 0 0 20px rgba(99, 102, 241, 0.35);">
                    Reply to {safe_name}
                </a>
            </td>
        </tr>
    </table>
    """
    html_body = _render_email_shell(
        f"New contact message from {safe_name}",
        f"New contact form message from {safe_name} ({safe_email})",
        "New contact message",
        body_html,
    )
    send_email(
        settings.support_email,
        f"New contact message from {name}",
        html_body,
        reply_to=email,
    )
