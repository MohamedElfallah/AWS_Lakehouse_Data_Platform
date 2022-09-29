provider "aws" {
  region = var.region
}

resource "aws_vpc" "my_vpc"{
  cidr_block = "10.10.0.0/16"
  tags = {
    Name = "my_vpc"
  }
}

resource "aws_subnet" "public_subnet" {
  cidr_block =  "10.10.0.0/24"
  vpc_id = aws_vpc.my_vpc.id
  availability_zone = "eu-west-3a"
  tags = {
    "Name" = "public_subnet"
  }
}

resource "aws_subnet" "private_subnet" {
  vpc_id = aws_vpc.my_vpc.id
  cidr_block = "10.10.1.0/24"
  availability_zone = "eu-west-3a"
  tags = {
    "Name" = "private_subnet"
  }
}

resource "aws_internet_gateway" "net_gw" {
  vpc_id = aws_vpc.my_vpc.id
  tags = {
    "Name" = "Internet GW"
  }
}

resource "aws_route_table" "pub_route_table"{
  vpc_id = aws_vpc.my_vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.net_gw.id
  }
}

resource "aws_route_table_association" "rt_assoc" {
  route_table_id = aws_route_table.pub_route_table.id
  subnet_id = aws_subnet.public_subnet.id
}

resource "aws_eip" "public_ip_nat" {
  vpc = true
  tags = {
    "Name" = "public_ip_for_nat"
  }
}

resource "aws_nat_gateway" "nat_gw" {
    subnet_id = aws_subnet.public_subnet.id
    connectivity_type = "public"
    allocation_id = aws_eip.public_ip_nat.id
    tags = {
      "Name" = "NAT Gateway"
    }
}

resource "aws_route_table" "nat_route_table"{
  vpc_id = aws_vpc.my_vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_nat_gateway.nat_gw.id
  }
}

resource "aws_route_table_association" "nat_association" {
  subnet_id = aws_subnet.private_subnet.id
  route_table_id = aws_route_table.nat_route_table.id
}

resource "aws_security_group" "glue_security_group" {
  for_each= var.db_sources
  description = "glue security group ${each.key}"
  vpc_id = aws_vpc.my_vpc.id
  ingress {
    protocol = "TCP"
    from_port = 0
    to_port = 65535
    self = true
  }
  egress {
    protocol = "TCP"
    from_port = 0
    to_port = 65535
    self = true
  }
  egress {
    description = "${each.value.engine}_(${each.value.port})"
    protocol = "TCP"
    from_port = 5432
    to_port = 5432
    cidr_blocks = ["${each.value.host}/32"]
  }
}

resource "aws_glue_catalog_database" "catalog_db" {
    for_each = var.db_sources
    name = "${each.value.db_name}_source"
}

resource "aws_glue_connection" "glue_con"{
    for_each = var.db_sources    
    connection_properties = {
      JDBC_CONNECTION_URL = "jdbc:${each.value.engine}://${each.value.host}:${each.value.port}/${each.value.db_name}"
      PASSWORD = each.value.password
      USERNAME = each.value.username
    }
    physical_connection_requirements {
      availability_zone = var.availability_zone
      subnet_id = aws_subnet.private_subnet.id
      security_group_id_list = [
        aws_security_group.glue_security_group[each.key].id
      ]
    }
    name = "con_to_${each.value.db_name}"
}

resource "aws_glue_crawler" "crawler" {
  for_each = var.db_sources
  database_name = aws_glue_catalog_database.catalog_db[each.key].name 
  name = "${each.value.db_name}_crawler"
  role = "arn:aws:iam::998361403597:role/glue_datalake_manager"
  jdbc_target {
    connection_name = aws_glue_connection.glue_con[each.key].name
    path = "${each.value.db_name}/%"
  }
}