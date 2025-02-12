# 🚀 Automated data pipeline for asteroid analysis 🚀 

This project automates the retrieval, storage, and analysis of asteroid data using NASA's API. The main goal is to refresh the database periodically, store and refresh the data, and later analyze it in a Jupyter Notebook.  

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

The asteroid data stored PostgreSQL database is loaded into a Jupyter Notebook. This file contains several graphs along with short explanations.  

## **Project Architecture**

![Project Architecture](https://i.postimg.cc/DwWGWb0Z/etl.png)



