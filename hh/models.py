from django.db import models
from sitetree.models import TreeItemBase, TreeBase


class SiteTreeTree(TreeBase):
    """ HH tree model."""
    pass


class SiteTreeItem(TreeItemBase):
    """ HH tree item model."""

    icon = models.CharField(max_length=50, null=True, help_text='Иконка FontAwesome. Пример: fa-user.')
