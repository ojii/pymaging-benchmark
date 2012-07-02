# -*- coding: utf-8 -*-
import os

BENCH_DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'benchdata')

def get_file_path(fname):
    return os.path.join(BENCH_DATA_DIR, fname)
