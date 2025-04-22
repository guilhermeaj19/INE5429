from rng_algorithm import RNGAlgorithm

#Source: https://www.geeksforgeeks.org/python-program-for-basic-and-extended-euclidean-algorithms-2/
def gcd_extended(a: int, b: int) -> tuple[int, int, int]: 
    if a == 0 : 
        return b, 0, 1
            
    gcd,x1,y1 = gcd_extended(b%a, a) 
    
    x = y1 - (b//a) * x1 
    y = x1 
    
    return gcd, x, y 

def inverse_multiplicative(x: int,p: int) -> int:
    _, x_inverse, _ = gcd_extended(x, p) 

    return x_inverse % p #evitar x < 0

#Source: https://www.johndcook.com/blog/2020/02/19/inverse-congruence-rng/
class InversiveCongruentialGenerator(RNGAlgorithm):
    def __init__(self, seed: int, a: int, b: int, p: int) -> None:
        super().__init__(seed)
        self.a = a
        self.b = b
        self.p = p
    
    def generate(self) -> int:
        try:
            self.x/self.x #Its better do this than do a "if self.x == 0"
            x_inverse = inverse_multiplicative(self.x, self.p)
            self.x = (self.a*x_inverse + self.b) % self.p
        except ZeroDivisionError:
            self.x = self.b

        return self.x
