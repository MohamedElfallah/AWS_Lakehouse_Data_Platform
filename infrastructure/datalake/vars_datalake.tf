variable "region" {
    default = "eu-west-3"
}
variable "sources" {
    default = ["db1", "db2", "db3"]
}

variable "dl_zones"{
    default = ["raw", "processed"]
}

variable "glue_jobs" {
    default = [
        "db1_category_2_raw.py", 
        "db1_event_2_raw.py",
        "db1_venue_2_raw.py",
        "db2_listing_2_raw.py",
        "db2_date_2_raw.py",
        "db2_sales_2_raw.py",
        "db3_users_2_raw.py",
        "process_category.py",
        "process_event.py",
        "process_venue.py",
        "process_listing.py",
        "process_sales.py",
        "process_date.py",
        "process_users.py"
    ]
}