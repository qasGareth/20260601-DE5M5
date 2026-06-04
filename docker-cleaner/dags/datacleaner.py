import pandas as pd

TransactionFilePath = "InputFiles/03_Library Systembook.csv"
CustomerFilePath = "InputFiles/03_Library SystemCustomers.csv"

def fileLoader(TransactionFilePath, CustomerFilePath):
    try:
        Transactions = pd.read_csv(TransactionFilePath)
        Customers = pd.read_csv(CustomerFilePath)
        Error_Transactions =  Transactions.iloc[0:0].copy()
        Error_Customers = Customers.iloc[0:0].copy()
        return Transactions, Customers, Error_Transactions, Error_Customers 
    except Exception as e:
        print("Something went wrong:", e)

   

def naCheckCust(Customers, Error_Customers=None):
    fully_null = Customers[Customers.isnull().all(axis=1)].copy()
    fully_null["Error_Desc"] = "Fully null entry"
    Customers = Customers.drop(fully_null.index)   
    id_null = Customers[Customers["Customer ID"].isnull()].copy()
    id_null["Error_Desc"] = "Null Customer ID"
    Customers = Customers.drop(id_null.index) 
    name_null = Customers[Customers["Customer Name"].isnull()].copy()
    name_null["Error_Desc"] = "Null Customer ID"
    error_slices = [fully_null, id_null, name_null]
    Error_Customers = pd.concat([Error_Customers] + error_slices)
    Customers["Customer Name"] = Customers["Customer Name"].fillna("Name Unknown")
    return  Customers, Error_Customers

def naCheckTran(Transactions, Error_Transactions=None):
    fully_nullT = Transactions[Transactions.isnull().all(axis=1)].copy()
    fully_nullT["Error_Desc"] = "Fully null entry"
    Error_Transactions = pd.concat([Error_Transactions, fully_nullT])
    Transactions = Transactions.drop(fully_nullT.index)
    return Transactions, Error_Transactions

def dateCheckTran(Transactions, Error_Transactions=None):
    Transactions["Book checkout"] = Transactions["Book checkout"].str.strip('"')
    Transactions["Book checkout"] = pd.to_datetime(Transactions["Book checkout"], format="%d/%m/%Y", errors="coerce")
    Transactions["Book Returned"] = pd.to_datetime(Transactions["Book Returned"], format="%d/%m/%Y", errors="coerce")
    invalid_dates = Transactions[Transactions["Book checkout"].isnull()].copy()
    invalid_dates["Error_Desc"] = "Invalid Date"
    Error_Transactions = pd.concat([Error_Transactions, invalid_dates])
    Transactions = Transactions.drop(invalid_dates.index)
    return Transactions, Error_Transactions

def dataEnrich(Transactions):
    Transactions[["Borrow_Value", "Borrow_Interval"]] = Transactions["Days allowed to borrow"].str.split(" ", n=1, expand=True)
    interval_map = {"week": 7, "weeks": 7, "day": 1, "days": 1, "month": 30, "months": 30, "year": 365, "years": 365}
    Transactions["Borrow_Mult"] = Transactions["Borrow_Interval"].str.lower().map(interval_map)
    Transactions["Borrow Limit (Days)"] = Transactions["Borrow_Value"].astype(int) * Transactions["Borrow_Mult"]
    Transactions["Borrow Duration (Days)"] = (Transactions["Book Returned"] - Transactions["Book checkout"]).dt.days
    Transactions = Transactions.drop(columns=["Borrow_Value", "Borrow_Mult", "Borrow_Interval", "Days allowed to borrow"])
    return Transactions

def crossCheck(Customers, Error_Customers, Transactions, Error_Transactions):
    invalid_customers = Transactions[~Transactions["Customer ID"].isin(Customers["Customer ID"])].copy()
    invalid_customers["Error_Desc"] = "Invalid Customer ID"
    Error_Transactions = pd.concat([Error_Transactions, invalid_customers])
    Transactions = Transactions.drop(invalid_customers.index)
    return Transactions, Customers, Error_Transactions, Error_Customers

# def fileSaver(Customers, Error_Customers, Transactions, Error_Transactions):
#     Transactions.to_csv("OutputFiles/Transactions_Clean.csv", index=False)
#     Customers.to_csv("OutputFiles/Customers_Clean.csv", index=False)
#     Error_Transactions.to_csv("OutputFiles/Transaction_Errors.csv", index=False)
#     Error_Customers.to_csv("OutputFiles/Customer_Errors.csv", index=False)

#     with open("OutputFiles/Error_Summary.txt", "w") as f:
#         f.write("Customer Errors:\n")
#         f.write(Error_Customers.groupby("Error_Desc").size().to_string())
#         f.write("\n\nTransaction Errors:\n")
#         f.write(Error_Transactions.groupby("Error_Desc").size().to_string())
#     return print("Output files written to disk successfully")

def addToSQL(Customers, Error_Customers, Transactions, Error_Transactions):
    import os
    conn = (
    f"postgresql+psycopg2://"
    f"{os.environ['LIBRARY_DB_USER']}:{os.environ['LIBRARY_DB_PASSWORD']}"
    f"@{os.environ['LIBRARY_DB_HOST']}:{os.environ.get('LIBRARY_DB_PORT', '5432')}"
    f"/{os.environ['LIBRARY_DB_NAME']}")
    from sqlalchemy import create_engine
    engine = create_engine(conn)
    Transactions.to_sql("Transactions", engine, if_exists="replace", index=False)
    Customers.to_sql("Customers", engine, if_exists="replace", index=False)
    Error_Transactions.to_sql("Error_Transactions", engine, if_exists="replace", index=False)
    Error_Customers.to_sql("Error_Customers", engine, if_exists="replace", index=False)
    cust_summary = Error_Customers.groupby("Error_Desc").size().reset_index(name="Count")
    cust_summary["Category"] = "Customer"
    tran_summary = Error_Transactions.groupby("Error_Desc").size().reset_index(name="Count")
    tran_summary["Category"] = "Transaction"
    Error_Summary = pd.concat([cust_summary, tran_summary], ignore_index=True)
    Error_Summary.to_sql("Error_Summary", engine, if_exists="replace", index=False)
    print("Data written to PostgresDB")

if __name__ == "__main__":
    Transactions, Customers, Error_Transactions, Error_Customers = fileLoader(TransactionFilePath, CustomerFilePath)
    Customers, Error_Customers = naCheckCust(Customers, Error_Customers)
    Transactions, Error_Transactions = naCheckTran(Transactions, Error_Transactions)
    Transactions, Error_Transactions = dateCheckTran(Transactions, Error_Transactions)
    Transactions = dataEnrich(Transactions)
    Transactions, Customers, Error_Transactions, Error_Customers = crossCheck(Customers, Error_Customers, Transactions, Error_Transactions)
    addToSQL(Customers, Error_Customers, Transactions, Error_Transactions)