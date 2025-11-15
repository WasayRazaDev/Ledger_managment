# in use 

class Product:
    def __init__(self, product_id=None, company=None, name=None, status='active'):
        self.product_id = product_id
        self.company = company
        self.name = name
        self.status = status
    
    def __repr__(self):
        return f"Product(product_id='{self.product_id}', company='{self.company}', name='{self.name}', status='{self.status}')"