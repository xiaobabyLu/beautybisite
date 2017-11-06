import datetime
from haystack import indexes
from .models import BeautyUsers


class BeautyUsersIndex(indexes.SearchIndex,indexes.Indexable):
    text = indexes.CharField(document=True,use_template=True)
    nickname = indexes.CharField(model_attr='nickname')
    update_date = indexes.DateTimeField(model_attr='update_date')

    def get_model(self):
        return BeautyUsers

    def index_queryset(self, using=None):
        # return self.get_model().objects.filter(update_date__lte=datetime.datetime.now())
        return self.get_model().objects.all()
