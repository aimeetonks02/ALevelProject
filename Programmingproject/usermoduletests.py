import usermodule

# find a user
aimee = usermodule.find_user()
print(aimee)
print(aimee.userID)
print(aimee.username)
print(aimee.role)
print(aimee.email)


# change the user's email
# aimee.change_email()
# print(aimee.email)

# prove that the email address has been changed in the database
# aimee = usermodule.find_user()
# print(aimee)
# print(aimee.userID)
# print(aimee.username)
# print(aimee.role)
# print(aimee.email)

usermodule.list_users()