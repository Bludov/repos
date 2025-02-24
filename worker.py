from datetime import date
import time

from etl.showpath import tst


def load_worker():
    tst()
    time.sleep(10)  # для иллюстрации ожиданаия завершения worker-дага из main-дага


load_worker()
