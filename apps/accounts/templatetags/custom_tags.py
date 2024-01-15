from django import template

register = template.Library()


@register.filter(name="lang_switch_link")
def lang_switch_link(value, arg):
    # TODO: think about it
    # getting full path and checking if it contains more one language parameter
    if len(value.split("/")) > 1:
        # if it does then we need to add slash after language parameter
        return f"/{arg}/{'/'.join(value.split('/')[2:])}"
    # otherwise we just need to add language parameter
    return f"/{arg}{'/'.join(value.split('/')[2:])}/"
