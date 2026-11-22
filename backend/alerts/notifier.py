"""
Automated alert & notification engine.

Defaults to console/log output so the whole project runs with zero API keys.
Set NOTIFY_CHANNEL=twilio (and the TWILIO_* env vars) to actually send SMS,
or extend send() with a WhatsApp Business API call the same way.
"""
import config


def send(message: str, severity: str = "MEDIUM"):
    """Dispatches a notification through the configured channel."""
    if config.NOTIFY_CHANNEL == "twilio":
        _send_twilio(message)
    else:
        _send_console(message, severity)


def _send_console(message: str, severity: str):
    print(f"[CMAC ALERT | {severity}] {message}")


def _send_twilio(message: str):
    """
    Optional: requires `pip install twilio` and TWILIO_* env vars set.
    Left as an isolated function so the core project has zero required
    external service dependencies.
    """
    try:
        from twilio.rest import Client
    except ImportError:
        print("[CMAC ALERT] twilio package not installed — falling back to console.")
        _send_console(message, "MEDIUM")
        return

    client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=f"CMAC ALERT: {message}",
        from_=config.TWILIO_FROM_NUMBER,
        to=config.ALERT_TO_NUMBER,
    )
