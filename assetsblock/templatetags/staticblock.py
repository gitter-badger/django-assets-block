from django import template
from django.template.base import TemplateSyntaxError
from django.template.loader_tags import BlockNode, BLOCK_CONTEXT_KEY

from assetstack.assets import Registry

register = template.Library()


# almost the same as `block` node but makes use of
#  output_context introduced by django-output-context
class AssetBlockNode(BlockNode):
    def __init__(self, name, nodelist, output_context, parent=None):
        self.name = name
        self.nodelist = nodelist
        self.output_context = output_context
        self.parent = parent

    def __repr__(self):
        return "<Asset Block Node: %s. Contents: %r>" % (self.name, self.nodelist)

    def render(self, context):
        stack = self.output_context['assets'].get(self.name)
        block_context = context.render_context.get(BLOCK_CONTEXT_KEY)
        context.push()
        if block_context is None:
            stack.add_content(self.nodelist.render(context))
            result = ''
        else:
            push = block = block_context.pop(self.name)
            if block is None:
                block = self
            # Create new block so we can store context without thread-safety issues.
            block = AssetBlockNode(block.name, block.nodelist, block.output_context)
            block.context = context
            context['block'] = block
            result = block.super() + block.nodelist.render(context)
            if block_context.get_block(self.name):
                result = result + stack.get_content()
            if push is not None:
                block_context.push(self.name, push)
        context.pop()
        return result


# almost the same as `block` tag but makes use of
# output_context introduced by django-output-context
@register.tag('assets')
def do_assets(parser, token):
    """
    Define a block that can be overridden by child templates.
    """
    # token.split_contents() isn't useful here because this tag doesn't accept variable as arguments
    bits = token.contents.split()
    if len(bits) != 2:
        raise TemplateSyntaxError("'%s' tag takes only one argument" % bits[0])
    block_name = bits[1]

    if not hasattr(parser, 'output_context') or parser.output_context is None:
        parser.output_context = {}

    if 'assets' not in parser.output_context:
        parser.output_context['assets'] = Registry()
    # Keep track of the names of BlockNodes found in this template, so we can
    # check for duplication.
    try:
        if block_name in parser.__loaded_blocks:
            raise TemplateSyntaxError("'%s' tag with name '%s' appears more than once" % (bits[0], block_name))
        parser.__loaded_blocks.append(block_name)
    except AttributeError: # parser.__loaded_blocks isn't a list yet
        parser.__loaded_blocks = [block_name]
    nodelist = parser.parse(('endassets',))

    # This check is kept for backwards-compatibility. See #3100.
    endblock = parser.next_token()
    acceptable_endblocks = ('endassets', 'endassets %s' % block_name)
    if endblock.contents not in acceptable_endblocks:
        parser.invalid_block_tag(endblock, 'endassets', acceptable_endblocks)

    return AssetBlockNode(block_name, nodelist, parser.output_context)