# Life-cycle Assessment of Cellulosic Biofuel Production

Refer to the [publication](http://pubs.acs.org/doi/abs/10.1021/acssuschemeng.7b02116) for more details on the modeling and life-cycle accounting process.

## Model Dependencies
The core of the LCA-TEA model is written in Python 2.7. Below are the dependencies for the core model that can be easily installed using `pip`.

- [Python](https://www.python.org/download/releases/2.7/)
- [Numpy](https://docs.scipy.org/doc/numpy-1.10.1/user/install.html)
- [Pandas](http://pandas.pydata.org/pandas-docs/stable/install.html)
- [Flask](http://flask.pocoo.org/docs/0.12/installation/)

## Start a local instance
After you have installed the dependencies you can run a local instance of the webtool. Follow these steps:
- Clone the repo
- Navigate your command prompt inside the repo
- Start the server by running `FLASK_DEBUG=1 FLASK_APP=server.py flask run`
- Navigate to `localhost:5000`
- and Done! Easy!


## Background
Cellulosic biofuels are a promising option to meet a fraction of the liquid transportation fuel demand. They are a promising alternative to gasoline as they are a renewable and low-carbon option. To convert the biomass to a biofuel biologically, requires the deconstruction of the lignocelluloses to fermentable sugars. This process requires pretreatment of the lignocellulose. Certain ionic liquids can be used during the pretreatment step to facilitate the hydrolysis of the lignocellulose. This work assesses the life-cycle greenhouse gases and water requirements for biofuels produced by using ionic liquids as a pretreatment step. Various processes are examined, specifically, the conventional water-wash route and an integrated high gravity (iHG) process. The iHG process is further divided to a current approach which requires regeneration of the ionic liquids used and a projected approach that can eliminate that step saving on electricity requirements.


## Input Data

### Greenhouse Gas Model
- input-output cost data (`io_table_dollars.csv`)
- cost data (`impact_vectors/cost_impact.csv`)
- GHG emission impacts (`impact_vectors/co2_impact.csv`, `impact_vectors/ch4_impact.csv`, `impact_vectors/n2o_impact.csv`)

### Water Model
- input-output cost data (`io_table_dollars.csv`)
- cost data (`impact_vectors_water/cost_impact.csv`)
- Water consumption impacts (`impact_vectors_water/water_consumption.csv`)
- Water withdrawal (`impact_vectors_water/water_withdrawal.csv`)

## Modeling Parameters


## Algorithmic Process



## Outputs



## Webtool

