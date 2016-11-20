import copy


class cut:
    def __init__(self, a, b=0):
        self.a = a
        self.b = b

    def __add__(self, other):
        num, den = self.a[0] * other.a[1] + self.a[1] * other.a[0], self.a[1] * other.a[1]
        num, den = num/gcd(num, den), den/gcd(num, den)

        if self.a[2] == 0 and self.a[3] == 1:
            return cut([num, den, other.a[2], other.a[3]])
        elif other.a[2] == 0 and other.a[3] == 1:
            return cut([num, den, self.a[2], self.a[3]])
        elif other.a[3] == self.a[3]:
            return cut([num, den, self.a[2] + other.a[2], self.a[3]])
        else:
            print("add fucked up")

    def neg(self):
        ans = cut([- 1 * self.a[0], self.a[1], - 1 * self.a[2], self.a[3]])
        return ans

    def mag(self):
        return self.a[0] / self.a[1] + self.a[2] / self.a[3] ** 0.5

    def lik(self, other):
        for ind in range(0, 4):
            if self.a[ind] != other.a[ind]:
                return False
        return True

    def clean(self):
        if self.mag() >= 1:
            return cut.clean(self + cut([-1, 1, 0, 1]))
        elif self.mag() < 0:
            return cut.clean(self + cut([1, 1, 0, 1]))
        else:
            return copy.deepcopy(self)

    def __str__(self):
        return str(self.a)+str(self.b)+'('+str(self.mag())+")||"


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def cycle(a, b, c):

    inp = [cut([1, a, 0, 1]), cut([1, b, 0, 1]), cut([0, 1, 1, c])]
    if (c in [16,25,49]):
        inp[2] = cut([1, int(c**0.5), 0, 1])
    count, i = 0, -1
    flip = [cut([0, 1, 0, 1], -1), cut([0, 1, 0, 1], 1)]
    ent, ext = cut([0, 1, 0, 1]), cut([0, 1, 0, 1])

    # single flip
    while flip:

        i += 1
        count += 1
        s = 0
        temp = []
        ent, ext = cut.clean(ext), cut.clean(ext + inp[i % 3])

        # check to eliminate the case of all icing down
        if len(flip)==2 and ent.lik(flip[1]) and ext.lik(flip[0]) and flip[1].b == 1:
            flip[1].a = copy.deepcopy(ext.a)
            flip[0].b, flip[1].b = 1, -1
            continue


        # counting number of cuts with in selected portion
        if ent.mag() > ext.mag():
            while s < len(flip) and flip[s].mag() > ent.mag():
                s += 1
            while s < len(flip) and flip[s].mag() < ext.mag():
                s += 1

        else:
            while s < len(flip) and ext.mag() > flip[s].mag() > ent.mag():
                s += 1

        # switching cut positions
        for dummy in range(s):
            temp.insert(0, cut.clean(flip[0].neg() + (ent + ext)))
            temp[0].b = flip[0].b
            del flip[0]

        # adding entry exit
        if s % 2 == 0:
            temp.insert(0, copy.deepcopy(ent))
            temp.append(copy.deepcopy(ext))
            if flip:
                temp[0].b, temp[-1].b = flip[-1].b*-1, flip[-1].b
            else:
                temp[0].b, temp[-1].b = temp[-2].b, temp[-2].b*-1

        flip.extend(temp)

        # sending ext eq cuts to the back
        while flip[0].lik(ext):
            flip.append(flip[0])
            del flip[0]

        j = len(flip) -1
        while j >= 0:

            if flip[j-1].lik(flip[j]):
                if flip[j-1].b*flip[j].b == -1:
                    del flip[j]
                    del flip[j-1]
                    j += -1
                else:
                    print("lund")
            j += -1

    return count


def main():

    g = 53
    total = 0

    for c in range(g, 10, -1):
        for b in range(c - 1, 9, -1):
            for a in range(b - 1, 8, -1):
                k = cycle(a, b, c)
                print(a, b, c, ':', k)
                total += k
    print(total)

if __name__ == "__main__":
    main()
