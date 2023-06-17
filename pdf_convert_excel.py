#!/usr/bin/env python
# coding: utf-8

# ## pdf格式表格文件提取并合并为一个excel文档

# 修改文件所在路径和保存路径及包存的文件名
# tabula安装：
# pip install tabula-py

# In[ ]:


import os
import pandas as pd
import tabula


# Specify the path to the folder containing the PDF files
pdf_folder_path = "/home/Jupyter/order"

# Set up logging


# Initialize an empty DataFrame to store the merged data
merged_data = pd.DataFrame()

# Iterate over the PDF files in the folder
for filename in os.listdir(pdf_folder_path):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(pdf_folder_path, filename)

        print(f"Processing file: {pdf_path}")

        # Extract tables from the PDF
        tables = tabula.read_pdf(pdf_path, pages='all')

        # Keep only the first page of each table and remove repeated line headers
        cleaned_tables = []
        for table in tables:
            cleaned_table = table.drop_duplicates(keep="first")
            cleaned_tables.append(cleaned_table)

        # Merge the tables into a single DataFrame
        merged_data = pd.concat([merged_data] + cleaned_tables, ignore_index=True)

# Save the merged data to an Excel file
output_path = os.path.join(pdf_folder_path, "/home/Jupyter/merged_data.xlsx")
merged_data.to_excel(output_path, index=False)

print("Conversion complete. Output saved to: " + output_path)

