import re
# Imports the Python regular expression module 're' for pattern matching.

def is_valid_email(email):
# Defines a function to validate the format of an email address.
    """Basic email format validation"""
    # Docstring describing the purpose of the is_valid_email function.
    if not email:
    # Checks if the provided email string is empty or None.
        return False
        # Returns False if no email was provided.
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    # Defines a regular expression pattern that matches standard email formats (e.g., name@domain.com).
    return re.match(pattern, email) is not None
    # Uses re.match to check if the email fits the pattern and returns True if it does, False otherwise.

def is_valid_phone(phone):
# Defines a function to validate a phone number.
    """Basic phone validation: only digits, length 10-15"""
    # Docstring describing that a phone number must be 10-15 digits long.
    if not phone:
    # Checks if the provided phone variable is empty or None.
        return False
        # Returns False if no phone number was provided.
    phone = str(phone).strip()
    # Converts the phone variable to a string and removes leading or trailing whitespace.
    return phone.isdigit() and 10 <= len(phone) <= 15
    # Returns True if the phone string consists only of digits and its length is between 10 and 15 inclusive.

def is_valid_password(password):
# Defines a function to validate password length.
    """Password must be at least 6 characters"""
    # Docstring indicating the password requirement.
    if not password:
    # Checks if the password is empty or None.
        return False
        # Returns False if no password was provided.
    return len(str(password)) >= 6
    # Returns True if the string representation of the password is at least 6 characters long.

def is_not_empty(value):
# Defines a function to check if a value is not empty.
    """Check if value is a non-empty string"""
    # Docstring indicating this function checks for non-empty strings.
    if value is None:
    # Checks if the value is explicitly None.
        return False
        # Returns False if the value is None.
    return bool(str(value).strip())
    # Converts the value to a string, removes whitespace, and returns True if anything remains (i.e., not empty).

def capitalize_data(data):
# Defines a function to iterate through dictionary data and uppercase specific fields.
    """Capitalize string values for specific keys in data before saving"""
    # Docstring describing the purpose of standardizing certain text fields.
    keys_to_upper = ["name", "course", "faculty_name", "title", "author", "department", "subject", "code"]
    # Defines a list of dictionary keys whose corresponding string values should be converted to uppercase.
    for k, v in data.items():
    # Iterates through all key-value pairs in the provided data dictionary.
        if k in keys_to_upper and isinstance(v, str):
        # Checks if the current key is in the target list and its value is a string type.
            data[k] = v.upper()
            # Converts the string value to uppercase and updates the dictionary.
    return data
    # Returns the modified dictionary with standardized uppercase values.