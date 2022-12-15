import simpy
from models.assembler import assembler_gen
from models.body_maker import body_maker_gen
from models.neck_maker import neck_maker_gen
from models.painter import painter_gen

guitars_made = 0
guitars_made_s = 0
guitars_made_h = 0

class GuitarFactory:
    def __init__(self, env, constants):
        self.wood = simpy.Container(
            env, capacity=constants.wood_capacity, init=constants.initial_wood)
        self.wood_control = env.process(self.wood_stock_control(env))
        self.singles = simpy.Container(
            env, capacity=constants.singles_capacity, init=constants.initial_singles)
        self.humbs= simpy.Container(
            env, capacity=constants.humbs_capacity, init=constants.initial_singles)
        self.singles_control = env.process(
            self.electronic_stock_control(env, self.singles, 'Сингл'))
        self.humbs_control = env.process(
            self.electronic_stock_control(env, self.humbs, 'Хамбакер'))
        self.body_pre_paint = simpy.Container(
            env, capacity=constants.body_pre_paint_capacity, init=0)
        self.neck_pre_paint = simpy.Container(
            env, capacity=constants.neck_pre_paint_capacity, init=0)
        self.body_post_paint = simpy.Container(
            env, capacity=constants.body_post_paint_capacity, init=0)
        self.neck_post_paint = simpy.Container(
            env, capacity=constants.neck_post_paint_capacity, init=0)
        self.dispatch = simpy.Container(
            env, capacity=constants.dispatch_capacity, init=0)
        self.dispatch_s = simpy.Container(
            env, capacity=constants.dispatch_capacity_s, init=0)
        self.dispatch_h = simpy.Container(
            env, capacity=constants.dispatch_capacity_h, init=0)
        self.dispatch_control = env.process(self.dispatch_guitars_control(env))
        self.constants = constants
        self.day_info = {
            'bodies': 0,
            'necks': 0,
            'bodies_painted': 0,
            'necks_painted': 0,
            'humbs': 0,
            'singles': 0,
        }
        self.logs = []

    def wood_stock_control(self, env):
        yield env.timeout(0)
        while True:
            if self.wood.level <= self.constants.wood_critial_stock:
                self.logs.append('Запас древесины ниже критического уровня ({0}) в день {1} час {2}'.format(
                    self.wood.level, int(env.now/8), env.now % 8))
                self.logs.append('Заказываем древесину')
                self.logs.append('----------------------------------')
                yield env.timeout(16)
                self.logs.append('Поставщик древесины прибудет в день {0} час {1}'.format(
                    int(env.now/8), env.now % 8))
                yield self.wood.put(300)
                self.logs.append('Новый запас древесины: {0}'.format(
                    self.wood.level))
                self.logs.append('----------------------------------')
                yield env.timeout(8)
            else:
                yield env.timeout(1)

    def electronic_stock_control(self, env, container, type):
        yield env.timeout(0)
        while True:
            if container.level <= self.constants.electronic_critical_stock:
                self.logs.append('Запас звукоснимателей "{3}" ниже критического уровня ({0}) в день {1} час {2}'.format(
                   container.level, int(env.now/8), env.now % 8, type))
                self.logs.append('Заказываем электронику')
                self.logs.append('----------------------------------')
                yield env.timeout(9)
                self.logs.append('Поставщик электроники прибудет в день {0} час {1}'.format(
                    int(env.now/8), env.now % 8))
                yield container.put(30)
                self.logs.append('Новый запас электроники "{1}": {0}'.format(
                    container.level, type))
                self.logs.append('----------------------------------')
                yield env.timeout(8)
            else:
                yield env.timeout(1)

    def dispatch_guitars_control(self, env):
        global guitars_made, guitars_made_s, guitars_made_h
        yield env.timeout(0)
        while True:
            if self.dispatch.level >= 10:
                self.logs.append('Отгрузочный запас: {0}, звонок в магазин продажи гитар в день {1} час {2}'.format(
                    self.dispatch.level, int(env.now/8), env.now % 8))
                self.logs.append('----------------------------------')
                yield env.timeout(4)
                self.logs.append('Магазин забрал {0} гитар ({3} с синглами и {4} с хамбакерами) в день {1} час {2}'.format(
                    self.dispatch.level, int(env.now/8), env.now % 8, self.dispatch_s.level, self.dispatch_h.level))
                guitars_made += self.dispatch.level
                guitars_made_s += self.dispatch_s.level
                guitars_made_h += self.dispatch_h.level
                
                yield self.dispatch.get(self.dispatch.level)
                yield self.dispatch_s.get(self.dispatch_s.level)
                yield self.dispatch_h.get(self.dispatch_h.level)
                self.logs.append('----------------------------------')
                yield env.timeout(8)
            else:
                yield env.timeout(1)
    
    def clear_day_info(self):
        self.day_info = {
            'bodies': 0,
            'necks': 0,
            'bodies_painted': 0,
            'necks_painted': 0,
            'humbs': 0,
            'singles': 0,
        }
        
    def start(self, env):
        env.process(body_maker_gen(env, self))
        env.process(neck_maker_gen(env, self))
        env.process(painter_gen(env, self))
        env.process(assembler_gen(env, self))
        
        


