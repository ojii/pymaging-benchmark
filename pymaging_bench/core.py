# -*- coding: utf-8 -*-
from collections import namedtuple
from contextlib import contextmanager
import shutil
import tempfile
import time
import fnmatch
import os


Benchmark = namedtuple('Benchmark', 'name description pymaging pil')
Result = namedtuple('Result', 'average runs')
BenchmarkResult = namedtuple('BenchmarkResult', 'benchmark pymaging pil')

nullfunc = lambda *args, **kwargs: None

def setdefault(obj, attr, value):
    setattr(obj, attr, getattr(obj, attr, value))

@contextmanager
def temporary_file_path():
    tempdir = tempfile.mkdtemp()
    yield os.path.join(tempdir, 'tempfile')
    shutil.rmtree(tempdir)


class Suite(object):
    min_iterations = 100
    target_time = 5

    def __init__(self):
        self.benchmarks = {}

    def autodiscover(self, root='benchmarks'):
        for mod_name in [os.path.splitext(fname)[0] for fname in os.listdir(root) if fnmatch.fnmatch(fname, '[!_]*.py')]:
            module = __import__('%s.%s' % (root, mod_name), fromlist=[root])
            if not getattr(module, 'benchmark', False):
                continue
            description = getattr(module, 'bench_description', None)
            pil_func = module.bench_pil
            setdefault(pil_func, 'setup', nullfunc)
            setdefault(pil_func, 'teardown', nullfunc)
            pymaging_func = module.bench_pymaging
            setdefault(pymaging_func, 'setup', nullfunc)
            setdefault(pymaging_func, 'teardown', nullfunc)
            self.benchmarks[mod_name] = Benchmark(mod_name, description, pymaging_func, pil_func)

    def benchmark(self, names=None):
        if not names:
            names = self.benchmarks.keys()
        results = []
        for name in names:
            benchmark = self.benchmarks[name]
            pymaging_result = self.run_func(benchmark.pymaging)
            pil_result = self.run_func(benchmark.pil)
            results.append(BenchmarkResult(benchmark, pymaging_result, pil_result))
        return results

    def run_func(self, func):
        with temporary_file_path() as filepath:
            def run():
                context = {'tempfile': filepath}
                func.setup(context)
                start = time.time()
                func(context)
                end = time.time()
                func.teardown(context)
                return end - start
            # warmup
            run()
            iterations_left = self.min_iterations
            time_left = self.target_time
            runs = []
            while iterations_left > 0 or time_left > 0:
                duration = run()
                runs.append(duration)
                iterations_left -= 1
                time_left -= duration
            average = sum(runs) / len(runs)
            return Result(average, runs)
