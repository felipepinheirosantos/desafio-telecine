# Movie List API

API to display a list of movies, including their respective casts.

  - Python3
  - Flask
 

# Instalation
Clone repository
  ```sh
$ git clone https://github.com/felipepinheirosantos/desafio-telecine.git
```
Create the enviroment
  ```sh
$ cd desafio-telecine
$ python3 -m venv venv
```
Activate the enviroment
  ```sh
$ . venv/bin/activate
```
Install Flask
  ```sh
$ pip install Flask
```
Install requirements
  ```sh
$ pip install -r requirements.txt
```

# Execute

Run
  ```sh
$ flask run
```

# Authentication

Test User
    - Login: **admin_test**
    - Password: 123456

The system uses basic authorization by sending the encrypted base64 login and password. After authorization, the user receives a access-token.

# Using the token
After receiving the token, the user needs to send the token in request header using the key **x-access-token**.
Example:
  ```sh
headers={'x-access-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiJmMGZiMGExMC0yYWM1LTRkMTctOGExNC04YmNiODcwNTg1NWQiLCJleHAiOjE1NTQ4ODUzNDB9.wmhHihz911R2q-z7RN24NPbvd1J82h8q3rIfgeYtvHc' })
```

# Creating new users
Send a POST request with name and password to following endpoint:
  ```sh
/user/create
```

# Listing users (token_required)
Send a request to following endpoint:
  ```sh
/users
```

# Searching movies (token_required)
Send a request to following endpoint:
  ```sh
/movie/<name>
```
Example:
  ```sh
/movie/Megamente
```
Response:
  ```sh
{
    "movies": [
        {
            "item": {
                "brazilian_title": "Megamente",
                "cast": [
                    {
                        "name": "Will Ferrell",
                        "role": "Megamind (voice)"
                    },
                    {
                        "name": "Brad Pitt",
                        "role": "Metro Man (voice)"
                    },
                    {
                        "name": "Tina Fey",
                        "role": "Roxanne Ritchi (voice)"
                    },
                    {
                        "name": "Jonah Hill",
                        "role": "Hal Stewart / Tighten (voice)"
                    },
                    {
                        "name": "David Cross",
                        "role": "Minion (voice)"
                    },
                    {
                        "name": "Ben Stiller",
                        "role": "Bernard (voice)"
                    },
                    {
                        "name": "Justin Theroux",
                        "role": "Megaminds's Father (voice)"
                    },
                    {
                        "name": "Jessica Schulte",
                        "role": "Megamind's Mother (voice)"
                    },
                    {
                        "name": "Tom McGrath",
                        "role": "Lord Scott / Prison Guard (voice)"
                    },
                    {
                        "name": "Emily Nordwind",
                        "role": "Lady Scott (voice)"
                    },
                    {
                        "name": "J.K. Simmons",
                        "role": "Warden (voice)"
                    },
                    {
                        "name": "Ella Olivia Stiller",
                        "role": "Schoolchild (voice)"
                    },
                    {
                        "name": "Quinn Dempsey Stiller",
                        "role": "Schoolchild (voice)"
                    },
                    {
                        "name": "Brian Hopkins",
                        "role": "Prisoner (voice)"
                    },
                    {
                        "name": "Christopher Knights",
                        "role": "Prison Guard (voice)"
                    },
                    {
                        "name": "Mike Mitchell",
                        "role": "Father in Crowd (voice)"
                    },
                    {
                        "name": "Jasper Johannes Andrews",
                        "role": "Crying Baby (voice)"
                    },
                    {
                        "name": "Justin Long",
                        "role": "Minions (voice)"
                    },
                    {
                        "name": "Bill Hader",
                        "role": "Bob Prickles (voice)"
                    },
                    {
                        "name": "Amy Poehler",
                        "role": "Linda Prickles (voice)"
                    },
                    {
                        "name": "Rob Corddry",
                        "role": "Random Citizen (voice)"
                    },
                    {
                        "name": "Jack Blessing",
                        "role": "Newscaster (voice)"
                    },
                    {
                        "name": "Stephen Kearin",
                        "role": "Mayor (voice)"
                    }
                ],
                "genres": "Animação, Ação, Comédia, Família, Ficção científica",
                "release_date": 2010,
                "title": "Megamind"
            }
        },
        {
            "item": {
                "brazilian_title": "Megamind: The Button of Doom",
                "cast": [
                    {
                        "name": "Will Ferrell",
                        "role": "Megamind"
                    },
                    {
                        "name": "David Cross",
                        "role": "Minion"
                    }
                ],
                "genres": "Animação, Ação, Comédia, Família",
                "release_date": 2011,
                "title": "Megamind: The Button of Doom"
            }
        }
    ]
}
```

# Runing tests
  ```sh
$ python test.py
```
** Desenvolvido por Felipe Pinheiro Santos **
