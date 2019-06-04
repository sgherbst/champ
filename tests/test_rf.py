from champ import *

def main():
    import matplotlib.pyplot as plt

    tf = s4p_to_tf('../data/peters_01_0605_B12_thru.s4p')
    imp = tf_to_imp(*tf)
    step = imp_to_step(*imp)
    pulse = center_pulse(*step_to_pulse(*step, 1/16e9))

    plt.stem(get_pulse_coeffs(*pulse, t_samp=1/16e9, n_pre=25, n_post=100))
    plt.show()

    plt.plot(*pulse)
    plt.show()

if __name__ == '__main__':
    main()