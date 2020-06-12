# -*- coding: utf-8 -*-
# tente algo como
def index(): return dict(message=auth.user_id)

@auth.requires_login()
def review():
    # Devolve vidios   com estado Visivel       ordenado pela data decrescente
    videos = db(Videos.estado == 'Visivel').select(orderby=~Videos.dtCriacao)

    #Devolve lista das subscrições
    user = db(db.auth_user.id == auth.user_id).select().first()
    subscricao = user.subscricao

    query = 'SELECT * FROM categoria WHERE categoria.id IN('

    for cat in subscricao:
        query = query + str(cat) +', '

    query = query[0:len(query)-2] + ')'
    categorias = db.executesql(query, as_dict=True)


    return dict(categorias=categorias, videos=videos)


@auth.requires_login()
def categoria():
    
    if request.args(0) != 'all':
        categoria  = db(Categoria.titulo == request.args(0)).select() #.first()
        # Devolve vidios   com estado Visivel      da categoria *            ordenado pela data decrescente
        videos = db(Videos.estado == 'Visivel' and Videos.categoria == categoria[0].id).select(orderby=~Videos.dtCriacao)
    else:
        # Devolve vidios   com estado Visivel       ordenado pela data decrescente
        videos = db(Videos.estado == 'Visivel').select(orderby=~Videos.dtCriacao)
    
    
    return dict(categoria=request.args(0),videos=videos)
