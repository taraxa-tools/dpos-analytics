import log
import csv

logger = log.get_logger_instance()

def empty_csv_file(csv_file, header):
    logger.debug(f'Emptying csv file')
    with open(csv_file, 'w', newline='') as c:
        writer = csv.DictWriter(c, fieldnames=header)
        writer.writeheader()