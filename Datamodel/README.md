# Sales Data Model – Star Schema

This document describes the data model designed for the Sales Analytics project.  
The model is built using a Star Schema to provide high performance, simplicity, and scalability for Power BI reporting.

---

## 1. Overview

The data model supports analytical use cases such as product performance, customer insights, market analysis, shipping analysis, and time-based reporting.

The structure includes:

- One fact table: fact_sales
- Seven dimension tables: dimProduct, dimDate, dimShipMode, dimOrderPriority, dimLocation, dimCustomer, dimMarket

---

## 2. Table Structure

### Fact Table: fact_sales  
This table contains all sales transactions and includes:

- Foreign keys referencing each dimension table  
- Numeric fields such as profit , quantity, shipping cost  
- Additional measures used for reporting and analysis  

### Dimension Tables  
Each dimension table contains a generated surrogate key (ID).  
These keys act as the primary key in each dimension and as foreign keys inside the fact table.

- dimProduct: product information  
- dimDate: full date attributes (day, month, year, quarter, etc.)  
- dimShipMode: shipping method information  
- dimOrderPriority: order priority categories  
- dimLocation: country, region, state , and city information  
- dimCustomer: customer profile and classification  
- dimMarket: market segments and business areas  

---

## 3. Data Cleaning and Preparation

Before building the data model, all tables were cleaned and prepared:

- Duplicate records were removed  
- Surrogate keys were generated for all dimension tables  
- Null values were handled and standardized  
- Column names were unified and normalized  
- Data granularity was validated across tables  
- Consistency checks were applied to ensure data quality  

---

## 4. Relationships

All dimension tables have a one-to-many relationship with the fact table.  
The direction is from the dimension table (one) to the fact table (many).

The dimDate table contains an inactive relationship with fact_sales through the ShipDate field. This relationship can be activated within DAX when needed.

---

## 5. Use Cases

This model enables analysis of:

- Sales performance over time  
- Product-level trends  
- Customer behavior and segmentation  
- Market and regional performance  
- Shipping method effectiveness  
- Order priority distribution  

It provides a structured, optimized foundation for building dashboards and reports in Power BI.

---