import pyinputplus as pyip

bread_price_list = {'wheat': 50, 'white': 100, 'sourdough': 150}
protein_price_list = {'chicken': 20, 'turkey': 30, 'ham': 30, 'tofu': 10}
cheese_price_list = {'cheddar': 40, 'swiss': 30, 'mozzarella': 20}

# select options
bread_type = pyip.inputMenu(['wheat', 'white', 'sourdough'], numbered=True, prompt = 'Please select the bread type \n')
protein_type = pyip.inputMenu(['chicken', 'turkey', 'ham', 'tofu'], numbered=True, prompt = '\nPlease select the protein type \n')
want_cheese = pyip.inputYesNo(prompt = '\nDo you want cheese. Please type yes/y/Y or no/n/N \n')
if want_cheese == 'yes': cheese_type = pyip.inputMenu(['cheddar', 'swiss', 'mozzarella'], numbered=True, prompt = '\nPlease select the bread type \n') 
want_mayo_tomamto_or_cheese = pyip.inputYesNo(prompt = '\nDo you want mayo, mustard, lettuce, or tomato. Please type yes/y/Y or no/n/N \n')
sandwich_num = pyip.inputNum(min = 1, prompt = '\nHow many sandwiches do you want? : ')


# calculate price
sandwich_price = sandwich_num * 50
mayo_tomato_lettuce_price = 40 if want_mayo_tomamto_or_cheese == 'yes' else 0
cheese_price = cheese_price_list[cheese_type] if want_cheese == 'yes' else 0
total_price = bread_price_list[bread_type] + protein_price_list[protein_type] + sandwich_price + mayo_tomato_lettuce_price + cheese_price
print(f'Total price is {total_price} dollars')

    




