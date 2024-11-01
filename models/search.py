from spyne import ComplexModel, Unicode

# Модель для параметрів пошуку
class SearchParams(ComplexModel):
    key = Unicode
    value = Unicode