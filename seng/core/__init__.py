import markdown
from markdown.extensions.smarty import SmartyExtension

mk = markdown.Markdown([ SmartyExtension() ])