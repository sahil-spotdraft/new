from core.mixins import ModelMixin
from models.user import User


class Contact(ModelMixin):
    meta = {
        "indexes": [
            {
                "fields": ["user"],
                "name": "contact_list",
                "unique": False
            },
        ],
    }

    def __init__(
        self,
        user: User,
        contact_user: User,
        contact_name: str = ""
    ):
        self.user = user
        self.contact_user = contact_user
        if contact_name:
            self.contact_name = contact_name
        else:
            self.contact_name = self.contact_user.name
        super().__init__()


class BlockUser(ModelMixin):
    meta = {
        "indexes": [
            {
                "fields": ["user"],
                "name": "block_list",
                "unique": False
            },
            {
                "fields": ["user", "contact_user"],
                "name": "block_list_map",
                "unique": True
            },
        ],
    }

    def __init__(
        self,
        user: User,
        contact_user: User,
    ):
        self.user = user
        self.contact_user = contact_user
        super().__init__()
