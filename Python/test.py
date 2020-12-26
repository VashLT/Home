import pyinputplus as pyip


def check(some):
    print(some)
    if some != "hola":
        raise Exception("??")
    return True

h = pyip.inputStr("Enter: ", postValidateApplyFunc=check)
print("success!")
