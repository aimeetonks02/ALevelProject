import purchaseordermodule

# PurchOrdID = purchaseordermodule.create_purchase_order()
order = purchaseordermodule.purchaseorder(5)
# print(order)
# order.list_items()
# order.add_item(1, 2)
# order.list_items()

# order.edit_quantity(1, 3)
# order.list_items()

# order.add_item(1,2)
# order.list_items()

# order.remove_item(1)
# order.list_items()

order.deliver_purchase()