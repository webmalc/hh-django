from django import template

register = template.Library()


@register.filter()
def get_item(dictionary, key):
    if key in dictionary:
        return dictionary[key]
    return None


@register.filter()
def ru_pluralize(value, endings):
    try:
        endings = endings.split(',')
        if value % 100 in (11, 12, 13, 14):
            return endings[2]
        if value % 10 == 1:
            return endings[0]
        if value % 10 in (2, 3, 4):
            return endings[1]
        else:
            return endings[2]
    except:
        raise template.TemplateSyntaxError('Endings not found')

