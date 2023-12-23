class Logic:
    def __init__(self):
        self.o = 0

    def l_not(self, i):
        if i == 0:
            self.o = 1
        elif i == 1:
            return 0

    def l_and(self, i):
        pass

    def l_or(self, i):
        pass


class Component:
    def __init__(self):
        pass

    def c_ld(self):
        pass

    def c_ldi(self):
        pass

    def c_ldp(self):
        pass

    def c_ldf(self):
        pass

    def c_relay(self):
        pass

    def c_timer(self, k):
        pass

    def c_counter(self, k):
        pass
