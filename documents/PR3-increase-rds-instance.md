
### Descrição do PR
Scale up database for Black Friday traffic
### Conteúdo do PR
```text
# terraform/database.tf
resource "aws_rds_instance" "main" {
  identifier        = "myapp-db"
  instance_class    = "db.r6g.8xlarge"  # antes: db.t3.medium
  allocated_storage = 1000                # antes: 100
  engine            = "postgres"
  engine_version    = "14.7"
}
```