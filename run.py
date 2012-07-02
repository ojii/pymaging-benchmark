# -*- coding: utf-8 -*-
from __future__ import print_function
from pymaging_bench.core import Suite

def main():
    suite = Suite()
    suite.autodiscover()
    results = suite.benchmark()
    print(u"Results:")
    for result in results:
        print(u"  %s" % result.benchmark.description or result.benchmark.name)
        print(u"    PIL:      %.5f / %.5f / %.5f (%d)" % (result.pil.average, max(result.pil.runs), min(result.pil.runs), len(result.pil.runs)))
        print(u"    Pymaging: %.5f / %.5f / %.5f (%d)" % (result.pymaging.average, max(result.pymaging.runs), min(result.pymaging.runs), len(result.pymaging.runs)))
        print("")
if __name__ == '__main__':
    main()
