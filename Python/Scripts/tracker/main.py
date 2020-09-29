import os
import sys
from datetime import datetime
from register import Logger
from register import PATH

#! Python 3

"""
    This script keep track of cash transactions
"""


def usage():
    usage = """
        Usage: $register id/cedula (add/substract) 'amount money' 
               $register id/cedula log (date ~optional) - Print all the additions and deletions 
        """
    print(usage)


def check_date_format(date):
    date_format = r'%d/%m/%Y'
    try:
        # check given arg is a right date-format
        datetime.strptime(date, date_format)
        return True

    except ValueError:
        return False


def main(sys_args):
    """ handle args catched by sys.argv """
    os.chdir(PATH)
    if len(sys_args) < 3:
        usage()

    else:
        args = sys_args[1:]
        cc, task = args[:2]
        logger = Logger(cc)
        if task == 'log':
            try:
                date = args[2]
                input(f": {date}")
                if not check_date_format(date):
                    print(
                        f"[INFO] {date} doesn't match a correct date. CORRECT DATE FORMAT dd/mm/yyyy")
                    date = None
            except IndexError:
                date = None
            logger.history(date=date)
        elif task == 'money':
            print(f'[EN PROGRESO] Obteniendo dinero total ...')
            money = logger.get_info('money')
            name = logger.get_info('name')
            print('[INFO] Dinero total:')
            print(f'      [{name} - {cc}] - ${money}')
        else:
            try:
                money = int(args[2])
                if task == 'add':
                    logger.add(money)
                elif task == 'substract':
                    logger.substract(money)
                else:
                    raise Exception(f"{task} doesn't match any valid task.")
            except IndexError:
                usage()
            except ValueError:
                print(
                    "[ERROR] Not valid data-type - CAUSE: Money isn't and integer value.")
                usage()
            except Exception as ex:
                print(f'[ERROR] {ex}')
    print('Thanks for using the script')


if __name__ == '__main__':
    main(sys.argv)
