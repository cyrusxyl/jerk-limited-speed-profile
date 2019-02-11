import math


class SpeedProfile:
    def __init__(self, s, v_max, a_max, j_max):
        self.s = s
        self.v_max = v_max
        self.a_max = a_max
        self.j_max = j_max
        case = self._get_trajectory_instance()
        self._get_region_times(case)
        self._setup_regions()

    def _get_trajectory_instance(self):
        s = self.s
        v_max = self.v_max
        a_max = self.a_max
        j_max = self.j_max

        v_a = a_max**2 / j_max
        s_a = 2 * a_max**3 / j_max**2

        if v_max < v_a and s >= s_a:
            return 1
        elif v_max >= v_a and s < s_a:
            return 2
        else:
            if v_max * j_max < a_max**2:
                M = 1
                N = 0
            else:
                M = 0
                N = 1

            s_v = v_max * (M * 2 * math.sqrt(v_max / j_max) + N *
                           (v_max / a_max + a_max / j_max))
            print(s_v)
            if v_max < v_a and s < s_a and s >= s_v:
                return 3
            elif v_max < v_a and s < s_a and s < s_v:
                return 4
            elif v_max >= v_a and s >= s_a and s >= s_v:
                return 5
            elif v_max >= v_a and s >= s_a and s < s_v:
                return 6

    def _get_region_times(self, instance_case):
        s = self.s
        v_max = self.v_max
        a_max = self.a_max
        j_max = self.j_max

        if instance_case == 1 or instance_case == 3:
            self.t_j = math.sqrt(v_max / j_max)
            self.t_a = self.t_j
            self.t_v = s / v_max
        elif instance_case == 2 or instance_case == 4:
            self.t_j = math.pow(s / (2 * j_max), 1 / 3)
            self.t_a = self.t_j
            self.t_v = 2 * self.t_j
        elif instance_case == 5:
            self.t_j = a_max / j_max
            self.t_a = v_max / a_max
            self.t_v = s / v_max
        elif instance_case == 6:
            self.t_j = a_max / j_max
            self.t_a = (math.sqrt((4 * s * j_max**2 + a_max**3) /
                                  (a_max * j_max**2)) - a_max / j_max) / 2
            self.t_v = self.t_a + self.t_j

    def _setup_regions(self):
        t1 = self._t1 = self.t_j
        t2 = self._t2 = self.t_a
        t3 = self._t3 = self.t_a + self.t_j
        t4 = self._t4 = self.t_v
        t5 = self._t5 = self.t_v + self.t_j
        t6 = self._t6 = self.t_v + self.t_a
        t7 = self._t7 = self.t_v + self.t_a + self.t_j

        J = self.j_max
        A = self.t_j * self.j_max

        T1 = self._T1 = t1
        T2 = self._T2 = t2 - t1
        T3 = self._T3 = t3 - t2
        T4 = self._T4 = t4 - t3
        T5 = self._T5 = t5 - t4
        T6 = self._T6 = t6 - t5
        T7 = self._T7 = t7 - t6

        v1 = self._v1 = J * T1**2 / 2
        v2 = self._v2 = v1 + A * T2
        v3 = self._v3 = v2 + A * T3 - J * T3**2 / 2
        v4 = self._v4 = v3
        v5 = self._v5 = v4 - J * T5**2 / 2
        v6 = self._v6 = v5 - A * T6

        p1 = self._p1 = J * T1**3 / 6
        p2 = self._p2 = p1 + v1 * T2 + A * T2**2 / 2
        p3 = self._p3 = p2 + v2 * T3 + A * T3**2 / 2 - J * T3**3 / 6
        p4 = self._p4 = p3 + v3 * T4
        p5 = self._p5 = p4 + v4 * T5 - J * T5**3 / 6
        p6 = self._p6 = p5 + v5 * T6 - A * T6**2 / 2

    def get_time_required(self):
        return self._t7

    def get_profile(self, t):
        t1 = self._t1
        t2 = self._t2
        t3 = self._t3
        t4 = self._t4
        t5 = self._t5
        t6 = self._t6
        t7 = self._t7

        J = self.j_max
        A = self.t_j * self.j_max

        v1 = self._v1
        v2 = self._v2
        v3 = self._v3
        v4 = self._v4
        v5 = self._v5
        v6 = self._v6

        p1 = self._p1
        p2 = self._p2
        p3 = self._p3
        p4 = self._p4
        p5 = self._p5
        p6 = self._p6

        if t >= 0.0 and t < t1:
            j = J
            a = J * t
            v = J * t**2 / 2
            s = J * t**3 / 6
        elif t >= t1 and t < t2:
            tau = t - t1
            j = 0
            a = A
            v = v1 + A * tau
            s = p1 + v1 * tau + A * tau**2 / 2
        elif t >= t2 and t < t3:
            tau = t - t2
            j = -J
            a = A - J * tau
            v = v2 + A * tau - J * tau**2 / 2
            s = p2 + v2 * tau + A * tau**2 / 2 - J * tau**3 / 6
        elif t >= t3 and t < t4:
            tau = t - t3
            j = 0
            a = 0
            v = v3
            s = p3 + v3 * tau
        elif t >= t4 and t < t5:
            tau = t - t4
            j = -J
            a = -J * tau
            v = v4 - J * tau**2 / 2
            s = p4 + v4 * tau - J * tau**3 / 6
        elif t >= t5 and t < t6:
            tau = t - t5
            j = 0.0
            a = -A
            v = v5 - A * tau
            s = p5 + v5 * tau - A * tau**2 / 2
        elif t >= t6 and t <= t7:
            tau = t - t6
            j = J
            a = -A + J * tau
            v = v6 - A * tau + J * tau**2 / 2
            s = p6 + v6 * tau - A * tau**2 / 2 + J * tau**3 / 6
        elif t < 0.0:
            j = 0.0
            a = 0.0
            v = 0.0
            s = 0.0
        else:
            j = 0.0
            a = 0.0
            v = 0.0
            s = self.s
        return (j, a, v, s)


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import speed_profile
    import numpy as np
    import time

    start = time.time()
    sp = SpeedProfile(200.0, 25.0, 5.0, 5.0)

    t_max = sp.get_time_required()
    T = np.linspace(0, t_max, math.ceil(t_max * 100), endpoint=False)
    J = []
    A = []
    V = []
    S = []

    for t in T:
        (j, a, v, s) = sp.get_profile(t)
        J = J + [j]
        A = A + [a]
        V = V + [v]
        S = S + [s]

    end = time.time()
    print(end - start)

    plt.figure(1)
    plt.plot(T, S, label='s')
    plt.plot(T, V, label='v')
    plt.plot(T, A, label='a')
    plt.plot(T, J, label='j')
    plt.legend()
    plt.show()
