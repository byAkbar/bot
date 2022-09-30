
def convert(list_convert):

    return [itm[0] for itm in list_convert]

    




def total_cost(list_quantity, list_price):
    
    order_total_cost = 0

    for ind, itm in enumerate(list_price):
        order_total_cost += list_quantity[ind]*list_price[ind]
        

        return order_total_cost


def total_quantity(list_quantity):

    order_total_quantity = 0

    for itm in list_quantity:
        order_total_quantity += itm

        return order_total_quantity

def get_total_coas(BD):

    all_product_id = BD.select_all_product_id()

    all_price = [BD.select_single_product_price(itm) for itm in all_product_id]

    all_quantity = [BD.select_order_quantity(itm) for itm in all_product_id]

    return total_cost(all_quantity, all_price)


def get_total_quantity(BD):

    all_product_id = BD.select_all_product_id()

    all_quantity = [BD.select_order_quantity(itm) for itm in all_product_id]

    return total_quantity(all_quantity)