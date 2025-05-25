from pydantic_core.core_schema import model_field
from sqladmin import ModelView
from house_app.db.models import House

class HouseAdmin(ModelView, model=House):
    name = "House"  # Отображаемое имя в меню
    icon = "fa fa-home"  # Иконка (опционально)
    column_list = [House.id, House.area, House.year, House.bath]  # Поля для отображения