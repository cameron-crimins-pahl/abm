from mesa import Agent
###
from random_walk import RandomWalker
import cfg
###
# from wolf_sheep.random_walk import RandomWalker
# # import wolf_sheep.cfg as cfg


#  Aric A. Hagberg, Daniel A. Schult and Pieter J. Swart, “Exploring network structure, dynamics, and function using NetworkX”, in Proceedings of the 7th Python in Science Conference (SciPy2008), Gäel Varoquaux, Travis Vaught, and Jarrod Millman (Eds), (Pasadena, CA USA), pp. 11–15, Aug 2008

# Harris, C.R., Millman, K.J., van der Walt, S.J. et al. Array programming with NumPy. Nature 585, 357–362 (2020). DOI: 0.1038/s41586-020-2649-2. (Publisher link).

# https://doi.org/10.5281/zenodo.3509134


# Kazil J., Masad D., Crooks A. (2020) Utilizing Python for Agent-Based Modeling: The Mesa Framework. In: Thomson R., Bisgin H., Dancy C., Hyder A., Hussain M. (eds) Social, Cultural, and Behavioral Modeling. SBP-BRiMS 2020. Lecture Notes in Computer Science, vol 12268. Springer, Cham. http://doi-org-443.webvpn.fjmu.edu.cn/10.1007/978-3-030-61255-9_30

# Crump, M. (2010). Mysteries of the Komodo Dragon: The Biggest, Deadliest Lizard Gives Up Its Secrets (Illustrated ed.). Boyds Mills Press.
#
#
# National Park Service. (2014, October 1). Bear Series, Part One: A Bear’s Sense of Smell - Yosemite National Park (U.S. National Park Service). https://www.nps.gov/yose/blogs/bear-series-part-one-a-bears-sense-of-smell.htm
#
#
# Nowak, R. M., & Wilson, D. E. (1999). Walker’s Mammals of the World (2-Volume Set) (6th ed.). Johns Hopkins University Press.


import pandas as pd
import numpy as np
import os
from os import path
import math
import random
from scipy import spatial
import networkx as nx


dfw = pd.DataFrame([])
dfs = pd.DataFrame([])
dfg = pd.DataFrame([])
dfc = pd.DataFrame([])


