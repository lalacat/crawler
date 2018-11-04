import logging

try:
    i = 0
    try:
        j = 2 % i
    except Exception as e :
        print("sad")
    try:
        import test.ppp
    except Exception as e :
        raise ModuleNotFoundError(e)

    print("sad")

except Exception as e :
    logging.error(e,exc_info = True )
