import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy.integrate import simps
from numpy import trapz
from itertools import count

from matplotlib.animation import FuncAnimation

from mpl_toolkits import mplot3d
import random


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
    # print(df["unique_id"].nunique())

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
    df.columns =["step_no","allosaurs_at_carcass"]
    print("allosaurs at carcasses:")
    print(df)
    print(df[df["step_no"]=="91"])
    print(df[df["step_no"]==91])
    return df

def sauropod_data():
    df = pd.read_csv("sheep_data_sheet.csv")



    # ttl_saurp = df["unique_id"].nunique()
    #
    df = df.groupby(["step_no"]).count()
    #
    df = df.reset_index()

    df["animal"]="carcasses"

    df =df[["step_no","unique_id","animal"]]

    df.columns = ["step_no","carcasses","animal"]
    print(df)


    return df

def cmrsrs_data():
    df = pd.read_csv("goat_data_sheet.csv")
    print(df)

    print(len(df["step_no"].tolist()))

    df = df.groupby(["step_no"]).count()
    #
    df = df.reset_index()

    df["animal"]="living-sauropods"

    df =df[["step_no","unique_id","animal"]]
    df.columns = ["step_no","living-sauropods","animal"]
    print(df)
    return df

def srphgnx_data():
    df = pd.read_csv("coyote_data_sheet.csv")
    "unique sauropod carcasses"
    # print("ttl srphgnx")

    ttl_saurp = df["unique_id"].nunique()


    df = df.groupby(["step_no"]).count()
    #
    df = df.reset_index()

    df["animal"]="allosaur-predators"

    df =df[["step_no","unique_id","animal"]]
    df.columns = ["step_no","allosaur-predators","animal"]
    # print(df)
    return df


def total_allosaurs():
    df = pd.read_csv("wolf_data_sheet.csv")
    # print(df[df["step_no"]==1])
    # df = df.groupby(["unique_id"]).sum() <== this is maybe good to see how each allosaur fared
    ttl_allsr = df["unique_id"].nunique()
    # print(ttl_allsr)
    return ttl_allsr

def total_goats():
    df = pd.read_csv("goat_data_sheet.csv")
    # print(df[df["step_no"]==1])
    # df = df.groupby(["unique_id"]).sum() <== this is maybe good to see how each allosaur fared
    ttl = df["unique_id"].nunique()
    # print(ttl_allsr)
    return ttl

def goat_reprd_true():
    df = pd.read_csv("goat_data_sheet.csv")

    print(df.head())

    dft = df[df["reproduced"]==True]
    print(len(df.index))
    print(len(dft.index))

    print(df["unique_id"].nunique())

    print(dft)

def total_carcasses():
    df = pd.read_csv("sheep_data_sheet.csv")
    "unique sauropod carcasses"
    # print("ttl sauropods")
    ttl_saurp = df["unique_id"].nunique()
    # print(ttl_saurp)
    return ttl_saurp

def max_allsr():
    df = pd.read_csv("wolf_data_sheet.csv")
    df = df.groupby(["step_no"]).count()
    df = df.reset_index()
    df["animal"]="allosaur-scavengers"
    # print(df.columns)
    df =df[["step_no","unique_id","animal"]]
    df.columns = ["step_no","count","animal"]
    return df["count"].max()

def max_srphgnx():
    df = pd.read_csv("coyote_data_sheet.csv")
    df = df.groupby(["step_no"]).count()
    df = df.reset_index()
    df["animal"]="allosaur-predators"
    # print(df.columns)
    df =df[["step_no","unique_id","animal"]]
    df.columns = ["step_no","count","animal"]
    return df["count"].max()

def max_cmrsrs():
    df = pd.read_csv("goat_data_sheet.csv")
    df = df.groupby(["step_no"]).count()
    df = df.reset_index()
    df["animal"]="live sauropods"
    # print(df.columns)
    df =df[["step_no","unique_id","animal"]]
    df.columns = ["step_no","count","animal"]
    return df["count"].max()

def max_carcasses():
    df = pd.read_csv("sheep_data_sheet.csv")
    df = df.groupby(["step_no"]).count()
    df = df.reset_index()

    df =df[["step_no","unique_id","animal"]]
    df.columns = ["step_no","count","animal"]
    return df["count"].max()

def day_steps():
    df = pd.read_csv("sheep_data_sheet.csv")
    df = df.groupby(["step_no"]).count()
    df = df.reset_index()
    return len(df.index)

def avg_size():
    df = pd.read_csv("sheep_data_sheet.csv")

    print(df["strt_mass"].mean())
    return df["strt_mass"].mean()

def crc_appearance_rate():

    df = pd.read_csv("sheep_data_sheet.csv")

    print(df)
    print("SEE HERE")

    df = df.groupby(["step_no"]).count()
    df = df.reset_index()
    print(df)



