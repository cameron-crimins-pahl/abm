"""
Wolf-Sheep Predation Model
================================
Replication of the model found in NetLogo:
    Wilensky, U. (1997). NetLogo Wolf Sheep Predation model.
    http://ccl.northwestern.edu/netlogo/models/WolfSheepPredation.
    Center for Connected Learning and Computer-Based Modeling,
    Northwestern University, Evanston, IL.
"""

from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.batchrunner import BatchRunner

# # #######

from agents import Sheep, Wolf, GrassPatch, Goat, Coyote
from schedule import RandomActivationByBreed
import cfg
import agents
import plot_thickens as pt
#
# # #######
# from wolf_sheep.agents import Sheep, Wolf, GrassPatch, Goat, Coyote
# from wolf_sheep.schedule import RandomActivationByBreed
# import wolf_sheep.cfg as cfg
# import wolf_sheep.agents as agents
# import wolf_sheep.plot_thickens as pt


class WolfSheep(Model):
    """
    Wolf-Sheep Predation Model
    parameters
    """

    height = 20
    width = 20

    initial_sheep = 10
    initial_wolves = 20
    initial_goats = 5

    sheep_reproduce = 0.04
    wolf_reproduce = 0.05


    wolf_gain_from_food = cfg.wolf_gn()

    grass = False
    grass_regrowth_time = 30
    sheep_gain_from_food = 4

    verbose = False  # Print-monitoring

 

    def __init__(
        self,
        height          = cfg.dimensions(),
        width           = cfg.dimensions(),
        initial_sheep   = cfg.initial_carcs(),
        initial_wolves  = cfg.initial_allsrs(),
        initial_coyotes = cfg.initial_srphs(),
        initial_goats   = cfg.initial_cmrser(),
        sheep_reproduce = 0.04,
        wolf_reproduce  = 0.05,
        wolf_gain_from_food = cfg.wolf_gn(),
        grass           = False,
        grass_regrowth_time = 30,
        sheep_gain_from_food = 4,
    ):

        super().__init__()
        # Set parameters
        self.height = height
        self.width = width
        self.initial_sheep = initial_sheep
        self.initial_wolves = initial_wolves
        self.initial_goats = initial_goats
        self.initial_coyotes = initial_coyotes
        self.sheep_reproduce = sheep_reproduce
        self.wolf_reproduce = wolf_reproduce
        self.wolf_gain_from_food = wolf_gain_from_food
        self.grass = grass
        self.grass_regrowth_time = grass_regrowth_time
        self.sheep_gain_from_food = sheep_gain_from_food

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        self.datacollector = DataCollector(
            {
                "Wolves" : lambda m: m.schedule.get_breed_count(Wolf),
                "Sheep"  : lambda m: m.schedule.get_breed_count(Sheep),
                "Coyotes": lambda m: m.schedule.get_breed_count(Coyote),
                "Goats"  :lambda m: m.schedule.get_breed_count(Goat),
            }
        )
        # def mk_anml():
        #
        # p=Pool(8)
        # p.map(self.step_breed, [i for i in range(self.initial_sheep)])
        # self.steps += 1
        # self.time += 1

        # Create sheep:
        for i in range(self.initial_sheep):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            energy = self.random.randrange(2 * self.sheep_gain_from_food)
            sheep = Sheep(self.next_id(), (x, y), self, True, energy)
            self.grid.place_agent(sheep, (x, y))
            self.schedule.add(sheep)

        # Create goats
        for i in range(self.initial_goats):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            energy = self.random.randrange(2 * self.wolf_gain_from_food)
            goat = Goat(self.next_id(), (x, y), self, True, energy)
            self.grid.place_agent(goat, (x, y))
            self.schedule.add(goat)

        # # Create coyotes
        for i in range(self.initial_coyotes):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            energy = self.random.randrange(2 * self.wolf_gain_from_food)
            coyote = Coyote(self.next_id(), (x, y), self, True, energy)
            self.grid.place_agent(coyote, (x, y))
            self.schedule.add(coyote)

        # Create wolves
        for i in range(self.initial_wolves):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            energy = self.random.randrange(2 * self.wolf_gain_from_food)
            wolf = Wolf(self.next_id(), (x, y), self, True, energy)
            self.grid.place_agent(wolf, (x, y))
            self.schedule.add(wolf)

        # Create grass patches
        if self.grass:
            for agent, x, y in self.grid.coord_iter():

                fully_grown = self.random.choice([True, False])

                if fully_grown:
                    countdown = self.grass_regrowth_time
                else:
                    countdown = self.random.randrange(self.grass_regrowth_time)

                patch = GrassPatch(self.next_id(), (x, y), self, fully_grown, countdown)
                self.grid.place_agent(patch, (x, y))
                self.schedule.add(patch)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        # collect data
        # print(self.schedule.step())
        self.datacollector.collect(self)
        if self.verbose:
            print(
                [
                    self.schedule.time,
                    self.schedule.get_breed_count(Wolf),
                    self.schedule.get_breed_count(Sheep),
                    self.schedule.get_breed_count(Goat),
                    self.schedule.get_breed_count(Coyote)
                ]
            )

    def run_model(self, step_count=200):

        print("step "+str(step_count))

        if self.verbose:
            print("Initial number wolves: ", self.schedule.get_breed_count(Wolf))
            print("Initial number sheep: ", self.schedule.get_breed_count(Sheep))

        for i in range(step_count):
            self.step()


        if self.verbose:
            print("")
            print("Final number wolves: ", self.schedule.get_breed_count(Wolf))
            print("Final number sheep: ", self.schedule.get_breed_count(Sheep))


if __name__=="__main__":
    # #
    md = WolfSheep()

    for itms in range(365):
        md.step()

    # pt.sauropod_neighbors()
    # pt.plot_allsr_vs_carcass()
    cfg.summary(cfg.dimensions(), cfg.wolf_gn(), cfg.radyis(), cfg.fmr_cost(), cfg.initial_carcs()
                , cfg.initial_allsrs(), cfg.saurp_mass(), cfg.saurp_crcs_apprnce_rate(), pt.total_allosaurs(), pt.total_carcasses()
                , pt.max_allsr(), pt.day_steps(), pt.max_srphgnx(), cfg.initial_cmrser(), pt.max_srphgnx()
                , pt.max_cmrsrs(),pt.avg_size(),pt.total_goats())