def factory_simulation(constants):
    env = simpy.Environment()
    guitar_factory = GuitarFactory(env, constants)
    global guitars_made, guitars_made_h , guitars_made_s
    
    days_info_list = []
    days_info_dict = {
        'bodies': [],
        'necks': [],
        'bodies_painted': [],
        'necks_painted': [],
        'humbs': [],
        'singles': [],
    }
    
    guitar_factory.logs.append(f'ЗАПУСК СИМУЛЯЦИИ')
    guitar_factory.logs.append(f'----------------------------------')
    
    guitar_factory.start(env)

    for i in range(constants.days):
        env.run(until = i * constants.hours + constants.hours)
        days_info_list.append(guitar_factory.day_info)
        days_info_dict['bodies'].append(guitar_factory.day_info['bodies'])
        days_info_dict['necks'].append(guitar_factory.day_info['necks'])
        days_info_dict['bodies_painted'].append(guitar_factory.day_info['bodies_painted'])
        days_info_dict['necks_painted'].append(guitar_factory.day_info['necks_painted'])
        days_info_dict['humbs'].append(guitar_factory.day_info['humbs'])
        days_info_dict['singles'].append(guitar_factory.day_info['singles'])
        
        guitar_factory.clear_day_info()
    
    guitar_factory.logs.append(f'----------------------------------')
    guitar_factory.logs.append(f'Прошло %d дней' % constants.days)
    guitar_factory.logs.append('Перед покраской: {0} корпусов и {1} грифов.'.format(
        guitar_factory.body_pre_paint.level, guitar_factory.neck_pre_paint.level))
    guitar_factory.logs.append('После покраски готовы к сборке: {0} корпусов и {1} грифов.'.format(
        guitar_factory.body_post_paint.level, guitar_factory.neck_post_paint.level))
    guitar_factory.logs.append(f'%d гитар готовы к отправке!' % guitar_factory.dispatch.level)
    guitar_factory.logs.append(f'----------------------------------')
    guitar_factory.logs.append('Всего гитар изготовлено: {0}'.format(guitars_made + guitar_factory.dispatch.level))
    guitar_factory.logs.append('С синглами: {0}'.format(guitars_made_s + guitar_factory.dispatch_s.level))
    guitar_factory.logs.append('С хамбакерами: {0}'.format(guitars_made_h + guitar_factory.dispatch_h.level))
    guitar_factory.logs.append(f'----------------------------------')
    guitar_factory.logs.append('Отправлено в магазин: {0}'.format(guitars_made))
    guitar_factory.logs.append('С синглами: {0}'.format(guitars_made_s))
    guitar_factory.logs.append('С хамбакерами: {0}'.format(guitars_made_h))
    guitar_factory.logs.append(f'----------------------------------')
    guitar_factory.logs.append(f'СИМУЛЯЦИЯ ЗАВЕРШЕНА')
    
    in_factory = {
        'body_pre_paint': guitar_factory.body_pre_paint.level,
        'neck_pre_paint': guitar_factory.neck_pre_paint.level,
        'body_post_paint': guitar_factory.body_post_paint.level,
        'neck_post_paint': guitar_factory.neck_post_paint.level,
        'dispatch': guitar_factory.dispatch.level,
    }
    
    overall = {
        'guitars_made': guitars_made + guitar_factory.dispatch.level,
        'guitars_made_s': guitars_made_s + guitar_factory.dispatch_s.level,
        'guitars_made_h': guitars_made_h + guitar_factory.dispatch_h.level,
        'guitars_store': guitars_made,
        'guitars_store_s': guitars_made_s,
        'guitars_store_h': guitars_made_h,
    }
    
    guitars_made_h = 0 
    guitars_made_s = 0 
    guitars_made = 0
    
    
    return {
        'logs': guitar_factory.logs,
        'days_info_dict': days_info_dict,
        'days_info_list': days_info_list,
        'in_factory': in_factory,
        'overall': overall,
    }
