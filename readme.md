# Biblioteca-Django

TODO: Adicionar descrição do projeto

## Requisitos

- Python 3.8+
- Django 3.2+

## Instalação

1. Clone o repositório:

   ```sh
   git clone https://github.com/seu-usuario/Biblioteca-Django.git
   cd Biblioteca-Django
   ```

2. Crie um ambiente virtual e ative-o:

   ```sh
    python -m venv .venv
    source .venv/bin/activate # Para Windows, use `venv\Scripts\activate`
    ```

3. Instale as dependências:

   ```sh
   pip install -r requirements.txt
   ```

4. Execute as migrações:

   ```sh
    python manage.py makemigrations
    ```
    ```sh
    python manage.py migrate
    ```

5. Carregue os dados iniciais:

   ```sh
    python manage.py loaddata fixtures/initial_data.json
    ```

6. Crie um superusuário:

   ```sh
    python manage.py createsuperuser
    ```

7. Execute o servidor de desenvolvimento:

   ```sh
    python manage.py runserver
    ```

8. Acesse `http://localhost:8000/`

