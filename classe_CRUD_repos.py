import requests
import base64
from math import ceil
import pandas as pd

class ManipulaRepositorios:

    def __init__(self,username):
        self.username = username
        self.api_base_url = 'https://api.github.com'
        self.access_token = 'meu_token'
        self.headers = {'Authorization':'Bearer '+self.access_token,
                        'X-GitHub-Api-Version': '2022-11-28'}
        
    def create(self,nome_repo,*args):
        url_create = f'{self.api_base_url}/user/repos'
        
        if len(args) == 0:
            data = {
                'name': nome_repo,
                'description': 'Dados de repositórios de algumas empresas',
                'private': False
            }
        elif len(args) == 1:
            data = {
                'name': nome_repo,
                'description': args[0],
                'private': False
            }
        else:
            raise ValueError(f"Número de argumentos inválido. Esperado 1 ou 2 argumentos.")

        response = requests.post(url_create, json=data, headers=self.headers)

        return response

    
    def fork(self, forked_user, nome_repo):
        url_fork = f'{self.api_base_url}/repos/{forked_user}/{nome_repo}/forks'

        response = requests.post(url_fork, headers=self.headers)

        return response

    def get(self,nome_repo):
        url_get = f'{self.api_base_url}/repos/{self.username}/{nome_repo}'

        response = requests.get(url_get)

        return response


    def update(self, nome_repo, nome_arquivo, path_arquivo, *args):
        url_set = f'{self.api_base_url}/repos/{self.username}/{nome_repo}/contents/{nome_arquivo}'
        
        with open (path_arquivo, 'rb') as file:
            file_content = file.read()
        
        encoded_content = base64.b64encode(file_content)

        if len(args) == 0:
            data = {
                'message': 'Teste do método update',
                'content': encoded_content.decode('utf-8')
            }
        elif len(args) == 1:
            data = {
                'message': args[0],
                'content': encoded_content.decode('utf-8')
            }
        else:
            raise ValueError(f"Número de argumentos inválido. Esperado 3 ou 4 argumentos.")


        response = requests.put(url_set, json = data, headers=self.headers)

        return response


    def delete(self, nome_repo):
        url_delete = f'{self.api_base_url}/repos/{self.username}/{nome_repo}'

        response = requests.delete(url_delete, headers=self.headers)

        return response


    def lista_repositorios(self):
        repos_list = []
        pages_request = requests.get(f'{self.api_base_url}/users/{self.username}')
        num_pages = ceil(pages_request.json()['public_repos']/30)
        for page_num in range(1,num_pages+1):
            try:
                url_page = f'{self.api_base_url}/users/{self.username}/repos?page={page_num}'
                r = requests.get(url_page, headers=self.headers)
                if len(r.json()):
                    repos_list.append(r.json())
                else:
                    break
            except:
                print('Exception')
                repos_list.append(None)
        return repos_list
    
    def nomes_repos(self):
        repos_name = []
        repos_list = self.lista_repositorios()
        for page in repos_list:
            for repo in page:
                try: 
                    repos_name.append(repo['name'])
                except:
                    pass

        return repos_name
    
    def nomes_linguagens(self):
        repos_language = []
        repos_list = self.lista_repositorios()
        for page in repos_list:
            for repo in page:
                try:
                    repos_language.append(repo['language'])
                except:
                    pass
        return repos_language
    
    def cria_df_linguagens(self):
        dados = pd.DataFrame()
        dados['repository_name'] = self.nomes_repos()
        dados['language'] = self.nomes_linguagens()

        return dados

manipula_repo = ManipulaRepositorios('NycolleNailde')

# c_test = manipula_repo.create('teste-CRUD','Repositório para testar métodos de CRUD de uma classe criada por mim em Python com a biblioteca requests.')
# c_test = manipula_repo.create('teste2-CRUD')
# print(c_test.status_code)

# r_test = manipula_repo.get('teste2-CRUD')
# print(r_test.json()['name'])

# u_test = manipula_repo.update('teste2-CRUD','dados/netflix_git_languages.csv','dados/liguagens_netflix.csv','Teste do método update.')
# print(u_test.status_code)

# d_test = manipula_repo.delete('teste-CRUD')
# print(d_test.status_code)

# f_test = manipula_repo.fork('leonppontes','analytics-handbook')
# print(f_test.status_code)