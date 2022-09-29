variable "region" {
    default = "eu-west-3"
}

variable "database" {
    default = "db2_source"
}

variable "tables" {
    default =[{"location": "db1.public.category", "columns": [{"name": "catid", "type": "text"}, {"name": "catgroup", "type": "text"}, {"name": "catname", "type": "text"}, {"name": "catdesc", "type": "text"}]}, {"location": "db1.public.venue", "columns": [{"name": "venueid", "type": "text"}, {"name": "venuename", "type": "text"}, {"name": "venuecity", "type": "text"}, {"name": "venuestate", "type": "text"}, {"name": "venueseats", "type": "text"}]}, {"location": "db1.public.event", "columns": [{"name": "eventid", "type": "text"}, {"name": "venueid", "type": "text"}, {"name": "catid", "type": "text"}, {"name": "dateid", "type": "text"}, {"name": "eventname", "type": "text"}, {"name": "starttime", "type": "text"}]}]
}