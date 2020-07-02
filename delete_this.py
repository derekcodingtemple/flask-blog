# calculation = 5**5
# my_dict = {'working': True}
# try:
#     print(calculation)
#     print(my_dict['not_working'])
# except KeyError:
#     # print(error)
#     print("That key doesn't exist")
#     # print("That thing isn't defined yet")
# finally:
#     print("This will execute regardless")

x = input("Type something here")
if x != int:
    raise NameError('You have to have convert it to an integer first.')