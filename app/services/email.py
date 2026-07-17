from fastapi_mail import ConnectionConfig
from app.core.config import settings
from fastapi_mail import FastMail, MessageSchema, MessageType

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    USE_CREDENTIALS=True,
)

async def send_email(recipients: list[str],subject: str,body: str) -> None:

    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        body=body,
        subtype=MessageType.plain,
    )

    fm = FastMail(conf)

    await fm.send_message(message)


async def send_verification_email(email: str,code: str,):
    body = f"""
    Hello,

    Welcome to AI Meeting!

    Your verification code is:

    {code}

    This code expires in 10 minutes.

    If you didn't create this account,
    please ignore this email.

    AI Meeting Team
    """

    await send_email(
        recipients=[email],
        subject="Verify your email",
        body=body,
    )