###
# Variables for AWS builders
###

locals {
  now = formatdate("YYYYMMDD-hhmmss", timestamp())
}

#Add multiple regions: default     = ["us-east-1","us-east-2"]
variable "aws_ami_regions" {
  description = "List of regions to copy the AMIs to. Tags and attributes are copied along with the AMIs"
  type        = list(string)
  default     = ["us-east-1"]
}

variable "aws_ami_groups" {
  description = "List of groups that have access to launch the resulting AMIs,`all` will make the AMI publicly accessible"
  type        = list(string)
  default     = []
}

variable "aws_ami_users" {
  description = "List of account IDs that have access to launch the resulting AMI"
  type        = list(string)
  default     = []
}

variable "aws_instance_type" {
  description = "EC2 instance type to use while building the AMIs"
  type        = string
  default     = "c7i.8xlarge"
}

variable "aws_region" {
  description = "Name of the AWS region in which to launch the EC2 instance to create the AMIs"
  type        = string
  default     = "us-east-1"
}

variable "aws_ssh_username" {
  description = "Default user name for EC2 instances"
  type        = string
  default     = "ubuntu"
}

variable "aws_source_ami_filter_ubuntu_2204_hvm" {
  description = "Object with source AMI filters for Ubuntu 22.04"
  type = object({
    name   = string
    owners = list(string)
  })
  default = {
    name = "aws-parallelcluster-3.12.0-ubuntu-2204-lts-hvm-x86_64-202412170018 2024-12-17T00-22-52.615Z"
    owners = [
      "247102896272"
    ]
  }
}

variable "aws_temporary_security_group_source_cidrs" {
  description = "List of IPv4 CIDR blocks to be authorized access to the instance"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}


###
# Variables for Azure builders
###


###
# Variables for GCP builders
###



###
# Variables used by all platforms
###

variable "root_volume_size" {
  description = "Size in GB of the root volume"
  type        = number
  default     = 330
}


###
# End of variables blocks
###
# Start of source blocks
###

source "amazon-ebs" "base" {
  ami_name                    = "da-cluster-${local.now}.x86_64-gp3"
  ami_regions                 = var.aws_ami_regions
  ami_users                   = var.aws_ami_users
  ami_groups                  = var.aws_ami_groups
  associate_public_ip_address = true
  communicator                = "ssh"
  ena_support                 = true
  force_deregister            = false
  instance_type               = var.aws_instance_type
  launch_block_device_mappings {
    delete_on_termination = true
    device_name           = "/dev/sda1"
    volume_size           = var.root_volume_size
    volume_type           = "gp3"
    iops                  = 10000
    throughput            = 1000
  }
  max_retries                           = 20
  sriov_support                         = true
  ssh_port                              = 22
  ssh_pty                               = true
  ssh_timeout                           = "60m"
  ssh_username                          = var.aws_ssh_username
  ssh_interface                         = "private_ip"
  subnet_id                             = "subnet-04d911e4b55853ef7"
  tags                                  = { Name = "DA-Cluster-${local.now}" }
  temporary_security_group_source_cidrs = var.aws_temporary_security_group_source_cidrs
}

###
# End of source blocks
###
# Start of build blocks
###

build {
  source "amazon-ebs.base" {
    ami_description = "DA Training Cluster"
    name            = "DA-Cluster-Ubuntu-22.04-hvm"
    source_ami_filter {
      filters = {
        virtualization-type = "hvm"
        name                = var.aws_source_ami_filter_ubuntu_2204_hvm.name
        root-device-type    = "ebs"
      }
      owners      = var.aws_source_ami_filter_ubuntu_2204_hvm.owners
      most_recent = true
    }
  }

  provisioner "shell" {
    execute_command = "{{ .Vars }} sudo -E '{{ .Path }}'"
    script          = "${path.root}/da-cluster-start-script.sh"
    valid_exit_codes = [0,1,2]
  }
}
###
# End of build blocks
###
