from core.mixins import ModelMixin
from models.user import User


GLOBAL_SCAM_LIMIT = 10
class Spam(ModelMixin):
    meta = {
        "indexes": [
            {
                "fields": ["user", "spam_user"],
                "name": "spam_map",
                "unique": True
            },
            {
                "fields": ["spam_user"],
                "name": "spam_count",
                "unique": False
            },
        ],
    }

    def __init__(
        self,
        user: User,
        spam_user: User
    ):
        self.user = user
        self.spam_user = spam_user
        super().__init__()