# def plot_allsr_vs_carcass():
def plot_allsr_vs_carcass(f_pth):
    df = pd.read_csv("wolf_data_sheet.csv")

    print(df)
    print("SEE HERE")

    df = df.groupby(["step_no"]).count()
    df = df.reset_index()


    df["animal"]="allosaur-scavengers"
    df =df[["step_no","unique_id","animal"]]
    df.columns = ["step_no","allosaur-scavengers","animal"]
    print(df)
    print(df[df["step_no"]==91])
    print(df[df["step_no"]==1])
    # df = df.groupby(["unique_id"]).sum() <== this is maybe good to see how each allosaur fared

    df_saurp = sauropod_data()
    print("carcasses")
    print(df_saurp)

    df_cmr = cmrsrs_data()
    print("living-sauropods")
    print(df_cmr)

    df_srph = srphgnx_data()
    print("allosaur-predators")
    print(df_srph)





    neighbs = sauropod_neighbors()

    # neighbs = dict(zip(neighbs["step_no"],neighbs["consuming_wolves"]))

    # df = df.reset_index()
    # df = df[["step_no","unique_id"]]
    # df["srp"] = df["step_no"].map(sauropod_map())
    # df.columns = ["step_no","allsr","srp"]

    # df = df.append(df_saurp,ignore_index=True)
    # df = df.append(df_cmr,ignore_index=True)
    # df = df.append(df_srph,ignore_index=True)

    # df = df.pivot(index='x', columns='color', values='y')
    # df = df.pivot(index='step_no', columns='animal', values='count')
    fig, ax = plt.subplots()

    colrs = { "allosaur-scavengers"  : "#e6178e"
             ,"allosaurs_at_carcass" : "#6a17e6"
             ,"carcasses"            : "#e68a17"
             ,"allosaur-predators"   : "#17e68a"}

    df.plot(kind="line",y="allosaur-scavengers",ax=ax,color="#e6178e")#00adb5
    neighbs.plot(kind="line",y="allosaurs_at_carcass",ax=ax,color="#6a17e6")
    df_srph.plot(kind="line",y="allosaur-predators",ax=ax,color="#17e68a")
    df_cmr.plot(kind="line",y="living-sauropods",ax=ax, color="#0254a1")
    df_saurp.plot(kind="line",y="carcasses",ax=ax,color="#e68a17")

    ax.set_xlabel("Day")
    ax.set_ylabel("Population")

    plt.title("allosaur population vs carrion supply over time")
    # plt.show()
    plt.savefig(f_pth)
    plt.savefig("/Users/cameronpahl/Documents/Science:Class/2020_Rewrite_citations/results/04-vrnd-2k-test/figure_1.png")

def pop_check():

    df=pd.read_csv("sheep_data_sheet.csv")
    # print(df.sort_values(by=['strt_mass']))
    df = df.groupby(["step_no"]).count()
    df = df.reset_index()
    df["animal"]="carcasses"
    df = df[["step_no","unique_id","animal"]]
    df.columns = ["step_no","carcasses","animal"]
    print(df)

    """drop duplicates keep first uniquq_id to get the real distribution of animal carcass sizes"""

    df2 = pd.read_csv("wolf_data_sheet.csv")
    df2 = df2.groupby(["step_no"]).count()
    # print(df2)
    df2 = df2.reset_index()
    # # df2 =df2.drop_duplicates(subset=["step_no"],keep="first")
    #
    df2["animal"]="carnosaur-scavengers"
    df2 = df2[["step_no","unique_id","animal"]]
    df2.columns = ["step_no","carnosaur-scavengers","animal"]
    #
    # df2["carnosaur-scavengers"] = df2.index
    # # df2.columns = ["step_no","carnosaur-scavengers"
    # print(df2)
    # print(df2.columns)

    df3 = pd.read_csv("goat_data_sheet.csv")
    df3 = df3.groupby(["step_no"]).count()
    df3 = df3.reset_index()
    df3 = df3[["step_no","unique_id"]]
    df3.columns = ["step_no","living-sauropods"]
    print(df3)

    df4 = pd.read_csv("coyote_data_sheet.csv")
    df4 = df4.groupby(["step_no"]).count()
    df4 = df4.reset_index()
    df4 = df4[["step_no","unique_id"]]
    df4.columns = ["step_no","carnosaur-predators"]
    # print(df3.head())
    # # #
    fig, ax = plt.subplots()
    df.plot(kind="line",y="carcasses",ax=ax,color="orange")
    df2.plot(kind="line",y="carnosaur-scavengers",ax=ax,color="blue")
    df3.plot(kind="line",y="living-sauropods",ax=ax,color="green")
    df4.plot(kind="line",y="carnosaur-predators",ax=ax,color="green")
    plt.show()
    # df = df[df["unique_id"]==1]
    # print(df.loc[df["unique_id"]==1,"initial_energy"].head(1).item())


def distribution():

    print(np.random.uniform(1,45000,10))



if __name__=="__main__":

   # asyn execution of lambda

   # distribution()
   # pop_check()
   # avg_size()
   goat_reprd_true()





    # jobs = []
    # for object in obj.list:
    #     job = apply_async(pool, lambda a, b: (a, b, a * b), (i, i + 1))
    #     job = apply_async(pool,f, object)
    #     jobs.append(job)
    #
    # for job in jobs:
    #     print(job.get())
