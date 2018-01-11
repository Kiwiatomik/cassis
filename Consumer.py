# -*- coding: utf-8 -*-

"""
Issues:
    - hard coded cdf functions
    - max between two random variable is hardcoded too
Possible fixes:
    - tweak sympy
"""


import numpy as np
import sympy as sp
import Distribution


x, y, z = sp.symbols('x y z')  # Add / Delete symbols if needed
    

class Consumer:
    """
    Represents a consumer who search and switch.
    Attributes:
        id
        search costs : when she decides to visit a new shop she has never seen
        switch costs : when she decides to leave her curent shop
        valuations : set of valuation of every product in every shop
        time on the market ???
    Methods: maximal_valuation, get_favorite, decision

    Ideas : Share of info by overwriting __add__ (+) [for waaaaaaaaaaaay later]
            Incomplete memory by overwriting __sub__ (-)
    """

    def __init__(self,
                 consumer_id=0,
                 type_search='onebyone',
                 search_costs=0,
                 switch_costs=0,
                 distributions=Distribution.Uniform(0, 1),
                 valuations=np.array([])):
        """
        Assumptions:
            - Level of information can be deduced from valuations, i.e
        if a valuation is missing, she does not know the product
            - Valuations are never equal
        
        Difficulty:
            - We know the shops she visited, but not her valuations (useful?)
            - Modeling what the consumer does not know
        """
        
        self.consumer_id = consumer_id
        self.type_search = type_search
        self.search_costs = search_costs
        self.switch_costs = switch_costs
        self.distributions = distributions
        
        self.valuations = valuations
        self.maximal_valuation = self.maximal_valuation()
        self.favourite = self.get_favorite()


    def maximal_valuation(self):
        """
        Returns : maximal valuation the consumer knows
        Input : arrays of valuations
        Difficulty : valuations are arrays different lengths
                     but numpy.max requires square matrixes
                     
        Expected difficulty : If we introduce collections, 
                                there would be another hierarchy to deal with
        Possible solution : recursive function
        """
        
        max_valuations = [np.amax(i) for i in self.valuations]
        return np.amax(max_valuations)
    
    
    def get_favorite(self):
        """
        Gets the best valuation a consumer knows
        Input : valuations (and seller's id?) 
        Output: a valuation
        
        Expected difficulty : If we introduce collections, 
                                there would be another hierarchy to deal with
        Possible solution : ?
        """
        
        max_valuations_per_shop = [np.amax(i) for i in self.valuations]
        return np.argmax(max_valuations_per_shop)
    
    
    def decision(self, unknown_products):
        """
        Get the shop(s) the consumer will visit
            Have a think regarding search / consumer search
        Input : array of numbers of unknown products in each shop
                array of search costs
                array of switching costs
        
        Expected difficulty : If the consumer can visit many shops a each time
        Possible solution : iterative method? Recursive method?
        """
        
        return 0
    
    
    def __repr__(self):
        return "Consumer {}".format(self.consumer_id)


    def __str__(self):
        s = "Consumer {} prefers shop {} that gives her valuation {}".format(
                self.consumer_id, self.favourite, self.maximal_valuation)
        return s