class Sheep(RandomWalker):
    """
    A sheep that walks around, reproduces (asexually) and gets eaten.
    The init is the same as the RandomWalker. the time thing must be related to this_cell
    """
    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

        self.energy = cfg.goat_size_at_birth()


        # print("sheep energy is "+ str(self.energy))
        """the sheep's lifespan is len(dfs[dfs["unique_id"]==unique_id])"""

    def step(self):

        def decay_equation(n):
            rep = ( -87/(1+ math.exp(-0.208506*n + 6.1256) ) + 100 )

            # print(rep)

            return rep/100

        def carcs_per_day(n,dys):

            return n/dys

        data = pd.read_csv("sheep_data_sheet.csv")

        da = data[data["unique_id"]==self.unique_id]

        print("init_mass")

        if len(da.index) <1:
            init_mass = self.energy

        else:

            init_mass = da.loc[da["unique_id"]==self.unique_id,"initial_energy"].head(1).item()

        print(init_mass)

        self.age = len(da.index)
        """
        A model step. Move, then eat grass and reproduce.

        But for me it will be each step the sheep loses energy according to the decay equation.
        I need to record the number of days the sheep has existed by step.
        """
        # self.random_move()
        living = True

        nrg = self.energy

        self.energy *= decay_equation(self.age)

        nw_nrg = self.energy

        """if self.model.schedule.time between 1 and 90, it is spring
        if between 270 and 365, reproduce"""

        """i definitely need the list of adjacent wolves because i need to demonstrate that multiple wolves profit
           from a single carcassj
           and i can't forget to measure how many steps they take avg to find a carcass
           and I need to make them stay at a carcass once they find  it,"""
        this_cell = self.model.grid.get_neighbors(pos=self.pos,moore=True,radius=1)

        wlvs = [obj for obj in this_cell if isinstance(obj, Wolf)]

        if self.energy < np.random.uniform(0,init_mass*.15):

            """9000 kg is 20% of the original mass of the carcass
               when it becomes effectively useless to local animals.
               At that point, it is mostly bones and inedible elements
               """

            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            living = False

        # if self.model.grass:
        #     # Reduce energy by a certain amount
        #
        #     # If there is grass available, eat it
        #     this_cell = self.model.grid.get_cell_list_contents([self.pos])
        #     grass_patch = [obj for obj in this_cell if isinstance(obj, GrassPatch)][0]
        #     if grass_patch.fully_grown:
        #         self.energy += self.model.sheep_gain_from_food
        #         grass_patch.fully_grown = False

            # Death


        rprd = "false"

        days = self.model.schedule.time
        nt = data["unique_id"].nunique()

        """if total number of created carcasses / steps is greater than 1.3,
        do nothing,
        else make a new carcass
        for the ones with live animals ,
        if the animal dies it creates a carcass of its size
        i need to remmeber to make one with normally distributed animal size so like only 5 percent are full size
        just to see what happens to them
        when does predation become profitable ? when proportion of adults gets below a certain size?
        or when attack success is over a certain amount? I guess I'll find out
        also the situation with adults is that if the allosaur hits an adult more than 2x its own mass
        it autofails the hunt and maybe dies at like 80% of the time because of course a 4000 kg sauropod would be unkillable
        """
        print("day "+str(days))
        # if days > 1 and days < 365:
        #     # print("low yield season")
        #     if carcs_per_day(nt,days) < cfg.saurp_crcs_apprnce_rate():
        #     # if carcs_per_day(nt,days) < (cfg.saurp_crcs_apprnce_rate()*5):
        #
        #             print("CARCS PER DAY")
        #             print(carcs_per_day(nt,days))
        #
        #             """if the carcass hasn't reproduced yet, make a new carcass
        #                otherwise collect the data and do nothing"""
        #
        #             rprd="true"
        #
        #
        #             """i might need to make this produce like 2 carcasses per day
        #                based on 100k kg average carrion production per day.
        #                if only 5 die every year
        #
        #                if 1.5 animals died per day at 45000kg each, that would be avg 180kg per day
        #                I'll need to do it this way to demonstrate algebraic supply demand
        #                but
        #                """
        #             # self.nwnrg = random.randrange(20000,45000)
        #
        #             n_x = random.randrange(cfg.dimensions())
        #             n_y = random.randrange(cfg.dimensions())
        #
        #             npos = (n_x,n_y)
        #
        #             lamb = Sheep(self.model.next_id(), npos, self.model, self.moore, 1)
        #
        #             self.model.grid.place_agent(lamb, npos)
        #
        #             self.model.schedule.add(lamb)
        #
        #             print("new lamb position = "+str(npos))
        # elif 1 < days < 365:
        #     if carcs_per_day(nt,days) < cfg.saurp_crcs_apprnce_rate():
        #
        #             print("CARCS PER DAY")
        #             print(carcs_per_day(nt,days))
        #
        #             """if the carcass hasn't reproduced yet, make a new carcass
        #                otherwise collect the data and do nothing"""
        #
        #             rprd="true"
        #
        #
        #             """i might need to make this produce like 2 carcasses per day
        #                based on 100k kg average carrion production per day.
        #                if only 5 die every year
        #
        #                if 1.5 animals died per day at 45000kg each, that would be avg 180kg per day
        #                I'll need to do it this way to demonstrate algebraic supply demand
        #                but
        #                """
        #             # self.nwnrg = random.randrange(20000,45000)
        #
        #             n_x = random.randrange(cfg.dimensions())
        #             n_y = random.randrange(cfg.dimensions())
        #
        #             npos = (n_x,n_y)
        #
        #             # lamb = Sheep(self.model.next_id(), npos, self.model, self.moore, 1)
        #             #
        #             # self.model.grid.place_agent(lamb, npos)
        #             #
        #             # self.model.schedule.add(lamb)
        #
        #             print("new lamb position = "+str(npos))

        dst= {"consuming_wolves"  :[str(len(wlvs))]
            , "unique_id"         :[str(self.unique_id)]
            , "initial_energy"    :[str(nrg)]
            ,"resulting_energy"   :[str(nw_nrg)]
            ,"reproduced"         :[str(rprd)]
            ,"step_no"            :[str(self.model.schedule.time)]
            ,"age"                :[str(self.age)]
            ,"strt_mass"          :[str(init_mass)]}

        dsx = pd.DataFrame(dst)
        # print("sheep",dst)
        dsx.to_csv("sheep_data_sheet.csv",mode="a",header=False)






