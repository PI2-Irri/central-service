# Central Service - API de comunicação central - interface

## Objetivo

Microsserviço de comunicação entre a [interface web do Irri](https://github.com/PI2-Irri/webapp) e a central de controle do sistema de módulos e atuadores.

Nesta aplicação persistimos/retornamos os dados do **usuário**, **controladoras**, **módulos**, e as **medidas** tanto dos atuadores quanto dos módulos.

## Como utilizar?

### Ambiente de desenvolvimento

Para subir o ambiente de desenvolvimento, você deve ter o ```docker``` e o ```docker-compose``` instalados.

Após a instalação de ambos, caso seja a primeira vez que o ambiente é usado ou quando realiza alguma alteração no arquivo Dockerfile, execute:

```
sudo docker-compose up --build
```

Caso contrário, após ter feito a build anteriormente, mas sem realizar alterações no Dockerfile, use:

```
sudo docker-compose up
```

Para acessar o container ou do simulador:

```
sudo docker exec -it central-service bash
```

ou de seu banco associado:

```
sudo docker exec -it central-db bash
```

## Endpoints

### Usuários

Disponibiliza a funcionalidade de login e registro do usuário, retornando informações não-confidenciais que identificam que auxiliam na construção do FrontEnd.

#### SignUp

**POST**: http://localhost:4001/signup/

| Parâmetro | Descrição |
|:---------:|:---------:|
| username  | Nome de usuário para identificação e login |
| fullname  | Nome completo do usuário cadastrado |
| email     | Email do usuário cadastrado |
| password  | Senha da conta do usuário |

#### Login

**POST**: http://localhost:4001/login/

| Parâmetro | Descrição |
|:---------:|:---------:|
| username  | Nome de usuário para identificação e login |
| password  | Senha da conta do usuário |

ou

| Parâmetro | Descrição |
|:---------:|:---------:|
| email     | Email do usuário cadastrado |
| password  | Senha da conta do usuário |

### Controladoras

#### Criação de Controladoras

**POST**: http://localhost:4001/controllers/

É necessário colocar o ```token de autenticação``` no ```header``` do ```request```.

| Parâmetro | Descrição |
|:---------:|:---------:|
| name | Nome fictício da controladora |
| token | Identificador único de cada central |
| is_active | Identificador do estado da controladora |

#### Coleta de dados de cada controller

**GET**: http://localhost:4001/controllers/

É necessário colocar o ```token de autenticação``` no ```header``` do ```request```.

| Parâmetro | Descrição |
|:---------:|:---------:|
| token | Identificador único de cada central |

Quando ```200``` : retorna a central desejada

#### Coleta de dados das controladoras de um usuário específico

**GET**: http://localhost:4001/controllers_info/

É necessário colocar o ```token de autenticação``` no ```header``` do ```request```.

Sem parâmetros

Quando ```200``` : retorna a central desejada, juntamente com os dados da zona e da última medida coletada pelo módulo associado a central.

### Módulos

#### Criação dos módulos medidores

**POST**: http://localhost:4001/modules/

É necessário colocar o ```token de autenticação``` no ```header``` do ```request```.

| Parâmetro | Descrição |
|:---------:|:---------:|
| rf_address | Identificador único de cada módulo |
| controller | Controladora responsável pelo módulo |

#### Coleção de todos os módulos medidores de uma controller

**GET**: http://localhost:4001/modules/

É necessário colocar o ```token de autenticação``` no ```header``` do ```request```.

| Parâmetro | Descrição |
|:---------:|:---------:|
| controller | Controladora responsável pelos módulos |

Quando ```200``` : retorna todos os módulos associados à central inserida

#### Coleção de todos os módulos medidores de um usuário

**GET**: http://localhost:4001/modules/

É necessário colocar o ```token de autenticação``` no ```header``` do ```request```.

Sem parâmetros

Quando ```200``` : retorna todos os módulos associados ao usuário

### Zonas

#### Criação de zona

**POST**: http://localhost:4001/zones/

É necessário colocar o ```token de autenticação``` no ```header``` do ```request```.

| Parâmetro | Descrição |
|:---------:|:---------:|
| name | Nome para a zona onde a controladora se localiza |
| zip | Endereço do local onde a controladora se encontra |
| controller | Controladora responsável pela zona |

#### Coleção das zonas associadas à controladora

**GET**: http://localhost:4001/zones/

É necessário colocar o ```token de autenticação``` no ```header``` do ```request```.

| Parâmetro | Descrição |
|:---------:|:---------:|
| controller | Controladora responsável pela zona |

### Medições

#### Medidas dos atuadores

**GET**: http://localhost:4001/actuators_measurements/

É necessário colocar o ```token de autenticação``` no ```header``` do ```request```.

| Parâmetro | Descrição |
|:---------:|:---------:|
| controller | Controladora responsável pelas medidas dos atuadores |

#### Medidas dos módulos medidores

**GET**: http://localhost:4001/modules_measurements/

É necessário colocar o ```token de autenticação``` no ```header``` do ```request```.

| Parâmetro | Descrição |
|:---------:|:---------:|
| module | Módulo responsável pelas medidas dos atuadores |
