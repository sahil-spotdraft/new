from enum import Enum
from typing import Optional

from core.mixins import ModelMixin


class CountryCode(Enum):
    INDIA = "+91"
    USA = "+1"
    RUSSIA = "+7"

    
class User(ModelMixin):
    meta = {
        "indexes": [
            {
                "fields": ["phone_number"],
                "name": "phone_number_map",
                "unique": True
            }
        ]
    }
    
    def __init__(
        self, 
        name: str, 
        phone_number: str,
        code: Optional[CountryCode] = CountryCode.INDIA.value,
        is_spam: Optional[bool] = False, 
    ):
        self.name = name
        self.code = code
        self.phone_number = self._validate_phone_number(phone_number)  # primary key (unique identifier)
        self.is_spam = is_spam  # global spam
        super().__init__()

    def _validate_phone_number(self, phone_number: str) -> str:
        if User.filter(["phone_number"], [phone_number]).count() == 1:
            raise Exception("User already exists")
        elif len(phone_number) != 10 or not phone_number.isdigit():
            raise Exception("Invalid phone number!!!")
        else:
            pass
        return phone_number
    
    def mark_as_spam(self):
        """Mark as global scam"""
        self.is_spam = True
    
    def unmark_as_spam(self):
        """Unmark as global scam"""
        self.is_spam = False
