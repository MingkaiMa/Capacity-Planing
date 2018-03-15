import matplotlib.pyplot as plt


def plot_(nb_of_terminal, thinktime, D_CPU, D_Disk):
    fig = plt.figure()
    max_D = max(D_CPU, D_Disk)
    slop =  1 / (thinktime + D_CPU + D_Disk)
        
    N =  [i for i in range(0, nb_of_terminal + 1)]
    when_max_N_is = (thinktime + D_CPU + D_Disk) * (1 / max_D)

    y = []

    for i in N:
        if i < when_max_N_is:
            y.append(slop * i)
        else:
            y.append(1 / max_D)


    plt.plot(N, y)
    plt.xlabel('Nb of terminals')
    plt.ylabel('Throughout')
    plt.legend(loc='upper left')
    plt.show()


plot_(20, 14, 2.312, 2.182)
            
    
