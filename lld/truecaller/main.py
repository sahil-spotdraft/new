from models.spam import Spam
from models.user import User


user1 = User(name="Alice", phone_number="1234567890")
user2 = User(name="Bob", phone_number="2345678901")
user3 = User(name="Charlie", phone_number="3456789012")
user4 = User(name="David", phone_number="4567890123")
user5 = User(name="Eve", phone_number="5678901234")
user6 = User(name="Frank", phone_number="6789012345")
user7 = User(name="Grace", phone_number="7890123456")
user8 = User(name="Henry", phone_number="8901234567")
user9 = User(name="Ivy", phone_number="9012345678")
# user10 = User(name="Jack", phone_number="0123456789")

# Spam(user1, user2)
# Spam(user3, user2)

# # print(
# #     {
# #         id: user.to_dict()
# #         for id, user in User.__objects.items()
# #     }
# # )

# def make_call(u1, u2):
#     User.notify(u2, u1)

# print(User.filter(["phone_number"], [user1.phone_number]))
# print(User.filter(["name"], ["Bob", "eve"]))

from application import TrueCaller


# TrueCaller.register_user(
#     name="Alice",phone_number="1234567890"
# )
# TrueCaller.register_user(
#     name="Bob", phone_number="2345678901"
# )
# TrueCaller.register_user(
#     name="Jack", phone_number="0123456789"
# )

# user = TrueCaller.get_user_by_phone_number

# TrueCaller.report_spam(
#     user1, user2
# )

def start():
    TrueCaller.start_cli()

start()
breakpoint()


"""
add_contact user_id=1,contact_user_id=4,contact_name=user-1-4
block_user user_id=1,block_user_id=4
unblock_user user_id=1,block_user_id=4
"""