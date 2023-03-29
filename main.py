from config import Config
from flask import Flask, jsonify
from connector_analytics.analyticsV2 import zohoConnectV2
import pandas as pd
import csv


app = Flask(__name__)

@app.route("/api/get_bitacora")
def get_bitacora():
    try:
        objZoho = zohoConnectV2(srvUrl=Config.SERVERAUTH,
                        tokenToRefresh=Config.REFRESHTOKEN,
                        clientId=Config.CLIENTID,
                        clientSecret=Config.CLIENTSECRET)

        sql_query = 'SELECT%20usuario,ID%20FROM%20bitacora2%20LIMIT%2020'
        data = objZoho.zohoQuery(srvUrl='https://analyticsapi.zoho.com',
                                                        orgid='806718080', 
                                                        workspace='ITSON', 
                                                        table_name='bitacora2',
                                                        email=Config.LOGINEMAILID, 
                                                        sql_query=sql_query)
        columns = data['response']['result']['column_order']
        data = pd.DataFrame(data['response']['result']['rows'])
        list = data.values.tolist()
        data.to_csv('zoho-data.csv', header=columns, index=False)

        return jsonify({'status': True, 'message': 'Success', 'data': { 'columns':  columns, 'rows': list}}), 201
    except :
        return jsonify({'status': False, 'message': 'Error'}), 500

@app.route("/api/process_storage")
def process_storage():
    try:

        csv_data = []
        headers = []
        with open('zoho-data.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            count = 0

            for row in reader:
                if count > 0:
                    row.append(row[0])
                    csv_data.append(row)
                else:
                    headers = row
                    headers.append('new_column')
                count = count+1
       
        data = pd.DataFrame(csv_data)
        data.to_csv('zoho-data.csv', header=headers, index=False)

        return jsonify({'status': True, 'message': 'Success', 'data': csv_data}), 200
    except:
        return jsonify({'status': False, 'message': 'Error'}), 500
    
if __name__ == "__main__":
    app.run(debug=False)

