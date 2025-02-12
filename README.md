# 🚀 Integration of AWS, NASA's API, and PostgreSQL for data retrieval and analysis 🚀 

This project focuses on the extraction and periodic update of asteroid data from NASA's API. The collected data is stored in a database and later analyzed in a Jupyter Notebook to identify the characteristics and factors that differentiate potentially hazardous asteroids from non-hazardous ones. The following list contains all the integrated services and tools used in this project:

## **AWS Services**  

- **EC2** : Used to create a remote Linux instance in order to generate a zip package containing all required Python libraries for later use.  

- **S3** : The library package generated in EC2 was uploaded to an S3 bucket and later downloaded locally.  

- **RDS** : A PostgreSQL database was deployed to store asteroid data retrieved from NASA’s API.  

- **Lambda** : 
  - The Lambda function: Used to automate the ETL process, periodically fetching asteroid data, formatting it, and loading it into the PostgreSQL database.  
  - Lambda Layer: The function includes a custom layer containing the prepackaged Python libraries generated in EC2 and required for execution.  

## **External API**  
**[NASA API](https://api.nasa.gov/)** : Provides data on Near Earth Objects (NEOs), which is periodically retrieved and processed.  

## **Jupyter Notebook**  

The asteroid data stored in PostgreSQL database is loaded into a Jupyter Notebook. This file contains several graphs along with short explanations and a conclusion about the differences between the potentially hazardous and non-hazardous asteroids. The Jupyter Notebook was created and modified in Google Colab. 

## **Project Architecture**


<p align="center">
  <img src="https://i.postimg.cc/DwWGWb0Z/etl.png" alt="Project Architecture">
</p>
