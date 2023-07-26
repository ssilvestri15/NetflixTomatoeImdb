from datetime import datetime

def extract_year_from_date(date_string):

    if date_string is None or date_string == "":
        return "NA"

    try:
        date_object = datetime.strptime(date_string, "%Y-%m-%d")  # Assuming the format is "YYYY-MM-DD"
    except ValueError:
        print("Invalid date format. Please provide a date string in the format 'YYYY-MM-DD'.")
        return None

    # Extract the year from the datetime object
    year = date_object.year.__str__()

    return year
