import random
from constants import mean_neck, std_neck, num_neck

def neck_maker(env, guitar_factory):
    while True:
        yield guitar_factory.wood.get(1)
        neck_time = random.gauss(mean_neck, std_neck)
        yield env.timeout(neck_time)
        yield guitar_factory.neck_pre_paint.put(2)

def neck_maker_gen(env, guitar_factory):
    for _ in range(num_neck):
        env.process(neck_maker(env, guitar_factory))
        yield env.timeout(0)