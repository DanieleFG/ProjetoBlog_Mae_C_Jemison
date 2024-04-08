O projeto final deste Bootcamp de Back-End visa consolidar e aplicar o
conhecimento adquirido em GitHub, HTML5, CSS3, Bancos de Dados e o Framework
Django. Vamos transformar essa jornada de aprendizado em um prático e
envolvente Sistema de Blog com Django.


# Projeto Final 
## Portal de Noticias Mae C Jemison

### Instalação do ambiente virtual

 ```
 pip install virtualenv

 ```

### Criar ambiente Virtual

```
python3 -m venv .venv

```

### Ativar ambiente 
```
source .venv/bin/activate

```
### Instalar Django

```
pip install django

```

### Criar Projeto

```
django-admin startproject projeto_blog .

```

### Rodar o projeto
```
python3 manage.py runserver

```
### Comando aplicativo
```
python3 manage.py startapp base

```


### Comando instalar bootstrap

``` 
pip install django-bootstrap-v5

```

### Comandos para criar arquivo do Banco de Dados

 ```
    python3 manage.py makemigrations
 ```

### Comandos para enviar para  Banco de Dados

 ```
    python3 manage.py migrate
 ```

 ### Comandos para ecriar super usuario

 ```
    python3 manage.py createsuperuser
 ```

usuario: admin
senha: admin
email: admin@gmail.com
video explicando upload imagens
https://www.youtube.com/watch?v=uoiiwyemmvw