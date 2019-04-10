from app import app
import unittest
import base64
from flask import json
from random import randint
import movies_api

class TestCore(unittest.TestCase):
    
    def test_user_list(self):
      tester = app.test_client(self)

      response = tester.get('/users')
      self.assertEqual(response.status_code, 401, 'Acesso não autorizado')

      response = self.login('admin_test', '123456')

      data = json.loads(response.data)

      tester = app.test_client(self)

      response = tester.get(
          '/users',
          headers={'x-access-token': data['token'] })

      self.assertEqual(response.status_code, 200, 'Lista de usuários exibida com sucesso')

    #Test valid and invalid login
    def test_authentication(self):

      response = self.login('admin_test', '123456')
      self.assertEqual(response.status_code, 200)

      response = self.login('admin_test', 'wrongpass')
      self.assertEqual(response.status_code, 401)

    def test_api_return(self):
      response = self.login('admin_test', '123456')

      data = json.loads(response.data)

      tester = app.test_client(self)

      response = tester.get(
          '/movie/Megamente',
          headers={'x-access-token': data['token'] })

      self.assertEqual(response.status_code, 200, 'Lista de filmes retornada com sucesso')

    def test_external_api(self):

      #Check API Search
      response = movies_api.getMovies('Star Wars')
      self.assertTrue(response)

      #Check API Movie Cast endpoint
      response = movies_api.getCast('74849')
      self.assertTrue(response)

      #Check API Genres endpoint
      response = movies_api.getGenre(12)
      self.assertTrue(response)

    #Do login and return the request
    def login(self, user, password):
      tester = app.test_client(self)

      auth_data = bytes(user + ':' + password, encoding='utf8')
      valid_credentials = base64.b64encode(auth_data).decode('utf-8')
      return tester.get(
          '/authenticate',
          headers={'Authorization': 'Basic ' + valid_credentials })

if __name__ == '__main__':
    unittest.main()