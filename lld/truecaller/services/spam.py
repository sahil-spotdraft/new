from core.exceptions import Raise404
from models.spam import GLOBAL_SCAM_LIMIT, Spam
from models.user import User


class SpamService:
    @staticmethod
    def report_spam(user_id: int, spam_user_id: int) -> Spam:
        user = User.get(user_id)
        spam_user = User.get(spam_user_id)
        spam = Spam(user=user, spam_user=spam_user)
        SpamService._check_global_scam(spam_user)
        return spam

    @staticmethod
    def remove_spam(user_id: int, spam_user_id: int):
        user = User.get(user_id)
        spam_user = User.get(spam_user_id)
        spam = Spam.filter(["user", "spam_user"], [user, spam_user])
        if not spam: 
            raise Raise404
        spam_id = spam[0].id
        Spam.delete(ids=[spam_id])
        SpamService._check_global_scam(spam_user)

    def _check_global_scam(spam_user: User):
        if Spam.filter(["spam_user"], [spam_user]).count() >= GLOBAL_SCAM_LIMIT:
            spam_user.mark_as_spam()
        else:
            spam_user.unmark_as_spam()

    @staticmethod
    def spam_count(user: User):
        return Spam.filter(["spam_user"], [user.id]).count()
    
    @staticmethod
    def check_user_in_spam(
        user: User, spam_user: User
    ) -> bool:
        """
            - Check user is marked as global scam
            - Check if given user is in scam 
              list of the other user
        """
        if spam_user.is_spam:
            return True
        if Spam.filter(
            ["user", "spam_user"], [user, spam_user]
        ).count():
            return True

        return False
    