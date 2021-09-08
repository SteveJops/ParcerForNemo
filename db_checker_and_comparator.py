from datetime import datetime
from tqdm import tqdm
from nemo_alchemy.models import Profile, Link
from nemo_alchemy import session as a_session
import pandas as pd


def parse_data_from_file(path_to: str) -> tuple:
    """[The func is exctracting data from info.xlsx]

    Args:
        path_to (str): [the str with path to file]

    Returns:
        tuple: [returns tuples with sorted and formated data from info.xlsx]
    """
    read_excel = pd.read_excel(path_to, sheet_name='Sheet1')
    index_inn = read_excel['client_INN'].to_list()
    user_pib = read_excel['client_PIB'].to_list()
    user_path = read_excel['path'].to_list()
    relative_connection_inn_profile = read_excel["client_parent_INN"].to_list()
    relative_connection_pib_profile = read_excel['client_parent_PIB'].to_list()
    relative_connection_path = read_excel['relative_path'].to_list()
    return index_inn, user_pib, user_path, relative_connection_inn_profile, relative_connection_pib_profile, relative_connection_path


def db_check_info_and_add(profile_data: tuple):
    """[The func is cheking and updating info about user if exists in our db
    if not adds it]

    Args:
        profile_data (tuple): [tuple with lists of data about clients]
    """
    df = pd.DataFrame()
    df1 = pd.DataFrame()
    (index_inn, user_pib, user_path_to_file,  relative_connection_inn_profile, relative_connection_pib_profile, relative_connection_path) = profile_data
    # variable to designation what the relative will be in the current
    # iterating
    index = 0
    for profile_inn in tqdm(index_inn):
        new_data = {}
        dict_data_with_not_find = {}
        try:
            if profile_inn:
                print(f"Profile INN: {profile_inn}")
                # inn from file is getting as float
                profile_inn = int(profile_inn)
                profile_inn = str(profile_inn)
                # request to look for a person_id by inn
                an_user = a_session.query(Profile).filter_by(
                    inn=profile_inn
                    ).all()

                if an_user:
                    # if user exist than adds all the info that we need
                    # to new_data dict
                    print(f"User data in the base: {an_user}")
                    an_user = str(an_user[0]).split(" ")
                    an_user = int(an_user[1])
                    new_data['parent_person_id'] = an_user
                    new_data['parent_inn'] = int(profile_inn)
                    new_data['parent_pib'] = str(
                        user_pib[index]
                        ).split("\n")[0]
                    new_data['parent_path'] = user_path_to_file[index]
                relative_profile_inn = relative_connection_inn_profile[index]
                relative_profile_inn = str(relative_profile_inn).strip('-')
                if len(relative_profile_inn) > 9:
                    # request to look for a person_id by inn(relative)
                    relative_user = a_session.query(Profile).filter_by(
                        inn=relative_profile_inn
                        ).all()
                    if relative_user:
                        try:
                            # if user exist than adds all the info that
                            # we need to new_data dict
                            relative_user = str(relative_user).split(" ")
                            relative_user = int(relative_user[1])
                            new_data['person_id'] = relative_user
                            new_data['person_inn'] = int(relative_profile_inn)
                            new_data['person_pib'] = str(
                                relative_connection_pib_profile[index]
                                ).split("\n")[0]
                            new_data['person_path'] = relative_connection_path[
                                index
                                ]
                        except Exception:
                            pass

                    else:
                        # if user doesn`t exist than adds all the info that we
                        # need to new_data dict and adds to our db
                        new_data['person_inn'] = str(relative_profile_inn)
                        new_data['person_pib'] = str(
                            relative_connection_pib_profile[index]
                            ).split("\n")[0]
                        new_data['person_path'] = relative_connection_path[
                            index
                            ]
                        try:
                            # splitting pib to divided names ( name, last_name,
                            # mid_name)
                            pib_split_by = new_data['person_pib'].strip(

                            ).split(' ')
                            print(f"PIB else: {pib_split_by}")
                            (last_name, first_name, middle_name) = pib_split_by
                            # checking user`s gender
                            # if middle_name.endswith('ович') or
                            # middle_name.endswith('ОВИЧ'):
                            # elif middle_name.endswith('вна') or
                            # middle_name.endswith('ВНА'):
                            # adding user
                            new_relative_user = Profile(
                                person_type_id=15,
                                inn=str(new_data['person_inn']),
                                last_name=last_name, first_name=first_name,
                                middle_name=middle_name,
                                last_update=datetime.now())
                            a_session.add(new_relative_user)
                            a_session.commit()
                            exist_user = a_session.query(Profile).filter_by(
                                inn=str(new_data['person_inn'])
                                ).all()
                            exist_user = str(exist_user[0]).split(" ")
                            exist_user = int(exist_user[1])

                            user_path = Link(person_id=exist_user, link=str(
                                new_data['person_path']), site_id=5)
                            a_session.add(user_path)
                            a_session.commit()
                        except Exception as e:
                            print(e)

                else:
                    # if inn doesn`t exist or wrong that adds it to this dict
                    dict_data_with_not_find['profile_inn'] = profile_inn
                    # df1 = df1.append(pd.DataFrame(dict_data_with_not_find,
                    # index=range(len(df1), len(df1) +
                    # len(dict_data_with_not_find))))
            index += 1
            df1 = df1.append(pd.DataFrame(
                dict_data_with_not_find,
                index=range(len(df1), len(df1) + len(dict_data_with_not_find)))
                )
            df = df.append(pd.DataFrame(
                new_data,
                index=range(len(df), len(df) + len(new_data)))
                )
        except Exception as e:
            print(f"error: {e}")
    df = df.drop_duplicates(subset=['parent_person_id'])
    df.to_excel("info11.xlsx")
    df1.to_excel("if_not_find.xlsx")
