from piranha_checker_and_comparator import compare_data_and_add, get_data
from parcer import extract_data
from db_checker_and_comparator import parse_data_from_file
from db_checker_and_comparator import db_check_info_and_add


if __name__ == '__main__':
    path = 'C:\\Users\\analytic8\\Desktop\\ParcerForNemo\\Soft'
    path_to_excel = 'info.xlsx'
    extract_data(path)
    if path_to_excel:
        parsed_data = parse_data_from_file(path_to_excel)
        db_check_info_and_add(parsed_data)
        print("Account data has been uploaded.")
        print("Data has successfully copied.")
    else:
        print('There is nothing to check')
    path_to = 'info11.xlsx'
    get_data_tuple = get_data(path_to)
    try:
        compare_data_and_add(get_data_tuple)
        print("Account data has been uploaded.")
        print("Data has successfully created")
    except Exception as e:
        print(f"Error: {e}")
    print("All tasks has been done.")
