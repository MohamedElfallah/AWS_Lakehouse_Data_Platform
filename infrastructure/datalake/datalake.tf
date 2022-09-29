provider "aws" {
    region = var.region
}

resource "aws_s3_bucket" "datalake" {
    for_each= toset(var.dl_zones)
    bucket = "mylake-${each.key}-zone"
    force_destroy = true 
}

resource "aws_s3_bucket_public_access_block" "block_public_access" {
    for_each = toset(var.dl_zones)
    bucket = aws_s3_bucket.datalake[each.key].id 
    block_public_policy = true
    block_public_acls = true
}

resource "aws_glue_catalog_database" "glue_catalog" {
    for_each = toset(flatten([for i in var.dl_zones : [for j in var.sources : "${i}-${j}"]]))
    name = each.key
}

resource "aws_glue_crawler" "crawlers" {
    for_each = toset(flatten([for i in var.dl_zones : [for j in var.sources : "${i}-${j}"]]))
    name = "${each.key}-crawler"
    database_name = aws_glue_catalog_database.glue_catalog[each.key].name 
    role = "arn:aws:iam::998361403597:role/glue_datalake_manager"
    s3_target {
      path = "s3://mylake-${split("-", "${each.key}")[0]}-zone/${split("-", "${each.key}")[1]}"
    }
}

resource "aws_glue_job" "glue_job" {
    count = length(var.glue_jobs)
    name = var.glue_jobs[count.index]
    role_arn = "arn:aws:iam::998361403597:role/glue_datalake_manager"
    max_retries = 0
    glue_version = "3.0"
    command {
      script_location = "s3://etl-glue-jobs/glue_etl/${var.glue_jobs[count.index]}"
      python_version = 3
    }
}