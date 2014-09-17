# -*- coding: utf-8 -*-
__author__ = 'Bruno Konrad'

import sys
import os
import dropbox


class Chest(object):
    """
    Classe mãe para a gerência e o funcionamento do backup.
    """

    _authorize_file = ".authorize"

    def __init__(self, args):
        self._args = args
        self._local = self._args[1]
        self._external_dir = self._args[2]

    def _delete_authorization(self):
        """
        Deleta o arquivo de autorização, se o mesmo existir.
        """
        if self._is_authorized():
            os.remove(Chest._authorize_file)

    def _is_authorized(self):
        """
        Verifica se o usuário autorizou o uso de sua conta para sincronização no Chest.
        :return: True se está autorizado. False senão.
        """
        if os.path.isfile(Chest._authorize_file):
            return True
        return False

    def _authorize(self):
        """
        Método para começar o processe de autorização do uso da conta no Dropbox para o processo de backup da Chest.
        """
        if not self._is_authorized():
            flow = dropbox.client.DropboxOAuth2FlowNoRedirect('cys4uyq1vppz0yv', 'cj43gq1hhatgvgd')
            authorize_url = flow.start()
            print("A url para gerar o token é: %s" % authorize_url)
            token = raw_input("Digite aqui o token, por favor: ")

            access_token, user_id = flow.finish(token)

            a = open(Chest._authorize_file, 'w')
            a.write(access_token)

    def _get_authorization_token(self):
        """
        Obtém o token de autorização salvo localmente.
        :return: o token em string, se existir. Senão None.
        """
        if self._is_authorized():
            a = open(Chest._authorize_file)
            return a.readline()
        return None

    def start(self):
        """
        Começa o processo de sincronização.
        """
        print("Começando processo...")
        if not self._is_authorized():
            self._authorize()

        client = dropbox.client.DropboxClient(self._get_authorization_token())

        upload_file = open(self._local)
        print ("Começando a sincronizar...")
        try:
            client.put_file("/%s" % self._external_dir, upload_file)
            print ("Sincronizado...")
        except dropbox.rest.ErrorResponse as e:
            print ("Rolou alguma merda...")
            if e.status == 401:
                self._delete_authorization()
                self.start()


if __name__ == "__main__":
    if len(sys.argv) == 3:
        chest = Chest(sys.argv)
        chest.start()
    else:
        print("Você precisa dizer o arquivo que deseja salvar e em que pasta no Dropbox.")
