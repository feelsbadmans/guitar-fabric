import random
from constants import mean_paint, std_paint, num_paint

def painter(env, guitar_factory):
    while True:
        yield guitar_factory.body_pre_paint.get(5)
        yield guitar_factory.neck_pre_paint.get(5)
        paint_time = random.gauss(mean_paint, std_paint)
        yield env.timeout(paint_time)
        yield guitar_factory.body_post_paint.put(5)
        yield guitar_factory.neck_post_paint.put(5)

def painter_gen(env, guitar_factory):
    for _ in range(num_paint):
        env.process(painter(env, guitar_factory))
        yield env.timeout(0)
