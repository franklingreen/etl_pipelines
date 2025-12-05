from typing import TypedDict, Optional


class Recipient(TypedDict):
    typ: str
    sms_active: bool
    email_active: bool
    mobile: Optional[str]
    email: str