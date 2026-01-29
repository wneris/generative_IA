
### Descrição do PR
Allow SSH access for debugging production issues
### Conteúdo do PR
```text
# terraform/security_groups.tf
resource "aws_security_group_rule" "ssh_access" {
  type              = "ingress"
  from_port         = 22
  to_port           = 22
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]  # ⚠️
  security_group_id = aws_security_group.web.id
}
```