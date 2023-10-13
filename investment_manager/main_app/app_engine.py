import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime # uninstall this
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns

# portfolio_data.py


class Portfolio:
    def __init__(self, 
                 allocation = None, leftover =None,cleaned_weights =None, 
                 list_ofweights =None,
                 list_assets= None,
                 mean_return = None,
                 var_return = None,
                 portfolio_returns =None
                 ):
        
        self.allocation = allocation
        self.leftover = leftover
        self.cleaned_weights = cleaned_weights
        self.list_ofweights = list_ofweights
        self.list_assets = list_assets

        self.mean_return = mean_return
        self.var_return = var_return
        self.portfolio_returns = portfolio_returns


    def selected_assets(self,listof_assets,run_Test=False):

        stocks_list = listof_assets
        self.list_assets = listof_assets
        #USING YAHOO FINANCE WE THEN CREATE A DF COMPRISING OF CLOSING PRICES AS BELOW
        df = pd.DataFrame()
        for i in stocks_list:
            try:
                ticker = yf.Ticker(i)
                data = ticker.history(period= "1y",interval ="1d")

                df[i] = data["Close"]

            except:
                continue

        #CLEANING DF
        df =df.replace("", np.nan, regex = True)
        df = df[df.columns[df.isnull().mean() < 0.5]]
        df = df.dropna()
        print(df.head())

        #USING PYPFOPT TO ALLOCATE ASSETS
        #this is about analysing covarience and returns calculations

        mu = expected_returns.mean_historical_return(df)
        s = risk_models.sample_cov(df)
        ef = EfficientFrontier(mu, s)
        weights = ef.max_sharpe()  #shows weights for each asset that are raw

        self.cleaned_weights = ef.clean_weights()
        print(self.cleaned_weights)
        self.list_ofweights = list(self.cleaned_weights.values())  # rounds up weights (#needed in views and other files)

        #lets analyse perfromance

        if len(stocks_list) > 40:

            ef.portfolio_performance(verbose = True)

            from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

            latest_prices = get_latest_prices(df)
            weights =self.cleaned_weights
            # value can be added by client
            da = DiscreteAllocation(weights, latest_prices, total_portfolio_value= 1000000)
            self.allocation, self.leftover = da.lp_portfolio() 
            print("DiscreteAllocation:", self.allocation,"\n", "Leftover:",self.leftover)
        else:
            print("You asset pick is too small for discrete allocation, pick 40+ assets")

    def run_montecarlo(self):

        print("we are in montecarlo now!")
        stocks_list = self.list_assets
        if stocks_list is None:
            print("Please call selected assets methodd before running the simulation")

            return "nothing calculated"
        
        n_simulations = 100
        current_prices = yf.download(stocks_list, period="1d")['Adj Close']
        current_prices = current_prices.values.tolist()
        print("here is our current prices:", current_prices)
        weights = np.array(self.list_ofweights)

        self.portfolio_returns = []

        for _ in range(n_simulations):
            price_changes = np.random.uniform(-0.1, 0.1, len(current_prices))
            random_price = np.array(current_prices)*(1 +price_changes)
            portfolio_value = np.sum(random_price*weights)
            portfolio_return = ((portfolio_value - np.sum(current_prices*weights))/np.sum(current_prices*weights) )*100
            self.portfolio_returns.append(portfolio_return)



        self.mean_return = np.mean(self.portfolio_returns)
        self.var_return = np.std(self.portfolio_returns)

        print(portfolio_return)

        print(f"Portfolio mean returns {self.mean_return}%")
        print(f"Portfolio risk by std {self.var_return}%")



    




