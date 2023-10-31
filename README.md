# Stock Portfolio Builder
Markowitz model and montercarlo simulations to build robust risk averse investment portfolios

📈 The system uses Modern Portfolio Theory to allocate assets

➡️We use Pypfopt to allocate assets based on the Efficient Frontier

➡️The allocation of asset aims to get the maximum returns with least risk

➡️For risk management, there is a montercarlo simulation that 10000 to 1000000 simulations of random price changes at 20% price changes

💡APP system

The app is built on django framework, However the data presentation is slowly done with plotly's DASH APPLICATIONS

📝Lessons Learnt

⚡️Use of finance and big data API's to create models for investing.

⚡️Data presentation using web friendly framework ie Dash

⚡️General risk assesment using montercarlo simulations, to correctly evaluate risk

⚡Improved use of Object Oriented Programming to access various values



Build yours 😁

# Portfolio Allocator - Creating Optimal Portfolios with Efficient Frontier

The Portfolio Allocator is a web application that enables you to create optimal investment portfolios using the Efficient Frontier. It utilizes Django as the backend framework and Plotly Dash for data presentation. The app aims to help you make informed investment decisions.

## Getting Started

These instructions will help you set up the Portfolio Allocator on your local machine for development and testing purposes.

### Prerequisites

To run the Portfolio Allocator app, you need the following installed on your system:

- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [Plotly Dash](https://dash.plotly.com/)
- [Virtualenv](https://pypi.org/project/virtualenv/)

### Installation

1. Clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/portfolio-allocator.git
cd portfolio-allocator
Create a virtual environment and activate it:
bash
Copy code
virtualenv venv
source venv/bin/activate
Install the required Python packages:
bash
Copy code
pip install -r requirements.txt
Migrate the database:
bash
Copy code
python manage.py migrate
Create a superuser account to access the admin panel:
bash
Copy code
python manage.py createsuperuser
Start the development server:
bash
Copy code
python manage.py runserver
Access the Portfolio Allocator web application at http://localhost:8000
Usage
Log in with your superuser credentials to access the admin panel.
Add assets, such as stocks, bonds, or other investment options, to the system.
Set your risk-free rate and other portfolio constraints.
Use the Efficient Frontier to create optimal portfolios.
View the created portfolios with their performance metrics on the dashboard.
Deployment
To deploy the Portfolio Allocator app in a production environment, you can use platforms like AWS, Google Cloud, or Heroku. Follow these general steps:

Set up a production server with Python, Django, and Plotly Dash.
Clone the Portfolio Allocator repository on your production server.
Configure environment variables for production settings.
Collect static files for production:
bash
Copy code
python manage.py collectstatic
Configure your web server (e.g., Nginx, Apache) as a reverse proxy.
Use a process manager like Gunicorn to serve the application.
Remember to secure your deployment and manage server resources efficiently for a reliable and responsive application.

Built With
Django - Backend server
Plotly Dash - Frontend data presentation
Efficient Frontier - Portfolio optimization
Python - The programming language
Virtualenv - For Python environment isolation
License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
The Django and Plotly Dash communities for providing robust frameworks
Efficient Frontier for portfolio optimization techniques
Happy Portfolio Allocation!
