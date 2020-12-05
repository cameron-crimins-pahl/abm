from collections import defaultdict

from mesa.time import RandomActivation
from multiprocessing import Pool, Process, Manager, Queue
from functools import partial
from itertools import repeat

import pandas as pd


def f(ob):
    print(ob)
    print("stepped-function")
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
            dkt = self.agents_by_breed
            ded = pd.DataFrame.from_dict(dkt,orient="index").transpose()
            # ded = ded.fillna("")
            # # ded.columns = ["A"]
            # print(ded)
            # print(ded.columns)

            da = ded.iloc[:,0]
            da = da[da.notna()]
            da = da.tolist()

            db = ded.iloc[:,1]
            db = db[db.notna()]
            db = db.tolist()


            dc = ded.iloc[:,2]
            dc = dc[dc.notna()]
            dc = dc.tolist()

            dd = ded.iloc[:,3]
            dd = dd[dd.notna()]
            dd = dd.tolist()

            # print("da")

            # print(da)
            objcts = [da,db,dc,dd]
            # dl = ded["A"].tolist()
            #
            #  p = Pool()
            #
            # """"""
            #  p.apply_async(f,args=(dl,))

            # nl = list(range(len(self.agents_by_breed)))
            # print(self.agents_by_breed)
            # print(nl)
            # p=Pool(8)
            # p.map(self.step_breed, nl)
            # self.steps += 1
            # self.time += 1
            # print("keys")
            # agent_keys = list(self.agents_by_breed[breed].keys())

            for itms in objcts:
                print(itms)

                self.step_breed(itms)


            # print(self.agents_by_breed.keys())
            # for agent_class in self.agents_by_breed:
            #     """agent class is breed"""
            #     print("agent class step keys")
            #     agent_keys = list(self.agents_by_breed[agent_class].keys())
            #     print(agent_keys)
            #     for agent_key in agent_keys:
            #     # print(self.agents_by_breed)
            #         print(self.agents_by_breed[agent_class][agent_key])
            #         print(agent_class)
            #         self.step_breed(self.agents_by_breed[agent_class][agent_key])
                # self.step_breed(agent_class)

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

        # agent_keys = list(self.agents_by_breed[breed].keys())
        # self.model.random.shuffle(agent_keys)
        #
        # dkt = self.agents_by_breed[breed]
        # print("step-breed")
        # # print(dkt)
        # ded = pd.DataFrame.from_dict(dkt,orient="index")
        #
        # ded.columns = ["A"]
        # print(ded["A"].iloc[0])
        # dl = ded["A"].tolist()
        # print(dl)

        # f(ded["A"].iloc[0])

        print("breed list")
        print(breed)

        p = Pool()

        """"""
        p.map(f,breed)
        # p.apply_async(f,args=(dl,))
        # print("stepped")

        #
        # for agent_key in agent_keys:
        #
        #     print("agent_key iterator")
        #
        #     print(self.agents_by_breed[breed][agent_key])
        #
        #     self.agents_by_breed[breed][agent_key].step()

    def get_breed_count(self, breed_class):
        """
        Returns the current number of agents of certain breed in the queue.
        """
        return len(self.agents_by_breed[breed_class].values())
