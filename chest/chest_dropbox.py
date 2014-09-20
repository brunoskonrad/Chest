# -*- coding: utf-8 -*-
__author__ = 'Bruno Konrad'

from . import Storager
from . import Authorizator
import dropbox


class DropboxStorager(Storager):

    def start(self, local, external):
        client = dropbox.client.DropboxClient(self._authorizator.get_authorization_token())

        upload_file = open(local)
        print ("Começando a sincronizar...")
        try:
            client.put_file("%s" % external, upload_file)
            print ("Sincronizado...")
        except dropbox.rest.ErrorResponse as e:
            print ("Rolou alguma merda...")
            if e.status == 401:
                self._authorizator.delete_authorization()
                self.start()


class DropboxAuthorizator(Authorizator):

    def authorize(self):
        if not self.is_authorized():
            flow = dropbox.client.DropboxOAuth2FlowNoRedirect('cys4uyq1vppz0yv', 'cj43gq1hhatgvgd')
            authorize_url = flow.start()
            print("A url para gerar o token é: %s" % authorize_url)
            token = raw_input("Digite aqui o token, por favor: ")

            access_token, user_id = flow.finish(token)

            a = open(Authorizator._authorize_file, 'w')
            a.write(access_token)

    def get_authorization_token(self):
        if self.is_authorized():
            a = open(Authorizator._authorize_file)
            return a.readline()
        return None