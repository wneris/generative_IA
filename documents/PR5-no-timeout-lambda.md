
### Descrição do PR
Deploy new data processing Lambda function
### Conteúdo do PR
```text
# cloudformation/lambda.yaml
MyFunction:
  Type: AWS::Lambda::Function
  Properties:
    FunctionName: data-processor
    Runtime: python3.11
    Handler: index.handler
    MemorySize: 3008
    # Timeout: não especificado (default: 3s)
    Environment:
      Variables:
        DB_HOST: prod-db.internal

```