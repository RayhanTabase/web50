from django import forms

from .models import Listing,Bid

class Listing_form(forms.Form):
    listing_name = forms.CharField(label="title", max_length="30", strip="True",required=True)
    listing_description = forms.CharField(required=False,
                widget=forms.Textarea(
                    attrs={
                            'placeholder':"Add a description",
                        }
                )  
            )
    starting_bid = forms.DecimalField(decimal_places=2,max_digits=12,required=True)    
    listing_category = forms.CharField(max_length = 20,required=True)
    #image = forms.URLField(blank=True, verbose_name="Image URL", null=True)
    listing_image = forms.URLField(required=False)


class Comment_form(forms.Form):
    comment = forms.CharField(label="",required=True,
                widget=forms.Textarea(
                    attrs={
                            'placeholder':"Add a comment",
                    
                        }
                )  
            )

class Bid_form(forms.Form):
    bid = forms.DecimalField(decimal_places=2,max_digits=12,required=True)
    listing_id = forms.DecimalField(required=True)

    def clean_listing_id(self):
        listing_id = self.cleaned_data["listing_id"]
   
        listing = Listing.objects.get(id=listing_id)
        if listing and listing.active: 
            return listing_id
        else:
            raise forms.ValidationError("Invalid listing")
        


    def clean_bid(self):
        bid = self.cleaned_data["bid"]
        #print(self.data["listing_id"])

        if self.highest_bid():
            if bid > self.highest_bid():
                #print(self.highest_bid())
                return bid
            else:
                raise forms.ValidationError("Invalid bid")
        else:
            listing_id = self.data["listing_id"]
            item = Listing.objects.get(id=listing_id)

            if bid >= item.bid_price:
                return bid
            else:
                raise forms.ValidationError("Invalid bid")


    def highest_bid(self):
        listing_id = self.data["listing_id"]
       
        item = Listing.objects.get(id=listing_id)
        highest_bids = item.bid_item.order_by('-bid')
        highest_bid = highest_bids.first()

        if not highest_bid:       
            return False

        #print(highest_bid)
        return highest_bid.bid
    