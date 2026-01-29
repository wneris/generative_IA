
### Descrição do PR
Add cost tracking tags to EC2 instances
### Conteúdo do PR
```text
# terraform/ec2.tf
resource "aws_instance" "worker" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"

  tags = {
    Name       = "worker-01"
    CostCenter = "engineering"  # ✅ novo
    Owner      = "platform-team"
  }
}
```