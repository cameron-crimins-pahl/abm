import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from mpl_toolkits import mplot3d
import random



def plot_sauropods():
   
    df = pd.read_csv("sheep_data_sheet.csv")
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
    return df

def sauropod_data():
    df = pd.read_csv("sheep_data_sheet.csv")
    df = df.groupby(["step_no"]).count()
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
    df = df.reset_index()
    df["animal"]="living-sauropods"
    df =df[["step_no","unique_id","animal"]]
    df.columns = ["step_no","living-sauropods","animal"]
    print(df)
    return df

def srphgnx_data():
    df = pd.read_csv("coyote_data_sheet.csv")
    ttl_saurp = df["unique_id"].nunique()
    df = df.groupby(["step_no"]).count()
    df = df.reset_index()
    df["animal"]="allosaur-predators"
    df =df[["step_no","unique_id","animal"]]
    df.columns = ["step_no","allosaur-predators","animal"]
    return df


def total_allosaurs():
    df = pd.read_csv("wolf_data_sheet.csv")
    ttl_allsr = df["unique_id"].nunique()
    return ttl_allsr

def total_goats():
    df = pd.read_csv("goat_data_sheet.csv")
    ttl = df["unique_id"].nunique()
    return ttl

def reprd_true(fle):
    df = pd.read_csv(fle)

    dft = df[df["reproduced"]==True]



def kill_true(fle):
    df = pd.read_csv(fle)
    print(df.head())
    dft = df[df["killed_something"]==True]
    print(df["unique_id"].nunique())
    print(dft[["initial_energy","resulting_energy","age","killed_something","step_no"]])

def eat_true(fle):
    df = pd.read_csv(fle)
    dft = df[df["eat"]==True]
    print(len(df.index))
    print(len(dft.index))
    print(df["unique_id"].nunique())
    print(dft[["initial_energy","resulting_energy","age","eat","step_no"]])


def goat_samples():
    df = pd.read_csv("goat_data_sheet.csv")
    df = df.head(20)
    df=df.drop_duplicates(['unique_id'])
    df = df.sample(frac=.01)
    print(df["unique_id"].tolist())

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
    df =df[["step_no","unique_id","animal"]]
    df.columns = ["step_no","count","animal"]
    return df["count"].max()

def max_cmrsrs():
    df = pd.read_csv("goat_data_sheet.csv")
    df = df.groupby(["step_no"]).count()
    df = df.reset_index()
    df["animal"]="live sauropods"
    df =df[["step_no","unique_id","animal"]]
    df.columns = ["step_no","count","animal"]
    print(df["count"].max())
    return df["count"].max()

def max_carcasses():
    df = pd.read_csv("sheep_data_sheet.csv")
    df = df.groupby(["step_no"]).count()
    df = df.reset_index()

    df =df[["step_no","unique_id"]]
    df.columns = ["step_no","count"]
    print(df["count"].max())
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


def sheep_eaten():
    df = pd.read_csv("sheep_data_sheet.csv")
    print(df[df["unique_id"]=="56"])
    df =df[df["unique_id"]==56]
    print(df)
    return df.to_csv("test_test_test.csv")




def plot_allsr_vs_carcass(f_pth):
    df = pd.read_csv("wolf_data_sheet.csv")
    print(df)
    print("SEE HERE")
    df = df.groupby(["step_no"]).count()
    df = df.reset_index()
    df["animal"]="allosaur-scavengers"
    df =df[["step_no","unique_id","animal"]]
    df.columns = ["step_no","allosaur-scavengers","animal"]


    df_saurp = sauropod_data()
    print("carcasses")
    print(df_saurp["carcasses"])
    for unit in df_saurp.index:
        df_saurp["carcasses"][unit] = df_saurp["carcasses"][unit]  * random.uniform(.2,2.2)
    df_saurp["carcasses"] = df_saurp["carcasses"].round()
    df_saurp["carcasses"] = df_saurp["carcasses"].rolling(window=11).mean()

    print(df_saurp["carcasses"])
    print(df_saurp)

    df_cmr = cmrsrs_data()
    print("living-sauropods")
    print(df_cmr)

    df_srph = srphgnx_data()
    print("allosaur-predators")
    print(df_srph)

    neighbs = sauropod_neighbors()
    fig, ax = plt.subplots()

    colrs = { "allosaur-scavengers"  : "#e6178e"
             ,"allosaurs_at_carcass" : "#6a17e6"
             ,"carcasses"            : "#e68a17"
             ,"allosaur-predators"   : "#17e68a"}

    df.plot(kind="line",y="allosaur-scavengers",ax=ax,color="#e6178e")#00adb5
    # neighbs.plot(kind="line",y="allosaurs_at_carcass",ax=ax,color="#6a17e6")
    df_srph.plot(kind="line",y="allosaur-predators",ax=ax,color="#17e68a")
    # df_cmr.plot(kind="line",y="living-sauropods",ax=ax, color="#0254a1")
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



    df5 = sauropod_neighbors()

    """drop duplicates keep first uniquq_id to get the real distribution of animal carcass sizes"""

    df2 = pd.read_csv("wolf_data_sheet.csv")
    df2 = df2.groupby(["step_no"]).count()
    # print(df2)
    df2 = df2.reset_index()

    df2["animal"]="carnosaur-scavengers"
    df2 = df2[["step_no","unique_id","animal"]]
    df2.columns = ["step_no","carnosaur-scavengers","animal"]


    df3 = pd.read_csv("goat_data_sheet.csv")
    df3 = df3.groupby(["step_no"]).count()
    df3 = df3.reset_index()
    df3 = df3[["step_no","unique_id"]]
    df3.columns = ["step_no","living-sauropods"]


    df4 = pd.read_csv("coyote_data_sheet.csv")
    df4 = df4.groupby(["step_no"]).count()
    df4 = df4.reset_index()
    df4 = df4[["step_no","unique_id"]]
    df4.columns = ["step_no","carnosaur-predators"]


    scavs = np.array(df2["carnosaur-scavengers"].tolist())

    minimas = (np.diff(np.sign(np.diff(scavs))) > 0).nonzero()[0] + 1

    fig, ax = plt.subplots()

    df.plot(kind="line",y="carcasses",ax=ax,color="orange")

    df4.plot(kind="line",y="carnosaur-predators",ax=ax,color="black")
    df5.plot(kind="line",y="allosaurs_at_carcass",ax=ax,color="green")

    for minima in minimas:
        plt.plot(df2.iloc[minima]["carnosaur-scavengers"], marker="o")
    plt.show()



def distribution():

    print(np.random.uniform(1,45000,10))



if __name__=="__main__":

   # asyn execution of lambda

   print(np.random.uniform())



   #

   # eat_true("wolf_data_sheet.csv")
   eat_true("coyote_data_sheet.csv")
   kill_true("coyote_data_sheet.csv")
   #
   sheep_eaten()
   pop_check()


   # reprd_true("wolf_data_sheet.csv")
   #
   # max_cmrsrs()
   # max_carcasses()
   # reprd_true("coyote_data_sheet.csv")

   # avg_size()
   # goat_samples()
   # goat_samples()





    # jobs = []
    # for object in obj.list:
    #     job = apply_async(pool, lambda a, b: (a, b, a * b), (i, i + 1))
    #     job = apply_async(pool,f, object)
    #     jobs.append(job)
    #
    # for job in jobs:
    #     print(job.get())
