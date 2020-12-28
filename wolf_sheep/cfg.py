# from wolf_sheep import plot_thickens as pt
import plot_thickens as pt
import subprocess
import os
import numpy as np
import random
import pandas as pd

def dimensions():
    """ if this is 50x50, dimesnions = 50"""
    dimensions = 70
    return dimensions

def wolf_gn():
    fd = 43
    return fd

def radyis():
    """detection radius for consumer"""
    r = 9
    return r

def fmr_cost():
    c = 17.04
    return c

def initial_carcs():
    c = 3
    return c

def initial_allsrs():
    a = 30
    return a

def initial_srphs():
    a = 30
    return a

def initial_cmrser():
    a = 21
    return a

def saurp_mass():
    m = 45000
    return m

def allsr_reprd_rte():
    m = .03
    return m

def goat_reprd_rte():
    # m = .02
    m = random.uniform(12,14)
    return m

def saurp_crcs_apprnce_rate():

    # df = pd.read_csv("sheep_data_sheet.csv")
    #
    # dys = df["step_no"].nunique()
    # anm = df["unique_id"].nunique()

    """ user df.sample(frac=.05) to get 3 random rows
        then kill n sauropods to make a 5% mortality / cycle"""

    """.85 per day"""
    # # r = .99
    r = random.uniform(.4,.99)
    # return dys/anm
    return r

def age_limit():
    r = random.uniform(15,18)
    return r

def goat_size_at_birth():
    vn = np.random.uniform(1,45000,9)
    """the first argument is mean center of the distribution, eg 20
        the next argument is scale, so if 1 it is normal dist between 19 and 21.
        last arg is length of the list"""
    # vu = np.random.uniform(17,25,10)

    # print(vn)
    # d = abs(vn)
    # d = np.add(vn,abs(np.min(vn)))

    vn= np.sort(vn)
    # print("random")
    # print(random.choices(vn,[.15,.15,.1,.1,.05,.06,.04,.04,.15,.15])[0])

    return random.choices(vn,[.15,.15,.1,.1,.05,.05,.05,.17,.18])[0]
    # print(random.choices(vn,[.15,.15,.1,.1,.05,.06,.04,.04,.15,.15]))


metab_dkt = {9.04   :"1000kg_varanid"
            ,17.04  :"2000kg_varanid"
            ,5.94   :"1000kg_reptile"
            ,11.01  :"2000kg_reptile"
            ,18     :"1000kg_bird"
            ,28     :"2000kg_bird"
            ,17.17  :"1000kg_mammal"
            ,28.57  :"2000kg_mammal"} #2000*2339 = 4,678,000/490,000 = 9.55 kg/ha, too high
    # """<== notes:
    #    Gene A - max between 1500 and 1750,
    #    Gene B - max between 1600 and 2200 kg.
    #    make their energy needs conditional within each object based on Nagy
    #    Gene C - 35% chance to kill on contact of living sauropod 25% to be killed, rest of % draw
    #    Gene D - 25% chance to kill on contact of living sauropod 35% to be killed, rest of % draw"""
