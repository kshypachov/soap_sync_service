from spyne import ComplexModel, Unicode

# Модель для параметров поиска
class SearchParams(ComplexModel):
    key = Unicode
    value = Unicode