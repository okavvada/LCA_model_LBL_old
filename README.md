# Life-cycle Assessment of Cellulosic Biofuel Production

Refer to the [publication](http://pubs.acs.org/doi/abs/10.1021/acssuschemeng.7b02116) for more details on the modeling and life-cycle accounting process.

## Model Dependencies
The core of the LCA-TEA model is written in Python 2.7. The model can be run through docker. Docker will take care of the dependencies and will create an instance of the tool locally on your computer. Please install docker to be able to run the model.

[Docker](https://docs.docker.com/docker-for-mac/install/)

Below are the dependencies for the core model. You do not need to install them separately as they are installed for you through docker.
- [Python](https://www.python.org/download/releases/2.7/)
- [Numpy](https://docs.scipy.org/doc/numpy-1.10.1/user/install.html)
- [Pandas](http://pandas.pydata.org/pandas-docs/stable/install.html)
- [Flask](http://flask.pocoo.org/docs/0.12/installation/)
- [xlrd](https://pypi.python.org/pypi/xlrd)
- [unitconvert](https://pypi.python.org/pypi/unitconvert/1.0.3)

## Start a local instance
The tool can be run through docker. After you have installed the dependencies you can run a local instance of the webtool. Follow these steps:
- Clone the repo
- Navigate your command prompt inside the repo
- After you have installed docker, run `docker build -t flask-sample-one:latest .` and `docker run -d -p 5000:5000 flask-sample-one` in your command prompt
- # Start the server by running `FLASK_DEBUG=1 FLASK_APP=server.py flask run`
- Navigate to `localhost:5000`
- and Done! Easy!


## Background
Cellulosic biofuels are a promising option to meet a fraction of the liquid transportation fuel demand. They are a promising alternative to gasoline as they are a renewable and low-carbon option. To convert the biomass to a biofuel biologically, requires the deconstruction of the lignocelluloses to fermentable sugars. This process requires pretreatment of the lignocellulose. Certain ionic liquids can be used during the pretreatment step to facilitate the hydrolysis of the lignocellulose. This work assesses the life-cycle greenhouse gases and water requirements for biofuels produced by using ionic liquids as a pretreatment step. Various processes are examined, specifically, the conventional water-wash route and an integrated high gravity (iHG) process. The iHG process is further divided to a current approach which requires regeneration of the ionic liquids used and a projected approach that can eliminate that step saving on electricity requirements.


## Input Data
#### Greenhouse Gas Model
- input-output data in physical units (`io_table_physicalunits.csv`)
- GHG emission impacts (`impact_vectors/co2_impact.csv`, `impact_vectors/ch4_impact.csv`, `impact_vectors/n2o_impact.csv`)

#### Water Model
- input-output data in physical units (`io_table_physicalunits_water.csv`)
- Water consumption impacts (`impact_vectors_water/water_consumption.csv`)
- Water withdrawal impacts (`impact_vectors_water/water_withdrawal.csv`)

####SuperPro
The tool is compatible with outputs from the Intelligen Inc, SuperPro Designer tool. To use the output of the SuperPro tool to set your parameter values please follow the instructions to generate the compatible file before running the `Use SuperPro Values` command. If the compatibility file is not generated an error will appear on the screen. 

Steps:
- Copy a SuperPro output file in the form of `.xls` into the `input_data` folder. 
- Open your command promp and navigate inside the repository
- Run `python RUN_SuperPro.py 'input_data/your_SuperPro_filename.xls' 'corn_stover' 'waterwash'`
This will generate a compatibility file for a SuperPro run with `corn stover` as the feedstock and `waterwash` the pre proceesing step. If you are running for a different feedstock, pre processing method or fuel please substitute appropriately. The valid options are:
feedstock: `corn_stover`, `sorgum`
pre processing method: `waterwash`, `iHG-Current`, `iHG-Projected`

## Modeling Parameters


## Algorithmic Process



## Outputs



## Webtool