def summary(dmnsn, wolf_gn, rdius, fmr_cost, intl_crcs
            , intl_als, saurp_mass, carcass_apprnce_rte, totl_allsrs, totl_crcs
            , mx_pop_allsr, len_sim, intl_cyts, intl_gts, mx_pop_cyte
            , mx_pop_goats, avg_carcass_size, total_goats):

    """extinct=TRUE if days didn't reach 365
       competition = TRUE if multiple phenotypes compete for resources"""

    thrtcl_max_allsrs =  ((avg_carcass_size * totl_crcs)/365)/fmr_cost
    txt = "Results\n"+\
    "dimensions                     : "+str(dmnsn)+"x"+str(dmnsn)+" squares at 1km each\n"+\
    "area                           : "+str(dmnsn * dmnsn)+ "sq km\n"+\
    "mass & metabolism              : "+str(metab_dkt[fmr_cost])+"\n"+\
    "fmr                            : "+str(fmr_cost)+"kg / day\n"+\
    "max food consumption rate      : "+str(wolf_gn)+"kg/day \n"+\
    "carcass detection radius       : "+str(rdius)+"km\n"+\
    "initial allosaur population    : "+str(intl_als)+"\n"+\
    "initial srpghgnx population    : "+str(intl_cyts)+"\n"+\
    "initial live srpd population   : "+str(intl_gts)+"\n"+\
    "initial carcass population     : "+str(intl_crcs)+"\n"+\
    "max carcass mass               : "+str(saurp_mass)+"\n"+\
    "average distance of carcass when first detected : \n"+\
    "percent of allosaurs out of range:\n"+\
    "percent of allosaurs with gene : A  [start , end]\n"+\
    "percent of allosaurs with gene : B  [start , end]\n"+\
    "percent of allosaurs with gene : C  [start , end]\n"+\
    "percent of allosaurs with gene : D  [start , end]\n"+\
    "allosaur reproduction rate / step :\n"+\
    "decay euqation                 : rep = ( -87/(1+ math.exp(-0.208506*n + 6.1256) ) + 100 )\n"+\
    "disappear when mass between 0 and 15000kg (25% of initial mass)\n"+\
    "rate of carcass appearance     : "+str(carcass_apprnce_rte)+"/day\n"+\
    "\n"+\
    "total allosaurs made           : "+str(totl_allsrs)+"\n"+\
    "---allosaurs pop plateau reached at day 160 ish, between 1750-1899---\n"+\
    "total carcasses made           : "+str(totl_crcs)+"\n" +\
    "mean of carcass size @ death   : "+str(avg_carcass_size)+"\n" +\
    "max pop of live srpds @ any time : "+str(mx_pop_goats)+"\n" +\
    "total live srpds made          : "+str(total_goats)+"\n" +\
    "actual max of allosaurs        : "+str(mx_pop_allsr)+"\n" +\
    "actual max of  srphgnx         : "+str(mx_pop_cyte)+"\n" +\
    "theoretical max of allosaurs   : "+str( thrtcl_max_allsrs )+"\n" +\
    "In gross terms "+str(totl_crcs)+" carcasses at "+str(saurp_mass)+" kg is enough to feed "+ str( ((saurp_mass * totl_crcs)/365)/fmr_cost ) +" allosaurs\n"+\
    "-- "+str(mx_pop_allsr)+" is "+str( (mx_pop_allsr-thrtcl_max_allsrs)/thrtcl_max_allsrs )+"% of theoretical max\n"+\
    "-- "+str(mx_pop_cyte)+" is "+str( (mx_pop_cyte-thrtcl_max_allsrs)/thrtcl_max_allsrs )+"% of theoretical max\n"+\
    "total living adult sauropod pop: "+str(totl_crcs*20)+"\n"+\
    "sauropod density               : "+str( ((totl_crcs/3)*10)/(dmnsn * dmnsn))+" / km2\n"+\
    "allosaur density               : "+str( mx_pop_allsr/(dmnsn * dmnsn))+ " /km2\n"+\
    "number of unmet carcasses      :\n"+\
    "allosaurs that starved         :\n"+\
    "avg swarm size per carcass     :\n"

    # print(txt)
    # print(os.path.dirname(os.path.realpath(__file__)))

    # new_path = os.path.dirname(os.path.realpath(__file__))+"/"+str(metab_dkt[fmr_cost])
    new_path = "/Users/cameronpahl/Documents/Science:Class/2020_Rewrite_citations/results/"+str(metab_dkt[fmr_cost])+"-test"
    print(new_path)

    if len_sim<365:
        extinction="TRUE"
    else:
        extinction="FALSE"
    #
    subprocess.call("mkdir "+new_path, shell=True)
    #"/Users/cameronpahl/Documents/Science:Class/2020_Rewrite_citations/results/04-vrnd-2k-test/figure_1.png"
    # "45000kg_saurp-extinct-FALSE-competition.txt"
    f       = open(new_path+"/"+str(saurp_mass)+"_kg_saurp-extinction-"+extinction+"-competition-TRUE-seasons-FALSE-sr-"+str(rdius)+".txt","w")
    fg      =      new_path+"/"+str(saurp_mass)+"_kg_saurp-extinction-"+extinction+"-competition-TRUE-seasons-FALSE-sr-"+str(rdius)+".png"
    print(fg)
    f.write(txt)
    pt.plot_allsr_vs_carcass(fg)




    #
    #
    # """ at mass 2000kg, 45kg sauropods support 5969 carnosaurs at sauropod adult pop 30k (total popl 100)
    #     that ratio is 6:10
    #
    #     so far, a pop of 10k saurops in the simulation has sustained 1750 allosaurs at once but total of 3670 created.
    #     that really makes sense
    #
    #     update: K might be 1500-1750 , 273 carcasses"""


if __name__=="__main__":

    summary(70, 20, 6, 9.04, 13, 10, 45000, .82, 6000, 299, 1720,50)
