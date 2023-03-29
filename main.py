from config import Config
from connector_analytics.analyticsV2 import zohoConnectV2

objZoho = zohoConnectV2(srvUrl=Config.SERVERAUTH,
					tokenToRefresh=Config.REFRESHTOKEN,
					clientId=Config.CLIENTID,
					clientSecret=Config.CLIENTSECRET)

sql_query = 'SELECT%20ID%20FROM%20bitacora'
data = objZoho.zohoQuery(srvUrl='https://analyticsapi.zoho.com',
                                                orgid='806718080', 
                                                workspace='ITSON', 
                                                table_name='bitacora',
                                                email=Config.LOGINEMAILID, 
                                                sql_query=sql_query)
print(data)

