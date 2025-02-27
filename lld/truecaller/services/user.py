from core.exceptions import Raise404
from models.user import User
from services.spam import SpamService


# class CallMessage:
#     def __init__(
#         self,
#         from_number: str,
#         in_spam: bool,
#         spam_count: int,
#     ) -> None:
#         self.from_number = from_number
#         self.in_spam = 


class UserService:
    @staticmethod
    def register_user(
        name: str, phone_number: str
    ) -> User:
        return User(name=name, phone_number=phone_number)
    
    @staticmethod
    def check_gloabl_scam(
        user: User
    ) -> bool:
        """
            - Check user is marked as global scam
        """
        return user.is_spam
    
    @staticmethod
    def notify(from_user: "User", to_user: "User"):
        spam_count = SpamService.spam_count(to_user)
        in_spam = to_user.check_user_in_spam(from_user)
        print(
            f"{ in_spam } | { spam_count }"
        )

    @staticmethod
    def get_user_by_phone_number(
        phone_number: str
    ) -> User:
        try:
            return User.phone_number_map[phone_number]
        except KeyError:
            raise Raise404