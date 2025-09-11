#!/usr/bin/python3
import os
import json
import csv
import time
from cryptography.fernet import Fernet
import mysql.connector

while True:
    try:
        jsonfile = "mylinux.json"
        csvpath = "myfilecsv.csv"

        # Load JSON config
        with open(jsonfile) as f:
            config = json.load(f)

        # Detect OS and run df command
        os_flavour = os.popen(config["os_flavour"]).read().strip()
        if "Ubuntu" in os_flavour or "Zorin" in os_flavour or "Red Hat" in os_flavour or "Debian" in os_flavour:
            os.system(config["df_cmd"])  # df command writes to CSV
            print(f"OS detected: {os_flavour}")
            print("Disk usage data written to myfilecsv.csv")
        else:
            print("Other OS found:", os_flavour)

        # Fetch MySQL credentials
        print("Fetching MySQL credentials from environment...")
        username_mysql = os.getenv("MYSQL_USER")
        password_mysql = os.getenv("MYSQL_PASSWORD")
        host_mysql = os.getenv("MYSQL_HOST")
        db_mysql = os.getenv("MYSQL_DATABASE")

        if not all([username_mysql, password_mysql, host_mysql, db_mysql]):
            raise Exception("Missing one or more required MySQL environment variables")

        # Encrypt/decrypt demo
        message = password_mysql.encode("utf-8")
        key = Fernet.generate_key()
        f = Fernet(key)
        enc = f.encrypt(message)
        dec = f.decrypt(enc)
        passwd_mysql = dec.decode("utf-8")

        # Connect to MySQL
        mydb = mysql.connector.connect(
            host=host_mysql,
            user=username_mysql,
            password=passwd_mysql,
            database=db_mysql,
            port=3306
        )
        mycursor = mydb.cursor()

        # Read CSV and insert into DB
        print("Reading CSV file and inserting into MySQL...")
        with open(csvpath) as csv_file:
            csvfile = csv.reader(csv_file, delimiter=',')
            all_values = []
            for row in csvfile:
                if len(row) < 9:
                    continue
                all_values.append(tuple(row[:9]))

            if all_values:
                query = """
                INSERT INTO my_df_data
                (filesystem, size, used, avail, usage_with_per, mounted_on, datetime, ip_address, hostname)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
                mycursor.executemany(query, all_values)
                mydb.commit()
                print("Data has been imported into DB successfully.")
            else:
                print("No valid data found in CSV to insert.")

        mycursor.close()
        mydb.close()

    except Exception as e:
        print("Something went wrong:", e)

    # Wait before next iteration
    time.sleep(60)  # adjust interval as needed
