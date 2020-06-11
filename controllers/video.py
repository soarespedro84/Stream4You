# -*- coding: utf-8 -*-
# tente algo como
def index(): return dict(message=auth.user_id)

def review():
    # Devolve vidios   com estado Visivel       ordenado pela data decrescente
    videos = db(Videos.estado == 'Visivel').select(orderby=~Videos.dtCriacao)
    
    if auth.user_id != None:
        #Devolve lista das subscrições
        user = db(db.auth_user.id == auth.user_id).select().first()
        subscricao = user.subscricao
        
        query = 'SELECT * FROM categoria WHERE categoria.id IN('

        for cat in subscricao:
            query = query + str(cat) +', '

        query = query[0:len(query)-2] + ')'
        categorias = db.executesql(query, as_dict=True)
    
        categorias.append({'descritivo': 'Mais recentes', 'id': '0', 'titulo': 'Mais recentes'})
    else:
        categorias = {'descritivo': 'Mais recentes', 'id': '0', 'titulo': 'Mais recentes'}

    return dict(categorias=categorias, videos=videos)
