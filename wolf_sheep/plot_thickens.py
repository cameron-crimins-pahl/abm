import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy.integrate import simps
from numpy import trapz
from itertools import count

from matplotlib.animation import FuncAnimation

from mpl_toolkits import mplot3d

# import matplotlib.animation as animation
import time


"""from sauropod sheet
   get nunique unique_ids for total number of carcasses,
   then compute number of sauropods that could make nunique items
   graph individuals w/ decay patterns
   graph total amount of food
   number unused carcasses
   density of carcasse / sq mile
   against estimated values
   comput ratio of carnosaurs to sauropods
   population changes over time AND
   the fact that they spiked at birth , then dropped because babies only had 10 days of travel reserves to find a new carcass
   and some of them couldn't do it in time.
   this really makes sense anyway because the babies had to rely on carcasses to survive,
   there is no effing way 2ft long juvenile allosauyrs hunted anything
   NOTE I ALSO NEED TO DO A SINGLE CARCASS VS A SINGLE POPULATION OF ALLOSAURS TO SEE HOW THE CARCASS RESPONDS TO MULTIPLE ANIMALS W/ and W/OUT COMPETITION
   THIS SHOULD BE A 10x10 PLOT WITH A SINGLE CARCASS"""


def plot_sauropods():
    df = pd.read_csv("sheep_data_sheet.csv")
    """205 carcasses over 171 days is 1.19 mortalities/ day. that is really good.
    there must be a point at which density of carcasses is high enough to support allosaurs

    I need to run this model for each metabolism where 1 dead sauropod and n number of allosaurs eat it. then get the data
    about how carcasses are consumed  with COMPETITION"""
    print(df["unique_id"].nunique())

    # step_no = x axis
    # enrgy = y axis
    # unique_id = columns

    df = df[["step_no","initial_energy","unique_id"]]

    df = df.pivot(index='step_no', columns='unique_id', values='initial_energy')
    df.plot(kind="line")
    plt.show()

def sauropod_neighbors():
    df = pd.read_csv("sheep_data_sheet.csv")

    df = df[["step_no","consuming_wolves"]].groupby(["step_no"]).sum()
    df = df.reset_index()
    df.columns =["step_no","allosarus_at_carcass"]
    return df

def sauropod_data():
    df = pd.read_csv("sheep_data_sheet.csv")
    "unique sauropod carcasses"
    print("ttl sauropods")



    ttl_saurp = df["unique_id"].nunique()
    print(ttl_saurp)

    # print(df.head())

    # df = df[["step_no","unique_id"]]

    # tfr = df[df["step_no"]==24]
    # print(tfr.groupby(["initial_energy"]).mean())
    #
    # print(len(tfr.index))
    #
    # tfv = df[df["step_no"]==25]
    # print(tfv.groupby(["initial_energy"]).mean())
    #
    # print(len(tfv.index))
    #
    # ts = df[df["step_no"]==26]
    # print(ts.groupby(["initial_energy"]).mean())
    #
    # print(len(ts.index))
    #
    df = df.groupby(["step_no"]).count()
    #
    df = df.reset_index()

    df["animal"]="sauropod"

    df =df[["step_no","unique_id","animal"]]

    df.columns = ["step_no","count","animal"]
    print(df)


    return df

def total_allosaurs():
    df = pd.read_csv("wolf_data_sheet.csv")
    # print(df[df["step_no"]==1])
    # df = df.groupby(["unique_id"]).sum() <== this is maybe good to see how each allosaur fared
    "unique allosaur carcasses"
    print("ttl allosaurs")
    ttl_allsr = df["unique_id"].nunique()
    print(ttl_allsr)
    return ttl_allsr

def total_carcasses():
    df = pd.read_csv("sheep_data_sheet.csv")
    "unique sauropod carcasses"
    print("ttl sauropods")
    ttl_saurp = df["unique_id"].nunique()
    print(ttl_saurp)
    return ttl_saurp

def max_allsr():
    df = pd.read_csv("wolf_data_sheet.csv")
    df = df.groupby(["step_no"]).count()
    df = df.reset_index()
    df =df[["step_no","unique_id","animal"]]
    df.columns = ["step_no","count","animal"]
    return df["count"].max(level="step_no")

def max_carcasses():
    df = pd.read_csv("sheep_data_sheet.csv")
    df = df.groupby(["step_no"]).count()
    df = df.reset_index()
    df =df[["step_no","unique_id","animal"]]
    df.columns = ["step_no","count","animal"]
    return df["count"].max(level="step_no")


def plot_allsr_vs_carcass():
    df = pd.read_csv("wolf_data_sheet.csv")
    # print(df[df["step_no"]==1])
    # df = df.groupby(["unique_id"]).sum() <== this is maybe good to see how each allosaur fared

    df_saurp = sauropod_data()
    df = df.groupby(["step_no"]).count()
    df = df.reset_index()
    df["animal"]="allosaur"
    df =df[["step_no","unique_id","animal"]]
    df.columns = ["step_no","count","animal"]
    neighbs = sauropod_neighbors()

    # neighbs = dict(zip(neighbs["step_no"],neighbs["consuming_wolves"]))

    # df = df.reset_index()
    # df = df[["step_no","unique_id"]]
    # df["srp"] = df["step_no"].map(sauropod_map())
    # df.columns = ["step_no","allsr","srp"]

    df = df.append(df_saurp,ignore_index=True)

    # df = df.pivot(index='x', columns='color', values='y')
    df = df.pivot(index='step_no', columns='animal', values='count')
    fig, ax = plt.subplots()

    df.plot(kind="line",ax=ax)
    neighbs.plot(kind="line",y="allosaurs_at_carcass",ax=ax)

    ax.set_xlabel("Day")
    ax.set_ylabel("Population")

    plt.title("allosaur population vs carrion supply over time")
    plt.show()
    plt.savefig("/Users/cameronpahl/Documents/Science:Class/2020_Rewrite_citations/results/04-vrnd-2k-test/figure_1.png")

def pop_check():

    return 6/5

if __name__=="__main__":

    plot_allsr_vs_carcass()
