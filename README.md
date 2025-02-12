# 🚀 Automated data pipeline for asteroid analysis 🚀 

This project focuses on the extraction and periodic update of asteroid data from NASA's API. The collected data is stored in a database and later analyzed in a Jupyter Notebook to identify the characteristics and factors that differentiate potentially hazardous asteroids from non-hazardous ones.

## **AWS Services**  

- **EC2** : Used to create a remote Linux instance and to generate a zip package containing all required Python libraries for later use.  

- **S3** : The library package generated in EC2 was uploaded to an S3 bucket and later downloaded locally.  

- **RDS (Relational Database Service)** : A PostgreSQL database was deployed to store asteroid data retrieved from NASA’s API.  

- **Lambda** : 
  - The Lambda function: Used to automate the ETL process, periodically fetching asteroid data, formatting it, and loading it into the PostgreSQL database.  
  - Lambda Layer: The function includes a custom layer containing the prepackaged Python libraries generated in EC2 and required for execution.  

## **External API**  
**[NASA API](https://api.nasa.gov/)** : Provides data on Near-Earth Objects (NEOs), which is periodically retrieved and processed.  

## **Jupyter Notebook for Data Analysis**  

The asteroid data stored PostgreSQL database is loaded into a Jupyter Notebook. This file contains several graphs along with short explanations and a conclusion.  

## **Project Architecture**

![Project Architecture](https://i.postimg.cc/DwWGWb0Z/etl.png)