class Wolf(RandomWalker):
    """
    A wolf that walks around, reproduces (asexually) and eats sheep.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

        """i think my math is WAAAY wrong.
           i think my carcass generation freq needs to be changed to
           or maybe i roll the dice to say odds of carcass duplicating are 3 in 365"""

        # if self.energy>45000:
        #     self.energy =45000
        """how much energy should the wolves start with?
           should it be 1000 kg? yes
           and depending on metabolism

           okay so this is good: a monitor lizard loses 0.2 % of its mass every day it goes without eating
           after 168 days of no food, it dies, having lost 29% of its body mass.

           i need to check this citation. if 0.2% of body mass is near its FMR ,

           i think if the allosaur gets to 70% body mass as an ectotherm, it dies -- this might require math about how much energy is stored
           with each consumption event... 90% energy or whatever for carnivores.  That could also be weird because the math
           would be tough to bring above 1000 maybe?  it might be more complicated than I want to do on this round.

           edit = i could possibly get raound this by setting a maximum mass on the allosaur side of things.  Maybe they hit a max mass between
           1750 and 2000, and then have a heritability component associated with size.

           Gene A - max between 1500 and 1750,
           Gene B - max between 1600 and 2200 kg.
           make their energy needs conditional within each object based on Nagy

           Gene C - 35% chance to kill on contact of living sauropod 25% to be killed, rest of % draw
           Gene D - 25% chance to kill on contact of living sauropod 35% to be killed, rest of % draw

           no -- if the animal goes 10 consecutive days without eating it dies or if it gets to below 0 energy
           that is pretty generous so i should do this with a range of values... even if it could only go 10 days wihtout food it dies

           the more i think about this, the more the 70% body mass thing sounds good because starvation conditions are common in nature.
           The only drawback is that if I argue the sauropods died of starvation as a primary cause of mortality, would they have less than adult mass?
           they fattened up during good times and starved it out during bad times.  I also think that if I write seasonality component, the allosaurs
           will need a. size

           this is another great citation
           Huitu, O.; Koivula, M.; Korpimäki, E.; Klemola, T. & Norrdahl, K. (2003) “Winter food supply limits growth of northern vale populations in the absence of predation”, Ecology, 84, pp. 2108-2118.

           this paper is outstanding:
           starvation physiology:
           https://www.sciencedirect.com/science/article/pii/S109564331000005X?casa_token=ZrU6VR5dfeYAAAAA:1fRVw4gypP82tqjz72Rwuo6E160PMW_2ocdHRRnjSTMClCJCHklwaQIGjZXROQkqJco_ZBzIEQ
           section 1.3
           also for bird and mammal physiology they can only go like 5 days wihtout food, arbitrary but good

           """

        self.energy +=200
        """100 energy is roughly 10 days of energy at hatch time for varanid metabolism. if the animal cant find food in 10 days it dies """

    def step(self):

        def path_to_closest_sheep(crnt_crdnt,trgt_crdnt):
            G = nx.grid_2d_graph(cfg.dimensions(),cfg.dimensions())


            # coor1= self.pos
            # coor2 = sheep.pos

            pth = nx.bidirectional_shortest_path(G, source=crnt_crdnt, target=trgt_crdnt)

            # print(pth)

            return pth[1]

        """ life cost is 9kg / day for 1000kg varanid metabolism"""
        # print(self.energy)
        nrg = self.energy
        self.energy -= cfg.fmr_cost()
        # print(self.energy)
        rprd="false"
        nw_nrg=self.energy
        eat="false"

        """ it costs self.energy to move"""

        data = pd.read_csv("wolf_data_sheet.csv")

        da = data[data["unique_id"]==self.unique_id]

        self.age = len(da.index)

        x, y = self.pos

        """radius = 10 km because
           komodo dragons can smell carcasses 10km away
           brown bears may be at 20km but email here for sources: heiko jansen bear smell
           the other thing is that giant rotting sauropods must have smelled awful

           """
        this_cell = self.model.grid.get_neighbors(pos=self.pos,moore=True,radius=cfg.radyis())
        cl_shp = self.model.grid.get_neighbors(pos=self.pos,moore=True,radius=2)
        # this_cell = self.model.grid.get_cell_list_contents([self.pos])
        # print("close neighbors line 337")
        # print(cl_shp)

        """ the given list of sheep in adjacent cells with self.model.grid.get_cell_list_contents is inaccurate.
            self.model.grid.get_neighbors is better
        2020 9 17 and i can't forget to measure how many steps they take avg to find a carcass
        and I need to make them stay at a carcass once they find  it,"""

        sheep = [obj for obj in this_cell if isinstance(obj, Sheep)]

        clsshp = [objn for objn in cl_shp if isinstance(objn, Sheep)]
        # print("close sheep 1")
        # print(clsshp)

        # nw_nrg = self.energy

        # dist_f_carc = "None detected"

        # if random.random() < .02:
        een = random.random()
        if een < cfg.allsr_reprd_rte():

            print("line 320, random.random()= "+str(een)+" rprd rate "+str(cfg.allsr_reprd_rte()))
            """ reproduce if wolf energy is greater than 270 (1 month of food survival?)
            or
            reproduce if step is between 275-280 for breeding season
            all of them reproduce every day for 5 days because they hatch out of eggs and a bunch of new ones appear at once?
            sounds dumb

            I think I should do the same thing I did with carcasses.
            if the ratio of allosaurs to sauropods is lower than x , then reproduce?
            if total allosaurs per sq km is less than x , then reproduce?
            or should reproduction not happen?
            where does equilibrium take place? should i be concentrating on how many allosaurs is too many?
            how many does it take to deplete the supply, or do most sauropods disappear without allosaurs"""


            """self.energy/=2 divides the wolf's energy by 2 as a cost of having a cub, i don't want this because dinosaurs laid eggs"""
            # self.energy *= 0.45

            """new wolves start with 1+x energy"""

            n_x = random.randrange(cfg.dimensions())
            n_y = random.randrange(cfg.dimensions())

            npos = (n_x,n_y)

            cub = Wolf(self.model.next_id(), npos, self.model, self.moore, 1)
            self.model.grid.place_agent(cub, npos)
            self.model.schedule.add(cub)
            rprd = "true"
            # print("cub stats")
            # print(cub.unique_id)
            # print(cub.energy)
            # print("reprd = " + rprd)

        if len(sheep) > 0:
            # print("\nSHEEP")
            # print(self.unique_id,sheep)

            """this captures the list of all sheep objects within 10 step radius of the wolf
                wolves need to go toward the closest one, and eat it, or move randomly if none are detected"""

            cls_shp = []

            for ps in sheep:
                """this is the list of sheep object coordinates the wolf can detect based on detection radius=10 in line 217"""
                cls_shp.append(ps.pos)

            tree = spatial.KDTree(cls_shp)

            arr = tree.query([self.pos])

            clsst_shp = arr[1][0]

            sheep_to_eat = sheep[clsst_shp]
            # print("close sheep:")
            # print(clsst_shp)
            # print(sheep_to_eat)
#
            # print("SHEEP TO TARGET COORDINATES:")
            # print(self.pos)
            # print(sheep_to_eat.pos)


            to_trgt = path_to_closest_sheep(self.pos,sheep_to_eat.pos)
            # print("TO TARGET")
            # print(self.energy)
            # print(cls_shp)
            # print(to_trgt)
            # print(sheep_to_eat)
            # print(self.pos)

            self.non_random_move(to_trgt)
            # print(self.pos)

            # sheep_to_eat = self.random.choice(sheep)
            """ if the sheep is NOT adjacent to the wolf square,
                move toward it
                else
                don't move at all adn keep eating"""
            # print(sheep)

            start_e = sheep_to_eat.energy

            """make a dataframe to record the actions of each agent, if they ate, etc.  """

            # print("sheep from wolf perspective has  " +str(start_e)+ " energy")
            # """this selects the random sheep to be consumed """
            # print("sheep to eat and etc")
            print(sheep_to_eat)
            # print(clsshp)
            # if sheep_to_eat in clsshp:

            if sheep_to_eat.pos == self.pos:
                # print("eating a carcass")
                eat="true"
                # print("ate a sheep ", sheep_to_eat, clsshp)
                # print(self.unique_id,self.energy)
                # print(self.energy)
                # print("gains ",self.model.wolf_gain_from_food)
                self.energy = self.energy + self.model.wolf_gain_from_food
                # print(self.unique_id,self.energy)
                sheep_to_eat.energy = sheep_to_eat.energy - self.model.wolf_gain_from_food
                nw_nrg = self.energy
                # print(self.unique_id,nw_nrg)

        else:
            self.random_move()
            nw_nrg = self.energy

            rprd = "false"

        """ if the reptile allosaur's body mass drops by 30%, it dies.
            just as in monitor lizards"""
        idddd = str(self.unique_id)

        if self.energy < 1:
            # print("wolf dead "+ str(idddd))
            self.model.grid._remove_agent(self.pos, self)
            # print(self)
            self.model.schedule.remove(self)

        nw_nrg = self.energy

        dkt= {"adjacent_sheep"  :[str(len(clsshp))]
            , "unique_id"       :[str(self.unique_id)]
            , "initial_energy"  :[str(nrg)]
            , "resulting_energy" :[str(nw_nrg)]
            , "reproduced"       :[str(rprd)]
            ,"step_no"           :[str(self.model.schedule.time)]
            ,"age"               :[str(self.age)]
            ,"eat"              :[str(eat)]}
            # ,"dist_from_carc"   :[str(dist_f_carc)]}

        # print("wolf",dkt)
        dfx = pd.DataFrame(dkt)
        dfx.to_csv("wolf_data_sheet.csv",mode="a",header=False)


