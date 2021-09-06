from nemo_alchemy import session
from nemo_alchemy.models import Profile

# # # Insert
# # new_user = User(username='Lendiz', password='123456', role_id=3, is_active=1)
# # session.add(new_user)
# # session.commit()
# new_data = {}

profile_inn = '3225605745'
# Select
an_user = session.query(Profile).filter_by(inn=profile_inn).first()
print(an_user)
# an_user = a_session.query(Profile).filter_by(inn=profile_inn).first()
# if an_user:
#     new_data['parent_person_id'] = an_user.person_id
# # Update
# # an_user.password = '654321'
# # session.commit()
# print(new_data)

# inn = ' 41100480 –'
# inn = inn.strip().strip('-')
# print(inn)

inn1 = ' 2323617731'
inn1 = inn1.strip('-')
print(inn1)
