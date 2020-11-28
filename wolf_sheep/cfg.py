import plot_thickens as pt

def dimensions():
    """ if this is 50x50, dimesnions = 50"""
    dimensions = 70
    return dimensions

def wolf_gn():
    fd = 30
    return fd

def radyis():
    """detection radius for consumer"""
    r = 6
    return r

def fmr_cost():
    c = 9
    return c

def initial_carcs():
    c = 5
    return 5

metab_dkt = {9:"1000kg varanid"
            ,17:"2000kg varanid"}

def print_text_summary(dmnsn, wolf_gn, rdius, fmr_cost, intl_crcs, intl_als, saurp_pop):

    txt = "Results\n"+\
    "dimensions                     :"+str(dmnsn)+"x"+str(dmnsn)+" squares at 1km each\n"
    "area                           :"+str(dmnsn * dmnsn)+ "sq km\n"
    "carnosaur parameters           :\n"
    "mass & metabolism              : "+metab_dkt[fmr_cost]+"\n"
    "fmr                            : "+str(fmr_cost)+"kg / day\n"
    "max food consumption rate      : "+str(wolf_gn)+"kg/day \n"
    "carcass detection radius       : "+str(rdius)+"km\n"
    "initial carnosaur population   : "+str(intl_als)+"\n"
    "initial carcass population     : "+str(intl_crcs)+"\n"
    "average distance of carcass when first detected:\n"
    "percent of allosaurs that cannot detect anything/day:\n"
    "percent of allosaurs with gene : A  [start , end]\n"
    "percent of allosaurs with gene : B  [start , end]\n"
    "percent of allosaurs with gene : C  [start , end]\n"
    "percent of allosaurs with gene : D  [start , end]\n"
    reproduction rate / step :
    OR
    reproduce on days [30,90,180,275,320,420]
    carcass parameters:
    initial population: 8
    starting mass : 45000
    decay as expected in rep = ( -87/(1+ math.exp(-0.208506*n + 6.1256) ) + 100 )
    disappear when mass between 0 and 15000kg (25% of initial mass)
    rate of appearance: .82/day

    results:

    total allosaurs made: 6285
    allosaurs pop plateau reached at day 160 ish, between 1750-1899
    total carcasses: 318

    max pop of allosaurs at any given time = 1899

    in gross terms 318 carcasses at 45k kg is enough to feed 2168 allosaurs per day
    so my numbers of 1899 are right on the money

    299*20 = 5980 adults
    5980/3 = 1993
    1993*10 = 19,930 total animals
    is density of 1.993 living sauropods / km2

    carcasses represent living sauropod pop of :

    number of unmet carcasses:

    number of allosaurs that couldn't find food:

    average swarm size around one carcass:





"





    """ at mass 2000kg, 45kg sauropods support 5969 carnosaurs at sauropod adult pop 30k (total popl 100)
        that ratio is 6:10

        so far, a pop of 10k saurops in the simulation has sustained 1750 allosaurs at once but total of 3670 created.
        that really makes sense

        update: K might be 1500-1750 , 273 carcasses"""
