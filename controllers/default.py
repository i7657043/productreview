# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------

@auth.requires_login()
def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))

    #local variables to show in view
    customMsg = "Hi"
    session.c = session.get('c',0) + 1
    message = 'c = %s' %session.c
    #return the local variables initialised above

    blogForm = SQLFORM(db.blog_post).process()
    productForm = SQLFORM(db.product).process()
    #order posts by most recent
    blogRows = db(db.blog_post).select()
    return locals()
    """
    name = auth.user.first_name
    return dict(name=auth.user.first_name)
@auth.requires_login()
def selected_product():
    
    #Working to show only right posts about right products#
    the_product = db.product(request.args(0))
    previous_posts = db(db.blog_post.prod_ident==request.args(0)).select()
    db.blog_post.prod_ident.default = the_product.id
    db.blog_post.prod_ident.readable = False
    db.blog_post.prod_ident.writable = False
    ##################################################
    
    db.blog_post.post_ident.default = auth.user.id
    db.blog_post.post_ident.readable = False
    db.blog_post.post_ident.writable = False
    blog_post_form = SQLFORM(db.blog_post).process()
    if blog_post_form.accepted:
        session.flash = "Your comment has been posted !"
        redirect(URL('selected_product', args=request.args(0)))


    return locals()

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
@auth.requires_membership('managers')
def post_management():
    if auth.has_membership('managers'):
        grid = SQLFORM.grid(db.blog_post, deletable=True, editable=True, user_signature = False)
    else:
        grid = SQLFORM.grid(db.blog_post, deletable=False, editable=False, user_signature = False)
    return locals()
@auth.requires_membership('managers')
def prod_management():
    if auth.has_membership('managers'):
        grid = SQLFORM.grid(db.product, create=True, deletable=True, editable=True, user_signature = False)
    else:
        grid = SQLFORM.grid(db.product, create=True, deletable=False, editable=False, user_signature = False)
    return locals()
@auth.requires_login()
def show_products():
    if len(request.args)>0:
        productRows = db(db.product.prod_type == request.args(0)).select()
    else:
        productRows = db(db.product).select()

    pass
    return locals()
@auth.requires_login()
def search_products():
    search_form = SQLFORM.factory(
                  Field('name', default=None),
                  submit_button="Search",
                  )

    query = None

    if search_form.process().accepted:
        name = search_form.vars.name

        if name:
            query = db.product.name.contains(name)

    results = db(query).select(orderby=~db.product.id)
    return dict(search_form=search_form, results=results)


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
