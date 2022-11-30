import simpy
from constants import *
from models.assembler import assembler_gen
from models.body_maker import body_maker_gen
from models.neck_maker import neck_maker_gen
from models.painter import painter_gen

guitars_made = 0

class Guitar_Factory:
    def __init__(self, env):
        self.wood = simpy.Container(
            env, capacity=wood_capacity, init=initial_wood)
        self.wood_control = env.process(self.wood_stock_control(env))
        self.electronic = simpy.Container(
            env, capacity=electronic_capacity, init=initial_electronic)
        self.electronic_control = env.process(
            self.electronic_stock_control(env))
        self.body_pre_paint = simpy.Container(
            env, capacity=body_pre_paint_capacity, init=0)
        self.neck_pre_paint = simpy.Container(
            env, capacity=neck_pre_paint_capacity, init=0)
        self.body_post_paint = simpy.Container(
            env, capacity=body_post_paint_capacity, init=0)
        self.neck_post_paint = simpy.Container(
            env, capacity=neck_post_paint_capacity, init=0)
        self.dispatch = simpy.Container(
            env, capacity=dispatch_capacity, init=0)
        self.dispatch_control = env.process(self.dispatch_guitars_control(env))

    def wood_stock_control(self, env):
        yield env.timeout(0)
        while True:
            if self.wood.level <= wood_critial_stock:
                print('Запас древесины ниже критического уровня ({0}) в день {1} час {2}'.format(
                    self.wood.level, int(env.now/8), env.now % 8))
                print('Заказываем древесину')
                print('----------------------------------')
                yield env.timeout(16)
                print('Поставщик древесины прибудет в день {0} час {1}'.format(
                    int(env.now/8), env.now % 8))
                yield self.wood.put(300)
                print('Новый запас древесины: {0}'.format(
                    self.wood.level))
                print('----------------------------------')
                yield env.timeout(8)
            else:
                yield env.timeout(1)

    def electronic_stock_control(self, env):
        yield env.timeout(0)
        while True:
            if self.electronic.level <= electronic_critical_stock:
                print('Запас электроники ниже критического уровня ({0}) в день {1} час {2}'.format(
                    self.electronic.level, int(env.now/8), env.now % 8))
                print('Заказываем электронику')
                print('----------------------------------')
                yield env.timeout(9)
                print('Поставщик древесины прибудет в день {0} час {1}'.format(
                    int(env.now/8), env.now % 8))
                yield self.electronic.put(30)
                print('Новый запас электроники: {0}'.format(
                    self.electronic.level))
                print('----------------------------------')
                yield env.timeout(8)
            else:
                yield env.timeout(1)

    def dispatch_guitars_control(self, env):
        global guitars_made
        yield env.timeout(0)
        while True:
            if self.dispatch.level >= 50:
                print('Отгрузочный запас: {0}, звонок в магазин продажи гитар в день {1} час {2}'.format(
                    self.dispatch.level, int(env.now/8), env.now % 8))
                print('----------------------------------')
                yield env.timeout(4)
                print('Магазин забрал {0} гитар в день {1} час {2}'.format(
                    self.dispatch.level, int(env.now/8), env.now % 8))
                guitars_made += self.dispatch.level
                yield self.dispatch.get(self.dispatch.level)
                print('----------------------------------')
                yield env.timeout(8)
            else:
                yield env.timeout(1)


def factory_simulation():
    print(f'ЗАПУСК СИМУЛЯЦИИ')
    print(f'----------------------------------')

    env = simpy.Environment()
    guitar_factory = Guitar_Factory(env)

    env.process(body_maker_gen(env, guitar_factory))
    env.process(neck_maker_gen(env, guitar_factory))
    env.process(painter_gen(env, guitar_factory))
    env.process(assembler_gen(env, guitar_factory))

    env.run(until = total_time)
    
    
    print(f'----------------------------------')
    print(f'Прошло %d дней' % days)
    print('Перед покраской: {0} корпусов и {1} грифов.'.format(
    guitar_factory.body_pre_paint.level, guitar_factory.neck_pre_paint.level))
    print('После покраски готовы к сборке: {0} корпусов и {1} грифов.'.format(
        guitar_factory.body_post_paint.level, guitar_factory.neck_post_paint.level))
    print(f'%d гитар готовы к отправке!' % guitar_factory.dispatch.level)
    print(f'----------------------------------')
    print('Всего гитар изготовлено: {0}'.format(guitars_made + guitar_factory.dispatch.level))
    print(f'----------------------------------')
    print(f'СИМУЛЯЦИЯ ЗАВЕРШЕНА')
