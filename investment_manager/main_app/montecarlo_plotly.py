from .app_engine import Portfolio
import plotly.graph_objects as go
import plotly.offline as pyo
import numpy as np



portfolio = Portfolio()
weights = portfolio.cleaned_weights

class Graphs:
    def __init__(self, plot_div1 = None, plot_div2 = None):

        self.plot_div1 = plot_div1
        self.plot_div2 = plot_div2

    def create_graphs(self,weights, portfolio_returns):
        print('About to create graphs')

        if weights is not None:
            num_ofsimulations = 10000 #this should be updatable
            print('WE CAN START GETTING OUR GRAPHS')
            labels =list(weights.keys())
            values = list(weights.values())

            fig1 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
            fig1.update_layout(title =f"Portfolio Allocation by Modern Portfolio Theory(MPT)", height= 500, width =500)
            self.plot_div1 = fig1
            # self.plot_div1 = pyo.plot(fig1, output_type ="div")

            #histogram for risk assesment
            y = portfolio_returns
            # print("HERE IS A LIST OF MY PORTFOLIO RETURNS:",y)
            mean_return = np.mean(portfolio_returns)
            risk_var = np.std(portfolio_returns)

            #mean_return and risk var will be shown on the graphs
            fig2 = go.Figure(data=[go.Histogram(y=y)])

            # Add horizontal lines to the histogram 
            fig2.update_layout(title =f"Montecarlo Risk Assesment {num_ofsimulations} simulations"
                               ,height= 500,
                                 width =700,
                                 xaxis = dict(title="Probability Density by Frequency"),
                                 yaxis = dict(title="Portfolio returns %"),
                              
                                 )
            
            fig2.add_hline(y=mean_return, line_dash ="dash", line_color ="green",annotation_text=f'Mean: {mean_return}%')
            fig2.add_hline(y=risk_var, line_dash ="dash",line_color ="red",annotation_text=f'Risk: {risk_var}%')
                
            self.plot_div2 = fig2
            # self.plot_div2 = pyo.plot(fig2, output_type="div")

