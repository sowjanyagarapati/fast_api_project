# fast_api_project

## How to run?

**Install the requirements:**

>pip install -r requirements.txt

---
### Go to the Project Directory and Run the below command:

>uvicorn main:app

## Description:

## APIs:

**/upload_file/**: Takes the csv file as an input, loads into database and returns the success response.


**/records/**: Returns the number of records in the table.


**/banks/**: Returns the number of unique banks present in the table.


**/{from_date}/{to_date}**: Takes two parameters `date_from` and `date_to`.


  > `date_from` and `date_to` should be entered in `YYYY-mm-dd` format.
  
  
**/customer_names/**: Returns the customer names in the table.


**/transaction_summary/**: Returns number of transactions based on transaction type.


**/transaction_amount_summary/**: Returns total amount of transactions based on transaction type.


**/total_transaction_amount/**: Returns total transaction amount.
