"""
bot
"""

import random
import string
import requests


class LikeABot:
    """
    Bot to signup users, create and like posts with data given in config file.
    """
    users_number = int
    posts_per_user = int
    likes_per_user = int
    users = dict
    posts_ids = list

    def __init__(self):
        self.users = {}
        self.posts_ids = []

    def start(self, path_to_config_file):
        """
        Method to start requests to server.
        :param path_to_config_file: string, Path to file with configs.
        :return: None
        """
        self.read_config(path_to_config_file)
        self.create_users()
        self.create_posts()
        self.like_posts()

    def read_config(self, path_to_config_file):
        """
        Read configs file line-by-line and get initial parameters.
        :param path_to_config_file: string with path to file with configs
        :return: None
        """
        with open(path_to_config_file) as configs_file:
            content = configs_file.readlines()

        content = [line.strip().split('=') for line in content]
        self.users_number = int(content[0][1])
        self.posts_per_user = int(content[1][1])
        self.likes_per_user = int(content[2][1])

    def generate_user_credentials(self):
        """
        Generate random username and password.
        :return: tuple (username, password)
        """
        username = ''.join(random.choices(string.ascii_lowercase, k=10))
        password = ''.join(
            random.choices(
                string.ascii_lowercase + string.digits, k=10
            )
        )
        return username, password

    def _make_request(self, method, url, params, headers=None):
        """
        Make request to server API.
        :param url: string, API endpoint
        :param params: dictionary, Custom parameters to use in request body.
        :param headers: dictionary, Optional headers to server
        :return: request object
        """
        r = None

        if method == 'post':
            r = requests.post(url, data=params, headers=headers)
        elif method == 'put':
            r = requests.put(url, data=params, headers=headers)

        response = r.json()
        r.raise_for_status()

        return response

    def create_users(self):
        """
        Method for user creation. Create a number of users equals to
        self.users_number by sending a POST request to project signup API
        endpoint.
        :return: None
        """
        signup_url = 'http://127.0.0.1:8000/api/v1/users/signup'

        for i in range(self.users_number):
            username, password = self.generate_user_credentials()

            signup_response = self._make_request(
                'post',
                signup_url, params={
                    'username': username,
                    'password': password
                }
            )
            user_id = signup_response.get('id')
            token = signup_response.get('token')

            self.users[username] = {
                'id': user_id,
                'password': password,
                'token': token
            }

    def create_posts(self):
        """
        For each user create N number of posts where N = self.posts_per_user
        :return: None
        """
        create_post_url = 'http://127.0.0.1:8000/api/v1/posts/'

        for username, credentials in self.users.items():
            for i in range(self.posts_per_user):
                content = ''.join(
                    random.choices(
                        string.ascii_lowercase + string.ascii_uppercase, k=300
                    )
                )
                user_id = credentials.get('id', None)
                token = credentials.get('token', None)

                create_post_response = self._make_request(
                    'post',
                    create_post_url,
                    params={
                        'content': content,
                        'user': user_id
                    },
                    headers={
                        'Authorization': f'JWT {token}'
                    }
                )
                post_id = create_post_response.get('id', None)
                self.posts_ids.append(post_id)

    def like_posts(self):
        """
        For each user randomly like N posts where N = self.likes_per_user
        :return: None
        """
        for _, credentials in self.users.items():
            token = credentials.get('token', None)

            for i in range(self.likes_per_user):
                post_id = random.choice(self.posts_ids)

                likes_url = (f'http://127.0.0.1:8000/api/v1/'
                             f'posts/like/{post_id}')

                self._make_request(
                    'put',
                    likes_url,
                    params={
                        'action': 'like'
                    },
                    headers={
                        'Authorization': f'JWT {token}'
                    }
                )


if __name__ == '__main__':
    bot = LikeABot()
    bot.start(path_to_config_file='bot-config.txt')

