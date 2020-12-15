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

    description = (
        """A model for simulating wolf and sheep (consumer-resource) ecosystem modelling.
        Note height and width determine the height and width of the environment, which is separate from the
        params in server.py line 45 . They need to be the same numbers. If this is 100 x 100, then the server.py params must be 100x100

        100x100 = 10k sauropods at 1/km.
                    3000 adults = 150 die / year
                                    0.41 / day


        my dad says 100x100 could reasonably be 100km by 100km, but even 200km by 200km. He suggested that
        a reasonable allosaur could easily travel 1 or more km per day and could smell a gigantic carcass from 2-10km away, i need
        to check this with olfaction in allosaurs. but this is good.
        now i need to know how many carcasses would reasonably appear per year in a 200x200 sized space
        since 1-2 sauropods could have existed per square km in the most conservative estimates, that means
        a 40,000 square km space could have supported 40,000-80,000 sauropods. Which means 12000- 24,000 adults if 30% were adults.
        at 5% mortality that would be 600- 1200 carcasses/year. That is 3.2 per day at a constant rate, or 1.6 per day
        if the population was half as dense.
        I need to do this linearly, but also seasonally, which means I should do a dry season death with 80% of
        casualties in a 3 month time span, then 20% spread through the rest of the year.


        Don't forget to do a scatter plot of different genotypes over time? no i can just do a line graph
        oen color for predators/scavs plus strict scavengers
        also different colors for 20% winners vs 35% winners"""
    )

    def __init__(
        self,
        height          = cfg.dimensions(),
        width           = cfg.dimensions(),
        initial_sheep   = cfg.initial_carcs(),
        initial_wolves  = cfg.initial_allsrs(),
        initial_coyotes = cfg.initial_allsrs(),
        initial_goats   = cfg.initial_cmrser(),
        sheep_reproduce = 0.04,
        wolf_reproduce  = 0.05,
        wolf_gain_from_food = cfg.wolf_gn(),
        grass           = False,
        grass_regrowth_time = 30,
        sheep_gain_from_food = 4,
    ):
        """
        Create a new Wolf-Sheep model with the given parameters.
        Args:
            initial_sheep: Number of sheep to start with
            initial_wolves: Number of wolves to start with
            sheep_reproduce: Probability of each sheep reproducing each step
            wolf_reproduce: Probability of each wolf reproducing each step
            wolf_gain_from_food: Energy a wolf gains from eating a sheep
            grass: Whether to have the sheep eat grass for energy
            grass_regrowth_time: How long it takes for a grass patch to regrow
                                 once it is eaten
            sheep_gain_from_food: Energy sheep gain from grass, if enabled.
        """
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

        # Create coyotes
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
    #
    # md = WolfSheep()
    #
    # for itms in range(365):
    #     md.step()

    # pt.sauropod_neighbors()
    # pt.plot_allsr_vs_carcass()
    cfg.summary(cfg.dimensions(), cfg.wolf_gn(), cfg.radyis(), cfg.fmr_cost(), cfg.initial_carcs()
                , cfg.initial_allsrs(), cfg.saurp_mass(), cfg.saurp_crcs_apprnce_rate(), pt.total_allosaurs(), pt.total_carcasses()
                , pt.max_allsr(), pt.day_steps(), pt.max_srphgnx(), cfg.initial_cmrser(), pt.max_srphgnx()
                , pt.max_cmrsrs(),pt.avg_size(),pt.total_goats())
