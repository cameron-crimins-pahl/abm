from collections import defaultdict

from mesa.time import RandomActivation
from multiprocessing import Pool, Process, Manager, Queue
from functools import partial
from itertools import repeat

import pandas as pd


def f(ob):
    return ob.step()

class RandomActivationByBreed(RandomActivation):
    """
    A scheduler which activates each type of agent once per step, in random
    order, with the order reshuffled every step.
    This is equivalent to the NetLogo 'ask breed...' and is generally the
    default behavior for an ABM.
    Assumes that all agents have a step() method.
    """


    def __init__(self, model):
        super().__init__(model)
        self.agents_by_breed = defaultdict(dict)



    def add(self, agent):
        """
        Add an Agent object to the schedule
        Args:
            agent: An Agent to be added to the schedule.
        """

        self._agents[agent.unique_id] = agent
        agent_class = type(agent)
        self.agents_by_breed[agent_class][agent.unique_id] = agent

    def remove(self, agent):
        """
        Remove all instances of a given agent from the schedule.
        """

        del self._agents[agent.unique_id]

        agent_class = type(agent)
        del self.agents_by_breed[agent_class][agent.unique_id]

    def step(self, by_breed=True):
        """
        Executes the step of each agent breed, one at a time, in random order.
        Args:
            by_breed: If True, run all agents of a single breed before running
                      the next one.
        """
        if by_breed:

            # nl = list(range(len(self.agents_by_breed)))
            # print(self.agents_by_breed)
            # print(nl)
            # p=Pool(8)
            # p.map(self.step_breed, nl)
            # self.steps += 1
            # self.time += 1
            # print("keys")
            # agent_keys = list(self.agents_by_breed[breed].keys())

            # print(self.agents_by_breed.keys())
            for agent_class in self.agents_by_breed:
                # print("agent class")
                print(agent_class)
                self.step_breed(agent_class)
            self.steps += 1
            self.time  += 1
        else:
            super().step()





    def step_breed(self, breed):
        """
        Shuffle order and run all agents of a given breed.
        Args:
            breed: Class object of the breed to run.
        """

        agent_keys = list(self.agents_by_breed[breed].keys())
        self.model.random.shuffle(agent_keys)

        # dkt = self.agents_by_breed[breed]
        # # print(dkt)
        # ded = pd.DataFrame.from_dict(dkt,orient="index")
        #
        # ded.columns = ["A"]
        # print(ded)
        # dl = ded["A"].tolist()

        # p = Pool()

        """"""
        # p.apply_async(f,args=(dl,))

        #
        for agent_key in agent_keys:

            print("agent_key iterator")

            print(self.agents_by_breed[breed][agent_key])

            self.agents_by_breed[breed][agent_key].step()

    def get_breed_count(self, breed_class):
        """
        Returns the current number of agents of certain breed in the queue.
        """
        return len(self.agents_by_breed[breed_class].values())
