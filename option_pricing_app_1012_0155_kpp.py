# 代码生成时间: 2025-10-12 01:55:29
# Option Pricing Application using Python and Bottle
#
# This application provides a simple interface to calculate the price of a European call option
# using the Black-Scholes model.

from bottle import Bottle, request, response, run
import math

# Define the Bottle application
app = Bottle()

# Constants for the Black-Scholes model
RISK_FREE_RATE = 0.05  # Risk-free interest rate
VOLATILITY = 0.3  # Volatility of the underlying asset
TIME_TO_EXPIRATION = 1.0  # Time to expiration in years

# Helper function to calculate the cumulative distribution function of the standard normal distribution
def cnd(d):
    A1 = 0.31938153
    A2 = -0.356563782
    A3 = 1.781477937
    A4 = -1.821255978
    A5 = 1.3302744297
    sign = 1 if d >= 0 else -1
    d = abs(d)
    cnd = 1 - (1/(math.sqrt(2*math.pi))) * \
        (math.exp(-0.5*d*d) * \
        (A1 + A2*d + A3*d**2 + A4*d**3 + A5*d**4))
    return 0.5 * (1 + sign * cnd)

# Helper function to calculate the Black-Scholes price for a European call option
def black_scholes_call(S, K, T, r, sigma):
    d1 = (math.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    return (S * cnd(d1) - K * math.exp(-r * T) * cnd(d2))

# Route to calculate the option price
@app.route('/price', method='GET')
def price():
    # Get parameters from the query string
    S = request.query.S
    K = request.query.K
    T = request.query.T
    r = request.query.r
    sigma = request.query.sigma
    
    # Validate input parameters
    try:
        S = float(S)
        K = float(K)
        T = float(T)
        r = float(r)
        sigma = float(sigma)
    except ValueError:
        response.status = 400
        return {"error": "Invalid input parameters. Please provide valid numerical values for S, K, T, r, and sigma."}
    
    # Calculate the option price using the Black-Scholes model
    try:
        option_price = black_scholes_call(S, K, T, r, sigma)
        return {"option_price": option_price}
    except Exception as e:
        response.status = 500
        return {"error": "An error occurred while calculating the option price: " + str(e)}

# Run the application if this file is executed directly
if __name__ == '__main__':
    run(app, host='localhost', port=8080)