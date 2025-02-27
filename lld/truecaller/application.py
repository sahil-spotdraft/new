import inspect
from typing import List, Tuple

from core.application import CommandLineApplication
from models.contact import BlockUser, Contact
from models.spam import Spam
from models.user import User
from services.contact import ContactService
from services.spam import SpamService
from services.user import UserService


commands = {}
def tc_make_command(help: str):
    def decorator(func):
        commands[func.__name__] = {
            "method": func,
            **{
                param.name: param.annotation 
                for param in inspect.signature(func).parameters.values()
            },
            "help": help
        }
        return func
    return decorator


class TrueCaller(CommandLineApplication):
    @staticmethod
    @tc_make_command(help="Register user")
    def register_user(
        name: str, phone_number: str
    ) -> User:
        return UserService.register_user(name=name, phone_number=phone_number)

    @staticmethod
    @tc_make_command(help="get_user_by_phone_number")
    def get_user_by_phone_number(
        phone_number: str
    ) -> User:
        return UserService.get_user_by_phone_number(phone_number)
    
    @staticmethod
    @tc_make_command(help="report_spam")
    def report_spam(user_id: int, spam_user_id: int) -> Spam:
        return SpamService.report_spam(user_id=user_id, spam_user_id=spam_user_id)
    
    @staticmethod
    @tc_make_command(help="add_contact")
    def add_contact(user_id: int, contact_user_id: int, contact_name: str = "") -> Contact:
        return ContactService.add_contact(user_id=user_id, contact_user_id=contact_user_id, contact_name=contact_name)
    
    @staticmethod
    @tc_make_command(help="add_contact")
    def user_contacts(
        user_id: int
    ) -> Tuple[List[User], int]:
        contacts, count = ContactService.user_contacts(user_id=user_id)
        return contacts, len(contacts)
    
    @staticmethod
    @tc_make_command(help="add_to_block_list")
    def block_user(user_id: int, block_user_id: int):
        user = User.get(user_id)
        contact_user = User.get(block_user_id)
        block_user = BlockUser(user=user, contact_user=contact_user)
        return block_user
    
    @staticmethod
    @tc_make_command(help="unblock_user")
    def unblock_user(user_id: int, block_user_id: int):
        # user = User.get(user_id)
        # contact_user = User.get(block_user_id)
        block_user = BlockUser.block_list_map[(user_id, block_user_id)]
        BlockUser.delete(ids=[block_user.id])


setattr(
    TrueCaller, "commands", commands
)