class Coyote(RandomWalker):
    """
    A coyote that walks around, reproduces (asexually) and either scavenges or kills other animals.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

        self.energy +=200
        """100 energy is roughly 10 days of energy at hatch time for varanid metabolism. if the animal cant find food in 10 days it dies """

    def step(self):

        def path_to_closest_sheep(crnt_crdnt,trgt_crdnt):
            G = nx.grid_2d_graph(cfg.dimensions(),cfg.dimensions())
            pth = nx.bidirectional_shortest_path(G, source=crnt_crdnt, target=trgt_crdnt)
            return pth[1]


        nrg         = self.energy

        """ life cost is 9kg / day for 1000kg varanid metabolism"""
        self.energy = self.energy - cfg.fmr_cost()

        eat="false"
        nw_nrg      = self.energy
        rprd        = "false"
        """ it costs self.energy per day to live fmr"""

        data = pd.read_csv("coyote_data_sheet.csv")

        killer ="false"

        da = data[data["unique_id"]==self.unique_id]

        self.age = len(da.index)

        sheep=[]
        goats=[]
        print("day")

        print(str(self.model.schedule.time))

        x, y = self.pos

        if self.energy < 2:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)


        if random.random() < cfg.allsr_reprd_rte():

            """new wolves start with 1+x energy"""

            n_x = random.randrange(cfg.dimensions())
            n_y = random.randrange(cfg.dimensions())

            npos = (n_x,n_y)

            cb = Coyote(self.model.next_id(), npos, self.model, self.moore, 1)

            self.model.grid.place_agent(cb, npos)

            self.model.schedule.add(cb)

            rprd = "true"

            """radius = 10 km because
               komodo dragons can smell carcasses 10km away
               brown bears may be at 20km but email here for sources: heiko jansen bear smell
               the other thing is that giant rotting sauropods must have smelled awful

               """
        else:

            this_cell       = self.model.grid.get_neighbors(pos=self.pos,moore=True,radius=cfg.radyis())

            this_cell_close = self.model.grid.get_neighbors(pos=self.pos,moore=True,radius=1)

            sheep = [obj for obj in this_cell if isinstance(obj, Sheep)]

            goats = [obj for obj in this_cell_close if isinstance(obj, Goat)]

            if len(goats) > 0:

                goat_to_eat = self.random.choice(goats)

                nbr = random.random()

                if goat_to_eat.energy<3000:
                    print("goat_to_eat")
                    print(goat_to_eat.energy)

                    print(goat_to_eat)

                    if nbr < .35:

                        self.energy = self.energy + self.model.wolf_gain_from_food

                        killer = "true"
                        eat    = "true"

                        print(goat_to_eat)

                        self.model.grid._remove_agent(goat_to_eat.pos, goat_to_eat)

                        self.model.schedule.remove(goat_to_eat)

                        shp = Sheep(self.model.next_id(), self.pos, goat_to_eat.model, goat_to_eat.moore, goat_to_eat.energy)

                        self.model.grid.place_agent(shp, self.pos)

                        self.model.schedule.add(shp)

                        nw_nrg = self.energy

                    elif nbr >= .4 and nbr <= .5:

                        self.model.grid._remove_agent(self.pos, self)

                        self.model.schedule.remove(self)

            elif len(sheep) > 0:

                """ the given list of sheep in adjacent cells with self.model.grid.get_cell_list_contents is inaccurate.
                    self.model.grid.get_neighbors is better
                2020 9 17 and i can't forget to measure how many steps they take avg to find a carcass
                and I need to make them stay at a carcass once they find  it,"""

                nw_nrg = self.energy

                """this captures the list of all sheep objects within 10 step radius of the wolf
                        wolves need to go toward the closest one, and eat it, or move randomly if none are detected"""

                cls_shp = []

                for ps in sheep:
                    """this is the list of sheep object coordinates the wolf can detect based on detection radius=10 in line 217"""
                    cls_shp.append(ps.pos)

                tree = spatial.KDTree(cls_shp)

                arr = tree.query([self.pos])

                clsst_shp = arr[1][0]

                sheep_to_eat = sheep[clsst_shp]

                to_trgt = path_to_closest_sheep(self.pos,sheep_to_eat.pos)

                self.non_random_move(to_trgt)

                start_e = sheep_to_eat.energy

                """this selects the random sheep to be consumed """

                if self.pos == sheep_to_eat.pos:
                    self.energy = self.energy + self.model.wolf_gain_from_food
                    sheep_to_eat.energy = sheep_to_eat.energy + self.model.wolf_gain_from_food
                    nw_nrg = self.energy

            else:
                self.random_move()
                rprd = "false"

        dkt= {"adjacent_sheep"   :[str(len(sheep))]
            , "unique_id"        :[str(self.unique_id)]
            , "initial_energy"   :[str(nrg)]
            , "resulting_energy" :[str(nw_nrg)]
            , "reproduced"       :[str(rprd)]
            ,"step_no"           :[str(self.model.schedule.time)]
            ,"age"               :[str(self.age)]
            ,"killed_something"  :[str(killer)]
            ,"eat"               :[str(eat)]}
            # ,"dist_from_carc"   :[str(dist_f_carc)]}
        # print(dkt)

        dfx = pd.DataFrame(dkt)
        dfx.to_csv("coyote_data_sheet.csv",mode="a",header=False)

class Goat(RandomWalker):
    """
    A sheep that walks around, reproduces (asexually) and gets eaten.
    The init is the same as the RandomWalker.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

        # self.energy += cfg.saurp_mass()
        self.energy = self.energy + cfg.goat_size_at_birth()

    def step(self):

        def animal_per_day(n,dys):
            return n/dys

        rprd="false"

        data = pd.read_csv("goat_data_sheet.csv")

        # ds = pd.read_csv("sheep_data_sheet.csv")

        # ds = ds["unique"]

        da = data[data["unique_id"]==self.unique_id]

        nt = data["unique_id"].nunique()

        self.age = len(da.index)

        self.random_move()

        nrg = self.energy
        nw_nrg = self.energy

        days = self.model.schedule.time

        # if animal_per_day(ds,days) < cfg.saurp_crcs_apprnce_rate():
            # shp = Sheep(self.model.next_id(), self.pos, self.model, self.moore, self.energy)
            #
            # self.model.grid.place_agent(shp, self.pos)
            #
            # self.model.schedule.add(shp)
            #
            # self.model.grid._remove_agent(self.pos, self)
            #
            # self.model.schedule.remove(self)

        if days > 0:

            dn = data[data["step_no"]==self.model.schedule.time-1]
            dn = dn.sample(n=1)
            """probability that 5% of max die? or 5% die every day? this makes no sense"""
            rndms = dn["unique_id"].tolist()



            # print(animal_per_day(nt,days))
            # if random.random() < .02:
            if self.unique_id in rndms:

                shp = Sheep(self.model.next_id(), self.pos, self.model, self.moore, self.energy)

                self.model.grid.place_agent(shp, self.pos)

                self.model.schedule.add(shp)

                self.model.grid._remove_agent(self.pos, self)

                self.model.schedule.remove(self)

            if animal_per_day(nt,days) < cfg.goat_reprd_rte():

                rprd="true"
                # self.energy /= 2
                n_x = random.randrange(cfg.dimensions())

                n_y = random.randrange(cfg.dimensions())

                npos = (n_x,n_y)

                lmb = Goat(self.model.next_id(), npos, self.model, self.moore, 1)

                self.model.grid.place_agent(lmb, npos)

                self.model.schedule.add(lmb)

            else:

                rprd="false"

        dst= {"unique_id"         :[str(self.unique_id)]
            , "initial_energy"    :[str(nrg)]
            ,"resulting_energy"   :[str(nw_nrg)]
            ,"reproduced"         :[str(rprd)]
            ,"step_no"            :[str(self.model.schedule.time)]
            ,"age"                :[str(self.age)]}

        dsx = pd.DataFrame(dst)
        dsx.to_csv("goat_data_sheet.csv",mode="a",header=False)


class GrassPatch(Agent):
    """
    A patch of grass that grows at a fixed rate and it is eaten by sheep
    """

    def __init__(self, unique_id, pos, model, fully_grown, countdown):
        """
        Creates a new patch of grass
        Args:
            grown: (boolean) Whether the patch of grass is fully grown or not
            countdown: Time for the patch of grass to be fully grown again
        """
        super().__init__(unique_id, model)
        self.fully_grown = fully_grown
        self.countdown = countdown
        self.pos = pos

    def step(self):
        if not self.fully_grown:
            if self.countdown <= 0:
                # Set as fully grown
                self.fully_grown = True
                self.countdown = self.model.grass_regrowth_time
            else:
                self.countdown -= 1


def function_test():
    print("test")
