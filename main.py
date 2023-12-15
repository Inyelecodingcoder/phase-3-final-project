from sqlalchemy import create_engine
from sqlalchemy.orm import  sessionmaker
from validate_email_address import validate_email
from my_tables import Base, Customer, Order





engine = create_engine('sqlite:///decor_orders.db')
Base.metadata.create_all(engine)  


Session = sessionmaker(bind=engine)
session = Session()

items = ('Mirror', 'Chairs', 'Lamps', 'Vase')


def is_valid_email(email):
    try:
        validate_email(email)
        return True
    except ValueError:
        return False


def register_user():
    user_name = input("Hello, welcome to CustomDecor, kindly enter your name to proceed: \n")
    print('')
    customer_email = input('Kindly enter your email: \n')
    print('')

    if not is_valid_email(customer_email):
        print("Invalid email address. Please enter a valid email. \n")
        print('')
        return

    customer = Customer(name=user_name, email=customer_email)
    session.add(customer)
    session.commit()

    print(f"Registration successful! Your customer ID is: {customer.id}\n")


def place_order(customer_id):
    user = session.query(Customer).filter_by(id=customer_id).first()
    
    if not user:
        print(f"Customer not found with ID: {customer_id}\n")
        return

    print('')
    client_order = input(f"Hello {user.name}. These: {items} are the items we make. Kindly press 1 to record your order. \n")
    print('')
    
    if client_order != '1':
        print("Invalid input for order. Please press 1 to record your order.\n")
        print('')
        return

    item_name = input('Which item would you like? \n').lower()
    print('')

    if item_name not in map(str.lower, items):
        print(f"Invalid item name. Please choose one of: {', '.join(items)} \n")
        print('')
        return

    try:
        item_quantity = int(input('How many pieces would you like? \n'))
        print('')
    except ValueError:
        print('Invalid input for quantity. Please enter a valid integer. \n')
        print('')
        return
    
    order = Order(item_name=item_name, item_quantity=item_quantity, customer=user)
    session.add(order)
    session.commit()

    print('Your order has been placed successfully. \n')


def view_orders(customer_id):
    user = session.query(Customer).filter_by(id=customer_id).first()
    
    if not user:
        print(f"Customer not found with ID: {customer_id}\n")
        return

    orders = session.query(Order).filter_by(customer=user).all()

    if orders:
        for order in orders:
            print(f"Order ID: {order.id}, Item: {order.item_name}, Quantity: {order.item_quantity}\n")
    else:
        print(f"No orders found for customer with ID: {customer_id}\n")


def change_order(customer_id):
    user = session.query(Customer).filter_by(id=customer_id).first()
    
    if not user:
        print(f"Customer not found with ID: {customer_id}\n")
        return

    view_orders(customer_id)
    order_id = int(input('Kindly enter the ID of the order you want to change: \n'))
    print('')
    order = session.query(Order).filter_by(id=order_id, customer=user).first()

    if order:
        new_item_name = input('Enter the new item name: \n')
        print('')

        if new_item_name.capitalize() not in items:
            print(f"Invalid item name. Please choose one of: {', '.join(items)} \n")
            print('')
            return

        try:
            new_item_quantity = int(input('Enter the new quantity: \n'))
            print('')
        except ValueError:
            print('Invalid input for quantity. Please enter a valid integer. \n')
            print('')
            return
        order.item_name = new_item_name
        order.item_quantity = new_item_quantity
        session.commit()
        print('Your order has been changed successfully. \n')
    else:
        print('Order not found. \n')


def delete_order(customer_id):
    user = session.query(Customer).filter_by(id=customer_id).first()
    
    if not user:
        print(f"Customer not found with ID: {customer_id}\n")
        return

    view_orders(customer_id)
    order_id = int(input('Kindly enter the ID of the order you want to delete: \n'))
    print('')
    order = session.query(Order).filter_by(id=order_id, customer=user).first()
    if order:
        session.delete(order)
        session.commit()
        print('Your order has been deleted successfully. \n')
    else:
        print('Order not found. \n')


def delete_customer(customer_id):
    user = session.query(Customer).filter_by(id=customer_id).first()
    
    if not user:
        print(f"Customer not found with ID: {customer_id}\n")
        return

    session.delete(user)
    session.commit()
    print(f'Customer with ID {customer_id} has been deleted successfully. \n')


def main():
    while True:
        print(' Welcome to CustomDecor Order(s) Manager \n')
        print('Press (r) to register, kindly note that registration is required to proceed ')
        print('Then press (p) to place an order')
        print('')
        print('To view your order, press (v)')
        print('To change your order, press (c)')
        print('To delete your order, press (dl)')
        print('To delete your account, press (da)')
        print('To quit, press (q) \n')

        client_choice = input('Please proceed by entering your selection from the choices above: \n ')
        print('')

        if client_choice == 'r':
            register_user()
        elif client_choice == 'p':
            customer_id = int(input('Enter your customer ID: '))
            place_order(customer_id)
        elif client_choice == 'v':
            customer_id = int(input('Enter your customer ID: '))
            view_orders(customer_id)
        elif client_choice == 'c':
            customer_id = int(input('Enter your customer ID: '))
            change_order(customer_id)
        elif client_choice == 'dl':
            customer_id = int(input('Enter your customer ID: '))
            delete_order(customer_id)
        elif client_choice == 'da':
            customer_id = int(input('Enter your customer ID: '))
            delete_customer(customer_id)
        elif client_choice == 'q':
            print('Order cancelled \n')
            break
        else:
            print('Your choice is invalid. Kindly choose a valid choice. \n')


if __name__ == "__main__":
    main()
