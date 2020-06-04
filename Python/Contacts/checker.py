import re

#utils for checking validity of data

def check_email(email):
    regular_email = r"""
    ^([a-zA-Z.0-9]+)   #unique addres
    (@)
    ([a-zA-Z]+)        #
    (\.[a-zA-Z]+)      # domain 
    (\.[a-zA-Z]+)?     #
    """
    regex_email = re.compile(email)
    if regex_email:
        return True
    return False

def check_gener(gener):
    GENERS = ['Male', 'Female','Others']
    if not gener in GENERS:
        return False
    return True

def check_phone(number):
    regular_cellphone = r"""(
    (\d{3}|\(\d{3}\))          #area code
    (\s|-|\.)?                  #separator
    (\d{3})                     #first 3 digits
    (\s|-|\.)?                  #separator
    (\d{4})                     #last 4 digits
    (\s*(ext|x|ext.)\s*(\d{2,5}))? #extension
    )"""
    regex_cellphone = re.compile(regular_cellphone, re.VERBOSE)
    if regex_cellphone:
        return True
    return False
    
