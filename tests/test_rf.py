from champ import *

def main():
    import matplotlib.pyplot as plt

    tf = s4p_to_tf('../data/peters_01_0605_B12_thru.s4p')
    imp = tf_to_imp(*tf)
    step = imp_to_step(*imp)
    pulse = step_to_pulse(*step, 1/16e9)

    plt.plot(*pulse)
    plt.show()

if __name__ == '__main__':
    main()