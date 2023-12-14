from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from my_tables import Base, Order, Customer  
engine = create_engine('sqlite:///decor_orders.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def place_order():
    items = ('Mirror','Chairs','Lamps','Vase')
    user_name = input("Hello, welcome to CustomDecor, kindly enter your name to proceed: ")
    client_order = input(f"Hello {user_name}.These: {items} are the items we make. Kindly press 1 to record your order. ")
    
    if client_order:

        item_name = input('Which item would you like? ')
        item_quantity = int(input('How many pieces would you like? '))

        customer_name = input('Kindly confirm the name you entered: ')
        customer_location = input('Kindly enter your location: ')
        customer_email = input('Kindly enter your email: ')

    customer = session.query(Customer).filter_by(name=customer_name, location=customer_location, email=customer_email).first()
    if not customer:
        customer = Customer( name=customer_name, location=customer_location, email=customer_email)
        session.add(customer)
        session.commit()

    order = Order(item_name=item_name, item_quantity=item_quantity, customer=customer)
    session.add(order)
    session.commit()

def view_orders():
    orders = session.query(Order).all()
    for order in orders:
        if order.customer:
            print(f"Order ID: {order.id}, Item: {order.item_name}, Quantity: {order.item_quantity}, Customer Name: {order.customer.name}")
        else:
            print(f"Order ID: {order.id}, Item: {order.item_name}, Quantity: {order.item_quantity}, Customer: None")
def change_order():
    view_orders()
    order_id = int(input('Kindly enter the ID of the order you want to change: '))
    order = session.query(Order).get(order_id)

    if order:
        new_item_name = input('Enter the new item name: ')
        new_item_quantity = int(input('Enter the new quantity: '))
        order.item_name = new_item_name
        order.item_quantity = new_item_quantity
        session.commit()
        print('Your order has been changed successfully.')
    else:
        print('Order not found.')

def delete_order():
    view_orders()
    order_id = int(input('Kindly enter the ID of the order you want to delete: '))
    order = session.get(Order, order_id)
    if order:
        session.delete(order)
        session.commit()
        print('Your order has been deleted successfully.')
    else:
        print('Order not found.')

def delete_customer():
    customer_name = input('Enter the name of the customer you want to delete: ')
    
    customer = session.query(Customer).filter_by(name=customer_name).first()
    
    if customer:
        session.delete(customer)
        session.commit()
        print(f'Customer {customer_name} has been deleted successfully.')
    else:
        print(f'Customer {customer_name} not found.')

def main():
    while True:
        print(' CustomDecor Order(s) Manager ')
        print('1) Choose 1 to place an order')
        print('2) Choose 2 to view orders')
        print('3) Choose 3 to change an order')
        print('4) Choose 4 to delete an order')
        print('5) Choose 5 to delete customer data')
        print('6) Choose 6 to quit')

        option = input('Choose an option: ')

        if option == '1':
            place_order()
        elif option == '2':
            view_orders()
        elif option == '3':
            change_order()
        elif option == '4':
            delete_order()
        elif option == '5':
            delete_customer()
        elif option == '6':
            print('Order cancelled')
            break
        else:
            print('Invalid option. Please choose a valid option.')

if __name__ == "__main__":
    main()