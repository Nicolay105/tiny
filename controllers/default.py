# -*- coding: utf-8 -*-

# from gluon.debug import dbg

def index():
    """

    """
    page = db(db.page.is_index==True).select().first()
    if not page:
        raise HTTP(404, T('sorry, the page you requested does not exist'))
    redirect(URL('pages','show_page',args=page.url))
    

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

def address():
    """
    Allows to access the "address" component
    """
    return dict()

def newsletter():
    """
    Allows to access the "newsletter" component
    """
    form = SQLFORM(db.registered_user, _class='blueText')
    if form.process().accepted:
       response.flash = T('form accepted')
    elif form.errors:
       response.flash = T('form has errors')
    return dict(form=form)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())

def contact_form():
    """
    Contact form
    """
    from gluon.tools import Recaptcha

    public_key = '6LfBX90SAAAAAKZn2zPK5i72PZsnm9Ouj6BC67k7'
    private_key = '6LfBX90SAAAAADRYFTj5xMyZnZoWycdkCBlF_Djb '
    
    form=SQLFORM.factory(
        Field('your_name',requires=IS_NOT_EMPTY(), label=T('Your name')),
        Field('your_email',requires=IS_EMAIL(), label=T('Your email')),
        Field('subject',requires=IS_NOT_EMPTY(), label=T('Subject')),
        Field('message', 'text',requires=IS_NOT_EMPTY(), label=T('Message'))
        )
    #form.element('table').insert(-1,(T('Confirm that you are not a machine'),Recaptcha(request, public_key, private_key),''))
    if form.process().accepted:
        message=T("""
            Name : %s
            Email : %s
            Subject : %s
            Message : %s
        """) % (form.vars.your_name, form.vars.your_email, form.vars.subject, form.vars.message)
        if mail.send(
                    to=WEBSITE_PARAMETERS.contact_form_email,
                    cc=WEBSITE_PARAMETERS.contact_form_cc,
                    bcc=WEBSITE_PARAMETERS.contact_form_bcc,
                    subject=T('Question from %s on %s website') % (form.vars.your_name,WEBSITE_PARAMETERS.website_name),
                    reply_to = form.vars.your_email,
                    message = message):
            response.flash = T('Your message has been sent. Thank you')
            response.js = "jQuery('#%s').hide()" % request.cid
        else:
            form.errors.your_email = T('Unable to send the email')
    return dict(form=form,
                left_sidebar_enabled=True,
                right_sidebar_enabled=True)

# def sitemap():
#     # Import Regex
#     from gluon.myregex import regex_expose
     
#     # Finding You Controllers
#     ctldir = path.join(request.folder,"controllers")
#     ctls=os.listdir(ctldir)
#     # Excluding The appadmin.py and the Manage.py
#     if 'appadmin.py' in ctls: ctls.remove('appadmin.py')
#     if 'manage.py' in ctls: ctls.remove('manage.py')
     
#     # Adding Schemas for the site map
#     xmlns='xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
#     xmlnsImg='xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"\n'
#     xmlnsVid='xmlns:video="http://www.google.com/schemas/sitemap-video/1.1"\n'
#     sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
#     sitemap_xml +='<urlset %s %s %s>\n'%(xmlns,xmlnsImg,xmlnsVid)
     
#     # Add The Pages That You Dont want in the XML Sitemap
#     ExcludedPages = ['Function_Name']
     
#     # Define Your Domain
#     Domain = WEBSITE_PARAMETERS.website_url
     
#     for ctl in ctls:
#         if ctl.endswith(".bak") == False:
#             filename = path.join(ctldir,ctl)
#             data = open(filename, 'r').read()
#             functions = regex_expose.findall(data)
#             ctl = ctl[:-3].replace("_"," ")
             
#             # Adding Statics URLs From Your Controllers
#             for f in functions:
#                 # Ignore the Pages from the list above ( ExcludedPages )
#                 if f not in ExcludedPages:
#                     sitemap_xml += '<url>\n<loc>%s/%s/%s</loc>\n</url>\n' %(Domain,ctl,f.replace("_"," "))
     
#     # Dynamic URLs From Tables For ex ... >> www.domain.com/post/1
#     pages = db().select(db.page.ALL)
#     for page in pages:
#         sitemap_xml += '<url>\n<loc>%s/default/show_page/%s</loc>\n</url>\n' %(Domain,page.url)
#     sitemap_xml +='</urlset>'
#     return sitemap_xml
