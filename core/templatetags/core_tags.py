from django import template
import datetime

# Instance de la bibliothèque de templates
register = template.Library() #template.Library() pour enregistrer vos nouveaux tags.

@register.simple_tag #décorateur qui transforme une simple fonction Python (qui retourne une valeur) en un tag utilisable dans les templates.
def current_year():
    return datetime.date.today().year