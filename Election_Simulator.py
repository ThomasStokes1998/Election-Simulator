import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Data from fivethirtyeight.com
states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'DoColumbia',
          'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana',
          'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana',
          'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina',
          'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina',
          'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia',
          'Wisconsin', 'Wyoming']
# [Dem, Rep, Ind]
polling = [[384, 567, 48], [434, 495, 71], [488, 458, 54], [373, 567, 60], [609, 317, 74], [536, 400, 64],
           [595, 337, 68], [589, 340, 71], [878, 85, 37], [491, 467, 42], [476, 473, 51], [626, 312, 62],
           [377, 574, 49], [554, 392, 54], [413, 515, 72], [475, 463, 62], [420, 513, 67], [390, 566, 44],
           [383, 546, 71], [538, 397, 65], [628, 306, 66], [661, 292, 47], [508, 428, 64], [507, 427, 66],
           [392, 550, 58], [450, 511, 39], [442, 508, 50], [442, 505, 53], [502, 435, 63], [536, 424, 40],
           [565, 361, 74], [534, 410, 56], [623, 317, 60], [492, 467, 41], [380, 564, 56], [465, 480, 55],
           [362, 580, 58], [575, 376, 49], [502, 450, 48], [647, 316, 37], [435, 510, 55], [401, 527, 72],
           [411, 543, 46], [466, 478, 56], [404, 509, 87], [637, 292, 71], [526, 412, 62], [589, 354, 57],
           [358, 596, 46], [507, 441, 52], [290, 659, 51]]

college_votes = [9, 3, 11, 6, 55, 9, 7, 3, 3, 29, 16, 4, 4, 20, 11, 6, 6, 8, 8, 4, 10, 11, 16, 10, 6, 10, 3, 5, 6, 4,
                 14, 5, 29, 15, 3, 18, 7, 7, 20, 4, 9, 3, 11, 38, 6, 3, 13, 12, 5, 10, 3]
dict_1 = {}
dict_2 = {}
for i in range(len(states)):
    state = states[i]
    dict_1[state] = polling[i]
    dict_2[state] = college_votes[i]


def random(pop=1000):
    return np.random.randint(0, 1000, pop)


def result(state, pop=1000):
    votes = random(pop)
    dem = dict_1[state][0]
    rep = dict_1[state][1]
    num = np.random.randint(min(dem - 500, rep - 500), max(dem - 500, rep - 500), 1)
    num = min(max(num, -100), 100)
    dem = dem * (1 + (num / 1000))
    rep = rep * (1 - (num / 1000))
    dem_votes = 0
    rep_votes = 0
    ind_votes = 0
    for v in votes:
        if v < dem:
            dem_votes += 1
        elif v < dem + rep:
            rep_votes += 1
        else:
            ind_votes += 1
    return [round(dem_votes * 1000 / pop), round(rep_votes * 1000 / pop), round(ind_votes * 1000 / pop)]


def election(pop=1000):
    dem_col = 0
    rep_col = 0
    ind_col = 0
    dem_pop = 0
    rep_pop = 0
    ind_pop = 0
    for state in states:
        res = result(state, pop)
        cv = dict_2[state]
        dem_pop += res[0] * cv / 538
        rep_pop += res[1] * cv / 538
        ind_pop += res[2] * cv / 538
        if np.max(res) == res[0]:
            dem_col += cv
        elif np.max(res) == res[1]:
            rep_col += cv
        else:
            ind_col += cv
    elec_res = [dem_col, rep_col, ind_col]
    pop_vote = [round(dem_pop) / 10, round(rep_pop) / 10, round(ind_pop) / 10]
    return elec_res, pop_vote


def simulation(iter=1000, pop=1000):
    dem_col = []
    rep_col = []
    dem_pop = []
    rep_pop = []
    for i in range(iter):
        col, ppl = election(pop)
        dem_col.append(col[0])
        rep_col.append(col[1])
        dem_pop.append(ppl[0])
        rep_pop.append(ppl[1])
        if i + 1 % 10 == 0:
            print('Elections simulated:', i)
    return dem_col, dem_pop, rep_col, rep_pop


def visualise(iter=1000, pop=1000, college=False, pop_line=False, pop_hist=False):
    dem_col, dem_pop, rep_col, rep_pop = simulation(iter, pop)
    demwincol = 0
    repwincol = 0
    demwinpop = 0
    repwinpop = 0
    for i in range(len(dem_col)):
        if dem_col[i] > 270:
            demwincol += 1
        if rep_col[i] > 270:
            repwincol += 1
        if dem_pop[i] > 50:
            demwinpop += 1
        if rep_pop[i] > 50:
            repwinpop += 1

    print('Democrats Win College%: ', round(100 * demwincol / len(dem_col), 2))
    print('Republicans Win College%: ', round(100 * repwincol / len(rep_col), 2))
    print('Median Democrats College Votes: ', np.median(dem_col))
    print('Median Republican College Votes: ', np.median(rep_col))
    print('Democrats Votes > 50%: ', round(100 * demwinpop / len(dem_pop), 2))
    print('Republican Votes > 50%: ', round(100 * repwinpop / len(rep_pop), 2))
    print('Average Democrats Votes%: ', round(np.mean(dem_pop), 2))
    print('Average Republican Votes%: ', round(np.mean(rep_pop), 2))

    plt.style.use('fivethirtyeight')
    if college:
        plt.hist(rep_col, bins=20, color='red', alpha=0.7)
        plt.hist(dem_col, bins=20, color='blue', alpha=0.7)
        plt.axvline(270, color='black', alpha=0.5)
        plt.xlabel('Electoral College Votes')
        plt.ylabel('Number of Simulations')
        plt.title('Electoral College')
    elif pop_hist:
        plt.hist(rep_pop, bins=20, color='red', alpha=0.6)
        plt.hist(dem_pop, bins=20, color='blue', alpha=0.6)
        plt.axvline(50, color='black', alpha=0.5)
        plt.xlabel('Vote %')
        plt.title('Popular Vote')
    elif pop_line:
        plt.plot(dem_pop, color='blue', alpha=0.8)
        plt.plot(rep_pop, color='red', alpha=0.8)
        plt.axhline(50, color='black', alpha=0.5)
        plt.ylabel('Vote %')
        plt.title('Popular Vote')
    plt.show()


x = datetime.now()
print(x)
visualise()
print(datetime.now() - x)
