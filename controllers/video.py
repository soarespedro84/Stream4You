# -*- coding: utf-8 -*-
# tente algo como
def index(): return dict(message=auth.user_id)


#----PAGIAN REVIEW----
@auth.requires_login()
def review():
    # Devolve vidios   com estado Visivel       ordenado pela data decrescente
    videos = db(Videos.estado == 'Visivel').select(orderby=~Videos.dtCriacao)

    #Devolve lista das subscrições
    user = db(db.auth_user.id == auth.user_id).select().first()
    subscricao = user.subscricao

    query = 'SELECT * FROM categoria WHERE categoria.id IN(0, '

    for cat in subscricao:
        query = query + str(cat) +', '

    query = query[0:len(query)-2] + ')'
    categorias = db.executesql(query, as_dict=True)
    
    #Devolver produtores
    produtor = db(db.auth_user).select()

    return dict(categorias=categorias, videos=videos, produtor=produtor)


#----PAGIAN CATEGORIAS----
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

#----PAGIAN PRODUTOR----
@auth.requires_login()
def produtor():
    
    #Devolver produtores
    produtores = db(db.auth_user.id == request.args(0)).select()
    produtor = produtores[0]
    
    #Devolve videos do produtor
    sugestoes = db(Videos.estado == 'Visivel' and Videos.autor == produtor.id).select(orderby=~Videos.dtCriacao)
    
    
    return dict(produtor=produtor,sugestoes=sugestoes)

#----PAGIAN PESQUISA----
@auth.requires_login()
def pesquisa():

    if request.vars._pesquisa:
        videos = db(Videos.titulo.like('%'+request.vars._pesquisa+'%')).select()
    else:
        videos = db(Videos).select()
    return dict(videos=videos)


#----PAGIAN VER VIDEO----
@auth.requires_login()
def ver():
    #Devolver viedo a ver
    videos = db(Videos.id == request.args(0)).select()
    video = videos[0]
    
    #Devolver produtores
    produtores = db(db.auth_user.id == video.autor).select()
    produtor = produtores[0]
    
    #Devolve videos do produtor
    sugestoes = db(Videos.estado == 'Visivel' and Videos.autor == produtor.id).select(orderby=~Videos.dtCriacao)
    
    #Acrescentar 1 visualização
    db(Videos.id == video.id).update(visualizacoes = video.visualizacoes + 1)
    
    return dict(video=video, produtor=produtor, sugestoes=sugestoes)

# SREAM low resolution
@auth.requires_login()
def streamerLow():
    videos = db(Videos.id == request.args(0)).select()
    video = videos[0].anexo
    import os
    path=os.path.join(request.folder,'uploads', video)
    response.headers['ContentType']="video/mp4"


    return response.stream(open(path,'rb'), chunk_size=4096)

# SREAM High resolution
@auth.requires_login()
def streamerHigh ():
    videos = db(Videos.id == request.args(0)).select()
    video = videos[0].anexo2
    import os
    path=os.path.join(request.folder,'uploads', video)
    response.headers['ContentType']="video/mp4"


    return response.stream(open(path,'rb'), chunk_size=4096)
