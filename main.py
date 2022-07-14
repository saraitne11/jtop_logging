import argparse
import os
import time
import datetime
import signal
import logging
from logging.handlers import RotatingFileHandler

# from jtop import jtop


SIG_KILL = False


def signal_handler(signum, frame):
    global SIG_KILL
    SIG_KILL = True
    print('receive signal', signum)
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-f', "--log_file", type=str, default='jtop.log',
                        help="logging file path")
    parser.add_argument('-p', "--log_period", type=int, default=5,
                        help="logging period(sec), greater than 1sec, default 5sec")
    args = parser.parse_args()

    logger = logging.getLogger('jtop')
    logger.setLevel(logging.INFO)

    handler = RotatingFileHandler(args.log_file, mode='a', maxBytes=1024 * 1024 * 10, backupCount=5)      # 10 MB
    formatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s]%(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    logging_time = time.time() + args.log_period
    while True:
        cur_time = time.time()
        if logging_time < cur_time:
            s = str(datetime.datetime.now())
            logger.info(s)
            logging_time = cur_time + args.log_period

        time.sleep(1)
        if SIG_KILL:
            break

    for hdlr in logger.handlers:
        hdlr.close()
