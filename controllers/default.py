# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- example index page ----


def index():
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))

# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET':
        raise HTTP(403)
    return response.json({'status': 'success', 'email': auth.user.email})

# ---- Smart Grid (example) -----
# can only be accessed by members of admin groupd
@auth.requires_membership('produtor')
def grid():
    response.view = 'generic.html'  # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables:
        raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[
                             tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----


def wiki():
    auth.wikimenu()  # add the wiki to the menu
    return auth.wiki()

# ---- Action for login/register/etc (required for auth) -----


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

# -------Novo Video--------
@auth.requires_membership('produtor')
def novo_video():
    form = SQLFORM(Videos)
    if form.process().accepted:
        session.flash = ' Novo Video registado: %s ' % form.vars.titulo
        redirect(URL('listar_video'))
    elif form.errors:
        response.flash = 'Erros no Formulário!'
    else:
        response.flash = 'Preencha o Formulário!'
    return dict(form=form)

# -------listar Video--------


def listar_video():
    grid = SQLFORM.grid(Videos)
    return dict(grid=grid)

# -------Editar Video--------


def editar_video():
    form = SQLFORM(Videos, request.args(0, cast=int),
                   showid=False, submit_button='Gravar',
                   readonly=False, deletable=True)
    if form.process().accepted:
        session.flash = 'Video atualizado: %s' % form.vars.titulo
        redirect(URL('listar_video'))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário!'
    return dict(form=form)

# -------Apagar Video--------


def apagar_video():
    record = db.Videos(request.args(0, cast=int))
    db(Videos.id == request.args(0, cast=int)).delete()
    session.flash = 'Video %s apagado!' % record.titulo
    redirect(URL('listar_video'))
