database = "db2_source"
tables = [{"location": "def.db2.date", "columns": [{"name": "dateid", "type": "text"}, {"name": "caldate", "type": "text"}, {"name": "day", "type": "text"}, {"name": "week", "type": "text"}, {"name": "month", "type": "text"}, {"name": "qtr", "type": "text"}, {"name": "year", "type": "text"}, {"name": "holiday", "type": "text"}]}, {"location": "def.db2.listing", "columns": [{"name": "listid", "type": "text"}, {"name": "sellerid", "type": "text"}, {"name": "eventid", "type": "text"}, {"name": "dateid", "type": "text"}, {"name": "numtickets", "type": "text"}, {"name": "priceperticket", "type": "text"}, {"name": "totalprice", "type": "text"}, {"name": "listtime", "type": "text"}]}, {"location": "def.db2.sales", "columns": [{"name": "salesid", "type": "text"}, {"name": "listid", "type": "text"}, {"name": "sellerid", "type": "text"}, {"name": "buyerid", "type": "text"}, {"name": "eventid", "type": "text"}, {"name": "dateid", "type": "text"}, {"name": "qtysold", "type": "text"}, {"name": "pricepaid", "type": "text"}, {"name": "commission", "type": "text"}, {"name": "saletime", "type": "text"}]}]