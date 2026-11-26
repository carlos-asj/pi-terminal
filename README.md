# DOCUMENTAÇÃO - ONIPONTO
Sistema desenvolvido em Python com autenticação simples de usuários e registro em uma lista de presença que pode ser conferida em outros momentos.
## LIBs UTILIZADAS
```
import hashlib
import json
import csv
from pathlib import Path
from datetime import date, datetime
```
## ARMAZENAMENTO
A maioria dos dados de uso dentro do sistema foram armazenados utilizando arquivos JSON os quais não possuem complexidade ou relação entre tabelas. Apenas a lista de presença fica salva em .csv pois tende a crescer em um ritmo muito diferente. Registros todos os dias.
## LOGIN
Ao executar o arquivo `main.py` a primeira tela mostra um menu com opção de login e cadastro.
O Login é feito comparando e-mail e senha digitados com os dados armazenados, a partir da função "autenticar()" que vem do arquivo `auth.py`, que valida os usuários salvos e compara as senhas criptografadas.
### HASH das senhas
As senhas dos usuários são gravadas depois de serem encriptadas com um biblioteca de hash do Python (hashlib).
## AUTENTICAÇÃO
A autenticação é feita em um arquivo separado, e a lógica é carregar os usuários gravados em um arquivo JSON (`usuarios.json`) na pasta `/dados` com a função "carregar_usuarios()" utilizando a _lib_ _json_ do Python.<br/>
A função "autenticar()" recebe um e-mail e uma senha e procura no arquivo lido e compara a senha recebida com a senha salva fazendo o hash.
## CADASTRO
**ALUNO**</br>
Caso seja selecionada a opção de cadastro no menu inicial, é solicitado o tipo de cadastro sendo "Motorista" ou "Aluno". Além disso, pede nome completo, e-mail, faculdade, telefone, senha e salva o usuário com perfil de aluno.</br>
Para o e-mail, é feita uma validação simples de string e depois se o e-mail já consta no cadastro com o auxílio da função "carregar_usuario()". E segue para o próximo menu perguntando se o usuário deseja marcar presença, caso seja confirmada, é solicitado o código do ônibus "qr_code_valido.json" na pasta `/dados`. A função "solicitar_qrcode()" compara o código informado com o válido e confirma a presença caso esteja correto. Depois dessas confirmações, a função "registrar_presenca()", que recebe o usuário e a assinatura confirmada, segue com o fluxo de registro na lista de presença.</br>

---
**MOTORISTA**</br>
Quando a opção de motorista for selecionada, é preciso informar o código para cadastro de motoristas (solução encontrada para evitar que qualquer pessoa crie um usuário do tipo motorista), `codigo_motorista.json` que fica na pasta `/dados`.</br>
Depois de cadastrado, o fluxo do motorista segue para a pergunta se o mesmo deseja ver a lista de presença do dia em questão.</br>

---
## PRESENÇA
No arquivo `presenca.py`, fica a função "registrar_presenca()" que cria um arquivo .csv em `/registros` com o nome `lista_presenca.csv` com o usuário, a data e hora do registro e se confirma ou não a presença.</br>
A função "carregar_registros()" é chamada dentro do arquivo `motorista.py` na função "alunos_que_assinaram_hoje()". A qual pega o dia em questão, formata no padrão armazenado, e confere registro por registro guardando apenas os que fazem parte do dia e depois confere se estão com a assinatura confirmada ou não. Devolvendo para o motorista a lista apenas com os alunos que confirmaram presença no dia, constando o nome, a faculdade e a hora em que o registro foi feito, a partir da função "exibir_lista_hoje()" que formata para melhor visualização no terminal.</br>
