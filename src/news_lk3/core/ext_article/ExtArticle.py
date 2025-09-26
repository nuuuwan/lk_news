from news_lk3.core.ext_article.ExtArticleBase import ExtArticleBase
from news_lk3.core.ext_article.ExtArticleFileSystem import ExtArticleFileSystem
from news_lk3.core.ext_article.ExtArticleRender import ExtArticleRender


class ExtArticle(ExtArticleFileSystem, ExtArticleBase, ExtArticleRender):
    pass
