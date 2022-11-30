import random
from constants import mean_body, std_body, num_body


def body_maker(env, guitar_factory):
    while True:
        yield guitar_factory.wood.get(1)
        body_time = random.gauss(mean_body, std_body)
        yield env.timeout(body_time)
        yield guitar_factory.body_pre_paint.put(1)

def body_maker_gen(env, guitar_factory):
    for _ in range(num_body):
        env.process(body_maker(env, guitar_factory))
        yield env.timeout(0)
