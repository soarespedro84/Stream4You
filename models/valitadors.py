# -*- coding: utf-8 -*-

#db.auth_user.subscricao.requires = IS_IN_DB(db, 'categoria.id', '%(titulo)s'

## Validadores de Vídio
Videos.titulo.requires = IS_NOT_EMPTY()
Videos.categoria.requires = IS_IN_DB(db, 'categoria.id', '%(titulo)s')
Videos.dtCriacao.requires = IS_DATETIME(format='%d/%m/%Y')
Videos.capa.requires = IS_EMPTY_OR(IS_IMAGE())
