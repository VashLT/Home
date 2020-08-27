from configparser import ConfigParser
import logging, os
from pathlib import Path
from My_modules.Location import location

NAME_DEBUG_FILE = "debug_info_db_init.txt"
FILE_LOCATION =  Path(Path.home() / 'jose2' / 'Documents' / 'Home' / 'Python' / 'SQL' / NAME_DEBUG_FILE)
logging.basicConfig(filename = FILE_LOCATION, level = logging.DEBUG, format = '%(asctime)s - %(message)s')
# logging.disable(logging.CRITICAL)

def read_db_config(filename = 'config.ini', section = 'mysql'):
    """ Read database configuration file and return a dictionary object
    :param filename: name of the configuration file
    :param section: section of database configuration
    :return: a dictionary of database parameters
    """
    #digest config
    parser = ConfigParser()
    parser.read(filename)
    
    if not parser.sections(): #solve possible issue file location not in cwd
        try:
            file_abs_path = location.search(path = os.getcwd(),target_file = filename)
            logging.debug(f"Absolute path = {file_abs_path} ")
            parser.read(file_abs_path)
        except:
            pass 
    logging.debug(f'sections: {parser.sections()}')
    #set mysql default config
    db = {}
    if parser.has_section(section):
        configs = parser.items(section)
        logging.debug(f"matched: {configs}")
        for config in configs:
            db[config[0]] = config[1]
    else:
        raise Exception(f"[ERROR] {section} not found in the {filename} file.")
    
    return db