import random
from constants import mean_ensam, std_ensam, num_ensam

def assembler(env, guitar_factory):
    while True:
        yield guitar_factory.body_post_paint.get(1)
        yield guitar_factory.neck_post_paint.get(1)
        yield guitar_factory.electronic.get(1)
        assembling_time = max(random.gauss(mean_ensam, std_ensam), 1)
        yield env.timeout(assembling_time)
        yield guitar_factory.dispatch.put(1)

def assembler_gen(env, guitar_factory):
    for i in range(num_ensam):
        env.process(assembler(env, guitar_factory))
        yield env.timeout(0)