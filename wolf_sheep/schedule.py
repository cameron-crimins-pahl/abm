from collections import defaultdict

from mesa.time import RandomActivation
import time
from functools import partial
from itertools import repeat
import concurrent.futures
import threading

import pandas as pd
import os




def f(ob):
    try:
        # print(ob)
        # print("stepped-function",ob)
        ob.step()
    except Exception as e:
        print("error",ob.age,ob.unique_id,ob)


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
            dkt = self.agents_by_breed
            ded = pd.DataFrame.from_dict(dkt,orient="index").transpose()

            objcts =[]

            for im in list(range(len(ded.columns))):
                print("length |||")
                print(ded.columns)
                print(range(len(ded.columns)))

                if len(ded.columns)<3:
                    break
                else:
                    print("im", im)
                ###########
                    da = ded.iloc[:,im]
                    da = da[da.notna()]
                    da = da.tolist()
                    objcts.append(da)

            for itms in objcts:
                # print(itms)
                self.step_breed(itms)


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

        output1 = list()
        # print(breed)
        with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
            for out1 in executor.map(f, breed):
                output1.append(out1)

                # confirm output
                # print(output1)
                # print("Task Executed {}".format(threading.current_thread()))


    def get_breed_count(self, breed_class):
        """
        Returns the current number of agents of certain breed in the queue.
        """
        return len(self.agents_by_breed[breed_class].values())
