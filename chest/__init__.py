# -*- coding: utf-8 -*-
__author__ = 'Bruno Konrad'

import sys
import os


class Chest(object):
    """
    Classe mãe para a gerência e o funcionamento do backup.
    """

    def __init__(self, args, storager):
        self._args = args
        self._local = self._args[1]
        self._external_dir = self._args[2]
        self._authorizator = None
        self._storager = storager

    def set_authorizator(self, authorizator):
        self._authorizator = authorizator
        self._storager.set_authorizator(authorizator)

    def start(self):
        """
        Começa o processo de sincronização.
        """
        print("Começando processo...")
        if self._authorizator is not None and not self._authorizator.is_authorized():
            self._authorizator.authorize()

        self._storager.start(self._local, self._external_dir)


class Storager(object):

    def __init__(self):
        self._authorizator = None

    def start(self, local, external):
        raise NotImplementedError()

    def set_authorizator(self, authorizator):
        self._authorizator = authorizator

    def get_token(self):
        if self._authorizator is not None:
            return self._authorizator.get_authorization_token()
        return None


class Authorizator(object):

    _authorize_file = ".authorize"

    def delete_authorization(self):
        """
        Deleta o arquivo de autorização, se o mesmo existir.
        """
        if self.is_authorized():
            os.remove(Authorizator._authorize_file)

    def is_authorized(self):
        """
        Verifica se o usuário autorizou o uso de sua conta para sincronização no Chest.
        :return: True se está autorizado. False senão.
        """
        if os.path.isfile(Authorizator._authorize_file):
            return True
        return False

    def authorize(self):
        """
        Método para começar o processe de autorização do uso da conta no Dropbox para o processo de backup da Chest.
        """
        raise NotImplementedError()

    def get_authorization_token(self):
        """
        Obtém o token de autorização salvo localmente.
        :return: o token em string, se existir. Senão None.
        """
        return None



if __name__ == "__main__":
    if len(sys.argv) == 3:
        chest = Chest(sys.argv)
        chest.start()
    else:
        print("Você precisa dizer o arquivo que deseja salvar e em que pasta no Dropbox.")
