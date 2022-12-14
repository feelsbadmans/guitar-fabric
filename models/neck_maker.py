import random

def neck_maker(env, guitar_factory):
    while True:
        yield guitar_factory.wood.get(1)
        neck_time = random.gauss(guitar_factory.constants.mean_neck, guitar_factory.constants.std_neck)
        yield env.timeout(neck_time)
        yield guitar_factory.neck_pre_paint.put(2)
        guitar_factory.day_info['necks'] += 1

def neck_maker_gen(env, guitar_factory):
    for _ in range(guitar_factory.constants.num_neck):
        env.process(neck_maker(env, guitar_factory))
        yield env.timeout(0)