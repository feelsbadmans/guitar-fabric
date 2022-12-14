import random

def painter(env, guitar_factory):
    while True:
        if guitar_factory.body_pre_paint.level >= 5:
            yield guitar_factory.body_pre_paint.get(5)
            paint_time = random.gauss(guitar_factory.constants.mean_paint, guitar_factory.constants.std_paint)
            yield env.timeout(paint_time)
            yield guitar_factory.body_post_paint.put(5)
            guitar_factory.day_info['bodies_painted'] += 5
        if guitar_factory.neck_pre_paint.level >= 5:
            yield guitar_factory.neck_pre_paint.get(5)
            paint_time = random.gauss(guitar_factory.constants.mean_paint, guitar_factory.constants.std_paint)
            yield env.timeout(paint_time)
            yield guitar_factory.neck_post_paint.put(5)
            guitar_factory.day_info['necks_painted'] += 5
        yield env.timeout(0.01)

def painter_gen(env, guitar_factory):
    for _ in range(guitar_factory.constants.num_paint):
        env.process(painter(env, guitar_factory))
        yield env.timeout(0)
