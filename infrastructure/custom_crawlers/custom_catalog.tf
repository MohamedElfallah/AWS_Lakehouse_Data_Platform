provider "aws" {
    region = var.region
}

resource "aws_glue_catalog_database" "catalog_database"{
    name = var.database
}

resource "aws_glue_catalog_table" "catalog_table" {
  count = length(var.tables)
  database_name =  aws_glue_catalog_database.catalog_database.name
  name = var.tables[count.index].location
  storage_descriptor {
    location = "${var.tables[count.index].location}"
    dynamic "columns" {
      for_each = var.tables[count.index].columns 
      content {
        name =columns.value.name
        type = columns.value.type
      }
    }
  }
}