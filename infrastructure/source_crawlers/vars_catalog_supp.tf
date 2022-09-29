variable "region"{
    default = "eu-west-3"
}

variable "availability_zone" {
    default = "eu-west-3a"
}

variable "db_sources" {
    default = {
        "db1" : {"db_name": "db1", "username": "postgres" ,"password" : "mytestdb", "engine": "postgresql", "host" : "13.36.213.205", "port": "5432" },
        "db3" : {"db_name": "db3", "username": "postgres" ,"password" : "mytestdb", "engine": "postgresql", "host" : "35.180.5.80", "port": "5432" },
       }
}
