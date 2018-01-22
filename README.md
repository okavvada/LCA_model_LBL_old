# Life-cycle Assessment of Cellulosic Biofuel Production

Refer to the [publication](http://pubs.acs.org/doi/abs/10.1021/acssuschemeng.7b02116) for more details on the modeling and life-cycle accounting process.

## Model Dependencies
The core of the LCA-TEA model is written in Python 2.7. The model can be run through docker. Docker will take care of the dependencies and will create an instance of the tool locally on your computer. Please install [Docker](https://docs.docker.com/docker-for-mac/install/) to be able to run the model.


## Start a local instance
The tool can be run through docker. After you have installed the dependencies you can run a local instance of the webtool. Follow these steps:
- Clone this repository
- Navigate your terminal inside the repository
- After you have installed docker, generate a docker image by running `docker build -t flask-sample-one:latest .` in your terminal
- Start your container by running `docker run -d -p 5000:5000 flask-sample-one` in your terminal
- Navigate to `localhost:5000` in Chrome or your favorite browser 
- and Done! Easy!


## Background
Cellulosic biofuels are a promising option to meet a fraction of the liquid transportation fuel demand. They are a promising alternative to gasoline as they are a renewable and low-carbon option. To convert the biomass to a biofuel biologically, requires the deconstruction of the lignocelluloses to fermentable sugars. This process requires pretreatment of the lignocellulose. Certain ionic liquids can be used during the pretreatment step to facilitate the hydrolysis of the lignocellulose. This work assesses the life-cycle greenhouse gases and water requirements for biofuels produced by using ionic liquids as a pretreatment step. Various processes are examined, specifically, the conventional water-wash route and an integrated high gravity (iHG) process. The iHG process is further divided to a current approach which requires regeneration of the ionic liquids used and a projected approach that can eliminate that step saving on electricity requirements.


## Input Data
The model is based on an input-output lifecycle assessment (LCA) methodology similar to the one used in the Economic Input-Output LCA (EIO-LCA) but is based on physical units. The below data are required for the assessment. More data can be added to the files to be included in the analysis if necessary.

- input-output data in physical units (`io_table_physicalunits.csv`)

#### Greenhouse Gas Model
- GHG emission impacts (`impact_vectors/co2_impact.csv`, `impact_vectors/ch4_impact.csv`, `impact_vectors/n2o_impact.csv`)

#### Water Model
- Water consumption impacts (`impact_vectors_water/water_consumption.csv`)
- Water withdrawal impacts (`impact_vectors_water/water_withdrawal.csv`)

## Modeling Parameters
The tool allows the user to customize some of the modeling parameters to assess specific biorefinery impacts. The user defined model parameters are described in the user interface and grouped by each pre-processing method. Default values can be assigned to the parameters based on previous work [published](http://pubs.acs.org/doi/abs/10.1021/acssuschemeng.7b02116).

#### Intelligen Inc, SuperPro Designer
The tool is compatible with the Intelligen Inc, SuperPro Designer tool. To use the output of the SuperPro tool to set your parameter values please follow the instructions to generate the compatible file before running the `Use SuperPro Values` command. If the compatibility file is not generated an error will appear on the screen. 

Steps:
- Copy a SuperPro output file in the form of `.xls` into the `input_data` folder. 
- Open your terminal and navigate inside the repository
- In your terminal run `python RUN_SuperPro.py --path=input_data/CornStover-to-EtOH-waterwash.xls --feedstock=corn_stover --preprocess=waterwash`
This will generate a compatibility file for a SuperPro run with `corn stover` as the feedstock and `waterwash` the pre-proceesing step. If you are running for a different feedstock, pre-processing method or fuel please substitute appropriately. 

The valid options for the arguments are:
- feedstock: `corn_stover`, `sorgum`
- pre-processing method: `waterwash`, `iHG-Current`, `iHG-Projected`


## Outputs
The output is a graph of the lifecycle GHG impacts for the `GHG model` and water consumption or water withdrawals for the `Water Consumption` or `Water Withdrawal` models respectively. The impacts are grouped by each of the potential pre-processing methods and a breakdown of each of the components contribution can be identified. The resulting figure is interactive and can be downloaded to your local computer.

