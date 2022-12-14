class SimulationParams:
     def __init__(self, constants):
        self.hours = constants['hours']
        self.days = constants['days']
        self.total_time = self.hours * self.days
        
        self.wood_capacity = constants['wood_capacity']
        self.initial_wood = constants['initial_wood']
        
        self.singles_capacity = constants['singles_capacity']
        self.initial_singles = constants['initial_singles']
        
        self.humbs_capacity = constants['humbs_capacity']
        self.initial_humbs = constants['initial_humbs']
        
        self.body_pre_paint_capacity = constants['body_pre_paint_capacity']
        self.neck_pre_paint_capacity = constants['neck_pre_paint_capacity']
        self.body_post_paint_capacity = constants['body_post_paint_capacity']
        self.neck_post_paint_capacity = constants['neck_post_paint_capacity']
        
        self.dispatch_capacity = constants['dispatch_capacity']
        self.dispatch_capacity_s = constants['dispatch_capacity_s']
        self.dispatch_capacity_h = constants['dispatch_capacity_h']
        
        self.num_body = constants['num_body']
        self.mean_body = constants['mean_body']
        self.std_body = constants['std_body']
        
        self.num_neck = constants['num_neck']
        self.mean_neck = constants['mean_neck']
        self.std_neck = constants['std_neck']
    
        self.num_paint = constants['num_paint']
        self.mean_paint = constants['mean_paint']
        self.std_paint = constants['std_paint']
        
        self.num_ensam = constants['num_ensam']
        self.mean_ensam = constants['mean_ensam']
        self.std_ensam = constants['std_ensam']
        
        self.wood_critial_stock = (((8/self.mean_body) * self.num_body +
                      (8/self.mean_neck) * self.num_neck) * 3) #2 days to deliver + 1 marging

        self.electronic_critical_stock = (8/self.mean_ensam) * self.num_ensam * 2 #1 day to deliver + 1 marging
