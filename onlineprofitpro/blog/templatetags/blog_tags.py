# D:\Python\django\ONLINEPROFITPRO.RU\onlineprofitpro\blog\templatetags\blog_tags.py

# Импортируем модуль template для работы с шаблонами и наши модели:
from django import template
from blog.models import *

# экземпляр класса Library, через который происходит регистрация собственных шаблонных тегов:
register = template.Library()


menu = [{'title': "Главная", 'url_name': 'home'},
        {'title': "О нас", 'url_name': 'about'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Гостевой пост", 'url_name': 'guest_post'},
]
#  определим функцию def get_horizontal_menu(), которая будет выполняться при вызове нашего тега из шаблона
#  и свяжем эту функцию с тегом, или, превратим эту функцию в тег, используя специальный декоратор, доступный через переменную register:
@register.simple_tag()
def get_horizontal_menu():
    return menu
'''
После создания своего простого пользовательского тега для использования его в шаблонах
вначале выполним загрузку тегов в шаблон (base.html), определенных в этом файле blog_tags.py.
{% load blog_tags %}

Далее, в месте вывода меню просто запишем наш новый сформированный тег:
{% get_horizontal_menu %}
Подставить в цикл тег 'get_horizontal_menu' мы не можем, т.к. это не переменная, а тег шаблона. 
Для этого в Django в тегах шаблонов можно использовать специальное ключевое слово as, 
которое сформирует ссылку на данные тега.
{% get_horizontal_menu as horizontal_menu %}
Сформируется переменная 'horizontal_menu', которую уже можно использовать в теге цикла for. 
base.html:
                        {% get_horizontal_menu as horizontal_menu %}
                        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                            {% for item in horizontal_menu %}
                            <li class="nav-item">
                                <a class="nav-link" href="{% url item.url_name %}">{{ item.title }}</a>
                            </li>
                            {% endfor %}
                        </ul>
'''


# Для функции тега можем указать любое имя через параметр (name='menu_cat_subcat')
# И, далее, в шаблонах (base.html и. т.п.) следует использовать имя 'menu_cat_subcat':
# {% menu_cat_subcat as menu_cs %}

@register.simple_tag(name='menu_cat_subcat')
def get_vertical_menu_posts():
    categories = ModelCategories.objects.all()
    subcategories = ModelSubcategories.objects.all()

    cat_subcat_menu = {
        'categories': categories,
        'subcategories': subcategories,
    }

    return cat_subcat_menu

