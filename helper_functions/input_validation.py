import datetime
def input_validation(message:str):
    output=input(message)
    if output.lower()=="q":
        quit()
    return output

def input_table_validation(query_results:list[tuple],input_message:str):
    while True:
        selection=input(input_message)
        try:
            if selection.lower()=="q":
                quit()
            query_results[int(selection)-1]
            return int(selection)
        except(ValueError,IndexError):
            print("Invalid selection, please try again!")
            continue

def input_date_validation(format:str,input_message:str,example:str):
    is_valid=False
    print(example)
    while not is_valid:
        date=input(input_message)
        try:
            date_conversion=datetime.datetime.strptime(date,format)
            return date_conversion.strftime(format)
        except ValueError:
            print(f"Invalid time format {date}, it must match {format}")

def input_employer_validation(input_message:str,results):
    for result in results:
        print(f"{result[0]}. {result[1]}")
    user_result=input_validation(input_message)
    try:
        return int(user_result)
    except ValueError:
        for result in results:
            if user_result in result[1]:
                return result[0]
        return user_result