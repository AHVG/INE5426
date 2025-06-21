# Compilador


## Configurando ambiente

Para configurar o ambiente faça as seguintes ações:

Primeiro passo é criar um ambiente virtual python

```
python3 -m venv venv
```

Em seguida, faça a instalação das libs com o comando abaixo

```
pip3 install -r requirements.txt
```

## Como executar o compilador

Se você deseja executar o compilador, use algum dos dois comandos a seguir:

Passando o codigo via arquivo

```
python3 main.py --file hello_world.2025
```
ou passando o codigo via comando mesmo:

```
python3 main.py --program "def main() { int x; print x; }"
```

## Como executar os testes

Se você quer rodar os testes, use este comando:

```
pytest
```