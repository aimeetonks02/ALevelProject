import suppliermodule



supplierobject = suppliermodule.supplier(1)
print(supplierobject)
print(supplierobject.SupplierName)
print(supplierobject.Email)

supplierobject = suppliermodule.find_supplier_by_name()
print(supplierobject)
print(supplierobject.SupplierName)
print(supplierobject.Email)