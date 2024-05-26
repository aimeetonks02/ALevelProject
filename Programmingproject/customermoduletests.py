import customermodule

customerobject = customermodule.customer(2)
print(customerobject)
print(customerobject.FirstName)
print(customerobject.Email)

customerobject = customermodule.find_customer()
print(customerobject)
print(customerobject.FirstName)
print(customerobject.Email)