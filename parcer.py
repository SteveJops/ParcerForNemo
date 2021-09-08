import os
import zipfile
import pandas as pd
from striprtf.striprtf import rtf_to_text
from io import TextIOWrapper
from tqdm import tqdm


def extract_data(path):
    """This func extracts data from files '.rtf' and '.zip'

    Args:
        path (str): this func is taken a str with path to files as argument

    Returns:
        'info.xlsx': the func return a dataframe and a file with processed
        client data in excel tables file
    """
    try:
        df = pd.DataFrame()
        dict_with_whole_data = {}
        # walking on dirs and search files
        for root, dirs, files in os.walk(path):
            for fl in tqdm(files):
                fl = os.path.join(root, fl)
                # folder name
                dirname = (os.path.dirname(fl)).split('\\')[-1]
                # file name
                basename = (os.path.basename(fl)).split('.')[3]
                # looking for files with this format
                if fl.endswith('.rtf'):
                    try:
                        with open(fl) as f:
                            r = f.read()
                            # scraping the text info
                            text = rtf_to_text(r)
                            # if file doesn`t has  the same name as folder
                            # it`s relative
                            if basename != dirname:
                                dict_with_whole_data[
                                    'client_parent_INN'
                                    ] = text[:11]
                                dict_with_whole_data[
                                    'client_parent_PIB'
                                    ] = text[13:45]
                                dict_with_whole_data[
                                    'relative_path'
                                    ] = str(os.path.abspath(fl))
                            else:
                                # These are clients
                                dict_with_whole_data[
                                    'client_INN'
                                    ] = text[:11]
                                dict_with_whole_data[
                                    'client_PIB'
                                    ] = text[13:45]
                                dict_with_whole_data[
                                    'path'
                                    ] = str(os.path.abspath(fl))
                    except Exception as e:
                        print(e)
                        # looking for files with this format
                elif fl.endswith('.zip'):
                    try:
                        # reading zip
                        zip_file = zipfile.ZipFile(fl, 'r')
                        # checking that ain`t not empty
                        files = zip_file.namelist()
                        # opening the file
                        with zip_file.open(files[0]) as f:
                            # scraping the text and formating
                            # to normal-view text
                            text = rtf_to_text(TextIOWrapper(f).read())
                            # if file has the same name as folder it`s client
                            if basename == dirname:
                                dict_with_whole_data[
                                    'client_INN'
                                    ] = text[:11]
                                dict_with_whole_data[
                                    'client_PIB'
                                    ] = text[13:45]
                                dict_with_whole_data[
                                    'path'
                                    ] = str(os.path.abspath(fl))
                            else:
                                # these are relatives
                                dict_with_whole_data[
                                    'client_parent_INN'
                                    ] = text[:11]
                                dict_with_whole_data[
                                    'client_parent_PIB'
                                    ] = text[13:45]
                                dict_with_whole_data[
                                    'relative_path'
                                    ] = str(os.path.abspath(fl))
                    except Exception as e:
                        print(e)
                else:
                    pass
            # adding to dataframe dict
            df = df.append(pd.DataFrame(
                dict_with_whole_data,
                index=range(len(df), len(df) + len(dict_with_whole_data)))
                )
        # df = df.drop_duplicates(subset=['path', 'relative_path'])
        # adding to excel
        df.to_excel("info.xlsx")
        return df
    except Exception as e:
        print(e)
    finally:
        print('Data has been uploaded')
