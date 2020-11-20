
# from gridworld import Agent, TorusGrid, GridWorld
# from gridworld import moore_neighborhood, GridWorldGUI




"""100 animals, 2, 5 or 9 die at each step w/ randomly generated mass dependign on population structure
   30 animals (just adults) .6, 1.5, 2.7 die per step at 45,000 kg mass

   inheritance is also important; if an allosaur randomly encounters a living sauropod and we assume kills it,
   + 1 inheritance point to descendant with binocular vision + bite force. maybe some allosaurs randomly have more bite force  than others
   and if the number of allosaurs at step end have high bite force then selection favored them. only allosaurs with high bite force can kill though, so weak biters
   do nothing when they encounter a sauropod. I also need to make sure multiple animals can eat from the same carcass until it is depleted.

   Spatially distributed resources in Template 3 :  1. how do I set the temporal persistence / regeneration of patches?
                                                    2. can multiple individuals extract from the same cell until depletion?
                                                    3. how do I change the detection abilities of agents w/respect for patches?
                                                       I want agents to locate cells of
                                                           a. n-cells away and
                                                           b. greater supply favored

                                                       Example: Agents must move toward the cells with greatest supply in their radius.
                                                       They can detect spaces with supply vs those without , within a certain radius of themselves.

                                                    4. How do I distribute resources to be either 0 or 30k-50k? This would be just adult-sized carcasses.
                                                       or maybe by age class of the carcass? ex. some carcasses of size in adults range and some of adolescents range?
                                                       also the carcasses need to be present for like 2 months or until depleted

                                                    5. How long is a day? Should each iteration be 1 day, then run 365 steps to equal one year?
                                                       In that case should i incorporate seasonality into this model, to account for high vs low yield seasons?"""

""" I wonder if changing the Cell.Data document would solve the resource supply issue.
    Instead of Lat Long Growth Rate as fixed, i would do Lat Long Random number between numbers
    But, it would probably be better to generate his data in Pandas? So that each iteration gives
    a different number, but that when a cell gets + something it can either decay over time or remain
    in place until agents consume it.  I really wish I could just talk to a professor for an hour and get the answer. """

""" Template Model 16: Interacting Agents of Different Types """


"""  https://math.libretexts.org/Bookshelves/Applied_Mathematics/Book%3A_Introduction_to_the_Modeling_and_Analysis_of_Complex_Systems_(Sayama)/19%3A_AgentBased_Models/19.02%3A_Building_an_Agent-Based_Model

    1. Specific Problem to be solved by the ABM
    2. Design of agents and their static/dynamic attributes
    3. Design of an environment and the way agents iteract with it.
    4. Design of agents' behaviors/.. ==> do they get bigger as they consume, pass on size, and biggest 10th of individuals scare others away?  ghood idea
    5. Designe of agents' mutual interactions
    6. Availability of data.
    7. Method of model validation.

    """
