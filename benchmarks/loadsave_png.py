# -*- coding: utf-8 -*-
from PIL import Image as PIL
from pymaging.formats import registry
from pymaging.image import Image
from pymaging_png.png import PNG
from pymaging_bench.utils import get_file_path

filename = get_file_path('djangocon.png')

bench_description = "Load/Save a PNG file"
benchmark = True

def bench_pymaging(context):
    Image.open_from_path(filename).save_to_path(context['tempfile'] + '.png')

def setup_pymaging(context):
    registry._populate()
    context['old_registry'] = (registry.formats, registry.names)
    registry.formats = []
    registry.names = {}
    registry.register(PNG)

def teardown_pymaging(context):
    registry.formats, registry.names = context['old_registry']

bench_pymaging.setup = setup_pymaging
bench_pymaging.teardown = teardown_pymaging

def bench_pil(context):
    PIL.open(filename).save(context['tempfile'] + '.png')
