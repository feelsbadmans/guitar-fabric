import random

def body_maker(env, guitar_factory):
    while True:
        yield guitar_factory.wood.get(1)
        body_time = random.gauss(guitar_factory.constants.mean_body, guitar_factory.constants.std_body)
        yield env.timeout(body_time)
        yield guitar_factory.body_pre_paint.put(1)
        guitar_factory.day_info['bodies'] += 1

def body_maker_gen(env, guitar_factory):
    for _ in range(guitar_factory.constants.num_body):
        env.process(body_maker(env, guitar_factory))
        yield env.timeout(0)
