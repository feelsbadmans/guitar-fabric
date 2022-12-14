import random

def assembler(env, guitar_factory):
    while True:
        if guitar_factory.body_post_paint.level >= 1 and guitar_factory.neck_post_paint.level >= 1:
            type = random.randrange(5)
            el = guitar_factory.singles
            d = guitar_factory.dispatch_s
            msg = "Хамбакер" if type % 2 == 1 else 'Сингл'
            key = 'humbs' if type % 2 == 1 else 'singles'
            
            if type % 2 == 1:
                el = guitar_factory.humbs
                d = guitar_factory.dispatch_h 
            
            yield guitar_factory.body_post_paint.get(1)
            yield guitar_factory.neck_post_paint.get(1)
            yield el.get(2)
            
            
            guitar_factory.logs.append('----------------------------------')
            guitar_factory.logs.append('Гитара готова к сборке')
            guitar_factory.logs.append(f'Сборка гитары со звукоснимателями типа "{msg}"')
            
            assembling_time = max(random.gauss(guitar_factory.constants.mean_ensam, guitar_factory.constants.std_ensam), 1)
            
            yield env.timeout(assembling_time)
            guitar_factory.logs.append('Гитара собрана!')
            yield guitar_factory.dispatch.put(1)
            yield d.put(1)
            guitar_factory.day_info[key] += 1
        yield env.timeout(0.01)

def assembler_gen(env, guitar_factory):
    for i in range(guitar_factory.constants.num_ensam):
        env.process(assembler(env, guitar_factory))
        yield env.timeout(0)