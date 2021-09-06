import pandas as pd
from nemo_alchemy.models import EntityLink, Link, D_OtherLink
from nemo_alchemy import session as a_session


def get_data(path_to: str) -> tuple:
    """[This func is reading received data from info.xlsx which was processed in the previous func]

    Args:
        path_to (str): [this func is taken a str with path to files as argument]

    Returns:
        [tuple]: [returns tuples with sorted and formated data from info11.xlsx]
    """
    read_excel = pd.read_excel(path_to, sheet_name='Sheet1')
    parent_path = read_excel['parent_path'].to_list()
    person_path = read_excel["person_path"].to_list()
    parent_person_id = read_excel["parent_person_id"].to_list()
    person_id = read_excel["person_id"].to_list()
    paths = parent_path + person_path
    ids = parent_person_id + person_id
    return ids, paths


def compare_data_and_add(func_tuple: tuple) -> None:
    """[The func is cheking and updating info about user if exists in our db if not adds it]

    Args:
        func_tuple (tuple): [tuple with lists of data about clients]
    """
    (ids, paths) = func_tuple
    # variable to designation what the relative will be in the current iterating
    iterat = 0
    # user ids from exist and added clients in our db
    for i in ids:
        if str(i) != "nan" and paths[iterat] != "nan":
            # request to db to recheck user`s existence and finding users that fit to this criteria
            link = a_session.query(Link).filter(Link.person_id == int(i), Link.site_id == 5).all()
            if link != []:
                try:
                    # if user exist than take their link_id
                    link = link[0].link_id
                    # the same operations which were above but with entity_link table
                    entity = a_session.query(EntityLink).filter(EntityLink.link_id == link, EntityLink.entity_type_id == 5).all()
                    entity = entity[0].entity_id
                    # the same operations which were above but with other_link table
                    res = a_session.query(D_OtherLink).filter(D_OtherLink.other_link_id == entity)
                    print(f"Res: {res}")
                    if res:
                        # if res update value parameter that consist a path to file with user from piranha site
                        res[0].value = paths[iterat]
                        a_session.commit()
                except Exception:
                    pass
            else:
                # if user doesn`t exist in our db then check and add all the info
                link_id_user = a_session.query(Link).filter(Link.person_id == int(i)).all()
                if link_id_user != []:
                    site_id_user_add = Link(site_id=5, person_id=int(i))
                    a_session.add(site_id_user_add)
                    a_session.commit()
                    give_link_id = a_session.query(Link).filter(Link.person_id == int(i), Link.site_id == 5).all()
                    if give_link_id != []:
                        try:
                            print(f'Path else: {paths[iterat]}')
                            other_link = D_OtherLink(site_id=5, value=paths[iterat])
                            a_session.add(other_link)
                            a_session.commit()
                        except Exception:
                            pass
                        try:
                            other_link_id_get = a_session.query(D_OtherLink).filter(D_OtherLink.site_id == 5, D_OtherLink.value == paths[iterat])
                            if other_link_id_get != []:
                                entity_link = EntityLink(link_id=give_link_id, entity_type_id=5, entity_id=other_link_id_get.link_id)
                                a_session.add(entity_link)
                                a_session.commit()
                        except Exception:
                            pass
        else:
            pass
        iterat += 1
