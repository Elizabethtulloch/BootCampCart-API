import falcon
from playhouse.shortcuts import model_to_dict

from cart_api.database import DatabaseCartItem


# Exercise 3:
# Using the database model you created in Exercise 1 create a cartitems route
# CartItems should have a responder for POST and GET
# CartItem should have responders for GET DELETE PATCH
# Your API response statuses and bodies should conform to your OpenAPI spec


class CartItems:
    def on_get(self, req, resp):
        resp.media = [model_to_dict(item) for item in DatabaseCartItem.select()]
        resp.status = falcon.HTTP_200


    def on_post(self, req, resp):
        obj = req.get_media()
        cartItem = DatabaseCartItem(
            name= obj["name"],
            quantity = obj["quantity"],
            price = obj["price"]
        )
        cartItem.save()
        resp.media = model_to_dict(cartItem)
        resp.status = falcon.HTTP_201



class CartItem:
    def on_get(self, req, resp, product_id):
        cartItem = DatabaseCartItem.get(id=product_id)
        resp.media = model_to_dict(cartItem)
        resp.status = falcon.HTTP_200

    # def on_patch(self,req,resp,product_id):
    #     cartItem = DatabaseCartItem.get(id=product_id)
    #     cartItem["quantity"] = req.get_media()
    #     cartItem.save()
    #     resp.status = falcon.HTTP_204   

    def on_patch(self, req, resp,product_id):
        cartitem = DatabaseCartItem.get(id=product_id)
        changes = req.media
        if "quantity" in changes:
            cartitem.quantity = changes["quantity"]
            cartitem.save()
        resp.status = falcon.HTTP_204

    def on_delete(self, req, resp, product_id):
        DatabaseCartItem.delete_by_id(product_id)
        resp.status = falcon.HTTP_204

# Exercise 3: Build the Cart Item resources similar to Product. You should have two resources called CartItem and CartItems using the DatabaseCartItem database Model. (We did one above). The resources should support the following operations.

# CartItems:

# Add a new Cart Item row (very similar to adding a product) done 
# List out all the Cart Item rows
# CartItem:

# Fetch a Cart Item row based on the given item_id
# Delete a Cart Item row based on the given item_id
# Update a Cart Item row based on the given item_id
# Hints: Do not forget to add routes for the new resources to the Falcon API class. Several tests require POST to be correct before they will pass so start with on_post. After that it is useful to be able to GET all items available in the table so then you can use those ids for testing the other operations.