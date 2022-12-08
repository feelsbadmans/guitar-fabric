#working hours
hours = 8

#business days
days = 20

#total working time (hours)
total_time = hours * days

#containers
    #wood
wood_capacity = 500
initial_wood = 200

    #electronic
singles_capacity = 140
initial_singles = 100

humbs_capacity = 100
initial_humbs = 60

    #paint
body_pre_paint_capacity = 60
neck_pre_paint_capacity = 60
body_post_paint_capacity = 120
neck_post_paint_capacity = 120
    
    #dispatch
dispatch_capacity = 500
dispatch_capacity_s = 250
dispatch_capacity_h = 250


#employees per activity
    #body
num_body = 2
mean_body = 1
std_body = 0.1

    #neck
num_neck = 1
mean_neck = 1
std_neck = 0.2

    #paint
num_paint = 3
mean_paint = 3
std_paint = 0.3

    #ensambling
num_ensam = 2
mean_ensam = 1
std_ensam = 0.2


#critical levels
    #critical stock should be 1 business day greater than supplier take to come
wood_critial_stock = (((8/mean_body) * num_body +
                      (8/mean_neck) * num_neck) * 3) #2 days to deliver + 1 marging

electronic_critical_stock = (8/mean_ensam) * num_ensam * 2 #1 day to deliver + 1 marging