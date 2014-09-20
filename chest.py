# -*- coding: utf-8 -*-
__author__ = 'Bruno Konrad'

import sys
from chest import Chest
from chest.chest_dropbox import DropboxAuthorizator, DropboxStorager


if __name__ == "__main__":
    if len(sys.argv) == 3:
        dropboxStorager = DropboxStorager()
        dropboxAuthorizator = DropboxAuthorizator()

        chest = Chest(sys.argv, dropboxStorager)
        chest.set_authorizator(dropboxAuthorizator)
        chest.start()
    else:
        print("Você precisa dizer o arquivo que deseja salvar e em que pasta no Dropbox.")
