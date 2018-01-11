# -*- coding: utf-8 -*-

"""
Issues:
    - pdf function is not an attribute in the Distribution class --> decrease generality
    - 3 loops for the cdf of the maximum is certainly suboptimal
Possible fix:
    - Be a better programmer?
"""
import sympy as sp
from sympy import oo

x = sp.symbols('x')


class BoundError(LookupError):
    """
    To raise when a distribution has imporper bound
    """


class DensityError(LookupError):
    """
    To raise when a density function is wrong
    """
    

class Distribution():
    """
    Interface class for probability distributions
    Attributes: cdf function
    Methods: pdf, check_pdf
    
    Issues:
        - the pdf should be computable in this class
    """
    def __init__(self, cdf={'support': [-oo, +oo], 'pieces': 1}):
        self.cdf = cdf
#        self.pdf = self.pdf()
    
    
    def pdf(self):
        """
        Differentiates the cdf function and returns the pdf function
        Input: cdf function
        Output: pdf function
        """
#        print(self.cdf)
        cdf_pieces = self.cdf['pieces']
        support = self.cdf['support']
        pieces = [sp.diff(piece[1]) for piece in zip(support[1:], cdf_pieces)]
        pdf = {'support': self.cdf['support'], 'pieces': pieces}
        if not self.check_pdf(pdf):
            print('Hey ! This is not a density function!')
        return pdf
    
    
    def check_pdf(self, pdf):
        """
        Checks if the integral of the pdf function is equal to one
        Input: pdf function
        Output: Raise error DensityError is integral is not equal to one
        """
        support = pdf['support']
        pieces = pdf['pieces']
        lower = support[:-1]
        upper = support[1:]
        integrals = [sp.integrate(piece, (x, l, u)) for l, u, piece in zip(lower, upper, pieces)]
        integral = sum(integrals)
        if integral != 1:
            raise DensityError('Integrating the density does not give 1')
        return True
        
    def __repr__(self):
        return 'Distribution {}'.format(self.cdf)


class Uniform(Distribution):
    """
    Class of the uniform distribution
    Attributes: bounds, the cdf (and pdf?)
    Methods: cdf_uniform
    Heritates from the class Distribution
    """
    def __init__(self, bottom=0, top=1):
        if bottom >= top:
            raise BoundError('Bottom value is greater than top value')
        super().__init__(self)
        self.bottom = bottom
        self.top = top
        self.cdf = self.cdf_uniform()
        self.pdf = self.pdf()
    
    
    def cdf_uniform(self):
        """
        Calculates the cdf function for a Uniform distribution on supprt [bottom, top]
        Input: support
        Output: cdf
        """
        support = [-oo, self.bottom, self.top, +oo]
        cdf_function = (x - self.bottom) / (self.top - self.bottom)
        pieces = [0, cdf_function, 1]
        cdf = {'support': support, 'pieces': pieces}
        return cdf
    
    def __repr__(self):
        return 'Uniform [{}, {}]'.format(self.bottom, self.top)
    

class DistributionMaximum(Distribution):
    """
    Class of distributions of the maximum of several random variables
    Attributes: array of distributions, cdf
    Methods: cdf_maximum
    Heritates from the class Distribution
    """
    def __init__(self, distributions=[Uniform(), Uniform()]):
        super().__init__(self)
        self.distributions = distributions
        self.cdf = self.cdf_maximum()
        self.pdf = self.pdf()
        
    def cdf_maximum(self):
        """
        Calculates the cdf of the distribution of the maximum of an array of random variables
        Input: array of random variable
        Output: cdf
        
        Issue:
            - 3 loops is certainly suboptimal
        """
        supports = [distribution.cdf['support'] for distribution in self.distributions]
        support = sorted(set([s for sup in supports for s in sup]))
        lower = support[:-1]
        upper = support[1:]
        all_pieces = [distribution.cdf['pieces'] for distribution in self.distributions]

        pieces = []
        for bounds in zip(lower, upper):
            piece = 1
            for i in range(len(supports)):
                supps = supports[i][1:]
                for j in range(len(supps)):
                    supp = supps[j]
                    if bounds[0] < supp and supp >= bounds[1]:
                        piece *= all_pieces[i][j]
                        break
            pieces += [piece]
        
        zeros = len(pieces) - len(set(pieces))
        support = support[0:1] + support[zeros + 1:]
        pieces = pieces[0:1] + pieces[zeros + 1:]
        return {'support': support, 'pieces': pieces}