from typing import List, Tuple
from core.exceptions import Raise404
from models.contact import Contact
from models.user import User


class ContactService:
    @staticmethod
    def user_contacts(
        user: User
    ) -> Tuple[List[User], int]:
        try:
            contacts = Contact.contact_list[user]
            return contacts, len(contacts)
        except KeyError:
            raise Raise404
        
    @staticmethod
    def add_contact(user_id: User, contact_user_id: User, contact_name: str = "") -> Contact:
        user = User.get(user_id)
        contact_user = User.get(contact_user_id)
        return Contact(user=user, contact_user=contact_user, contact_name=contact_name)
    
    @staticmethod
    def user_contacts(
        user_id: int
    ) -> Tuple[List[User], int]:
        contacts = Contact.contact_list[user_id]
        return contacts, len(contacts)
